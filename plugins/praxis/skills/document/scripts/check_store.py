#!/usr/bin/env python3
"""Run the shared checks on a task's merged item store.

Usage: check_store.py <items.json>

The checks are the ones items-and-agreements.md lists under "Shared checks":
store integrity and the findings that block publishing, plus two flags that never
block. Links and id fields resolve against every id in the store, restricted items
included. Outside links and evidence links are not fetched here: they are listed
under "to_verify" for the filing step to resolve.

Prints {"findings": [...], "flags": [...], "to_verify": [...]}, each entry
{"item", "check", "detail"}, and exits 1 when there is any finding, 0 otherwise.
"""
import json
import re
import sys

ID_RE = re.compile(r"^([A-Z][A-Z0-9]*)-(\d+)$")
PERIOD_RE = re.compile(r"^P(?!$)(\d+Y)?(\d+M)?(\d+W)?(\d+D)?(T(?=\d)(\d+H)?(\d+M)?(\d+(\.\d+)?S)?)?$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}")
LINK_KINDS = {"serves", "blocked-by", "covers", "verifies", "supersedes", "amends",
              "answers", "opened-by", "rests-on", "breaks"}
NEEDS_DECIDE_BY = {"open", "lean", "proposed"}
STATES = {"open", "lean", "proposed", "deferred", "agreed", "superseded", "withdrawn", "recorded"}
EMPTY = (None, "", [], "unknown")
ACCEPTABLE = ("risk", "threat", "privacy threat")
SCALARS = {"text", "number", "date", "period", "when", "id"}
ID_LIKE = re.compile(r"^[A-Za-z]+-?\d+$")


def type_declared_ok(ftype):
    if isinstance(ftype, dict):
        return isinstance(ftype.get("enum"), list) and len(ftype) == 1
    if isinstance(ftype, str) and ftype.startswith("list of "):
        return type_declared_ok(ftype[len("list of "):])
    return ftype in SCALARS


def is_outside(target, prefixes):
    if not isinstance(target, str):
        return False
    m = ID_RE.match(target)
    if m:
        return m.group(1) not in prefixes
    return not ID_LIKE.match(target)


DUE_RE = re.compile(r"^(build start|end of round \d+|close-out)$")


def is_when(value, gates=("GATE",)):
    if not isinstance(value, str):
        return False
    m = ID_RE.match(value)
    return bool(DATE_RE.match(value) or DUE_RE.match(value) or (m and m.group(1) in gates))


def scalar_ok(ftype, value):
    if value in EMPTY:
        return True
    if isinstance(ftype, dict):
        return value in ftype.get("enum", [])
    if ftype == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if ftype == "date":
        return isinstance(value, str) and bool(DATE_RE.match(value))
    if ftype == "period":
        return isinstance(value, str) and bool(PERIOD_RE.match(value))
    if ftype == "when":
        return is_when(value)
    if ftype == "id":
        return isinstance(value, str) and bool(ID_RE.match(value))
    return True  # text


def check_field(find, iid, name, ftype, value, known):
    if isinstance(ftype, str) and ftype.startswith("list of "):
        if value in EMPTY:
            return
        if not isinstance(value, list):
            find(iid, "type", f"field {name!r} isn't a list")
            return
        for v in value:
            check_field(find, iid, name, ftype[len("list of "):], v, known)
        return
    if not scalar_ok(ftype, value):
        find(iid, "type", f"field {name!r} value {value!r} isn't a {ftype}")
    elif ftype == "id" and value not in EMPTY and value not in known:
        find(iid, "id-field", f"field {name!r} names {value!r}, which no item in the store is")


def one_person(value):
    return (isinstance(value, str) and value.strip() not in EMPTY
            and "," not in value and " and " not in value)


def live_names(kinds, iid):
    m = ID_RE.match(iid or "")
    return set(kinds.get(m.group(1), {}).get("live", {})) if m else set()


def main(argv):
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    with open(argv[1], encoding="utf-8") as fh:
        store = json.load(fh)

    out = {"findings": [], "flags": [], "to_verify": []}

    def add(bucket, item, check, detail):
        out[bucket].append({"item": item, "check": check, "detail": detail})

    def find(item, check, detail):
        add("findings", item, check, detail)

    kinds = store.get("kinds", {})
    for prefix, spec in kinds.items():
        for group in ("fields", "live"):
            for name, ftype in spec.get(group, {}).items():
                if not type_declared_ok(ftype):
                    find(prefix, "declared-type", f"{group} {name!r} has type {ftype!r}")
    items = store.get("items", [])
    agreements = store.get("agreements", [])

    seen = {}
    for item in items:
        iid = item.get("id", "")
        if not ID_RE.match(iid):
            find(iid or "?", "id", "not a prefix, a hyphen and a number")
            continue
        if iid in seen:
            find(iid, "id", "used by more than one item")
        seen[iid] = item
    known = set(seen) | {a.get("id") for a in agreements}

    for item in items:
        iid = item.get("id", "")
        if not ID_RE.match(iid):
            continue
        spec = kinds.get(ID_RE.match(iid).group(1))
        if spec is None:
            find(iid, "kind", "its prefix is declared by no kind")
            spec = {}
        elif item.get("kind") != spec.get("kind"):
            find(iid, "kind", f"its prefix belongs to kind {spec.get('kind')!r}")
        state = item.get("state")
        if state not in STATES:
            find(iid, "state", f"unknown state {state!r}")
        if not one_person(item.get("owner")):
            find(iid, "owner", "missing owner, or more than one")
        if state in NEEDS_DECIDE_BY and item.get("decide_by") in EMPTY:
            find(iid, "decide-by", f"{state} item with no decide-by")
        elif item.get("decide_by") not in EMPTY and not is_when(item.get("decide_by")):
            find(iid, "decide-by", f"decide-by {item.get('decide_by')!r} isn't a date, a gate or a due point")
        for link in item.get("links", []):
            kind, target = link.get("link"), link.get("to")
            if kind not in LINK_KINDS:
                find(iid, "link", f"unknown link kind {kind!r}")
            elif is_outside(target, set(kinds)):
                add("to_verify", iid, "link", f"{kind} outside target {target!r}")
            elif target not in known:
                find(iid, "link", f"{kind} target {target!r} resolves to nothing")
        for ev in item.get("evidence", []):
            link = ev.get("link") if isinstance(ev, dict) else None
            if not link:
                if not (isinstance(ev, dict) and isinstance(ev.get("who"), list) and ev.get("who") and ev.get("when")):
                    find(iid, "evidence", "evidence entry with no link, nor who took part and when")
            else:
                add("to_verify", iid, "evidence", f"evidence {link!r}")
            if isinstance(ev, dict) and ev.get("when") is not None and not DATE_RE.match(str(ev.get("when"))):
                find(iid, "date", f"evidence when {ev.get('when')!r} isn't a date")
        if item.get("first_filed") is not None and not DATE_RE.match(str(item.get("first_filed"))):
            find(iid, "date", f"first_filed {item.get('first_filed')!r} isn't a date")
        for note in (item.get("review") or {}).get("notes", []):
            if not (isinstance(note, dict) and DATE_RE.match(str(note.get("date"))) and note.get("what")):
                find(iid, "change-note", "change note without a date and what changed")
        declared = spec.get("fields", {})
        live = set(spec.get("live", {}))
        for name, value in item.get("fields", {}).items():
            if name in live:
                find(iid, "live-state", f"live field {name!r} written into the item")
            elif name in declared:
                check_field(find, iid, name, declared[name], value, known)

    for agr in agreements:
        aid = agr.get("id", "?")
        if agr.get("date") is not None and not DATE_RE.match(str(agr.get("date"))):
            find(aid, "date", f"agreement date {agr.get('date')!r} isn't a date")
        if not one_person(agr.get("decider")):
            find(aid, "decider", "no decider, or more than one")
        for settled in agr.get("settled", []):
            sid = settled.get("id")
            content = settled.get("content") or {}
            fields = content.get("fields", {}) if isinstance(content, dict) else {}
            if live_names(kinds, sid) & set(fields):
                find(aid, "live-state", f"live field written into the agreed content of {sid}")
            target = seen.get(sid)
            if target is None:
                continue
            if target.get("first_state") == "agreed" and agr.get("consulted") in (None, []):
                add("flags", sid, "accepted at creation", f"first filed agreed under {aid}, no one consulted")
            if target.get("kind") in ACCEPTABLE \
                    and target.get("fields", {}).get("response") == "accept" \
                    and agr.get("decider") == target.get("owner"):
                add("flags", sid, "self-acceptance", f"accepted under {aid} by its own owner")

    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 1 if out["findings"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
