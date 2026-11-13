#!/usr/bin/env python3
"""Resolve every view block of an item store into the rows a page shows.

Usage: resolve_views.py <items.json> [<live-state.json>] [--markdown]

Runs item-store-and-views.md's (sibling rules/ folder) "Up-front rejections" for views and its
"Resolving a view" steps 1 to 4 over every entry of the store's `views`, in the
JSON shape that rule pins. Prints {"rejections": [...], "views": [...]}, each
view {"page", "position", "caption", "as", "header", "groups": [{"group", "rows"}],
"none"}; a graph or chain view adds "edges", a timeline "not_placed". With
--markdown, prints instead each view's static table form as Markdown, under a
`<!-- view <page> <position> -->` line, which a Markdown backend writes as it is.

Exits 1 when any view is rejected, 0 otherwise. A rejected view is not resolved.
"""
import json
import re
import sys

ID_RE = re.compile(r"^([A-Z][A-Z0-9]*)-(\d+)$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}")
ROUND_RE = re.compile(r"^end of round (\d+)$")
LINKS = {"serves": "served-by", "blocked-by": "blocks", "covers": "covered-by",
         "verifies": "verified-by", "supersedes": "superseded-by", "amends": "amended-by",
         "answers": "answered-by", "opened-by": "opens", "rests-on": "supports",
         "breaks": "broken-by"}
REVERSE = {v: k for k, v in LINKS.items()}
STATES = ["open", "lean", "proposed", "deferred", "agreed", "superseded", "withdrawn", "recorded"]
SENSITIVITY = ["team", "restricted"]
COMMON = {"id", "title", "owner", "state", "decide_by", "sensitivity", "review.last", "review.next"}
PRESENTATIONS = {"table", "list", "cards", "matrix", "graph", "chain", "timeline"}
AGREEMENT_PARTS = {"decider", "consulted", "informed", "date", "link"}
VERIFICATION_PARTS = {"outcome", "when", "environment", "commit", "link"}
EMPTY = (None, "", [])


class Store:
    def __init__(self, data, live):
        self.kinds = {spec.get("kind"): dict(spec, prefix=p) for p, spec in data.get("kinds", {}).items()}
        self.items = data.get("items", [])
        self.by_id = {i.get("id"): i for i in self.items}
        self.order = {i.get("id"): n for n, i in enumerate(self.items)}
        self.agreements = data.get("agreements", [])
        self.live = (live or {}).get("items", {})
        self.observed = (live or {}).get("observed")
        self.reverse = {}
        for item in self.items:
            for link in item.get("links", []):
                self.reverse.setdefault((link.get("to"), LINKS.get(link.get("link"))), []).append(item.get("id"))

    def field_type(self, kind, name):
        spec = self.kinds.get(kind, {})
        return spec.get("fields", {}).get(name, spec.get("live", {}).get(name))

    def declares(self, kinds, name):
        return name in COMMON or any(self.field_type(k, name) is not None for k in kinds)

    def value(self, item, name):
        if name in ("id", "title", "owner", "state", "decide_by", "sensitivity"):
            return item.get(name)
        if name.startswith("review."):
            return (item.get("review") or {}).get(name[7:])
        if name in self.kinds.get(item.get("kind"), {}).get("live", {}):
            return self.live.get(item.get("id"), {}).get(name)
        return (item.get("fields") or {}).get(name)

    def targets(self, item, link):
        if link in LINKS:
            ts = [l.get("to") for l in item.get("links", []) if l.get("link") == link]
            return sorted(ts, key=lambda t: (t not in self.order, self.order.get(t, 0)))
        return sorted(self.reverse.get((item.get("id"), link), []), key=lambda i: self.order.get(i, 0))

    def covering(self, iid):
        hits = [a for a in self.agreements if any(s.get("id") == iid for s in a.get("settled", []))]
        return max(hits, key=lambda a: a.get("date") or "") if hits else None

    def label(self, target, show=None):
        item = self.by_id.get(target)
        if item is None:
            m = ID_RE.match(target or "")
            if m and m.group(1) in {s["prefix"] for s in self.kinds.values()}:
                return f"{target} [not in this document]"
            return str(target)
        if show:
            v = self.value(item, show)
            return "" if v in EMPTY else str(v)
        return f"{target} · {item.get('title', '')}"


def link_ok(name):
    return name in LINKS or name in REVERSE


def reject_view(store, key, view, subject=None):
    out = []
    if subject in EMPTY and any("page subject" in json.dumps(c) for c in view.get("where", [])):
        out.append("filters on page subject but the entry carries no subject")
    kinds = list(view.get("of") or []) + ([view.get("rows"), view.get("cols")] if view.get("as") == "matrix" else [])
    if not kinds:
        out.append("names no kind in `of`")
    for k in kinds:
        if k not in store.kinds:
            out.append(f"kind {k!r} isn't declared; `of` takes kinds, not prefixes")
    if view.get("as") not in PRESENTATIONS:
        out.append(f"presentation {view.get('as')!r} isn't one of {sorted(PRESENTATIONS)}")
    if not view.get("caption"):
        out.append("has no caption")
    prefixes = {spec["prefix"] for spec in store.kinds.values()}
    if " — " in (view.get("caption") or ""):
        out.append("caption contains ' — '")
    for c in view.get("where", []):
        if "field" in c and not any(op in c for op in ("is", "in", "not-in")):
            out.append(f"filter on {c['field']!r} has no is, in or not-in")
        elif "link" in c and not any(op in c for op in ("to", "not-to")):
            out.append(f"filter on link {c['link']!r} has no to or not-to")
        elif "link" in c and c.get("to", c.get("not-to")) in prefixes:
            out.append(f"filter link target {c.get('to', c.get('not-to'))!r} is a prefix; name the kind")
        if "field" in c:
            if c["field"] == "state" or c["field"] == "sensitivity":
                allowed = STATES if c["field"] == "state" else SENSITIVITY
                vals = c.get("in") or c.get("not-in") or [c.get("is")]
                bad = [v for v in vals if v not in allowed]
                if bad:
                    out.append(f"filter on {c['field']} with {bad}")
            elif not store.declares(kinds, c["field"]):
                out.append(f"filter field {c['field']!r} isn't declared on {kinds}")
        elif "link" in c:
            if not link_ok(c["link"]):
                out.append(f"filter link {c['link']!r} is neither a link kind nor a reverse")
        else:
            out.append(f"filter condition {c!r} names neither a field nor a link")
    for col in view.get("columns", []):
        out += reject_column(store, kinds, col)
        out += [f"column kinds name prefix {k!r}; name the kind" for k in col.get("kinds", []) if k in prefixes] \
            if isinstance(col, dict) else []
        if isinstance(col, dict) and col.get("field") in ("id", "title"):
            out.append("id and title are always shown; drop the column")
    if view.get("as") == "matrix":
        for part in ("rows", "cols"):
            if view.get(part) not in store.kinds:
                out.append(f"matrix {part} {view.get(part)!r} isn't a declared kind")
        cell = view.get("cell")
        for name in (cell if isinstance(cell, list) else [cell]):
            if not link_ok(name):
                out.append(f"matrix cell link {name!r} is neither a link kind nor a reverse")
    if view.get("as") == "graph":
        for name in view.get("edges") or [None]:
            if not link_ok(name):
                out.append(f"graph edge {name!r} is neither a link kind nor a reverse")
    if view.get("as") == "chain":
        if view.get("start") not in store.by_id:
            out.append(f"chain start {view.get('start')!r} isn't in the store")
        follow = view.get("follow")
        for name in (follow if isinstance(follow, list) else [follow]):
            if not link_ok(name):
                out.append(f"chain link {name!r} is neither a link kind nor a reverse")
    if view.get("as") == "timeline" and not store.declares(kinds, view.get("start_field") or ""):
        out.append(f"timeline start field {view.get('start_field')!r} isn't declared")
    for s in view.get("sort", []):
        if not store.declares(kinds, s.get("by", "")):
            out.append(f"sort key {s.get('by')!r} isn't declared")
    g = view.get("group")
    if g and not (("field" in g and store.declares(kinds, g["field"])) or ("link" in g and link_ok(g["link"]))):
        out.append(f"group {g!r} names no declared field or link")
    return [{"view": key, "detail": d} for d in out]


def reject_column(store, kinds, col):
    if not isinstance(col, dict):
        return [f"column {col!r} isn't an object; name a field, live, link, agreement, state, verification or body"]
    if "field" in col or "live" in col:
        name = col.get("field") or col.get("live")
        return [] if store.declares(kinds, name) else [f"column field {name!r} isn't declared on {kinds}"]
    if "link" in col:
        path = col["link"] if isinstance(col["link"], list) else [col["link"]]
        return [f"column link {n!r} is neither a link kind nor a reverse" for n in path if not link_ok(n)]
    if "agreement" in col:
        return [] if col["agreement"] in AGREEMENT_PARTS else [f"agreement column {col['agreement']!r}"]
    if "verification" in col:
        return [] if col["verification"] in VERIFICATION_PARTS else [f"verification column {col['verification']!r}"]
    if "state" in col or "body" in col:
        return []
    return [f"column {col!r} names nothing a view can show"]


def meets(store, item, cond, subject=None):
    if "field" in cond:
        cond = {k: (subject if x == "page subject" else
                    [subject if y == "page subject" else y for y in x] if isinstance(x, list) else x)
                for k, x in cond.items()}
        v = store.value(item, cond["field"])
        vals = v if isinstance(v, list) else [v]
        if "is" in cond:
            return v not in EMPTY and cond["is"] in vals
        if "in" in cond:
            return v not in EMPTY and any(x in cond["in"] for x in vals)
        if "not-in" in cond:
            return v in EMPTY or not any(x in cond["not-in"] for x in vals)
    targets = store.targets(item, cond["link"])
    want = cond.get("to", cond.get("not-to"))
    if want == "none":
        hit = bool(targets)
        return not hit if "to" in cond else hit
    hit = any(t == want or (store.by_id.get(t) or {}).get("kind") == want for t in targets)
    return hit if "to" in cond else not hit


def select(store, view, subject=None):
    kinds = set(view.get("of") or []) | ({view.get("rows"), view.get("cols")} if view.get("as") == "matrix" else set())
    named = {c.get("is") for c in view.get("where", []) if c.get("field") == "state"} | \
        {s for c in view.get("where", []) if c.get("field") == "state" for s in c.get("in", [])}
    rows = []
    for item in store.items:
        if item.get("kind") not in kinds:
            continue
        if item.get("state") in ("superseded", "withdrawn") and item.get("state") not in named:
            continue
        if all(meets(store, item, c, subject) for c in view.get("where", [])):
            rows.append(item)
    return rows


def cell(store, item, col):
    empty = col.get("empty", "")
    if "field" in col or "live" in col:
        v = store.value(item, col.get("field") or col.get("live"))
        if isinstance(v, list):
            v = "; ".join(str(x) for x in v)
    elif "body" in col:
        v = " ".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in item.get("body", []))
    elif "link" in col:
        path = col["link"] if isinstance(col["link"], list) else [col["link"]]
        frontier = [item.get("id")]
        for name in path:
            nxt = []
            for t in frontier:
                src = store.by_id.get(t)
                if src is not None:
                    nxt += store.targets(src, name)
            frontier = nxt
        if col.get("kinds"):
            frontier = [t for t in frontier if (store.by_id.get(t) or {}).get("kind") in col["kinds"]]
        v = "<br>".join(x for x in (store.label(t, col.get("show")) for t in frontier) if x)
    elif "agreement" in col:
        a = store.covering(item.get("id"))
        v = a.get(col["agreement"]) if a else None
        if isinstance(v, list):
            v = ", ".join(v)
    elif "state" in col:
        v = item.get("state")
        if item.get("why"):
            v = f"{v}: {item['why']}"
    else:
        vs = [e for e in item.get("evidence", []) if isinstance(e, dict) and "outcome" in e]
        latest = max(vs, key=lambda e: e.get("when") or "") if vs else None
        v = latest.get(col["verification"]) if latest else None
    return empty if v in EMPTY else str(v)


PERIOD_RE = re.compile(r"^P(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)W)?(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?)?$")
PERIOD_SECONDS = (365 * 86400, 30 * 86400, 7 * 86400, 86400, 3600, 60, 1)


def period_value(v):
    m = PERIOD_RE.match(str(v))
    if not m:
        return None
    return sum(float(g) * n for g, n in zip(m.groups(), PERIOD_SECONDS) if g)


def sort_key(store, item, s, kind_types):
    v = store.value(item, s["by"])
    if isinstance(v, list):
        v = v[0] if v else None
    if v in EMPTY:
        return (1 if s.get("empty") != "first" else -1, 0)
    ftype = kind_types.get(s["by"])
    if s["by"] in ("decide_by", "review.next") or ftype == "when":
        m, r = ID_RE.match(str(v)), ROUND_RE.match(str(v))
        rank = (0, str(v), 0) if DATE_RE.match(str(v)) else (1, "", 0) if v == "build start" else \
            (2, m.group(1), int(m.group(2))) if m else (3, "", int(r.group(1))) if r else \
            (4, "", 0) if v == "close-out" else (5, str(v), 0)
        return (0, rank)
    if s["by"] == "id" or ftype == "id":
        m = ID_RE.match(str(v))
        return (0, (m.group(1), int(m.group(2))) if m else (str(v), 0))
    if isinstance(ftype, dict):
        enum = ftype.get("enum", [])
        return (0, (-enum.index(v) if v in enum else 1, ""))
    if ftype == "period" and period_value(v) is not None:
        return (0, (period_value(v), ""))
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return (0, (v, ""))
    return (0, (0, str(v)))


def ordered(store, view, rows):
    types = {}
    for k in view.get("of") or []:
        spec = store.kinds.get(k, {})
        types.update(spec.get("fields", {}))
        types.update(spec.get("live", {}))
    for s in reversed(view.get("sort", [])):
        nonempty = [r for r in rows if store.value(r, s["by"]) not in EMPTY]
        blank = [r for r in rows if store.value(r, s["by"]) in EMPTY]
        nonempty.sort(key=lambda r: sort_key(store, r, s, types), reverse=bool(s.get("desc")))
        rows = blank + nonempty if s.get("empty") == "first" else nonempty + blank
    return rows


def grouped(store, view, rows):
    g = view.get("group")
    if not g or view.get("as") == "chain":
        return [{"group": None, "rows": rows}]
    groups, blank = {}, []
    for r in rows:
        if "field" in g:
            v = store.value(r, g["field"])
            v = (v[0] if v else None) if isinstance(v, list) else v
            key = None if v in EMPTY else str(v)
        else:
            ts = store.targets(r, g["link"])
            key = store.label(ts[0]) if ts else None
        (blank if key is None else groups.setdefault(key, [])).append(r)
    out = [{"group": k, "rows": v} for k, v in groups.items()]
    if blank:
        out.append({"group": "(none)", "rows": blank})
    return out


def ranks(store, rows, cols, types):
    """Per row, each cell's rank in the port's order for its column, for a backend that re-sorts."""
    out = [[0] * len(cols) for _ in rows]
    for j, col in enumerate(cols):
        name = col if isinstance(col, str) else col.get("field") or col.get("live")
        if name:
            def key(r, name=name):
                return sort_key(store, r, {"by": name}, types) if store.value(r, name) not in EMPTY else (1, (0, ""))
        else:
            def key(r, col=col):
                v = cell(store, r, col)
                return (0, (0, v)) if v else (1, (0, ""))
        for rank, i in enumerate(sorted(range(len(rows)), key=lambda i: key(rows[i]))):
            out[i][j] = rank
    return out


def column_label(col):
    if col.get("label"):
        return col["label"]
    if "state" in col:
        return "State"
    if "body" in col:
        return "Body"
    if "agreement" in col:
        return f"Agreement {col['agreement']}"
    if "verification" in col:
        return f"Latest {col['verification']}"
    name = col.get("field") or col.get("live") or col.get("link")
    return " → ".join(name) if isinstance(name, list) else str(name)


def resolve(store, view, subject=None):
    rows = ordered(store, view, select(store, view, subject))
    pres = view.get("as")
    res = {"caption": view.get("caption"), "as": pres}
    if view.get("render"):
        res["render"] = view["render"]
    joins = any("live" in c for c in view.get("columns", [])) or \
        (pres == "matrix" and store.kinds.get(view.get("rows"), {}).get("live"))
    if joins and store.observed:
        res["caption"] += f" — as observed {store.observed}"
    elif joins:
        res["caption"] += " — live state not observed"
    base = ["Id", "Title"]
    if pres in ("table", "list", "cards"):
        cols = view.get("columns", [])
        res["header"] = base + [column_label(c) for c in cols]
        types = {}
        for k in view.get("of") or []:
            types.update(store.kinds.get(k, {}).get("fields", {}))
            types.update(store.kinds.get(k, {}).get("live", {}))
        res["groups"] = []
        for g in grouped(store, view, rows):
            res["groups"].append({"group": g["group"],
                                  "rows": [[r["id"], r.get("title", "")] + [cell(store, r, c) for c in cols] for r in g["rows"]],
                                  "ranks": ranks(store, g["rows"], ["id", "title"] + cols, types)})
    elif pres == "matrix":
        rkind, ckind = view.get("rows"), view.get("cols")
        rws = [r for r in rows if r.get("kind") == rkind]
        cls = [c for c in rows if c.get("kind") == ckind]
        path = view["cell"] if isinstance(view["cell"], list) else [view["cell"]]
        live = list(store.kinds.get(rkind, {}).get("live", {}))
        res["header"] = base + live + [c["id"] for c in cls]
        out = []
        for r in rws:
            reach = cell(store, r, {"link": path, "show": "id"}).split("<br>")
            out.append([r["id"], r.get("title", "")] + [cell(store, r, {"live": n}) for n in live]
                       + [c["id"] if c["id"] in reach else view.get("empty", "") for c in cls])
        res["groups"] = [{"group": None, "rows": out}]
        rows = rws
    elif pres in ("graph", "chain"):
        edges, seen = [], set()
        if pres == "graph":
            sel = {r["id"] for r in rows}
            for r in rows:
                for name in view.get("edges", []):
                    for t in store.targets(r, name):
                        if t in sel or t not in store.by_id:
                            edges.append([r["id"], name, t, store.label(t)])
            res["header"] = base + ["Link", "Target"]
            tbl = [[e[0], store.by_id[e[0]].get("title", ""), e[1], e[3]] for e in edges]
            linked = {e[0] for e in edges} | {e[2] for e in edges}
            tbl += [[r["id"], r.get("title", ""), "", ""] for r in rows if r["id"] not in linked]
        else:
            follow = view["follow"] if isinstance(view["follow"], list) else [view["follow"]]
            sel = {r["id"] for r in rows} | {view["start"]}
            tbl, left_out = [], [0]
            def walk(iid, depth, src, via):
                item = store.by_id.get(iid)
                title = item.get("title", "") if item else store.label(iid)
                if iid in seen:
                    tbl.append([iid, title, src or "", f"{via} (repeats)"])
                    return
                seen.add(iid)
                tbl.append([iid, title, src or "", via or ""])
                if item is None:
                    return
                name = follow[depth % len(follow)]
                for t in store.targets(item, name):
                    if t in store.by_id and t not in sel:
                        left_out[0] += 1
                        continue
                    edges.append([iid, name, t, store.label(t)])
                    walk(t, depth + 1, iid, name)
            walk(view["start"], 0, None, None)
            rows = tbl
            if left_out[0]:
                res["caption"] += f" — {left_out[0]} links left out"
            res["header"] = base + ["From", "Link"]
        res["edges"] = edges
        res["groups"] = [{"group": None, "rows": tbl}]
    else:
        sf, ef = view.get("start_field"), view.get("end_field")
        tbl, not_placed = [], []
        for r in rows:
            s, e = store.value(r, sf), store.value(r, ef) if ef else None
            end = "milestone" if not ef or e in EMPTY or e == s else str(e)
            tbl.append([r["id"], r.get("title", ""), "" if s in EMPTY else str(s), end]
                       + [cell(store, r, c) for c in view.get("columns", [])])
            if s in EMPTY or not DATE_RE.match(str(s)) or (end != "milestone" and not DATE_RE.match(end)):
                not_placed.append(f"{r['id']} ({'no start' if s in EMPTY else 'not a date'})")
        res["header"] = base + ["Start", "End"] + [column_label(c) for c in view.get("columns", [])]
        res["groups"] = [{"group": None, "rows": tbl}]
        res["not_placed"] = not_placed
    res["none"] = not rows
    return res


def markdown(key, res):
    lines = [f"<!-- view {key[0] or 'index'} {key[1]} -->", f"*{res['caption']}*", ""]
    if res["none"]:
        lines.append("none")
    for g in res["groups"]:
        if res["none"]:
            break
        if g["group"] is not None:
            lines += [f"**{g['group']}**", ""]
        lines.append("| " + " | ".join(res["header"]) + " |")
        lines.append("|" + "---|" * len(res["header"]))
        for row in g["rows"]:
            lines.append("| " + " | ".join(str(c).replace("|", "\\|").replace("\n", " ") for c in row) + " |")
        lines.append("")
    if res.get("not_placed"):
        lines.append("Not placed: " + ", ".join(res["not_placed"]))
    lines.append("<!-- /view -->")
    return "\n".join(lines)


def main(argv):
    args = [a for a in argv[1:] if a != "--markdown"]
    if not args or len(args) > 2:
        print(__doc__, file=sys.stderr)
        return 2
    with open(args[0], encoding="utf-8") as fh:
        data = json.load(fh)
    live = None
    if len(args) == 2:
        with open(args[1], encoding="utf-8") as fh:
            live = json.load(fh)
    store = Store(data, live)
    out = {"rejections": [], "views": []}
    for entry in data.get("views", []):
        key = (entry.get("page"), entry.get("position"))
        view = entry.get("view") or {}
        rej = reject_view(store, key, view, entry.get("subject"))
        if rej:
            out["rejections"] += rej
            continue
        res = resolve(store, view, entry.get("subject"))
        out["views"].append(dict(page=key[0], position=key[1], **res))
    if "--markdown" in argv:
        for r in out["rejections"]:
            print(f"REJECTED {r['view']}: {r['detail']}", file=sys.stderr)
        print("\n\n".join(markdown((v["page"], v["position"]), v) for v in out["views"]))
    else:
        print(json.dumps(out, indent=2, ensure_ascii=False))
    return 1 if out["rejections"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
