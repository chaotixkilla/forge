#!/usr/bin/env python3
"""Render a page tree and its resolved views into the claude-artifacts site.

Usage: render_site.py <site.json> <views.json> <out-dir> [<items.json>]

<site.json> is the tree in the shape the claude-artifacts adapter pins; <views.json> is
resolve_views.py's JSON output for the same store. Writes <out-dir>/index.html, each
other page at its path, and items.json when given. The stylesheet and script are inlined
into every page; index.html is written without a document skeleton, which the host adds,
and every other page with its own.
Prints the written paths, index.html first. Exits 1, writing nothing, when a page names a
view the views file doesn't hold, a part outside now, plan and records, or no index.html.
"""
import html
import json
import os
import re
import shutil
import sys

PARTS = {"now": "Now", "plan": "The plan", "records": "Work records"}
TONES = {
    "holds": {"settled", "holds", "agreed", "merged", "built", "passed", "done", "met", "live", "recorded", "mitigated", "closed"},
    "open": {"open", "missing", "fails", "failed", "not set", "not named", "blocked", "late", "occurred", "high", "unsourced"},
    "unsettled": {"may change", "proposed", "lean", "deferred", "not checked", "not tested", "unverified", "planned", "medium",
                  "in review", "draft", "partly built", "unsettled"},
    "unchecked": {"none", "(none)", "low", "withdrawn", "superseded", "not recorded", "n/a", "unknown"},
}
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
FONTS = ("https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500;6..72,600"
         "&family=Public+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap")


KIND_WORDS = {"REQ": "Requirement", "AC": "Acceptance criterion", "Q": "Question", "DEC": "Decision", "BRF": "Brief", "RISK": "Risk",
              "ASM": "Assumption", "ISS": "Issue", "DEP": "Dependency", "UNIT": "Unit of work", "SLC": "Slice", "GATE": "Gate", "MET": "Metric",
              "TEST": "Test", "GRAD": "Graduation criterion", "THR": "Threat", "PTH": "Privacy threat", "MIT": "Mitigation", "ELM": "Element of the system",
              "SCR": "Screening criterion", "VEN": "Vendor", "RST": "Restore path", "RDY": "Readiness check", "BRK": "Breaking change", "MSG": "Notice",
              "A11Y": "Accessibility finding", "TERM": "Term", "FAQ": "FAQ answer", "DES": "Design section", "QG": "Quality goal", "IFC": "Interface",
              "NS": "North-star goal", "SLO": "Objective", "ALR": "Alert", "PROC": "Procedure", "AGR": "Agreement", "OVW": "Overview"}
ID_PAT = re.compile(r"\b(" + "|".join(sorted(KIND_WORDS, key=len, reverse=True)) + r")-(\d+)\b")


def nice(iid):
    """What a reader sees for an item's code: its step code for gates and slices, else its kind in words and number."""
    m = ID_PAT.fullmatch(iid or "")
    if not m:
        return iid
    item = (MODEL[0].by.get(iid) if MODEL[0] else None) or {}
    title = item.get("title", "")
    if m.group(1) in ("GATE", "SLC") and " · " in title and len(title.split(" · ")[0]) <= 4:
        return title.split(" · ")[0]
    return iid


REFS = [{}, []]  # site.json's refs (id as written -> {"url", "title"}) and ref_patterns ({match, url} with {1}.. groups)
USED_REFS = {}  # the sources the site mentions, for the Sources key: id -> (url, title)


def ref_rx():
    exact, pats = REFS
    if not exact and not pats:
        return None
    alts = [re.escape(k) for k in sorted(exact, key=len, reverse=True)] + [p_["match"] for p_ in pats]
    return re.compile(r"(?<![\w#/-])(?:" + "|".join(f"(?:{a})" for a in alts) + r")(?![\w-])")


def ref_for(t):
    """(url, title) for a mention of an outside source: the url from its refs entry, else from its pattern; the title
    from its refs entry, "" when it has none and "what it is isn't recorded" when the entry says null."""
    exact, pats = REFS
    url, title = "", ""
    if t in exact:
        v = exact[t]
        if isinstance(v, str):
            url = v
        else:
            v = v or {}
            url = v.get("url") or ""
            if "title" in v:
                title = v["title"] or "what it is isn't recorded"
    if not url:
        for p_ in pats:
            mm = re.fullmatch(p_["match"], t)
            if mm:
                url = re.sub(r"\{(\d+)\}", lambda g: mm.group(int(g.group(1))) or "", p_.get("url") or "")
                break
    return url, title


def link_refs(markup):
    """Link every outside source the site maps in refs or ref_patterns, with its title on hover, outside tags, links,
    code and SVG; a titled source with no address is marked so its title still shows."""
    rx = ref_rx()
    if not rx:
        return markup

    def one(mm):
        t = mm.group(0)
        url, title = ref_for(t)
        tip = f' title="{html.escape(title, quote=True)}"' if title else ""
        if url:
            return f'<a class="ext" href="{html.escape(url, quote=True)}" target="_blank" rel="noopener"{tip}>{t}</a>'
        return f'<span class="src"{tip}>{t}</span>' if title else t
    parts = re.split(r"(<[^>]+>)", markup)
    skip = 0
    for k, part in enumerate(parts):
        if part.startswith("<"):
            low = part.lower()
            if re.match(r"<(a|script|style|code|pre|title|svg|abbr)\b", low) or low.startswith('<span class="src"'):
                skip += 1
            elif re.match(r"</(a|script|style|code|pre|title|svg|abbr)>", low) or (skip and low == "</span>"):
                skip = max(0, skip - 1)
            continue
        if not skip:
            parts[k] = rx.sub(one, part)
    return "".join(parts)


def name_ids(markup):
    """Replace item codes in text (never inside tags or attributes) with their reader names, the code kept as a tooltip."""
    def one(mm):
        iid = mm.group(0)
        item = (MODEL[0].by.get(iid) if MODEL[0] else None) or {}
        kind = KIND_WORDS.get(mm.group(1), "").lower()
        tip = html.escape(iid + " · " + kind + (" · " + item["title"] if item.get("title") else ""), quote=True)
        return f'<abbr title="{tip}">{html.escape(nice(iid))}</abbr>'
    parts = re.split(r"(<[^>]+>)", markup)
    inside_code = 0
    for k, part in enumerate(parts):
        if part.startswith("<"):
            low = part.lower()
            if low.startswith(("<script", "<style", "<code", "<pre", "<title", "<svg")):
                inside_code += 1
            elif low.startswith(("</script", "</style", "</code", "</pre", "</title", "</svg")):
                inside_code = max(0, inside_code - 1)
            continue
        if not inside_code:
            parts[k] = ID_PAT.sub(one, part)
    return "".join(parts)


def inline(text):
    """Escape, then render **bold**, `code` and [text](href)."""
    s = html.escape(str(text or ""), quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![*\w])\*([^*\n]+)\*(?![*\w])", r"<i>\1</i>", s)
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: f'<a href="{html.escape(m.group(2))}">{m.group(1)}</a>', s)


def tone(text):
    t = str(text or "").strip().lower()
    head = t.split(":")[0].strip()
    for name, words in TONES.items():
        if t in words or head in words:
            return name
    return None


def cell(text):
    """A table or card value: a lone state word becomes a chip, an id stays an id."""
    t = str(text or "")
    if not t:
        return ""
    if "<br>" in t:
        return "<br>".join(cell(x) for x in t.split("<br>"))
    if re.match(r"^[A-Z][A-Z0-9]*-\d+$", t):
        return f'<span class="id">{t}</span>'
    k = tone(t)
    if k and len(t) <= 40:
        return f'<span class="chip c-{k}">{html.escape(t)}</span>'
    m = re.match(r"^([A-Z][A-Z0-9]*-\d+) · (.*)$", t)
    if m:
        return f'<span class="id">{m.group(1)}</span> {inline(m.group(2))}'
    return inline(t)


def label(h):
    return h[:1].upper() + h[1:] if h else h


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-") or "section"


def table_html(header, rows, ranks=None, sortable=False):
    out = ['<div class="tbl"><table><thead><tr>']
    for h in header:
        out.append(f'<th{" data-sortable" if sortable else ""}>{html.escape(label(h))}</th>')
    out.append("</tr></thead><tbody>")
    for i, row in enumerate(rows):
        out.append(f'<tr data-item="{html.escape(str(row[0]))}">' if sortable else "<tr>")
        for j, c in enumerate(row):
            rank = f' data-sort="{ranks[i][j]}"' if ranks else ""
            wide = ' class="wide"' if len(str(c)) > 80 else ""
            out.append(f"<td{rank}{wide}>{cell(c)}</td>")
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def static_tables(v):
    out = []
    for g in v["groups"]:
        if g.get("group") is not None:
            out.append(f'<p class="group">{inline(g["group"])}</p>')
        out.append(table_html(v["header"], g["rows"], g.get("ranks"), sortable=False))
    return "".join(out)


def alt(v):
    return f'<details class="alt"><summary>Table form, for reading or printing</summary>{static_tables(v)}</details>'


def card(header, row):
    pairs = [(h, c) for h, c in zip(header[2:], row[2:]) if c]
    short = [(h, c) for h, c in pairs if len(str(c)) <= 24 and "<br>" not in str(c)]
    long_ = [(h, c) for h, c in pairs if (h, c) not in short]
    facts = "".join(f"<span>{html.escape(label(h))} {cell(c) if tone(c) else '<b>' + inline(c) + '</b>'}</span>" for h, c in short)
    fields = "".join(f"<dt>{html.escape(label(h))}</dt><dd>{cell(c)}</dd>" for h, c in long_)
    return (f'<article class="card" data-item="{html.escape(str(row[0]))}"><h3><span class="id">{row[0]}</span> '
            f'{inline(row[1])}</h3>{"<div class=facts>" + facts + "</div>" if facts else ""}'
            f'{"<dl>" + fields + "</dl>" if fields else ""}</article>')


def view_html(v, view_opts):
    cap = f'<p class="caption">{inline(v["caption"])}</p>'
    if v["none"]:
        return f'{cap}<p><span class="chip c-unchecked">none</span></p>'
    many = sum(len(g["rows"]) for g in v["groups"]) > 8
    filt = '<input class="filter" type="search" placeholder="Filter rows" aria-label="Filter rows">' if many else ""
    pres = v["as"]
    if pres == "cards":
        if any(g.get("group") is not None for g in v["groups"]):
            lanes = "".join(f'<div class="lane"><header><span>{inline(g["group"])}</span><span>{len(g["rows"])}</span></header>'
                            + "".join(card(v["header"], r) for r in g["rows"]) + "</div>" for g in v["groups"])
            return f'{cap}{filt}<div class="board">{lanes}</div>{alt(v)}'
        cards = "".join(card(v["header"], r) for r in v["groups"][0]["rows"])
        return f'{cap}{filt}<div class="cards">{cards}</div>{alt(v)}'
    if pres == "timeline":
        mark = view_opts.get("mark") or {}
        col = v["header"].index(mark["column"]) if mark.get("column") in v["header"] else None
        items = []
        stage_seen = set()
        stage_col = v["header"].index(view_opts["stage"]) if view_opts.get("stage") in v["header"] else None
        for r in v["groups"][0]["rows"]:
            cls = "dot oneway" if col is not None and str(r[col]) == str(mark.get("is")) else "dot"
            stage = ""
            if stage_col is not None and r[stage_col] and r[stage_col] not in stage_seen:
                stage_seen.add(r[stage_col])
                stage = f'<span class="stage">{html.escape(str(r[stage_col]))}</span>'
            when = r[2] if r[2] else "undated"
            items.append(f'<li>{stage}<i class="{cls}"></i><b>{r[0]}</b><span title="{html.escape(str(r[1]))}">'
                         f'{inline(r[1] if len(str(r[1])) <= 34 else str(r[1])[:32] + "…")}</span><em>{html.escape(str(when))}</em></li>')
        key = '<div class="key"><span>○ a step</span>' + (f'<span>◆ {inline(mark.get("means", "marked"))}</span>' if col is not None else "") + "</div>"
        return f'{cap}<div class="rail"><ol>{"".join(items)}</ol></div>{key}{alt(v)}'
    if pres == "matrix":
        g = v["groups"][0]
        head = "".join(f'<th class="c">{html.escape(h)}</th>' for h in v["header"][2:])
        body = "".join(f'<tr><td><span class="id">{r[0]}</span> {inline(r[1])}</td>'
                       + "".join(f'<td class="c">{"<i class=d title=" + chr(34) + html.escape(str(x)) + chr(34) + "></i>" if x and x not in ("·", "none") else ""}</td>' for x in r[2:])
                       + "</tr>" for r in g["rows"])
        return f'{cap}<div class="tbl"><table class="dots"><thead><tr><th></th>{head}</tr></thead><tbody>{body}</tbody></table></div>{alt(v)}'
    out = [cap, filt]
    for g in v["groups"]:
        if g.get("group") is not None:
            out.append(f'<p class="group">{inline(g["group"])}</p>')
        out.append(table_html(v["header"], g["rows"], g.get("ranks"), sortable=bool(g.get("ranks"))))
    return "".join(out)


# ---- instruments: pages built around a reader's task, computed from the store ----

def shy(markup):
    """Soft hyphens in long words of a narrow label, at a vowel-consonant seam near the middle, so a word that can't fit
    breaks at a syllable with a hyphen rather than at any letter. Text between tags only."""
    def word(mm):
        w = mm.group(0)
        v = lambda k: w[k].lower() in "aeiouy"
        seams = [i for i in range(3, len(w) - 3) if v(i + 1) and not v(i) and w[i - 1:i + 1].lower() not in ("sh", "ch", "th", "ph", "ck", "gh", "wh")
                 and (v(i - 1) or (not v(i - 1) and v(i - 2)))]  # before a consonant-vowel, after a vowel or a vowel-consonant
        if not seams:
            return w
        i = min(seams, key=lambda k: abs(k - len(w) / 2))
        return w[:i] + "\u00ad" + w[i:]
    return "".join(part if part.startswith("<") else re.sub(r"(?<=\w)([._/])(?=\w)", "\\1\u200b", re.sub(r"[A-Za-z]{10,}", word, part))
                   for part in re.split(r"(<[^>]+>)", markup))


def body_only(item):
    """An item's filed body as plain text, whatever block shape it was filed in."""
    def one(b):
        if not isinstance(b, dict):
            return str(b)
        for k in ("p", "text", "callout", "quote"):
            if b.get(k):
                return str(b[k])
        for k in ("ul", "ol", "steps"):
            if isinstance(b.get(k), list):
                return "; ".join(str(x) for x in b[k])
        return ""
    return " ".join(t for t in map(one, item.get("body", []) or []) if t).strip()


def body_text(item):
    return body_only(item) or item.get("title", "")


class Model:
    def __init__(self, store):
        self.items = store.get("items", []) if store else []
        self.agreements = store.get("agreements", []) if store else []
        self.by = {i["id"]: i for i in self.items}
        self.rev = {}
        for i in self.items:
            for l in i.get("links", []):
                self.rev.setdefault((l.get("to"), l.get("link")), []).append(i["id"])

    def kind(self, k):
        return [i for i in self.items if i.get("kind") == k and i.get("state") not in ("superseded", "withdrawn")]

    def out(self, item, link, kind=None):
        return [l["to"] for l in item.get("links", []) if l.get("link") == link
                and (kind is None or self.by.get(l["to"], {}).get("kind") == kind)]

    def into(self, iid, link, kind=None):
        return [x for x in self.rev.get((iid, link), []) if kind is None or self.by[x].get("kind") == kind]

    def verdicts(self, item):
        vs = [e for e in item.get("evidence", []) if isinstance(e, dict) and e.get("outcome")]
        for t in self.into(item["id"], "verifies"):
            vs += [e for e in self.by[t].get("evidence", []) if isinstance(e, dict) and e.get("outcome")]
        return sorted(vs, key=lambda e: e.get("when") or "")

    def holds(self, item):
        v = self.verdicts(item)
        return bool(v) and v[-1].get("outcome") == "holds"

    def req_status(self, r):
        acs = self.into(r["id"], "serves", "acceptance criterion")
        units = self.into(r["id"], "serves", "unit")
        if self.holds(r) or (acs and all(self.holds(self.by[a]) for a in acs)):
            return "met"
        if any(self.holds(self.by[a]) for a in acs) or any((self.by[u].get("fields") or {}).get("ships in") for u in units):
            return "partly"
        return "not yet"

    def evidence(self, item):
        out = []
        for e in item.get("evidence", []):
            if isinstance(e, dict):
                out.append({"mark": {"holds": "ok", "fails": "bad"}.get(e.get("outcome"), "src" if not e.get("outcome") else "warn"),
                            "what": e.get("what", ""), "link": e.get("link"), "when": e.get("when")})
        return out


def trace_data(m):
    reqs = m.kind("requirement")
    req_ids = {r["id"] for r in reqs}
    units = [u for u in m.kind("unit") if any(t in req_ids for t in m.out(u, "serves"))]
    gates = gates_in_order(m)
    unit_ids = {u["id"] for u in units}
    data = {"work": [], "reqs": [], "gates": [], "links": []}
    for u in sorted(units, key=lambda u: (u.get("fields") or {}).get("order") or 0):
        f = u.get("fields") or {}
        data["work"].append({"id": u["id"], "label": f.get("ships in") or u["id"], "title": u.get("title", ""),
                             "merged": bool(f.get("ships in")), "body": body_text(u)})
        for t in m.out(u, "serves"):
            if t in req_ids:
                data["links"].append([u["id"], t])
    for r in reqs:
        f = r.get("fields") or {}
        acs = [m.by[a] for a in m.into(r["id"], "serves", "acceptance criterion")]
        data["reqs"].append({
            "id": r["id"], "title": r.get("title", ""), "shall": body_text(r), "group": f.get("stream") or "Other",
            "status": m.req_status(r), "why": f.get("rationale", ""), "verification": f.get("verification", ""),
            "accepted": [{"id": a["id"], "text": a.get("title", ""), "ok": m.holds(a)} for a in acs],
            "evidence": m.evidence(r) + [e for a in acs for e in m.evidence(a) if e["mark"] in ("ok", "bad", "warn")],
            "waits": m.out(r, "blocked-by")})
    for g in gates:
        f = g.get("fields") or {}
        ran = any(isinstance(e, dict) and e.get("outcome") for e in g.get("evidence", []))
        data["gates"].append({"id": g["id"], "title": g.get("title", ""), "when": f.get("opens on") or "",
                              "oneway": f.get("one-way") == "yes", "ran": ran})
        for u in m.out(g, "blocked-by", "unit"):
            if u in unit_ids:
                for t in m.out(m.by[u], "serves"):
                    if t in req_ids:
                        data["links"].append([t, g["id"]])
    data["links"] = [list(x) for x in dict.fromkeys(tuple(l) for l in data["links"])]
    return data


def testing_html(m):
    f_ = lambda i: i.get("fields") or {}
    tests, grads = m.kind("test"), m.kind("graduation criterion")
    out = []
    if tests:
        order = {}
        for t in tests:
            order.setdefault(str(f_(t).get("before") or "not set"), []).append(t)
        rows = []
        for when, ts in order.items():
            g = m.by.get(when)
            head = (g.get("title", when) if g else when)
            body = "".join(xrow(t, cell(m.verdicts(t)[-1]["outcome"] if m.verdicts(t) else "not run") + f' <span class="chip c-unchecked">{html.escape(f_(t).get("method", ""))}</span>',
                                f'<p><b>Passes when</b> {inline(f_(t).get("pass when", ""))}</p><p class="muted small">{html.escape(f_(t).get("purpose", ""))} · in {html.escape(", ".join(f_(t).get("environments", [])) or "no environment named")} · checks {ids(m.out(t, "verifies"))}</p>') for t in ts)
            rows.append(f'<p class="group">Before {inline(head)} <span class="count">{len(ts)}</span></p><div class="reqs">{body}</div>')
        out.append('<h3 class="sub">How it is tested</h3><p class="caption">Each test, grouped by the gate it must pass before, with its latest result.</p>' + "".join(rows))
    skew = [d for d in m.kind("design section") if f_(d).get("aspect") == "version skew"]
    compat = [t for t in tests if re.search(r"compat|skew", str(f_(t).get("purpose", "")))]
    if skew or sec_paras("Do old and new versions work together?"):
        why = " ".join(body_only(d) for d in skew) or " ".join(sec_paras("Do old and new versions work together?"))
        out.append(f'<div class="rung {"ok" if compat else "gap"}"><b>Old and new side by side</b>'
                   + (f'<span class="chip c-holds">{len(compat)} test{"s" if len(compat) != 1 else ""}</span>' if compat else '<span class="chip c-open">no test planned</span>')
                   + f'<p class="small">{inline(why)}</p></div>')
    if grads:
        out.append('<h3 class="sub">What must hold before each stage</h3><div class="reqs">' + "".join(
            xrow(g, cell("holds" if m.out(g, "rests-on") and all(m.holds(m.by[x]) for x in m.out(g, "rests-on") if x in m.by) else "not shown yet")
                 + f' <span class="muted small">before {html.escape(", ".join((m.by.get(x, {}).get("title", "").split(" · ")[0] or x) for x in m.out(g, "serves")) or str(f_(g).get("before") or "a gate not named"))}</span>',
                 f'<p><b>Stage.</b> {inline(f_(g).get("stage", ""))}</p><p class="small">Rests on ' + " ".join(f'{ids([x])} {cell("holds" if x in m.by and m.holds(m.by[x]) else "not shown yet")}' for x in m.out(g, "rests-on")) + f'; opens {ids(m.out(g, "serves"))}.</p>') for g in grads) + '</div>')
    return "".join(out)


def ac_html(m, a):
    """One acceptance criterion as given / when / then, its counter-example, and the test that checks it with its latest outcome."""
    text = body_only(a) or a.get("title", "")
    main, _, counter = text.partition("counter-example:")
    mm = re.match(r"\s*Given (.+?),\s*when (.+?),\s*then (.+?)[;.]?\s*$", main.strip().rstrip(";"), re.I | re.S)
    parts = ("".join(f'<div><dt>{k}</dt><dd>{inline(v)}</dd></div>' for k, v in zip(("Given", "When", "Then"), mm.groups()))
             if mm else f'<div><dt>Holds when</dt><dd>{inline(main.strip())}</dd></div>')
    tests = [m.by[t] for t in m.into(a["id"], "verifies", "test")]
    def outcome(t):
        ev = [e for e in t.get("evidence", []) if isinstance(e, dict) and e.get("outcome")]
        return (ev[-1]["outcome"] + (" on " + str(ev[-1]["when"]) if ev[-1].get("when") else "")) if ev else "not run yet"
    tl = " · ".join(f'<span class="id">{t["id"]}</span> {html.escape(", ".join((t.get("fields") or {}).get("environments") or []) or (t.get("fields") or {}).get("method", ""))}: {html.escape(outcome(t))}' for t in tests)
    return (f'<div class="ac {"ok" if m.holds(a) else "todo"}" id="{a["id"]}"><p class="pk"><span class="id">{a["id"]}</span>'
            f'<span class="chip c-{"holds" if m.holds(a) else "unchecked"}">{"holds" if m.holds(a) else "not shown yet"}</span></p><dl class="gwt">{parts}</dl>'
            + (f'<p class="small"><b>Not this:</b> {inline(counter.strip())}</p>' if counter.strip() else "")
            + f'<p class="small muted">Checked by {tl or "no test yet"}</p></div>')


def requirements_html(m, trace=None):
    reqs = m.kind("requirement")
    groups = {}
    for r in reqs:
        groups.setdefault((r.get("fields") or {}).get("stream") or "Other", []).append(r)
    verifs = sorted({(r.get("fields") or {}).get("verification") for r in reqs} - {None})
    types = sorted({(r.get("fields") or {}).get("type") for r in reqs} - {None})
    chips = lambda name, vals: (f'<div class="chipset" data-filter="{name}"><span>{label(name)}</span>'
                                 f'<button aria-pressed="true" data-v="">All</button>'
                                 + "".join(f'<button aria-pressed="false" data-v="{html.escape(v)}">{html.escape(v)}</button>' for v in vals) + "</div>")
    jump = "".join(f'<a href="#stream-{i}">{inline(g)}</a>' for i, g in enumerate(groups, 1))
    noac = [r["id"] for r in reqs if not m.into(r["id"], "serves", "acceptance criterion")]
    tbr = [r["id"] for r in reqs if m.out(r, "blocked-by")]
    one = len(groups) == 1 and "Other" in groups
    ins = [("next", f'{len(reqs)} requirements{"" if one else " in " + str(len(groups)) + (" stream" if len(groups) == 1 else " streams")}; {sum(1 for r in reqs if m.req_status(r) == "met")} met so far.')]
    if tbr:
        ins.append(("ask", f'{len(tbr)} wait on an open question before they can be settled: {" ".join(tbr[:8])}{"…" if len(tbr) > 8 else ""}.'))
    if noac:
        ins.append(("bottleneck", f'{len(noac)} have no acceptance criterion, so nothing says when they hold: {" ".join(noac[:8])}{"…" if len(noac) > 8 else ""}.'))
    aims = m.kind("north-star clause")
    aim_html = ('<div class="aims">' + "".join(f'<div class="aim"><span class="id">{a["id"]}</span><p>{inline(a.get("title", ""))}</p></div>' for a in aims) + '</div>') if aims else ""
    out = [aim_html, insights_html(ins), f'<div class="onpage"><span>Streams</span>{jump}</div>' if len(groups) > 1 else "",
           f'<div class="filters">{chips("verification", verifs)}{chips("type", types)}'
           '<div class="legend"><span><i class="st st-met"></i> met</span><span><i class="st st-partly"></i> partly</span><span><i class="st st-notyet"></i> not yet</span></div></div>']
    for gi, (g, rs) in enumerate(groups.items(), 1):
        out.append(f'<section class="stream" id="stream-{gi}">' + ("" if one else f'<h2><span class="sn">{gi:02d}</span>{inline(g)}</h2>') + '<div class="reqs">')
        for r in rs:
            f = r.get("fields") or {}
            st = m.req_status(r)
            acs = [m.by[a] for a in m.into(r["id"], "serves", "acceptance criterion")]
            threats = [t for mit in m.out(r, "serves", "mitigation") for t in m.out(m.by[mit], "covers")]
            design = m.into(r["id"], "serves", "design section")
            waits = m.out(r, "blocked-by")
            own = m.verdicts(r)[-1] if m.verdicts(r) else None
            acc = "".join(ac_html(m, a) for a in acs) or (
                f'<p><span class="chip c-{"holds" if own.get("outcome") == "holds" else "open"}">{html.escape(own.get("outcome", ""))}</span> on its own check, with no criterion of its own: '
                f'{inline(own.get("what") or "")}{" · " + html.escape(str(own["when"])) if own.get("when") else ""}</p>' if own else
                '<p class="muted">No criterion yet: nothing says when this holds.</p>')
            refs = lambda ids: ", ".join(f'<span class="id">{i}</span>' for i in dict.fromkeys(ids)) or "none"
            out.append(
                f'<details class="req" id="{r["id"]}" data-verification="{html.escape(f.get("verification", ""))}" data-type="{html.escape(f.get("type", ""))}">'
                f'<summary><i class="st st-{st.replace(" ", "")}" title="{st}"></i><span class="id">{r["id"]}</span>'
                f'<span class="shall">{inline(body_text(r))}</span><span class="chip c-unchecked">{html.escape(f.get("verification", ""))}</span></summary>'
                f'<div class="more">' + (f'<p><b>Why.</b> {inline(f["rationale"])}</p>' if f.get("rationale") else "")
                + f'<h4>Accepted when</h4><div class="acs">{acc}</div><dl class="refs">'
                f'<div><dt>Waits on</dt><dd>{refs(waits)}</dd></div><div><dt>Covers threats</dt><dd>{refs(threats)}</dd></div>'
                f'<div><dt>Design</dt><dd>{refs(design)}</dd></div><div><dt>Kind</dt><dd>{html.escape(f.get("type", ""))} · {html.escape(f.get("priority", ""))}</dd></div></dl>'
                f'<p class="where">Where it stands now: <span class="chip c-{ {"met": "holds", "partly": "unsettled"}.get(st, "unchecked") }">{st}</span>{(" · <a href=" + chr(34) + trace + "#" + r["id"] + chr(34) + ">follow it in Trace</a>") if trace else ""}</p></div></details>')
        out.append("</div></section>")
    nots = sec_list("What is out of scope?")
    if nots:
        out.append('<div class="notdoing"><span class="tools-label">Not doing</span><ul>' + "".join(f'<li>{inline(x)}</li>' for x in nots) + '</ul></div>')
    return "".join(out)


def register_html(m, trace=None):
    waiting = [i for i in m.items if i.get("kind") in ("question", "decision") and i.get("state") in ("open", "lean", "proposed")]
    decided = [i for i in m.items if i.get("kind") == "decision" and i.get("state") == "agreed"]
    who = lambda i: (i.get("fields") or {}).get("decider") or "No decider yet"
    people = {}
    for i in waiting:
        people.setdefault(who(i), []).append(i)
    order = sorted(people, key=lambda p: (p == "No decider yet", -len(people[p])))
    tiles = ['<button class="ptile" aria-pressed="true" data-v=""><b>' + str(len(waiting)) + '</b><span>Everyone</span><em>'
             + str(sum(1 for i in waiting if (i.get("fields") or {}).get("tier") == "1")) + ' tier 1</em></button>']
    for p_ in order:
        t1 = sum(1 for i in people[p_] if (i.get("fields") or {}).get("tier") == "1")
        tiles.append(f'<button class="ptile{" nodecider" if p_ == "No decider yet" else ""}" aria-pressed="false" data-v="{html.escape(p_)}">'
                     f'<b>{len(people[p_])}</b><span>{html.escape(p_)}</span><em>{t1} tier 1</em></button>')
    nod = [i for i in waiting if not (i.get("fields") or {}).get("decider")]
    t1w = [i for i in waiting if (i.get("fields") or {}).get("tier") == "1"]
    ins = [("next", f'{len(waiting)} questions and decisions are waiting (open, leaning or proposed); {len(t1w)} of them are tier 1.')]
    if nod:
        ins.append(("bottleneck", f'{len(nod)} have nobody named to decide them, ' + (f'including tier-1 {" ".join(i["id"] for i in nod if (i.get("fields") or {}).get("tier") == "1")}.' if any((i.get("fields") or {}).get("tier") == "1" for i in nod) else "none of them tier 1.")))
    out = [insights_html(ins), f'<div class="chipset ptiles" data-filter="decider">{"".join(tiles)}</div>'
           '<p class="caption">Select a person to see only what waits on them.</p>']

    def refs(ids):
        def one(i):
            if trace and i.startswith("REQ-"):
                return f'<a class="id" href="{trace}#{i}">{i}</a>'
            return f'<span class="id">{i}</span>'
        return " ".join(one(i) for i in ids) or '<span class="muted">nothing yet</span>'

    def card(i):
        f = i.get("fields") or {}
        tier, st = f.get("tier", ""), i.get("state")
        state = {"proposed": "proposed · needs a yes", "lean": "leaning"}.get(st, st)
        tone_ = {"proposed": "unsettled", "lean": "unsettled"}.get(st, "open")
        blocks = m.into(i["id"], "blocked-by")
        brief = [m.by[b] for b in m.into(i["id"], "serves", "brief")]
        proposal = f.get("chosen") or f.get("lean") or (brief and (brief[0].get("fields") or {}).get("recommendation"))
        why = ", ".join(x for x in (f.get("reversibility") and ("hard to undo" if f["reversibility"] == "one-way" else "can be undone"),
                                     f.get("reach")) if x)
        decider = f.get("decider")
        b_html = ""
        if brief:
            bf = brief[0].get("fields") or {}
            b_html = (f'<details class="brief"><summary>The brief ({brief[0]["id"]}): ' + str(len(bf.get("options", []))) + ' options and a recommendation</summary>'
                      + '<ol>' + "".join(f"<li>{inline(o)}</li>" for o in bf.get("options", [])) + '</ol>'
                      + (f'<p><b>If nobody decides.</b> {inline(bf["if undecided"])}</p>' if bf.get("if undecided") else "") + '</details>')
        return (f'<article class="qcard t{tier}" id="{i["id"]}" data-decider="{html.escape(who(i))}">'
                f'<p class="pk"><span class="id">{i["id"]}</span><span class="chip c-{"open" if tier == "1" else "unchecked"}">Tier {tier}</span>'
                f'<span class="chip c-{tone_}">{html.escape(state)}</span></p><h3>{inline(i.get("title", ""))}</h3>'
                f'<div class="box"><b>Where it stands</b><p>{inline(body_only(i) or "Nothing is written yet on where it stands.")}</p></div>'
                + (f'<div class="box prop"><b>Proposal</b><p>{inline(proposal)}</p></div>' if proposal else "")
                + '<dl class="kv">'
                f'<dt>Blocks</dt><dd>{refs(list(dict.fromkeys(blocks)))}</dd>'
                f'<dt>Why this tier</dt><dd>{html.escape(why)}</dd>'
                f'<dt>Decide by</dt><dd>{html.escape(str(i.get("decide_by") or ""))}</dd>'
                f'<dt>Decider</dt><dd>{html.escape(decider) if decider else "<span class=" + chr(34) + "chip c-open" + chr(34) + ">nobody named</span>"}</dd>'
                + (f'<dt>Consulted</dt><dd>{html.escape(", ".join(f["consulted"]))}</dd>' if f.get("consulted") else "")
                + '</dl>' + b_html + '</article>')

    for tier, head in (("1", "Tier 1, waiting for an answer"), ("2", "Tier 2, waiting for an answer")):
        items = [i for i in waiting if (i.get("fields") or {}).get("tier") == tier]
        if not items:
            continue
        note = ("Hard to undo or reaching beyond the team: each needs its decider before the step it blocks." if tier == "1"
                else "Reversible and contained: settled by their owner as the work reaches them.")
        if tier == "1":
            body_ = f'<div class="qgrid">{"".join(card(i) for i in items)}</div>'
        else:
            def qrow(i):
                f = i.get("fields") or {}
                inner = card(i)
                return (f'<details class="req" data-decider="{html.escape(who(i))}"><summary><i class="st"></i><span class="id">{i["id"]}</span><span class="shall">{inline(i.get("title", ""))}</span>'
                        f'<span>{cell(i.get("state", ""))}<span class="muted small">{html.escape(str(i.get("decide_by") or ""))}</span></span></summary><div class="more">{inner}</div></details>')
            body_ = f'<div class="reqs">{"".join(qrow(i) for i in items)}</div>'
        out.append(f'<section class="stream"><h3 class="sub">{head} <span class="count">{len(items)}</span></h3><p class="caption">{note}</p>{body_}</section>')
    if decided:
        rows = []
        for d in decided:
            f = d.get("fields") or {}
            agr = next((a for a in m.items if False), None)
            rows.append(f'<details class="req"><summary><i class="st st-met"></i><span class="id">{d["id"]}</span>'
                        f'<span class="shall">{inline(d.get("title", ""))}</span><span class="chip c-holds">agreed</span></summary><div class="more">'
                        + (f'<p><b>Chosen.</b> {inline(f["chosen"])}</p>' if f.get("chosen") else "")
                        + ('<h4>Gains</h4><ul class="checks-list">' + "".join(f'<li class="ok">{inline(x)}</li>' for x in f.get("gains", [])) + '</ul>' if f.get("gains") else "")
                        + ('<h4>Costs</h4><ul class="checks-list">' + "".join(f'<li class="warn">{inline(x)}</li>' for x in f.get("costs", [])) + '</ul>' if f.get("costs") else "")
                        + '<dl class="refs">'
                        f'<div><dt>Decided by</dt><dd>{html.escape(f.get("decider") or "not recorded")}</dd></div>'
                        f'<div><dt>Confidence</dt><dd>{html.escape(f.get("confidence") or "not stated")}</dd></div>'
                        f'<div><dt>Confirmed by</dt><dd>{inline(f.get("confirmation") or "not stated")}</dd></div>'
                        f'<div><dt>Reopen when</dt><dd>{inline(f.get("revisit when") or "not stated")}</dd></div></dl></div></details>')
        out.append(f'<section class="stream decided" data-decider="__all"><h2>Already decided <span class="count">{len(decided)}</span></h2><div class="reqs">{"".join(rows)}</div></section>')
    return "".join(out)


def gate_extras(m, g):
    f_ = lambda i: i.get("fields") or {}
    rdy = [r for r in m.kind("readiness check") if f_(r).get("before") == g["id"]]
    msg = [x for x in m.kind("notice") if f_(x).get("with") == g["id"] or f_(x).get("send on") == g["id"]]
    brk = [b for b in m.kind("breaking change") if g["id"] in (f_(b).get("removed at"), f_(b).get("deprecated on"))]
    out = ""
    if rdy:
        out += '<h4>Ready?</h4><ul class="checks-list">' + "".join(f'<li class="{ {"ready": "ok", "not ready": "bad"}.get(f_(r).get("outcome"), "todo") }">{inline(r.get("title", ""))} <span class="muted">({r["id"]})</span></li>' for r in rdy) + '</ul>'
    if brk or msg:
        out += '<h4>Tell</h4><ul class="checks-list">' + "".join(f'<li class="warn">{inline(b.get("title", ""))} <span class="muted">· {inline(f_(b).get("who", ""))} ({b["id"]})</span></li>' for b in brk) \
               + "".join(f'<li class="src">{inline(x.get("title", ""))} <span class="muted">· {inline(f_(x).get("audience", ""))} by {inline(f_(x).get("channel", "a channel not set"))} ({x["id"]})</span></li>' for x in msg) + '</ul>'
    return out


def people_html(m):
    f_ = lambda i: i.get("fields") or {}
    out = []
    rdy = m.kind("readiness check")
    if rdy:
        nr = [r for r in rdy if f_(r).get("outcome") != "ready"]
        out.append(f'<h3 class="sub">Is the service ready?</h3><p class="caption">{len(rdy) - len(nr)} of {len(rdy)} checks ready.</p><div class="reqs">' + "".join(
            xrow(r, cell({"ready": "holds", "not ready": "missing"}.get(f_(r).get("outcome"), "not checked")) + f' <span class="muted small">before {html.escape(str(f_(r).get("before") or "?"))}</span>',
                 f'<p class="muted small">{html.escape(f_(r).get("area", ""))}</p>') for r in sorted(rdy, key=lambda r: f_(r).get("outcome") == "ready")) + '</div>')
    brk, msg = m.kind("breaking change"), m.kind("notice")
    gname = lambda gid: (m.by.get(gid, {}).get("title", "").split(" · ")[0] or gid) if gid else "a step not set"
    if brk:
        cards = "".join(
            f'<article class="kcard" id="{b["id"]}"><p class="pk"><span class="chip c-open">{html.escape(f_(b).get("class", ""))}</span>'
            + "".join(f'<span class="chip c-unchecked">{html.escape(x)}</span>' for x in f_(b).get("breaks", []))
            + f'<span class="muted small">at {html.escape(gname(f_(b).get("removed at") or f_(b).get("deprecated on")))}</span></p>'
            f'<h3>{inline(b.get("title", ""))}</h3><p><b>Who.</b> {inline(f_(b).get("who", "not named"))}</p>'
            + (f'<p><b>What to change.</b> {inline(f_(b)["migration"])}</p>' if f_(b).get("migration") else '<p><span class="chip c-open">migration not written</span> Nothing yet tells them what to change.</p>')
            + '</article>' for b in brk)
        out.append(f'<h3 class="sub">For callers: what breaks, and what to change</h3><div class="dgrid">{cards}</div>')
    if msg:
        notices = [x for x in msg if f_(x).get("purpose") != "support reply"]
        replies = [x for x in msg if f_(x).get("purpose") == "support reply"]
        def copy(x):
            if not f_(x).get("copy"):
                return '<p><span class="chip c-open">copy not written</span></p>'
            q = re.sub(r"\[([^\]]+?): not known yet\]", r'<span class="gapmark">\1: not known yet</span>', inline(f_(x)["copy"]))
            loc = f_(x).get("locales") or []
            meta = ([f'<span class="chip c-unchecked">{html.escape(" · ".join(loc))}</span>'] if loc else []) \
                + (['<span class="chip c-open">drafted, not agreed</span>'] if x.get("state") == "proposed" else [])
            note = body_only(x)
            return (f'<blockquote>{q}</blockquote>' + (f'<p class="pk">{"".join(meta)}</p>' if meta else "")
                    + (f'<p class="muted small">{inline(note)}</p>' if note else ""))
        kit = ""
        if notices:
            kit += '<h4>Who we tell, and when</h4><div class="dgrid">' + "".join(
                f'<article class="kcard" id="{x["id"]}"><p class="pk"><span class="chip c-unchecked">{html.escape(f_(x).get("channel", "channel not set"))}</span>'
                f'<span class="muted small">with {html.escape(gname(f_(x).get("with") or f_(x).get("send on")))}'
                + (f', {html.escape(str(f_(x)["lead time"]).replace("P", "").replace("D", " day ahead"))}' if f_(x).get("lead time") else "") + '</span></p>'
                f'<h3>{inline(x.get("title", ""))}</h3><p class="muted small">To {inline(f_(x).get("audience", "an audience not named"))}</p>{copy(x)}</article>' for x in notices) + '</div>'
        if replies:
            kit += '<h4>What support says when asked</h4><div class="reqs">' + "".join(
                f'<details class="req qa" id="{x["id"]}"><summary><i class="st"></i><span class="id">{x["id"]}</span><span class="shall">{inline(x.get("title", ""))}</span>'
                f'<span>{cell("written" if f_(x).get("copy") else "missing")}</span></summary><div class="more"><p class="muted small">From {inline(f_(x).get("audience", "?"))}, by {inline(f_(x).get("channel", "?"))}</p>{copy(x)}</div></details>' for x in replies) + '</div>'
        esc_ = sec_paras("Where does a case go when support can't solve it?")
        if esc_:
            kit += f'<p class="caption"><b>When support can\'t solve it.</b> {" ".join(inline(t) for t in esc_)}</p>'
        out.append(f'<h3 class="sub">Support kit</h3>{kit}')
    a11 = m.kind("accessibility finding")
    if a11:
        out.append('<h3 class="sub">Can everyone still sign in?</h3><div class="reqs">' + "".join(
            xrow(a, cell({"pass": "holds", "fail": "fails"}.get(f_(a).get("outcome"), "not checked")), f'<p class="muted small">{html.escape(f_(a).get("scope", ""))} · hosted by {inline(f_(a).get("hosted by") or "us")}</p>') for a in a11) + '</div>')
    return "".join(out)


def cutover_html(m):
    gates = gates_in_order(m)
    if not gates:
        return '<p><span class="chip c-unchecked">none</span> No gate is filed yet.</p>'
    ran = lambda g: any(isinstance(e, dict) and e.get("outcome") for e in g.get("evidence", []))
    first = next((g["id"] for g in gates if not ran(g)), gates[0]["id"])

    def split(t):
        code, _, name = t.partition(" · ")
        return (code, name) if name and len(code) <= 4 else ("", t)
    rail, panels, stage = [], [], None
    for g in gates:
        f = g.get("fields") or {}
        code, name = split(g.get("title", ""))
        divider = ""
        if f.get("phase") != stage:
            divider = f'<span class="stage">{html.escape(str(f.get("phase") or ""))}</span>'
            stage = f.get("phase")
        cls = "dot oneway" if f.get("one-way") == "yes" else ("dot done" if ran(g) else "dot")
        short_name = name
        rail.append(f'<li class="ph-{html.escape(str(f.get("phase") or ""))}{" newstage" if divider and rail else ""}">{divider}'
                    f'<button class="gbtn" data-gate="{g["id"]}" aria-pressed="{"true" if g["id"] == first else "false"}" title="{html.escape(g.get("title", ""))}">'
                    f'<b>{html.escape(code or g["id"])}</b><i class="{cls}"></i><span>{shy(inline(short_name))}</span></button></li>')
        before = []
        for t in m.out(g, "blocked-by"):
            it = m.by.get(t, {})
            k = it.get("kind")
            if k == "unit":
                pr = (it.get("fields") or {}).get("ships in")
                before.append(f'<li class="{"ok" if pr else "todo"}">{inline(it.get("title", ""))} <span class="muted">· '
                              + (f'merged in {html.escape(pr)}' if pr else "not built yet") + "</span></li>")
            elif k:
                settled = it.get("state") in ("agreed", "recorded")
                what = {"question": "answered" if settled else "still open", "decision": "agreed" if settled else "not agreed yet",
                        "dependency": "in place" if settled else "not in place yet"}.get(k, it.get("state", ""))
                before.append(f'<li class="{"ok" if settled else "warn"}">{inline(it.get("title", ""))} <span class="muted">· {what} ({t})</span></li>')
        risks = [m.by[r] for r in m.into(g["id"], "opened-by", "risk")]
        lst = lambda v, cls: "".join(f'<li class="{cls}">{inline(x)}</li>' for x in (v if isinstance(v, list) else [v] if v else [])) or '<li class="todo">not set</li>'
        rb_main, _, left = str(f.get("rollback") or "").partition("Left behind:")
        tested = f.get("rollback tested on")
        who = lambda key, empty: f'<span>{html.escape(f[key])}</span>' if f.get(key) else f'<span class="chip c-open">{empty}</span>'
        panels.append(
            f'<article class="gpanel" id="{g["id"]}" data-gate="{g["id"]}"{"" if g["id"] == first else " hidden"}>'
            f'<p class="pk muted">gate{" · <span class=" + chr(34) + "chip c-open" + chr(34) + ">one-way</span>" if f.get("one-way") == "yes" else ""}'
            f'{" · <span class=" + chr(34) + "chip c-holds" + chr(34) + ">has run</span>" if ran(g) else ""}</p>'
            f'<h3><span class="id">{html.escape(code or g["id"])}</span> {inline(name)}</h3>'
            f'<p class="muted small">{html.escape(g["id"])} · opens {html.escape(str(f["opens on"])) if str(f.get("opens on") or "")[:1].isdigit() else "on a day not set"} · reaches {inline(f.get("exposure", "not stated"))}</p>'
            f'<h4>Before</h4><ul class="checks-list">{"".join(before) or "<li class=todo>nothing recorded</li>"}</ul>'
            f'<h4>Do</h4>' + ("".join(block_html(b, {}, {}) for b in g["body"] if isinstance(b, dict) and not {"view", "instrument"} & set(b)) if body_only(g) else '<p><span class="chip c-open">steps not written</span> Nothing yet says what to run at this gate.</p>')
            + f'<h4>Check</h4><ul class="checks-list">{lst(f.get("go when"), "ok")}</ul>'
            + ((f'<h4>What its runs showed</h4><ul class="checks-list">' + "".join(
                f'<li class="{"ok" if str(e.get("outcome")).lower() in ("holds", "passed", "pass", "met") else "bad"}"><b>{html.escape(fmt_day(str(e.get("when") or "")))}</b> · {html.escape(str(e.get("outcome")))}'
                + (f' · {inline(e.get("what") or "")}' if e.get("what") else "")
                + (f' <a href="{html.escape(e["link"])}">source</a>' if str(e.get("link") or "").startswith("http") else "") + '</li>'
                for e in sorted([e for e in g.get("evidence", []) if isinstance(e, dict) and e.get("outcome")], key=lambda e: str(e.get("when") or ""), reverse=True))
               + '</ul>') if any(isinstance(e, dict) and e.get("outcome") for e in g.get("evidence", [])) else "")
            + f'<h4>Stop and roll back when</h4><ul class="checks-list">{lst(f.get("abort when"), "bad")}</ul>'
            f'<h4>Roll back</h4><p>{inline(rb_main.strip() or "not set")}</p>'
            + "".join(f'<p class="small">Steps: <a class="id" href="{tab("runbook")}#{pid}">{pid}</a> {inline(m.by[pid].get("title", ""))}</p>' for pid in m.out(g, "rests-on", "procedure"))
            + (f'<p class="left"><b>Left behind.</b> {inline(left.strip())}</p>' if left.strip() else "")
            + f'<p class="muted small">Rollback {"tested " + html.escape(tested) + " in " + html.escape(f.get("rollback tested in") or "") if tested else "not rehearsed yet"}'
            + (f' · fix forward: {inline(f["fix forward when"])}' if f.get("fix forward when") else "") + '</p>'
            + gate_extras(m, g)
            + (f'<h4>Risks that open here</h4><ul class="checks-list">' + "".join(f'<li class="warn">{inline(r.get("title", ""))} <span class="muted">({r["id"]})</span></li>' for r in risks) + '</ul>' if risks else "")
            + f'<p class="gwho"><b>Calls go</b> {who("decides", "nobody named")} <b>Runs it</b> {who("driver", "nobody named")} <b>Holds for</b> {who("bake", "not set")}</p>'
            '</article>')
    n_one = sum(1 for g in gates if (g.get("fields") or {}).get("one-way") == "yes")
    rows = []
    for label_, test in (("A day to open", lambda g, f: bool(f.get("opens on")) and str(f.get("opens on"))[:1].isdigit()),
                         ("Who calls go", lambda g, f: bool(f.get("decides"))),
                         ("Who runs it", lambda g, f: bool(f.get("driver"))),
                         ("How long it holds", lambda g, f: bool(f.get("bake"))),
                         ("Rollback rehearsed", lambda g, f: bool(f.get("rollback tested on")))):
        cells = "".join(f'<td class="c" data-gate="{g["id"]}">{"<i class=" + chr(34) + "d ok" + chr(34) + "></i>" if test(g, g.get("fields") or {}) else "<i class=" + chr(34) + "d no" + chr(34) + "></i>"}</td>' for g in gates)
        rows.append(f'<tr><th scope="row">{label_}</th>{cells}</tr>')
    cells = []
    for g in gates:
        bl = m.out(g, "blocked-by")
        done = sum(1 for t in bl if (m.by.get(t, {}).get("kind") == "unit" and (m.by[t].get("fields") or {}).get("ships in"))
                   or m.by.get(t, {}).get("state") in ("agreed", "recorded"))
        cells.append(f'<td class="c" data-gate="{g["id"]}"><span class="frac{" full" if bl and done == len(bl) else ""}">{done}/{len(bl)}</span></td>')
    rows.append(f'<tr><th scope="row">Before done</th>{"".join(cells)}</tr>')
    head = "".join(f'<th class="c" scope="col"><button class="gpick" data-gate="{g["id"]}">{html.escape(split(g.get("title", ""))[0] or g["id"])}</button></th>' for g in gates)
    needs = (f'<h3 class="sub">What each gate still needs</h3><div class="tbl"><table class="dots needs"><thead><tr><th></th>{head}</tr></thead>'
             f'<tbody>{"".join(rows)}</tbody></table></div>'
             '<div class="key"><span><i class="d ok"></i> in place</span><span><i class="d no"></i> missing: a no-go until set</span></div>')
    comps = list(dict.fromkeys(c for g in gates for c in ((g.get("fields") or {}).get("touches") or [])))
    if comps:
        def mark(g, c):
            f = g.get("fields") or {}
            if c not in (f.get("touches") or []):
                return ""
            kind = "oneway" if f.get("one-way") == "yes" else ("prep" if f.get("users see it") == "no" else "feel")
            return f'<i class="tm {kind}" title="{html.escape(g.get("title", ""))}"></i>'
        trows = "".join(f'<tr><th scope="row">{inline(c)}</th>' + "".join(f'<td class="c" data-gate="{g["id"]}">{mark(g, c)}</td>' for g in gates) + '</tr>' for c in comps)
        needs = (f'<h3 class="sub">What each gate touches</h3><div class="tbl"><table class="dots needs"><thead><tr><th></th>{head}</tr></thead><tbody>{trows}</tbody></table></div>'
                 '<div class="key"><span><i class="tm prep"></i> prepares, nobody sees it</span><span><i class="tm feel"></i> a switch people feel</span><span><i class="tm oneway"></i> one-way</span></div>') + needs
    nodec = [g for g in gates if not (g.get("fields") or {}).get("decides")]
    nodate = [g for g in gates if not str((g.get("fields") or {}).get("opens on") or "")[:1].isdigit()]
    ins = [("next", f'{len(gates)} gates; {({0: "none has", 1: "1 has"}).get(sum(1 for g in gates if ran(g)), str(sum(1 for g in gates if ran(g))) + " have")} run; the next is {split(next((g for g in gates if not ran(g)), gates[0]).get("title", ""))[0] or "?"}.'),
           ("bottleneck" if nodec else "ok", f'{len(nodec)} gates have nobody named to call go, and {len(nodate)} have no day.' if nodec or nodate else "Every gate has a day and a decider.")]
    if n_one:
        ins.append(("ask", f'{n_one} gates are one-way: a backup and a tested restore must exist first.'))
    return insights_html(ins) + (f'<div class="cutover"><div><div class="gaterail"><ol>{"".join(rail)}</ol></div>'
            f'<div class="key"><span><i class="kd"></i> gate</span><span><i class="kd done"></i> has run</span>'
            f'<span><i class="kd oneway"></i> one-way: backup and tested restore first ({n_one})</span><span class="muted">Select a gate for its card.</span></div>{needs}</div>'
            f'<aside class="panel gpanels">{"".join(panels)}</aside></div>')


def metrics_html(m):
    """Each metric as one row: what it measures, a scale with its baseline, target and latest value, and the go and stop lines
    of every gate that reads it."""
    mets = m.kind("metric")
    if not mets:
        return ""
    f_ = lambda i: i.get("fields") or {}
    num = lambda v: v if isinstance(v, (int, float)) and not isinstance(v, bool) else None
    gates = gates_in_order(m)
    code = lambda g: (g.get("title", "").partition(" · ")[0] if " · " in g.get("title", "") else g["id"])

    def lines(mid):
        out = []
        for g in gates:
            for key, cls, word in (("go when", "go", "go"), ("abort when", "stop", "stop")):
                for c in f_(g).get(key) or []:
                    if re.search(r"\b" + re.escape(mid) + r"\b", str(c)):
                        txt = re.sub(r"^\s*" + re.escape(mid) + r"\s*", "", str(c))
                        txt = re.sub(r",\s*relative to \w+\s*$", "", txt)
                        out.append((g, cls, word, txt, "baseline" in str(c)))
        return out
    order = {"goal": 0, "guardrail": 1, "indicator": 2, "diagnostic": 3, "data-quality": 4}
    rows, blind = [], []
    for x in sorted(mets, key=lambda x: (order.get(f_(x).get("role"), 9), x["id"])):
        f = f_(x)
        base, target, val = num(f.get("baseline")), num(f.get("target")), num(f.get("value"))
        ls = lines(x["id"])
        if base is None and any(b for *_, b in ls):
            blind.append((x, sorted({code(g) for g, *_ , b in ls if b})))
        pts = [v for v in (base, target, val) if v is not None]
        if pts:
            hi = max(pts) * 1.25 or 1
            pos = lambda v: max(0.0, min(100.0, 100.0 * v / hi))
            marks = ""
            if base is not None and target is not None:
                a, b = sorted((pos(base), pos(target)))
                marks += f'<i class="mspan" style="left:{a:.1f}%;width:{b - a:.1f}%"></i>'
            for v, cls, word in ((base, "mb", "baseline"), (target, "mt", "target"), (val, "mv", "now")):
                if v is not None:
                    marks += f'<i class="mk {cls}" style="left:{pos(v):.1f}%" title="{word} {v:g}"><em>{word} {v:g}</em></i>'
            scale = f'<div class="mscale">{marks}<span class="m0">0</span></div>'
        else:
            scale = '<div class="mscale empty"><span>no baseline, target or reading yet</span></div>'
        arrow = {"down": "↓ lower is better", "up": "↑ higher is better", "hold": "↔ must hold"}.get(f.get("direction"), "")
        base_note = (f'baseline {base:g} over {html.escape(str(f.get("baseline window") or "a window not stated"))}' if base is not None
                     else ('<span class="chip c-open">baseline not measured</span>' if any(b for *_, b in ls) else 'no baseline'))
        glines = "".join(f'<li class="{cls}"><b>{html.escape(code(g))}</b> <span class="gw">{word}</span> {inline(txt)}</li>' for g, cls, word, txt, _ in ls)
        rows.append(f'<div class="mrow" id="{x["id"]}"><div class="mhead"><span class="chip c-unchecked">{html.escape(f.get("role", ""))}</span>'
                    f'<h3><span class="id">{x["id"]}</span> {inline(x.get("title", ""))}</h3><p class="small">{inline(f.get("definition", ""))}</p>'
                    f'<p class="muted small">{arrow} · {base_note} · {html.escape(str(f.get("cadence") or "cadence not set"))}</p></div>'
                    f'{scale}<ul class="mgates">{glines or "<li class=none>no gate reads it</li>"}</ul></div>')
    ins = [("next", f'{len(mets)} metrics; {sum(1 for x in mets if lines(x["id"]))} of them decide a gate.')]
    if blind:
        ins.append(("bottleneck", f'{len(blind)} metrics are judged against a baseline nobody has measured, so the gates that read them '
                    f'({", ".join(sorted({c for _, cs in blind for c in cs}))}) cannot tell go from stop yet: '
                    + ", ".join(x["id"] for x, _ in blind) + '.'))
    return (f'<h3 class="sub">What the gates read</h3>' + insights_html(ins)
            + '<div class="key"><span><i class="mk mb"></i> baseline</span><span><i class="mk mt"></i> target</span><span><i class="mk mv"></i> latest reading</span>'
            '<span><b class="gw go">go</b> the gate may proceed</span><span><b class="gw stop">stop</b> roll back</span></div>'
            f'<div class="metrics">{"".join(rows)}</div>')


def map_data(m):
    kinds = {"unit": "step", "gate": "gate", "question": "ask", "decision": "ask", "dependency": "dep"}
    nodes = {i["id"]: i for i in m.items if i.get("kind") in kinds and i.get("state") not in ("superseded", "withdrawn")}

    def done(i):
        f = i.get("fields") or {}
        k = i.get("kind")
        if k == "unit":
            return bool(f.get("ships in"))
        if k == "gate":
            return any(isinstance(e, dict) and e.get("outcome") for e in i.get("evidence", []))
        if k in ("question", "decision"):
            return i.get("state") in ("agreed", "recorded") or bool(m.into(i["id"], "answers"))
        return f.get("status") in ("closed", "met", "done")
    edges = [(t, i["id"]) for i in nodes.values() for t in m.out(i, "blocked-by") if t in nodes]
    used = {a for a, b in edges} | {b for a, b in edges}
    nodes = {k: v for k, v in nodes.items() if k in used}
    preds, succs = {}, {}
    for a, b in edges:
        preds.setdefault(b, []).append(a)
        succs.setdefault(a, []).append(b)
    layer = {}

    def depth(n, seen=()):
        if n in layer:
            return layer[n]
        if n in seen:
            return 0
        layer[n] = 1 + max((depth(p, seen + (n,)) for p in preds.get(n, [])), default=-1)
        return layer[n]
    for n in nodes:
        depth(n)
    for n in sorted(nodes, key=lambda x: -layer[x]):
        if not preds.get(n) and succs.get(n):
            layer[n] = max(0, min(layer[x] for x in succs[n]) - 1)
    open_ = {n for n in nodes if not done(nodes[n])}
    best = {}

    def longest(n, seen=()):
        if n in best:
            return best[n]
        if n in seen:
            return (0, [n])
        cand = [longest(p, seen + (n,)) for p in preds.get(n, []) if p in open_]
        top = max(cand, key=lambda c: c[0], default=(0, []))
        best[n] = (top[0] + (1 if n in open_ else 0), top[1] + [n])
        return best[n]
    ends = [n for n in nodes if nodes[n].get("kind") == "gate"] or list(nodes)
    crit = max((longest(n) for n in ends), key=lambda c: c[0], default=(0, []))[1]
    can = [n for n in open_ if all(p not in open_ for p in preds.get(n, []))]
    out = []
    for n, i in nodes.items():
        f = i.get("fields") or {}
        out.append({"id": n, "title": i.get("title", ""), "kind": kinds[i["kind"]], "layer": layer[n], "done": n not in open_,
                    "can": n in can, "crit": n in crit, "owner": f.get("decider") or i.get("owner") or "",
                    "state": i.get("state"), "tier": f.get("tier", ""), "pr": f.get("ships in", ""), "when": f.get("opens on", "") or i.get("decide_by") or ""})
    down = {}
    for n in nodes:
        seen, st = set(), [n]
        while st:
            x = st.pop()
            for y in succs.get(x, []):
                if y not in seen:
                    seen.add(y)
                    st.append(y)
        down[n] = seen
    for o in out:
        o["down"] = len([x for x in down[o["id"]] if x in open_])
        o["gates"] = len([x for x in down[o["id"]] if nodes[x].get("kind") == "gate" and x in open_])
    live = [o for o in out if not o["done"]]
    insights = []
    starts = [o for o in live if o["can"] and o["kind"] == "step"]
    nxt = max(starts, key=lambda o: (o["crit"], o["down"])) if starts else None
    if nxt:
        insights.append({"id": nxt["id"], "kind": "next", "text": f'Start with {nxt["id"]}: it can start now' + (", it is on the critical path" if nxt["crit"] else "") + f', and {nxt["down"]} things follow from it.', "title": nxt["title"]})
    open_preds = lambda n: [p for p in preds.get(n, []) if p in open_]
    merges = [o for o in live if o["kind"] in ("step", "gate") and len([p for p in open_preds(o["id"]) if nodes[p].get("kind") == "unit"]) >= 2]
    if merges:
        c = max(merges, key=lambda o: (o["down"] > 0, o["down"], len(open_preds(o["id"]))))
        lines = [p for p in open_preds(c["id"]) if nodes[p].get("kind") == "unit"]
        insights.append({"id": c["id"], "kind": "bottleneck", "text": f'{c["id"]} is where the work converges: it waits on {" and ".join(lines)}, and {c["down"]} things follow it.', "title": c["title"]})
    asks = [o for o in live if o["kind"] == "ask"]
    if asks:
        q = max(asks, key=lambda o: (o["down"], o["gates"]))
        if q["down"] >= 2:
            insights.append({"id": q["id"], "kind": "ask", "text": f'{q["id"]} holds up {q["down"]} things until it is answered.', "title": q["title"]})
    orphans = [i for i in m.items if i.get("kind") in ("question", "decision") and i.get("state") in ("open", "lean", "proposed")
               and (i.get("fields") or {}).get("tier") == "1" and not (i.get("fields") or {}).get("decider")]
    for o_ in orphans[:1]:
        blocks = m.into(o_["id"], "blocked-by")
        gates_hit = sorted({g for b_ in blocks for g in ([b_] if m.by[b_].get("kind") == "gate" else [])})
        named = [m.by[b_].get("title", b_) for b_ in blocks if m.by[b_].get("kind") in ("slice", "gate", "unit")] or [b_ for b_ in blocks]
        what = "; ".join(named[:3]) + ("…" if len(named) > 3 else "")
        insights.append({"id": o_["id"], "kind": "ask", "text": f'{o_["id"]} is tier 1 and nobody is named to decide it; it blocks {what or "nothing filed yet"}.', "title": o_.get("title", "")})
    ranked = sorted(live, key=lambda o: -o["down"])
    keyset = {o["id"] for o in ranked[:8]} | {i["id"] for i in insights} | {o["id"] for o in out if o["kind"] == "gate"}
    for o in out:
        o["key"] = o["id"] in keyset
    return {"nodes": out, "edges": edges, "crit": crit, "can": can, "open": len(open_), "insights": insights}


def map_html(m):
    d = map_data(m)
    first = next((n for n in d["crit"] if n in d["can"]), d["crit"][0] if d["crit"] else "")
    kinds_can = [x["kind"] for x in d["nodes"] if x["id"] in d["can"]]
    lead = (f'<p class="caption"><b>{len(d["can"])}</b> things can start now: {kinds_can.count("step")} pieces of work and {len(kinds_can) - kinds_can.count("step")} questions, decisions or dependencies. The critical path runs through '
            f'<b>{sum(1 for n in d["crit"] if any(x["id"] == n and not x["done"] for x in d["nodes"]))}</b> unfinished steps'
            + (f', starting with <span class="id">{first}</span>' if first else "") + '.</p>')
    modes = ('<div class="chipset modes" role="group" aria-label="Show"><span>Show</span>'
             '<button aria-pressed="true" data-mode="all">Everything</button><button aria-pressed="false" data-mode="crit">Critical path</button>'
             '<button aria-pressed="false" data-mode="can">Can start now</button>'
             '<label class="ctl">Owner <select id="map-owner"><option value="">anyone</option></select></label>'
             '<label class="ctl"><input type="checkbox" id="map-done" checked> done steps</label>'
             '<label class="ctl"><input type="checkbox" id="map-asks" checked> questions and decisions</label></div>')
    key = ('<div class="key"><span><i class="kd"></i> work</span><span><i class="kd done"></i> done</span><span><i class="kq"></i> question or decision</span>'
           '<span><i class="kg"></i> gate</span><span><i class="kc"></i> critical path</span></div>')
    marks = {"bottleneck": "!", "ask": "?", "next": "→"}
    ins = "".join(f'<li class="ins {i["kind"]}"><b>{marks[i["kind"]]}</b><span>{inline(i["text"])} <span class="muted">{inline(i["title"])}</span></span>'
                  f'<button class="ref" data-show="{i["id"]}">show</button></li>' for i in d.get("insights", []))
    lead = (f'<ul class="insights">{ins}</ul>' if ins else "") + lead
    key = key.replace('</div>', '<span><i class="ksz"></i> bigger: more waits on it</span></div>', 1)
    return (lead + modes + key + f'<div class="trace wide"><div class="trace-graph mapgraph" id="map-graph"></div><aside class="panel" id="map-panel" data-cutover="{tab("cutover")}" data-register="{tab("register")}">'
            '<p class="muted">Select a step to see what it waits on and what it unlocks.</p></aside></div>'
            f'<script type="application/json" id="map-data">{safe_json(d)}</script>')


def des_more(m, d, req_page=None):
    """A design section opened: its text, with any item it merely points at resolved to that item's words, then what it meets,
    what it rests on, and what was weighed against it."""
    f_ = lambda i: i.get("fields") or {}
    text = body_only(d)
    refs = [mm.group(0) for mm in ID_PAT.finditer(text) if mm.group(0) in m.by]
    bare = re.sub(r"\b[A-Z]+-\d+\b|in its words|see the [a-z ]+|[.,;:()\s]", "", text, flags=re.I) == ""
    out = []
    if text and not bare:
        out.append(f'<p>{inline(text)}</p>')
    for r in refs:
        it = m.by[r]
        out.append(f'<blockquote><b>{html.escape(nice(r))}</b> {inline(it.get("title", ""))}'
                   + (f'<br><span class="small">{inline(body_only(it))}</span>' if body_only(it) and bare else "") + '</blockquote>')
    reqs = m.out(d, "serves", "requirement")
    if reqs:
        out.append('<h4>Meets</h4><ul class="prose tight">' + "".join(
            f'<li><a class="id" href="{(req_page or "") + "#" + r}">{r}</a> {inline(m.by[r].get("title", ""))}</li>' for r in reqs) + '</ul>')
    decs = m.out(d, "rests-on", "decision")
    if decs:
        out.append('<h4>Rests on</h4><ul class="prose tight">' + "".join(
            f'<li><span class="id">{x}</span> {inline(m.by[x].get("title", ""))} <span class="muted small">· {html.escape(m.by[x].get("state", ""))}</span></li>' for x in decs) + '</ul>')
    weighed = [m.by[x] for x in m.into(d["id"], "serves", "design section") if f_(m.by[x]).get("aspect") in ("alternative", "drawback")]
    if weighed:
        out.append('<h4>Weighed against it</h4><ul class="checks-list">' + "".join(
            f'<li class="{"warn" if f_(w).get("aspect") == "drawback" else "src"}"><b>{"Cost" if f_(w).get("aspect") == "drawback" else "Instead"}:</b> {inline(w.get("title", ""))}'
            + (f' <span class="muted small">· {inline(body_only(w))}</span>' if body_only(w) else "") + '</li>' for w in weighed) + '</ul>')
    return "".join(out) or '<p class="muted">Nothing more is filed for this part.</p>'


def goal_words(m, d):
    """A goal's text, or the words of the clause it serves when its text only points there."""
    text = body_only(d)
    if re.sub(r"\b[A-Z]+-\d+\b|in its words|[.,;:\s]", "", text, flags=re.I):
        return text
    tgt = next((m.by[x] for x in m.out(d, "serves") if x in m.by), None)
    return (body_only(tgt) or tgt.get("title", "")) if tgt else text


def design_html(m, req_page=None):
    gates = gates_in_order(m)
    code = lambda t: t.split(" · ")[0] if " · " in t else ""
    gcol = {code(g.get("title", "")): k for k, g in enumerate(gates)}
    slices = m.kind("slice")
    phases = [(g.get("fields") or {}).get("phase") or "" for g in gates]
    breaks = {k for k in range(1, len(phases)) if phases[k] != phases[k - 1]}
    rows, panels = [], []
    for sl in slices:
        c = code(sl.get("title", ""))
        end = gcol.get(c)
        deps = [gcol.get(code(m.by[x].get("title", ""))) for x in m.out(sl, "blocked-by", "slice")]
        deps = [x for x in deps if x is not None]
        start = max(deps) if deps else 0
        if end is None:
            end = start
        start = min(start, end)
        reqs = m.out(sl, "serves", "requirement")
        gate = next((g for g in gates if code(g.get("title", "")) == c), None)
        units = list(dict.fromkeys(m.into(sl["id"], "serves", "unit") + (m.out(gate, "blocked-by", "unit") if gate else [])))
        asks = [x for x in m.out(sl, "blocked-by") if m.by.get(x, {}).get("kind") in ("question", "decision")]
        decs = sorted({d for r in reqs for d in m.into(r, "serves", "decision")})
        des = sorted({d for r in reqs for d in m.into(r, "serves", "design section")}, key=lambda x: int(x.split("-")[1]))
        shipped = [u for u in units if (m.by[u].get("fields") or {}).get("ships in")]
        built = bool(units) and len(shipped) == len(units)
        state = "built" if built else ("part" if shipped else "todo")
        cells = "".join(f'<td class="gc s-{state}{" on" if start <= k <= end else ""}{" end" if k == end else ""}{" stagebreak" if k in breaks else ""}"></td>' for k in range(len(gates)))
        rows.append(f'<tr class="srow" id="{sl["id"]}" data-slice="{sl["id"]}" tabindex="0"><th scope="row"><span class="id">{html.escape(c or sl["id"])}</span> '
                    f'{inline(sl.get("title", "").split(" · ", 1)[-1])}{" <span class=" + chr(34) + "chip c-holds" + chr(34) + ">built</span>" if built else ""}</th>{cells}</tr>')
        link = lambda ids: " ".join((f'<a class="id" href="{req_page}#{i}">{i}</a>' if req_page and i.startswith("REQ-") else f'<span class="id">{i}</span>') for i in ids) or '<span class="muted">none</span>'
        bullets = "".join(f'<li>{inline(m.by[d].get("title", ""))} <span class="muted">({d})</span></li>' for d in des[:8])
        panels.append(f'<article class="spanel" data-slice="{sl["id"]}" hidden><p class="pk muted">slice</p><h3><span class="id">{html.escape(c or sl["id"])}</span> {inline(sl.get("title", "").split(" · ", 1)[-1])}</h3>'
                      + (f'<h4>How it is built</h4><ul class="prose tight">{bullets}</ul>' if bullets else "")
                      + f'<h4>Requirements</h4><p>{link(reqs)}</p><h4>Work</h4><p>{link(units)}</p><h4>Decisions</h4><p>{link(decs)}</p>'
                      f'<h4>Open questions</h4><p>{link(asks)}</p></article>')
    head = "".join(f'<th class="c{" stagebreak" if k in breaks else ""}" scope="col"><span class="id">{html.escape(code(g.get("title", "")) or g["id"])}</span></th>' for k, g in enumerate(gates))
    spans, k = [], 0
    while k < len(phases):
        j = k
        while j + 1 < len(phases) and phases[j + 1] == phases[k]:
            j += 1
        spans.append(f'<th class="stage{" stagebreak" if k in breaks else ""}" colspan="{j - k + 1}">{html.escape(phases[k])}</th>')
        k = j + 1
    picture = (f'<div class="design"><div><div class="tbl"><table class="gantt"><thead><tr><th></th>{"".join(spans)}</tr><tr><th></th>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
               '<div class="key"><span><i class="kb built"></i> built</span><span><i class="kb part"></i> partly built</span><span><i class="kb todo"></i> not started</span>'
               '<span class="muted">Each slice runs from the gate it waits on to the gate that exposes it. Select one for its design, requirements, work and open questions.</span></div></div>'
               f'<aside class="panel">{"".join(panels)}<p class="muted sp-empty">Select a slice to see how it is built and what it carries.</p></aside></div>')
    pieces = connect_svg(m)
    if pieces:
        out_pieces = '<h3 class="sub">How the pieces connect</h3>' + pieces
    else:
        out_pieces = ""
    aspect = lambda d: (d.get("fields") or {}).get("aspect")
    ctx = [d for d in m.kind("design section") if aspect(d) == "context"]
    goals = [d for d in m.kind("design section") if aspect(d) == "goal"]
    nong = [d for d in m.kind("design section") if aspect(d) == "non-goal"]
    purpose = ("".join(f'<p>{inline(body_text(d))} <span class="id">{d["id"]}</span></p>' for d in ctx)
               + ('<ul class="checks-list">' + "".join(f'<li class="ok"><b>{inline(d.get("title", "").replace("Goal: ", ""))}.</b> {inline(goal_words(m, d))} <span class="id">{d["id"]}</span></li>' for d in goals)
                  + "".join(f'<li class="no"><b>Not: {inline(d.get("title", "").replace("Non-goal: ", ""))}.</b> {inline(body_text(d))} <span class="id">{d["id"]}</span></li>' for d in nong) + '</ul>'))
    qgs = sorted(m.kind("quality goal"), key=lambda q: (q.get("fields") or {}).get("rank") or 99)
    if qgs:
        purpose += '<h3 class="sub">How good it must be</h3><div class="reqs">' + "".join(
            xrow(q, cell("measure open" if str((q.get("fields") or {}).get("measure", "")).startswith("TBR") else "measured"),
                 f'<p><b>When</b> {inline((q.get("fields") or {}).get("stimulus", ""))} <b>in</b> {inline((q.get("fields") or {}).get("environment", ""))}, <b>then</b> {inline((q.get("fields") or {}).get("response", ""))}.</p>'
                 f'<p class="muted small">Measured by {inline((q.get("fields") or {}).get("measure", "") or "nothing yet")}</p>') for q in qgs) + '</div>'
    groups = [("How it is built", ("structure", "runtime", "deployment", "interface", "data")),
              ("Concerns across the design", ("security", "privacy", "observability", "version skew")),
              ("What we weighed and what it costs", ("alternative", "drawback")), ("Where the description and the code disagree", ("inconsistency",))]
    built = sum(1 for sl in slices if all((m.by[u].get("fields") or {}).get("ships in") for u in m.into(sl["id"], "serves", "unit")) and m.into(sl["id"], "serves", "unit"))
    dis = [d for d in m.kind("design section") if (d.get("fields") or {}).get("aspect") == "inconsistency"]
    ins = [("next", f'{len(slices)} slices from the copy to the contract; {built} built.')]
    if dis:
        ins.append(("ask", f'{len(dis)} places where the description and the code disagree; see the end of the page.'))
    out = [insights_html(ins), picture, '<h3 class="sub">What it is for</h3>' + purpose, out_pieces]
    for head_, aspects in groups:
        items = [d for d in m.kind("design section") if (d.get("fields") or {}).get("aspect") in aspects]
        if not items:
            continue
        if head_ in ("How it is built", "Concerns across the design"):
            out.append(f'<h3 class="sub">{html.escape(head_)}</h3><div class="reqs">' + "".join(
                xrow(d, cell(aspect(d) or ""), des_more(m, d, req_page)) for d in items) + '</div>')
            continue
        cards = "".join(
            f'<article class="dcard a-{html.escape((d.get("fields") or {}).get("aspect", ""))}" id="{d["id"]}"><p class="pk"><span class="chip c-unchecked">{html.escape((d.get("fields") or {}).get("aspect", ""))}</span>'
            + (f'<span class="chip c-{"holds" if (d.get("fields") or {}).get("applies") == "yes" else "unchecked"}">applies: {html.escape((d.get("fields") or {}).get("applies"))}</span>' if (d.get("fields") or {}).get("applies") else "")
            + f'</p><h3>{inline(d.get("title", ""))}</h3>{"<p>" + inline(body_only(d)) + "</p>" if body_only(d) else ""}'
            + (f'<p class="muted"><b>Why not.</b> {inline((d.get("fields") or {})["why not"])}</p>' if (d.get("fields") or {}).get("why not") else "")
            + '</article>' for d in items)
        out.append(f'<h3 class="sub">{html.escape(head_)}</h3><div class="dgrid">{cards}</div>')
    return "".join(out)


def connect_svg(m):
    """How the pieces connect: trust boundaries as containers, parts inside, flows as labelled arrows."""
    f_ = lambda i: i.get("fields") or {}
    els = m.kind("element")
    bounds = [e for e in els if f_(e).get("element") == "trust boundary"]
    nodes = [e for e in els if f_(e).get("element") not in ("trust boundary", "data flow")]
    flows = [e for e in els if f_(e).get("element") == "data flow" and f_(e).get("from") and f_(e).get("to")]
    if not nodes:
        return ""
    outside = [n for n in nodes if not f_(n).get("within")]
    out_ids = {n["id"] for n in outside}
    by_id = {e["id"]: e for e in els}
    pull = lambda b: -sum(1 for fl in flows if f_(fl)["from"] in out_ids and f_(by_id.get(f_(fl)["to"], {})).get("within") == b["id"])
    bounds = sorted(bounds, key=pull)
    cols = [(None, outside)] + [(b, [n for n in nodes if f_(n).get("within") == b["id"]]) for b in bounds]
    cols = [c for c in cols if c[1]]
    def wrap(t, n, lines=2):
        words, out_, cur = str(t).split(), [], ""
        for w in words:
            if cur and len(cur) + 1 + len(w) > n:
                out_.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        out_.append(cur)
        if len(out_) > lines:
            out_ = out_[:lines]
            out_[-1] = out_[-1][: n - 1].rstrip() + "…"
        return out_
    boxW, gapX, boxH, gap, top = 250, 230, 60, 26, 48
    colW = boxW + gapX
    pos, parts = {}, []
    H = top + max(len(c[1]) for c in cols) * (boxH + gap) + 30
    for k, (b, ns) in enumerate(cols):
        x0 = 20 + k * colW
        if b is not None:
            parts.append(f'<rect class="tb" x="{x0 - 14}" y="14" width="{boxW + 28}" height="{H - 24}" rx="10"/><text class="tbl" x="{x0 - 4}" y="32">{html.escape(b.get("title", ""))}</text>')
        for j, n in enumerate(ns):
            y = top + j * (boxH + gap)
            kind = f_(n).get("element", "")
            pos[n["id"]] = (x0, y)
            unan = f_(n).get("scope") == "not yet analysed"
            tl = wrap(n.get("title", ""), 30)
            parts.append(f'<g class="pc k-{kind.replace(" ", "-")}{" unan" if unan else ""}"><title>{html.escape(n["id"] + " · " + n.get("title", ""))}</title><rect x="{x0}" y="{y}" width="{boxW}" height="{boxH}" rx="{4 if kind == "process" else 12}"/>'
                         + "".join(f'<text class="pt" x="{x0 + 10}" y="{y + 19 + i * 15}">{html.escape(t)}</text>' for i, t in enumerate(tl))
                         + f'<text class="ps" x="{x0 + 10}" y="{y + boxH - 8}">{html.escape(n["id"] + " · " + kind + (" · not analysed" if unan else ""))}</text></g>')
    legend = []
    ends = {}  # (box, side) -> the flows meeting it there, so each gets its own port along the edge
    drawn = [fl for fl in flows if pos.get(f_(fl)["from"]) and pos.get(f_(fl)["to"])]
    for fl in drawn:
        a, b = pos[f_(fl)["from"]], pos[f_(fl)["to"]]
        right = b[0] > a[0]
        ends.setdefault((f_(fl)["from"], "r" if right else "l"), []).append(fl["id"])
        ends.setdefault((f_(fl)["to"], "l" if right else "r"), []).append(fl["id"])
    port = lambda box, side, fid: (ends[(box, side)].index(fid) - (len(ends[(box, side)]) - 1) / 2) * min(14, (boxH - 12) / max(1, len(ends[(box, side)])))
    for k_, fl in enumerate(drawn):
        a, b = pos[f_(fl)["from"]], pos[f_(fl)["to"]]
        right = b[0] > a[0]
        x1 = a[0] + boxW if right else a[0]
        x2 = b[0] if right else b[0] + boxW
        y1 = a[1] + boxH / 2 + port(f_(fl)["from"], "r" if right else "l", fl["id"])
        y2 = b[1] + boxH / 2 + port(f_(fl)["to"], "l" if right else "r", fl["id"])
        mx = x1 + (x2 - x1) * (0.35 + 0.3 * (k_ % 3) / 2)
        cx = (x1 + x2) / 2
        parts.append(f'<path class="pf" d="M{x1},{y1} C{cx},{y1} {cx},{y2} {x2},{y2}" marker-end="url(#pa)"><title>{html.escape(fl["id"] + " · " + fl.get("title", ""))}</title></path>')
        t_ = (mx - x1) / (x2 - x1) if x2 != x1 else .5
        by = y1 + (y2 - y1) * (3 * t_ * t_ - 2 * t_ ** 3)
        legend.append(fl)
        parts.append(f'<g class="pfn"><circle cx="{mx}" cy="{by}" r="9"/><text x="{mx}" y="{by + 3.5}" text-anchor="middle">{len(legend)}</text></g>')
    W = 20 + len(cols) * colW
    return (f'<div class="fig"><svg class="pieces" viewBox="0 0 {W} {H}" role="img" aria-label="How the pieces connect">'
            '<defs><marker id="pa" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L8,4 L0,8 z"/></marker></defs>'
            + "".join(parts) + '</svg></div>'
            + ('<ol class="flows">' + "".join(f'<li><b>{inline(fl.get("title", ""))}</b> <span class="muted small">{html.escape(by_id.get(f_(fl)["from"], {}).get("title", ""))} → {html.escape(by_id.get(f_(fl)["to"], {}).get("title", ""))} · {fl["id"]}</span></li>' for fl in legend) + '</ol>' if legend else "")
            + '<div class="key"><span>dashed: a trust boundary</span><span>numbered arrows: data that crosses one, listed above</span><span class="muted">From the threat model\'s parts and flows.</span></div>')


def runbook_html(m):
    out = []
    slos = m.kind("objective")
    alerts = m.kind("alert")
    if slos:
        tiles = []
        for o in slos:
            f = o.get("fields") or {}
            ind = m.by.get(f.get("indicator") or "", {})
            target = f.get("target")
            guards = [m.by[x] for x in m.into(o["id"], "serves", "alert")]
            tiles.append(f'<div class="slo"><span class="muted small">{html.escape(f.get("service", ""))}</span><h3>{inline(o.get("title", ""))}</h3>'
                         f'<b class="big">{html.escape(("%g" % float(target)) + "%") if target is not None else "no target yet"}</b>'
                         + (f'<p class="small">{inline((ind.get("fields") or {}).get("definition", ""))}</p>' if (ind.get("fields") or {}).get("definition") else "")
                         + (f'<div class="small muted">{body_html(o)}</div>' if body_html(o) else "")
                         + f'<p class="muted small">over a {html.escape(str(f.get("window type", "")))} {html.escape(str(f.get("window length", "")).replace("P", "").replace("D", " days"))}'
                         + (f' · when exhausted: {inline(f["when exhausted"])}' if f.get("when exhausted") else "") + '</p>'
                         + (('<p class="small"><b>Guarded by</b> ' + ", ".join(f'<a href="#{g["id"]}">{inline(g.get("title", ""))}</a>' for g in guards) + '</p>') if guards else '<p class="small muted">No alert guards it yet.</p>')
                         + '</div>')
        out.append(f'<h3 class="sub">Service levels</h3><div class="slos">{"".join(tiles)}</div>')
    alerts = m.kind("alert")
    undefined = [a for a in alerts if not (a.get("fields") or {}).get("defined in")]
    esc = {(a.get("fields") or {}).get("escalate") for a in alerts} - {None, ""}
    notes = []
    if slos and all((o.get("fields") or {}).get("target") is None for o in slos):
        notes.append(("ask", f'No service level has a target yet; {len(slos)} {"is" if len(slos) == 1 else "are"} named and waiting for one.'))
    if alerts and len(undefined) == len(alerts):
        notes.append(("bottleneck", f'None of the {len(alerts)} alerts exists in monitoring yet. Each card below is the playbook it will carry once it is defined.'))
    elif undefined:
        notes.append(("ask", f'{len(undefined)} of {len(alerts)} alerts are not defined in monitoring yet: {", ".join(a["id"] for a in undefined)}.'))
    if len(esc) == 1 and len(alerts) > 1:
        notes.append(("ask", f'Every alert escalates to {html.escape(next(iter(esc)))}. If they are away, nobody else is named.'))
    notes = [insights_html(notes)]
    who_ = sec_paras("Who answers, and who is next?")
    if who_:
        notes.append(f'<div class="tabnote"><h2>Who answers</h2><p>{" ".join(inline(t) for t in who_)}</p></div>')
    out[:0] = notes
    if alerts:
        cards = []
        for a in alerts:
            f = a.get("fields") or {}
            causes = "".join(f"<li>{inline(c)}</li>" for c in f.get("likely causes", []))
            procs = " ".join(f'<a class="id" href="#{p}">{p}</a>' for p in f.get("procedures", []))
            cards.append(f'<article class="acard {html.escape(f.get("severity", ""))}" id="{a["id"]}"><p class="pk"><span class="chip c-{"open" if f.get("severity") == "page" else "unsettled"}">{html.escape(f.get("severity", ""))}</span>'
                         f'<span class="chip c-unchecked">{html.escape(f.get("signal", ""))}</span>'
                         + (f'<span class="muted small">{html.escape(f["defined in"])}</span>' if f.get("defined in") else ('' if len(undefined) == len(alerts) else '<span class="chip c-open">not defined yet</span>'))
                         + f'</p><h3>{inline(a.get("title", ""))}</h3><p>{inline(f.get("means", ""))}</p>'
                         + (f'<p class="muted"><b>Impact.</b> {inline(f["impact"])}</p>' if f.get("impact") else "")
                         + '<ol class="steps-n">'
                         + (f'<li><b>First check.</b> {inline(f["first check"])}</li>' if f.get("first check") else "")
                         + (f'<li><b>Likely causes.</b><ul>{causes}</ul></li>' if causes else "")
                         + (f'<li><b>Do.</b> {inline(f["do"])} {procs}</li>' if f.get("do") else "")
                         + (f'<li><b>Escalate to.</b> {inline(f["escalate"])}</li>' if f.get("escalate") else "") + '</ol>'
                         + f'<pre class="cond"><code>{html.escape(f.get("condition", "condition not set"))}</code></pre>'
                         + (f'<div class="abody muted small">{body_html(a)}</div>' if body_html(a) else "")
                         + f'<p class="muted small">Routes to {inline(f.get("routes to") or "nobody yet")}</p></article>')
        out.append(f'<h3 class="sub">When an alert fires</h3><div class="acards">{"".join(cards)}</div>')
    procs = m.kind("procedure")
    if procs:
        cards = "".join(
            f'<article class="pcard" id="{p["id"]}"><p class="pk"><span class="id">{p["id"]}</span><span class="muted small">when {inline((p.get("fields") or {}).get("when", ""))}</span></p>'
            f'<h3>{inline(p.get("title", ""))}</h3>{body_html(p)}'
            f'<p><b>Check it worked.</b> {inline((p.get("fields") or {}).get("verify", "not stated"))}</p>'
            f'<p class="muted"><b>Undo.</b> {inline((p.get("fields") or {}).get("undo", "not stated"))}</p></article>' for p in procs)
        out.append(f'<h3 class="sub">Procedures</h3><div class="pcards">{cards}</div>')
    return "".join(out) or insights_html([("bottleneck", "Nothing is filed for on-call yet: no service level, alert or procedure. The runbook is owed before the first gate that changes what users get.")])


TAB_KINDS = {"status": ("unit", "requirement", "question", "decision", "gate"), "map": ("unit", "gate", "question", "decision", "dependency"),
             "register": ("question", "decision", "brief"), "raid": ("risk", "issue", "assumption", "dependency"),
             "trace": ("unit", "requirement", "gate"), "faq": ("answer",), "design": ("slice", "design section"),
             "requirements": ("requirement", "acceptance criterion"), "adrs": ("decision",),
             "threats": ("element", "threat", "privacy threat", "mitigation"), "data": ("screening criterion", "vendor or dependency", "restore path"),
             "cutover": ("gate", "metric", "risk"), "runbook": ("objective", "alert", "procedure"), "glossary": ("term",)}


def is_open(i):
    """An item still waiting: its state open or leaning, or its own status field open."""
    return i.get("state") in ("open", "lean") or str((i.get("fields") or {}).get("status", "")).lower() == "open"


def tab_counts(m, instrument):
    import datetime
    items = [i for i in m.items if i.get("kind") in TAB_KINDS.get(instrument, ()) and i.get("state") not in ("superseded", "withdrawn")
             and i.get("sensitivity") != "restricted"]
    have = {i["id"] for i in items}
    items += [m.by[x] for x in dict.fromkeys(x for i in list(items) for x in m.out(i, "blocked-by"))
              if x in m.by and x not in have and m.by[x].get("kind") in ("question", "decision")]
    today = datetime.date.today().isoformat()
    passed = [i for i in items if str(i.get("decide_by") or "")[:1].isdigit() and str(i["decide_by"])[:10] < today and i.get("state") not in ("agreed", "recorded")]
    return len([i for i in items if is_open(i)]), len(items), passed


def fix_counts(lead, page):
    """A lead's stated open and passed counts are the tab's own, computed here, never the run's."""
    inst = next((b["instrument"] for sec in page.get("sections", []) for b in sec.get("blocks", []) if "instrument" in b), None)
    if not inst or not MODEL[0] or not isinstance(lead, str):
        return lead
    o, n, past = tab_counts(MODEL[0], inst)
    pd = len(past)
    named = " (" + ", ".join(nice(i["id"]) for i in past[:4]) + ("…" if len(past) > 4 else "") + ")" if past else ""
    lead = re.sub(r"\b\d+ of this tab's \d+ items are open(?: or leaning)?", f"{o} of this tab's {n} items are open or leaning", lead)
    lead = re.sub(r"\bno due point has passed|\b\d+ due points? (?:has|have) passed", "no due point has passed" if not pd else f"{pd} due point{'s have' if pd != 1 else ' has'} passed{named}", lead)
    return lead


def gates_in_order(m):
    """Gates as the rollout runs them: by phase; within it, those that ran by when they ran, then by step code, then by id."""
    rank = {"expand": 0, "migrate": 1, "single": 1, "contract": 2}
    def key(g):
        code = g.get("title", "").split(" · ")[0] if " · " in g.get("title", "") else ""
        mm = re.match(r"([A-Z])(\d+)$", code)
        ran = min((str(e.get("when")) for e in g.get("evidence", []) if isinstance(e, dict) and e.get("outcome") and e.get("when")), default="~")
        return (rank.get((g.get("fields") or {}).get("phase"), 1), ran, mm.group(1) if mm else "~", int(mm.group(2)) if mm else 99, int(g["id"].split("-")[1]))
    return sorted(m.kind("gate"), key=key)


def dur(v):
    """An ISO 8601 duration in words: P1D -> 1 day, PT2H -> 2 hours."""
    mm = re.fullmatch(r"P(?:(\d+)W)?(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?)?", str(v or ""))
    if not mm or not any(mm.groups()):
        return v
    parts = [(n, w) for n, w in zip(mm.groups(), ("week", "day", "hour", "minute")) if n]
    return ", ".join(f"{n} {w}{'s' if n != '1' else ''}" for n, w in parts)


def fmt_day(d):
    try:
        import datetime
        return datetime.date.fromisoformat(str(d)[:10]).strftime("%-d %b")
    except Exception:
        return str(d)


def status_lead(m):
    units = m.kind("unit")
    merged = [u for u in units if (u.get("fields") or {}).get("ships in")]
    gates = gates_in_order(m)
    ran = lambda g: any(isinstance(e, dict) and e.get("outcome") for e in g.get("evidence", []))
    nxt = next((g for g in gates if not ran(g)), None)
    waiting = [i for i in m.items if i.get("kind") in ("question", "decision") and i.get("state") in ("open", "lean", "proposed")]
    t1 = [i for i in waiting if (i.get("fields") or {}).get("tier") == "1"]
    nodec = [i for i in t1 if not (i.get("fields") or {}).get("decider")]
    s = f"{len(merged)} of {len(units)} pieces of work are merged."
    if nxt:
        blk = [t for t in m.out(nxt, "blocked-by") if not ((m.by.get(t, {}).get("fields") or {}).get("ships in") or m.by.get(t, {}).get("state") in ("agreed", "recorded"))]
        s += f" The next gate is {nxt.get('title', '').split(' · ')[0] or nxt['id']}, {nxt.get('title', '').split(' · ', 1)[-1]}, and it waits on {len(blk)} thing{'s' if len(blk) != 1 else ''}."
    if t1:
        s += f" {len(t1)} tier-1 question{'s' if len(t1) != 1 else ''} need{'s' if len(t1) == 1 else ''} a decider's answer" + (f", {len(nodec)} with nobody named to give it." if nodec else ".")
    return s


def waits_words(m, ids_):
    if not ids_:
        return "waits on nothing"
    kinds = {}
    for i in ids_:
        kinds.setdefault(m.by.get(i, {}).get("kind", "item"), []).append(i)
    word = {"unit": ("piece of work", "pieces of work"), "question": ("question", "questions"), "decision": ("decision", "decisions"), "dependency": ("dependency", "dependencies")}
    bits = [f'{len(v)} {word.get(k, (k, k + "s"))[len(v) != 1]}' for k, v in kinds.items()]
    asks = [i for i in ids_ if m.by.get(i, {}).get("kind") in ("question", "decision")]
    first = asks[0] if asks else ids_[0]
    return f'waits on {" and ".join(bits)}, first {first}: {m.by.get(first, {}).get("title", "")}'


def status_html(m, links=None):
    links = links or {}
    units = m.kind("unit")
    merged = [u for u in units if (u.get("fields") or {}).get("ships in")]
    reqs = m.kind("requirement")
    waiting = [i for i in m.items if i.get("kind") in ("question", "decision") and i.get("state") in ("open", "lean", "proposed")]
    t1 = [i for i in waiting if (i.get("fields") or {}).get("tier") == "1"]
    gates = gates_in_order(m)
    ran = lambda g: any(isinstance(e, dict) and e.get("outcome") for e in g.get("evidence", []))
    settled = lambda t: bool((m.by.get(t, {}).get("fields") or {}).get("ships in")) or m.by.get(t, {}).get("state") in ("agreed", "recorded")
    nxt = next((g for g in gates if not ran(g)), None)
    code = lambda g: g.get("title", "").split(" · ")[0] if " · " in g.get("title", "") else g["id"]
    name = lambda g: g.get("title", "").split(" · ", 1)[-1]
    out = []

    # 0. what changes, as its outcomes, and what happened lately
    outcomes = [(mm.group(1), p_[mm.end():].strip()) for p_ in sec_paras("What changes and why") for mm in [re.match(r"\*\*(.+?)\*\*", p_)] if mm]
    if outcomes:
        out.append('<div class="outcomes"><span class="tools-label">What changes</span><ul>' + "".join(
            (f'<li><details><summary>{inline(o)}</summary><p>{inline(r_)}</p></details></li>' if r_ else f'<li>{inline(o)}</li>')
            for o, r_ in outcomes) + '</ul></div>')
    events = []
    for a in m.agreements:
        if a.get("date"):
            ids_ = [x.get("id") for x in a.get("settled", [])]
            events.append((str(a["date"]), f'{html.escape(a.get("decider") or "someone")} agreed ' + ", ".join(f'{i} <span class="muted">{inline(m.by.get(i, {}).get("title", ""))}</span>' for i in ids_)))
    for i in m.items:
        for e in i.get("evidence", []):
            if isinstance(e, dict) and e.get("outcome") and e.get("when"):
                events.append((str(e["when"]), f'{i["id"]} <span class="muted">{inline(i.get("title", ""))}</span> · {html.escape(e["outcome"])}'))
    first = min((str(i.get("first_filed")) for i in m.items if i.get("first_filed")), default=None)
    if first:
        events.append((first, f'first filed: {len(m.kind("requirement"))} requirements, {len(m.kind("unit"))} pieces of work, {len(m.kind("gate"))} gates'))
    filed_since = [(mm.group(1), x[mm.end():].lstrip(" \u2014-:").strip()) for x in sec_list("What changed since you last looked?")
                   for mm in [re.match(r"\*\*(.+?)\*\*", x)] if mm]
    if filed_since:  # the author's own account of each round outranks the computed one
        out.append('<div class="since long"><span class="tools-label">Lately</span><ol>' + "".join(
            f'<li><time>{inline(d)}</time><span>{inline(t)}</span></li>' for d, t in filed_since[:5]) + '</ol></div>')
        events = []
    if events:
        events = sorted(events, key=lambda e: e[0], reverse=True)[:5]
        out.append('<div class="since"><span class="tools-label">Lately</span><ol>' + "".join(
            f'<li><time>{html.escape(fmt_day(d))}</time><span>{t}</span></li>' for d, t in events) + '</ol></div>')

    # 1. the gates, as a progress strip
    cells = []
    for g in gates:
        f = g.get("fields") or {}
        bl = m.out(g, "blocked-by")
        done = sum(1 for t in bl if settled(t))
        st = "ran" if ran(g) else ("next" if g is nxt else "later")
        missing = [w for w, k in (("day", "opens on"), ("decider", "decides"), ("driver", "driver")) if not f.get(k) or (k == "opens on" and not str(f[k])[:1].isdigit())]
        cells.append(f'<a class="gs {st}{" oneway" if f.get("one-way") == "yes" else ""}" href="{links.get("cutover", "pages/cutover.html")}#{g["id"]}" title="{html.escape(g.get("title", ""))}">'
                     f'<b>{html.escape(code(g))}</b><i></i><span>{inline(name(g))}</span>'
                     f'<em>{"ran" if st == "ran" else str(done) + "/" + str(len(bl)) + " ready"}</em>'
                     + (f'<small>no {", ".join(missing)}</small>' if missing and st != "ran" else "") + '</a>')
    out.append(f'<div class="gstrip">{"".join(cells)}</div>')

    # 2. tiles
    met = sum(1 for r in reqs if m.req_status(r) == "met")
    nodec = [i for i in t1 if not (i.get("fields") or {}).get("decider")]
    nb = [t for t in m.out(nxt, "blocked-by") if not settled(t)] if nxt else []
    tiles = [(f"{len(merged)}/{len(units)}", "pieces of work merged", f"{len(units) - len(merged)} still to build", ""),
             (f"{met}/{len(reqs)}", "requirements met", "built and verified", ""),
             (str(len(t1)), "tier-1 questions waiting", f"{len(nodec)} with nobody named" if nodec else "each has a decider", "warn" if nodec else ""),
             (code(nxt) if nxt else "none", "next gate", (name(nxt) + " · " + waits_words(m, nb)) if nxt else "", "")]
    out.append('<div class="tiles">' + "".join(f'<div class="tile {w}"><b>{html.escape(v)}</b><span>{html.escape(l)}</span><em>{inline(n)}</em></div>' for v, l, n, w in tiles) + '</div>')

    # 3. what needs whom
    people = {}
    for i in waiting:
        people.setdefault((i.get("fields") or {}).get("decider") or "", []).append(i)
    order = sorted(people, key=lambda p: (p != "", -len(people[p])))
    rows = []
    for p_ in order:
        its = sorted(people[p_], key=lambda i: ((i.get("fields") or {}).get("tier") or "9", i["id"]))
        chips = "".join(f'<a class="tchip t{(i.get("fields") or {}).get("tier") or "x"}" href="{links.get("register", "pages/register.html")}" title="{html.escape(i.get("title", ""))}">{i["id"]}</a>' for i in its)
        rows.append(f'<div class="who{" nobody" if not p_ else ""}"><b>{html.escape(p_ or "Nobody named")}</b><span>{len(its)}</span><div>{chips}</div></div>')
    out.append('<h3 class="sub">What needs whom</h3><div class="whos">' + "".join(rows) + '</div><div class="key"><span><i class="tchip t1 k"></i> tier 1</span><span><i class="tchip t2 k"></i> tier 2</span><span class="muted">Hover a chip for the question; select it for the register.</span></div>')
    on_tab = {re.sub(r"[^a-z0-9]+", "-", h.lower()).strip("-") for h in TAB_DESIGN["Status"]["before"]}
    open_ = [re.sub(r"\]\(#([a-z0-9-]+)\)", lambda mm: mm.group(0) if mm.group(1) in on_tab else f"](records/status-as-filed.html#{mm.group(1)})", x)
             for b in SECS.get("Open", []) for x in ([b["p"]] if "p" in b else b.get("ul", []))]
    if open_:
        out.append('<ul class="prose opennote">' + "".join(f'<li>{inline(x)}</li>' for x in open_) + '</ul>')

    # 4. requirements by stream
    streams = {}
    for r in reqs:
        streams.setdefault((r.get("fields") or {}).get("stream") or "Other", []).append(m.req_status(r))
    bars = []
    for k, (st, vals) in enumerate(streams.items(), 1):
        n = len(vals)
        seg = lambda key: vals.count(key) / n * 100
        bars.append(f'<a class="sbar" href="{links.get("requirements", "pages/requirements.html")}#stream-{k}"><span class="sname">{inline(st)}</span>'
                    f'<span class="track"><i class="met" style="width:{seg("met"):.1f}%"></i><i class="partly" style="width:{seg("partly"):.1f}%"></i></span>'
                    f'<span class="snum">{vals.count("met")}/{n} met</span></a>')
    single = list(streams) == ["Other"]
    if single:
        bars = [b.replace('<span class="sname">Other</span>', '<span class="sname">All requirements</span>') for b in bars]
    out.append(f'<h3 class="sub">{"Requirements met" if single else "Requirements by stream"}</h3><div class="sbars">' + "".join(bars) + '</div>')

    # 5. the work, as compact rows
    crit = set(map_data(m)["crit"])
    preds = {u["id"]: m.out(u, "blocked-by", "unit") for u in units}
    done_ids = {u["id"] for u in merged}
    can_ = set(map_data(m)["can"])
    ready = [u for u in units if u["id"] not in done_ids and u["id"] in can_]
    later = sorted([u for u in units if u["id"] not in done_ids and u not in ready], key=lambda u: (u["id"] not in crit, (u.get("fields") or {}).get("order") or 0))

    def when_merged(u):
        pr = str((u.get("fields") or {}).get("ships in") or "").lstrip("#")
        for e in u.get("evidence", []):
            if isinstance(e, dict) and pr and pr in str(e.get("link", "")) and e.get("when"):
                return e["when"]
        return ""

    def row(u, kind):
        f = u.get("fields") or {}
        if kind == "merged":
            right = html.escape(f.get("ships in", "")) + (" · " + html.escape(when_merged(u)) if when_merged(u) else "")
        elif kind == "later":
            waits_ = [p for p in preds[u["id"]] if p not in done_ids] + [x for x in m.out(u, "blocked-by") if m.by.get(x, {}).get("kind") != "unit" and m.by.get(x, {}).get("state") not in ("agreed", "recorded")]
            right = "waits on " + " ".join(f'<span class="id">{p}</span>' for p in dict.fromkeys(waits_))
        else:
            right = "ready to start"
        return (f'<li class="w {kind}"><i></i><span class="id">{u["id"]}</span><span class="wt">{inline(u.get("title", ""))}'
                + (' <span class="chip c-open">critical path</span>' if u["id"] in crit and kind != "merged" else "")
                + f'</span><span class="wr">{right}</span></li>')
    open_rows = "".join(row(u, "ready") for u in ready) + "".join(row(u, "later") for u in later)
    merged_rows = "".join(row(u, "merged") for u in merged)
    out.append('<h3 class="sub">The work</h3>'
               f'<p class="caption">{len(ready)} can start now · {len(later)} waiting, critical path first · {len(merged)} merged</p>'
               f'<ul class="wlist">{open_rows or "<li class=muted>nothing open</li>"}</ul>'
               + (f'<details class="wmerged"><summary>{len(merged)} merged: '
                  + ", ".join(html.escape((u.get("fields") or {}).get("ships in", u["id"])) for u in merged)
                  + f'</summary><ul class="wlist">{merged_rows}</ul></details>' if merged else ""))

    # 6. latest evidence
    ev = []
    for i in m.items:
        for e in i.get("evidence", []):
            if isinstance(e, dict) and e.get("when") and str(e["when"])[:1].isdigit():
                ev.append((str(e["when"]), i, e))
    ev.sort(key=lambda x: x[0], reverse=True)
    seen, feed = set(), []
    for w, i, e in ev:
        key = (e.get("link"), re.sub(r"\s*\([A-Z][A-Z0-9]*-\d+\)\s*$", "", str(e.get("what", ""))), w[:10])
        if key in seen:
            continue
        seen.add(key)
        mark = {"holds": "ok", "fails": "bad"}.get(e.get("outcome"), "src")
        what = f'<a href="{html.escape(e["link"])}">{inline(e.get("what", ""))}</a>' if e.get("link") else inline(e.get("what", ""))
        feed.append(f'<li class="{mark}"><span class="date">{html.escape(w[:10])}</span><span class="id">{i["id"]}</span><span>{what}</span></li>')
        if len(feed) == 8:
            break
    if feed:
        out.append('<h3 class="sub">Latest evidence</h3><ul class="feed">' + "".join(feed) + '</ul>')
    return "".join(out)


def insights_html(rows):
    marks = {"bottleneck": "!", "ask": "?", "next": "→", "ok": "✓"}
    return ('<ul class="insights">' + "".join(f'<li class="ins {k}"><b>{marks.get(k, "!")}</b><span>{t}</span></li>' for k, t in rows) + '</ul>') if rows else ""


def ids(xs):
    return " ".join(f'<span class="id">{x}</span>' for x in dict.fromkeys(xs)) or '<span class="muted">none</span>'


def xrow(item, summary_right, body, cls=""):
    return (f'<details class="req {cls}" id="{item["id"]}"><summary><i class="st"></i><span class="id">{item["id"]}</span>'
            f'<span class="shall">{inline(item.get("title", ""))}</span><span>{summary_right}</span></summary><div class="more">{body}</div></details>')


def raid_html(m):
    f_ = lambda i: i.get("fields") or {}
    risks, issues = m.kind("risk"), [i for i in m.kind("issue") if f_(i).get("status") != "closed"]
    asms, deps = m.kind("assumption"), m.kind("dependency")
    lvl = {"high": 3, "medium": 2, "low": 1}
    score = lambda r: lvl.get(f_(r).get("probability"), 0) * 10 + lvl.get(f_(r).get("impact"), 0)
    rows = []
    if risks:
        top = max(risks, key=score)
        rows.append(("bottleneck", f'The biggest risk is {top["id"]}: {inline(top.get("title", ""))} ({f_(top).get("probability", "?")} probability, {f_(top).get("impact", "?")} impact).'))
        nore = [r["id"] for r in risks if not f_(r).get("response")]
        if nore:
            rows.append(("ask", f'{len(nore)} of {len(risks)} risks have no response yet: {" ".join(nore)}.'))
    opend = [d for d in deps if f_(d).get("status") == "open"]
    if opend:
        rows.append(("ask", f'{len(opend)} outside dependencies are not in place; the nearest is needed by {html.escape(str(f_(opend[0]).get("need by") or "a day not set"))}: {inline(opend[0].get("title", ""))}.'))
    unv = [a for a in asms if f_(a).get("status") == "open"]
    if unv:
        rows.append(("next", f'{len(unv)} assumptions are still to be checked; each names the gate it must hold by.'))
    out = [insights_html(rows)]
    gates = gates_in_order(m)
    if gates and (risks or deps):
        code = lambda g: g.get("title", "").split(" · ")[0] if " · " in g.get("title", "") else g["id"]
        cols = [("build start", "Build start", "")] + [(g["id"], code(g), g.get("title", "").split(" · ", 1)[-1]) for g in gates]
        lanes = []
        for key, lab, name in cols:
            rs = [r for r in risks if str(f_(r).get("proximity") or "build start") == key]
            ds = [d for d in deps if str(f_(d).get("need by") or "") == key and f_(d).get("status") == "open"]
            chips = "".join(f'<a class="tchip t{"1" if score(r) >= 32 else "2"}" href="#{r["id"]}" title="{html.escape(r.get("title", ""))}">{r["id"]}</a>' for r in sorted(rs, key=score, reverse=True))
            dchips = "".join(f'<a class="tchip tx" href="#{d["id"]}" title="{html.escape(d.get("title", ""))}">{d["id"]}</a>' for d in ds)
            lanes.append(f'<div class="rg{" hot" if rs or ds else ""}"><b>{html.escape(lab)}</b><span>{inline(name)}</span>'
                         f'<div class="rr">{chips or ""}</div><div class="rd">{dchips}</div></div>')
        out.append('<h3 class="sub">When each could hit</h3><div class="rgrail">' + "".join(lanes) + '</div>'
                   '<div class="key"><span><i class="tchip t1 k"></i> high risk</span><span><i class="tchip t2 k"></i> other risk</span><span><i class="tchip tx k"></i> an outside dependency still missing</span><span class="muted">Each sits under the gate where it could hit, or is needed by.</span></div>')
    if risks:
        grid = []
        for p in ("high", "medium", "low"):
            cells = "".join('<td class="rc l{}">'.format(lvl[p] + lvl[i]) + " ".join(f'<a class="tchip t{"1" if lvl[p] + lvl[i] >= 5 else "2"}" href="#{r["id"]}" title="{html.escape(r.get("title", ""))}">{r["id"]}</a>'
                                    for r in risks if f_(r).get("probability") == p and f_(r).get("impact") == i) + '</td>' for i in ("low", "medium", "high"))
            grid.append(f'<tr><th scope="row">{p}</th>{cells}</tr>')
        out.append('<div class="riskm"><table><thead><tr><th>probability ↓ · impact →</th><th>low</th><th>medium</th><th>high</th></tr></thead><tbody>' + "".join(grid) + '</tbody></table></div>')
        body = lambda r: (f'<p><b>If</b> {inline(f_(r).get("if", ""))} <b>then</b> {inline(f_(r).get("then", ""))}</p>'
                          + (f'<p class="muted"><b>Watch for.</b> {inline(f_(r)["trigger"])}</p>' if f_(r).get("trigger") else "")
                          + f'<dl class="refs"><div><dt>Response</dt><dd>{cell(f_(r).get("response") or "missing")}</dd></div><div><dt>Acts on it</dt><dd>{inline(f_(r).get("actionee") or "nobody named")}</dd></div>'
                          f'<div><dt>Could happen</dt><dd>{inline(str(f_(r).get("proximity") or "not set"))}</dd></div><div><dt>If it happens</dt><dd>{inline(f_(r).get("contingency") or "not planned")}</dd></div></dl>')
        chipr = lambda r: (f'<span class="chip c-{ {"high": "open", "medium": "unsettled"}.get(f_(r).get("probability"), "unchecked") }">{html.escape(str(f_(r).get("probability") or "?"))} likely</span>'
                           f'<span class="chip c-{ {"high": "open", "medium": "unsettled"}.get(f_(r).get("impact"), "unchecked") }">{html.escape(str(f_(r).get("impact") or "?"))} impact</span>'
                           + cell(f_(r).get("response") or "missing"))
        out.append('<h3 class="sub">Risks</h3><div class="reqs">' + "".join(xrow(r, chipr(r), body(r)) for r in sorted(risks, key=score, reverse=True)) + '</div>')
    if issues:
        out.append('<h3 class="sub">What has already happened</h3><div class="reqs">' + "".join(
            xrow(i, cell(f_(i).get("impact", "")), f'<p><b>Until it is fixed.</b> {inline(f_(i).get("workaround") or "no workaround")}</p><p class="muted">Must be fixed by {inline(str(f_(i).get("target date") or "a day not set"))}</p>') for i in issues) + '</div>')
    if asms:
        out.append('<h3 class="sub">What we are taking for granted</h3><div class="reqs">' + "".join(
            xrow(a, cell(f_(a).get("status", "")), f'<p><b>If it is false.</b> {inline(f_(a).get("if false", ""))}</p><p><b>How we check.</b> {inline(f_(a).get("validation", ""))} <span class="muted">by {inline(str(f_(a).get("validate by") or "—"))}</span></p>') for a in asms) + '</div>')
    if deps:
        out.append('<h3 class="sub">Whom we are waiting on</h3><div class="reqs">' + "".join(
            xrow(d, cell("met" if f_(d).get("status") in ("met", "closed") else "open"), f'<dl class="refs"><div><dt>We need</dt><dd>{inline(f_(d).get("needs", ""))}</dd></div><div><dt>From</dt><dd>{inline(f_(d).get("provides", ""))}</dd></div><div><dt>Needed by</dt><dd>{inline(str(f_(d).get("need by") or "not set"))}</dd></div></dl>') for d in deps) + '</div>')
    return "".join(out)


def threats_html(m):
    f_ = lambda i: i.get("fields") or {}
    thr = m.kind("threat") + m.kind("privacy threat")
    rank = {"high": 3, "medium": 2, "low": 1}
    rows_, gaps_mit, gaps_req = [], [], []
    for t in thr:
        mits = m.into(t["id"], "covers", "mitigation")
        reqs = sorted({r for x in mits for r in m.into(x, "serves", "requirement")})
        if not mits and f_(t).get("response") != "accept":
            gaps_mit.append(t["id"])
        elif mits and not reqs:
            gaps_req.append(t["id"])
        rows_.append((t, mits, reqs))
    hidden = [i for i in m.items if i.get("kind") == "threat" and i.get("sensitivity") == "restricted"]
    unan = [e for e in m.kind("element") if f_(e).get("scope") == "not yet analysed"]
    ins = [("next", f'{len(thr)} threats ranked, {sum(1 for t in thr if f_(t).get("rank") == "high")} of them high before mitigation.')]
    if gaps_mit:
        ins.append(("bottleneck", f'{len(gaps_mit)} threats have no mitigation and are not accepted: {" ".join(gaps_mit)}.'))
    if gaps_req:
        ins.append(("ask", f'{len(gaps_req)} threats are mitigated only on paper: no requirement makes sure the mitigation gets built and tested ({" ".join(gaps_req)}).'))
    if unan:
        ins.append(("ask", f'{len(unan)} parts of the system are not analysed yet: {" ".join(e["id"] for e in unan)}.'))
    out = [insights_html(ins)]

    def arrow(t):
        a, b = f_(t).get("rank") or "?", f_(t).get("residual") or "?"
        return f'<span class="arrow">{cell(a)} → {cell(b)}</span>'
    stride = ["spoofing", "tampering", "repudiation", "information disclosure", "denial of service", "elevation of privilege"]
    linddun = ["linking", "identifying", "non-repudiation", "detecting", "data disclosure", "unawareness and intervenability", "non-compliance"]
    elms = [e for e in m.kind("element") if f_(e).get("element") != "trust boundary"]
    groups_ = [(k, "Security", c) for k, c in (("threat", stride),) if any(t["kind"] == k for t in thr)] \
        + [(k, "Privacy", c) for k, c in (("privacy threat", linddun),) if any(t["kind"] == k for t in thr)]
    if groups_ and elms:
        top = "".join(f'<th class="grp{" gstart" if gi else ""}" colspan="{len(c)}" scope="colgroup">{g}</th>' for gi, (_, g, c) in enumerate(groups_))
        head_ = "".join(f'<th class="c rot{" gstart" if gi and ci == 0 else ""}"><span>{html.escape(c)}</span></th>' for gi, (_, _, cs) in enumerate(groups_) for ci, c in enumerate(cs))
        body_ = []
        for e in elms:
            if not any(e["id"] in (f_(t).get("elements") or []) for t in thr) and f_(e).get("scope") != "not yet analysed":
                continue
            cells = []
            for gi, (kind, _, cs) in enumerate(groups_):
                for ci, c in enumerate(cs):
                    hit = [t for t in thr if t["kind"] == kind and f_(t).get("category") == c and e["id"] in (f_(t).get("elements") or [])]
                    cells.append(f'<td class="c{" gstart" if gi and ci == 0 else ""}">' + "".join(f'<a class="tdot r-{html.escape(str(f_(t).get("residual") or f_(t).get("rank") or "x"))}{" gap" if t["id"] in gaps_mit + gaps_req else ""}" href="#{t["id"]}" title="{html.escape(t["id"] + " · " + t.get("title", "") + " · after mitigation: " + str(f_(t).get("residual") or "not ranked"))}"></a>' for t in hit) + '</td>')
            body_.append(f'<tr class="{"unan" if f_(e).get("scope") == "not yet analysed" else ""}"><th scope="row"><span class="id">{e["id"]}</span> {inline(e.get("title", ""))}'
                         f'<em>{html.escape(f_(e).get("element", ""))}{" · not analysed" if f_(e).get("scope") == "not yet analysed" else ""}</em></th>{"".join(cells)}</tr>')
        out.append(f'<h3 class="sub">Where each threat lands</h3><div class="tbl"><table class="dots tgrid"><thead><tr><th></th>{top}</tr><tr><th></th>{head_}</tr></thead><tbody>{"".join(body_)}</tbody></table></div>'
                   '<div class="key"><span><i class="tdot r-high"></i> high after mitigation</span><span><i class="tdot r-medium"></i> medium</span><span><i class="tdot r-low"></i> low</span><span><i class="tdot gap"></i> a gap: no mitigation, or none required</span><span class="muted">Hover a dot for the threat; select it to open it.</span></div>')
    for head, kind in (("Security threats", "threat"), ("Privacy threats", "privacy threat")):
        rs = sorted([r for r in rows_ if r[0]["kind"] == kind], key=lambda r: -rank.get(f_(r[0]).get("rank"), 0))
        if not rs:
            continue
        items = []
        for t, mits, reqs in rs:
            chain = (f'<p class="chain"><span>{html.escape(f_(t).get("category", ""))}</span> on {ids(f_(t).get("elements", []))}'
                     f' · mitigated by {ids(mits) if mits else cell("missing") if f_(t).get("response") != "accept" else "accepted"}'
                     f' · required by {ids(reqs) if reqs else cell("missing") if mits else "—"}</p>')
            body = chain + (f'<p>{inline(f_(t)["rationale"])}</p>' if f_(t).get("rationale") else "") + "".join(f'<p class="muted"><b>{m.by[x]["id"]}.</b> {inline(m.by[x].get("title", ""))}</p>' for x in mits)
            items.append(xrow(t, arrow(t), body, "gap" if t["id"] in gaps_mit + gaps_req else ""))
        out.append(f'<h3 class="sub">{head} <span class="count">ranked before → after mitigation</span></h3><div class="reqs">{"".join(items)}</div>')
    left_ = sec_paras("What's left after our responses?") + sec_paras("What's left for the people affected?")
    if left_:
        out.append(f'<p class="caption"><b>What is left.</b> {" ".join(inline(t) for t in left_)}</p>')
    gap_txt = sec_paras("What didn't this cover, and who checked it?") + sec_paras("What didn't this cover?")
    if gap_txt:
        out.insert(2, f'<p class="caption"><b>Not covered.</b> {" ".join(inline(t) for t in gap_txt)}</p>')
    if hidden:
        out.append(f'<p class="muted small">{len(hidden)} restricted threats are held apart and not shown here.</p>')
    return "".join(out)


def data_html(m):
    f_ = lambda i: i.get("fields") or {}
    scr = m.kind("screening criterion")
    yes = [c for c in scr if f_(c).get("met") == "yes"]
    unsure = [c for c in scr if f_(c).get("met") == "unsure"]
    if len(yes) >= 2:
        verdict = ("bottleneck", f'A DPIA is owed: {len(yes)} screening criteria are met, and two are enough.')
    elif len(yes) + len(unsure) >= 2:
        verdict = ("ask", f'A DPIA may be owed: {len(yes)} {"criterion" if len(yes) == 1 else "criteria"} met and {len(unsure)} unsure, against the two that make one owed. Settling the unsure ones decides it: '
                   + "; ".join(inline(c.get("title", "")) for c in unsure) + '.')
    else:
        verdict = ("ok", f'A DPIA is probably not owed: {len(yes)} criteria met and {len(unsure)} unsure.')
    ins = [verdict]
    vens = m.kind("vendor or dependency")
    unk = [v for v in vens if any(str(f_(v).get(k, "")).lower() in ("", "unknown") for k in ("region", "retention")) and f_(v).get("receives")]
    if unk:
        ins.append(("ask", f'{len(unk)} recipient{"s" if len(unk) != 1 else ""} of personal data with an unknown region or retention: {" ".join(v["id"] for v in unk)}.'))
    out = [insights_html(ins)]
    recips = [v for v in vens if f_(v).get("receives")]
    if recips:
        W, rowH, top = 980, 150, 14
        wide_reg = any(len(str(f_(v).get("region") or "")) > 25 for v in recips)
        if wide_reg:
            rowH = 180  # a region too long for its half-line gets its own lines above what is kept
        ptab = sec_table("What do we process, and why?")

        def purpose(v):
            if not ptab:
                return ""
            hdr = [h.lower() for h in ptab["header"]]
            if "purpose" not in hdr or "recipients" not in hdr:
                return ""
            keys = [w.lower() for w in re.findall(r"[A-Za-z0-9]{3,}", (f_(v).get("provider") or "") + " " + v.get("title", ""))[:3]]
            hits = [r[hdr.index("purpose")] for r in ptab["rows"] if any(k in str(r[hdr.index("recipients")]).lower() for k in keys)]
            return "; ".join(dict.fromkeys(hits))
        H = top + max(1, len(recips)) * rowH
        def box(x, y, w, h, title, sub, cls=""):
            return (f'<g class="fbox {cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>'
                    f'<text x="{x + 12}" y="{y + 22}" class="ft">{html.escape(title)}</text>' + "".join(f'<text x="{x + 12}" y="{y + 40 + k * 14}" class="fs">{html.escape(t)}</text>' for k, t in enumerate(sub)) + '</g>')
        mid = top + len(recips) * rowH / 2 - 6
        svg = [box(10, mid - 40, 170, 80, "People", ["members of every firm", "and their sign-ins"]),
               box(250, mid - 40, 170, 80, "Our tables", ["orgs, members, domains"], "ours")]
        svg.append(f'<path class="farrow" d="M180,{mid} L250,{mid}" marker-end="url(#fa)"/>')
        for k, v in enumerate(recips):
            y = top + k * rowH
            reg, ret = str(f_(v).get("region") or "unknown"), str(f_(v).get("retention") or "unknown")
            svg.append(f'<path class="farrow" d="M420,{mid} C500,{mid} 500,{y + 44} 560,{y + 44}" marker-end="url(#fa)"/>')
            rec = "; ".join(f_(v).get("receives", []))
            lines, cur = [], ""
            for w in rec.split():
                if len(cur) + len(w) > 62:
                    lines.append(cur)
                    cur = w
                else:
                    cur = (cur + " " + w).strip()
            lines.append(cur)
            lines = lines[:2]
            extra = []
            if purpose(v):
                extra.append("for " + purpose(v))
            if f_(v).get("exit"):
                ex = "exit: " + str(f_(v)["exit"])
                cur_ = ""
                for w_ in ex.split():
                    if cur_ and len(cur_) + 1 + len(w_) > 62:
                        extra.append(cur_)
                        cur_ = w_
                    else:
                        cur_ = (cur_ + " " + w_).strip()
                extra.append(cur_)
            svg.append(box(560, y + 4, 410, rowH - 14, v.get("title", ""), ["receives " + lines[0]] + lines[1:] + extra, "vendor"))
            if wide_reg:
                rl, cur_ = [], ""
                for w_ in ("region: " + reg).split():
                    if cur_ and len(cur_) + 1 + len(w_) > 52:
                        rl.append(cur_)
                        cur_ = w_
                    else:
                        cur_ = (cur_ + " " + w_).strip()
                rl.append(cur_)
                rl = rl if len(rl) <= 3 else rl[:2] + [rl[2][:49] + "…"]
                rows_ = [(t, reg.lower() in ("unknown", "")) for t in rl] + [("kept: " + ret, ret.lower() in ("unknown", ""))]
                for j, (t, bad) in enumerate(rows_):
                    svg.append(f'<text x="572" y="{y + rowH - 20 - (len(rows_) - 1 - j) * 15}" class="fb{" bad" if bad else ""}">{html.escape(t)}</text>')
            else:
                for j, (lab, val) in enumerate((("region", reg), ("kept", ret))):
                    bad = val.lower() in ("unknown", "")
                    svg.append(f'<text x="{572 + j * 255}" y="{y + rowH - 20}" class="fb{" bad" if bad else ""}">{lab}: {html.escape(val)}</text>')
        out.append('<h3 class="sub">Where personal data goes</h3><div class="fig"><svg class="flow" viewBox="0 0 ' + f'{W} {H + 10}" role="img" aria-label="Where personal data goes">'
                   '<defs><marker id="fa" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L8,4 L0,8 z"/></marker></defs>'
                   + "".join(svg) + '</svg></div>'
                   + (f'<p class="caption"><b>Kept back.</b> {" ".join(inline(t) for t in sec_paras("Could we use less?"))}</p>' if sec_paras("Could we use less?") else ""))
    if vens:
        def bars(v):
            out_ = []
            for lim in f_(v).get("limits", []) or []:
                t = str(lim)
                mo = re.search(r"(\d[\d,]*)\s+of\s+(\d[\d,]*)", t)
                nums = [int(n.replace(",", "")) for n in re.findall(r"\d[\d,]*", t)]
                used, cap = (int(mo.group(1).replace(",", "")), int(mo.group(2).replace(",", ""))) if mo else ((nums[1], nums[0]) if len(nums) >= 2 else (None, None))
                label_ = t.split(":")[0] if ":" in t else t
                if used is not None and cap:
                    pct = min(100, 100 * used / cap)
                    out_.append(f'<div class="lim{" near" if pct >= 80 else ""}"><span>{inline(label_)}</span><span class="track"><i style="width:{pct:.0f}%"></i></span>'
                                f'<span class="num">{used:,} of {cap:,}</span></div>')
                else:
                    out_.append(f'<div class="lim"><span>{inline(t)}</span></div>')
            return "".join(out_)
        cards = "".join(
            f'<article class="vcard" id="{v["id"]}"><p class="pk"><span class="chip c-unchecked">{html.escape(f_(v).get("kind", ""))}</span>'
            f'<span class="muted small">{inline(str(f_(v).get("plan") or "plan unknown"))}</span></p><h3>{inline(v.get("title", ""))}</h3>'
            + bars(v)
            + "".join(f'<p class="small"><span class="chip c-unsettled">early access</span> {inline(e)}</p>' for e in f_(v).get("early access", []) or [])
            + f'<p class="small"><b>Promises.</b> {inline(str(f_(v).get("commitment") or "unknown"))}</p>'
            + (f'<p class="small"><b>To leave.</b> {inline(f_(v)["exit"])}</p>' if f_(v).get("exit") else "")
            + '</article>' for v in vens)
        notes_ = sec_paras("Where are we near a limit?") + sec_paras("What could change under us?")
        out.append(f'<h3 class="sub">What we take on with each vendor</h3><div class="dgrid">{cards}</div>'
                   + (f'<p class="caption">{" ".join(inline(t) for t in notes_)}</p>' if notes_ else ""))
    if scr:
        cells = "".join(f'<div class="scr m-{html.escape(f_(c).get("met", ""))}" title="{html.escape(f_(c).get("reason", ""))}"><b>{cell(f_(c).get("met", ""))}</b><span>{inline(c.get("title", ""))}</span><em>{html.escape(f_(c).get("source", ""))}</em></div>'
                        for c in sorted(scr, key=lambda c: {"yes": 0, "unsure": 1, "no": 2}.get(f_(c).get("met"), 3)))
        said = sec_paras("What did the people affected say?")
        why_ = sec_paras("Does this change need a DPIA?")
        out.append(f'<h3 class="sub">Does it need a DPIA?</h3>' + (f'<p class="caption">{" ".join(inline(t) for t in why_)}</p>' if why_ else "")
                   + f'<div class="scrs">{cells}</div><p class="caption">Hover a criterion for the reason given.'
                   + (f' <b>The people affected:</b> {" ".join(inline(t) for t in said)}' if said else "") + '</p>')
    if vens:
        rst = m.kind("restore path")
        if rst:
            how_ = sec_paras("How do we restore it?") + sec_paras("What can't we get back?")
            out.append('<h3 class="sub">If we lose it, how we get it back</h3>' + (f'<p class="caption">{" ".join(inline(t) for t in how_)}</p>' if how_ else "") + '<div class="reqs">' + "".join(
                xrow(r, cell("tested " + str(f_(r)["tested"]) if f_(r).get("tested") else "not tested"),
                     f'<p>{inline(f_(r).get("data", ""))}</p><dl class="refs"><div><dt>Against</dt><dd>{inline(", ".join(f_(r).get("against", [])))}</dd></div>'
                     f'<div><dt>Copy</dt><dd>{cell(f_(r).get("copy") or "unknown")}</dd></div><div><dt>Loss allowed / achieved</dt><dd>{cell(dur(f_(r).get("loss target")) or "unknown")} / {cell(dur(f_(r).get("loss achieved")) or "unknown")}</dd></div>'
                     f'<div><dt>Back within / achieved</dt><dd>{cell(dur(f_(r).get("time target")) or "unknown")} / {cell(dur(f_(r).get("time achieved")) or "unknown")}</dd></div></dl>') for r in rst) + '</div>')
    return "".join(out)


def body_html(item):
    """An item's filed body drawn block by block, steps and commands kept."""
    return "".join(block_html(b, {}, {}) for b in item.get("body") or [] if isinstance(b, dict) and not ("view" in b or "instrument" in b))


def record_html(d):
    """The decision's own record, as its sections were filed, inside its row on the ADRs tab."""
    key = next((h for h in SECS if h == d["id"] or h.startswith(d["id"] + "-")), None)
    if not key:
        return ""
    bl = [b for b in SECS[key] if not ("view" in b or "instrument" in b) and b.get("h") != "What did we decide?"]
    inner = "".join(f'<h4>{inline(b["h"])}</h4>' if "h" in b else block_html(b, {}, {}) for b in bl)
    return f'<details class="rec"><summary>The record, {html.escape(key)}</summary>{inner}</details>' if inner else ""


def owes_record(d):
    """A decision that earns a record of its own: one-way, or one that shapes the system."""
    f = d.get("fields") or {}
    return f.get("reversibility") == "one-way" or f.get("architectural") == "yes"


def adrs_html(m):
    f_ = lambda i: i.get("fields") or {}
    decs = [d for d in m.kind("decision") if f_(d).get("chosen")]
    agreed = [d for d in decs if d.get("state") == "agreed"]
    risky = [d for d in decs if d.get("state") != "agreed" and f_(d).get("reversibility") == "one-way"]
    ins = [("ok", f'{len(agreed)} of {len(decs)} decisions are agreed.')]
    owes = [d for d in decs if owes_record(d)]  # any other two-way decision keeps only its register entry
    norec = [d for d in owes if d["id"] not in RECORDED]
    if norec:
        ins.append(("ask", f'{len(norec)} of the {len(owes)} decisions that earn a record have none written yet: {" ".join(d["id"] for d in norec)}.'))
    if risky:
        ins.append(("bottleneck", f'{len(risky)} one-way decision{"s are" if len(risky) != 1 else " is"} still only proposed: {" ".join(d["id"] for d in risky)}.'))
    out = [insights_html(ins)]
    order = sorted(decs, key=lambda d: (d not in risky, d.get("state") == "agreed", int(d["id"].split("-")[1])))
    rows = []
    for d in order:
        f = f_(d)
        words = lambda t: set(re.findall(r"[a-z0-9]{4,}", str(t).lower()))
        cw = words(f.get("chosen", ""))
        best = max(f.get("options", []) or [""], key=lambda o: len(words(o) & cw))
        opts = "".join(f'<li class="{"ok" if o == best else "no"}">{inline(o)}{" <span class=" + chr(34) + "muted small" + chr(34) + ">chosen</span>" if o == best else ""}</li>' for o in f.get("options", []))
        body = (f'<p><b>We will.</b> {inline(f.get("chosen", ""))}</p>'
                + (f'<h4>Options weighed</h4><ul class="checks-list">{opts}</ul>' if opts else "")
                + ('<h4>Gains</h4><ul class="checks-list">' + "".join(f'<li class="ok">{inline(x)}</li>' for x in f.get("gains", [])) + '</ul>' if f.get("gains") else "")
                + ('<h4>Costs</h4><ul class="checks-list">' + "".join(f'<li class="warn">{inline(x)}</li>' for x in f.get("costs", [])) + '</ul>' if f.get("costs") else "")
                + f'<dl class="refs"><div><dt>{"Decided by" if d.get("state") == "agreed" else "To be decided by"}</dt><dd>{inline(f.get("decider") or "nobody named")}</dd></div><div><dt>Confidence</dt><dd>{inline(f.get("confidence") or "not stated")}</dd></div>'
                f'<div><dt>We will know it worked when</dt><dd>{inline(f.get("confirmation") or "not stated")}</dd></div><div><dt>Reopen when</dt><dd>{inline(f.get("revisit when") or "not stated")}</dd></div></dl>')
        rests = m.into(d["id"], "rests-on")
        serves = m.out(d, "serves", "requirement")
        body = (f'<p class="small"><b>Built on it:</b> {ids(rests + serves)}</p>' if rests or serves else "") + body + record_html(d)
        right = (f'<span class="muted small">{len(rests) + len(serves)} rest on it</span>' if rests or serves else "") + cell("agreed" if d.get("state") == "agreed" else "proposed") + (f' <span class="chip c-{"holds" if d["id"] in RECORDED else "open"}">{"record written" if d["id"] in RECORDED else "no record yet"}</span>' if owes_record(d) else "") + (' <span class="chip c-open">one-way</span>' if f.get("reversibility") == "one-way" else "") + (' <span class="chip c-unchecked">shapes the system</span>' if f.get("architectural") == "yes" else "")
        row = xrow(d, right, body)
        if f.get("revisit when"):
            row = row.replace('</summary>', f'<span class="reopen">Reopen when {inline(f["revisit when"])}</span></summary>', 1)
        rows.append(row)
    out.append('<div class="reqs">' + "".join(rows) + '</div>')
    return "".join(out)


def faq_computed(m):
    """The questions every reviewer and teammate asks, answered from the store, each pointing at the tab that holds the detail."""
    f_ = lambda i: i.get("fields") or {}
    gates = gates_in_order(m)
    gname = lambda g: g.get("title", "").partition(" · ")[2] or g.get("title", "")
    see = lambda t, words: f'<p class="small"><a href="{tab(t)}">{words} →</a></p>'
    qa = []
    if gates:
        oneway = [g for g in gates if f_(g).get("one-way") == "yes"]
        phases = list(dict.fromkeys(str(f_(g).get("phase") or "") for g in gates))
        steps = "".join(f'<li><b>{html.escape(nice(g["id"]))}</b> {inline(gname(g))}'
                        + (' <span class="chip c-open">one-way</span>' if g in oneway else "") + '</li>' for g in gates)
        qa.append(("How does this ship?",
                   f'<p>In {len(gates)} gated steps{" over " + str(len(phases)) + " phases (" + ", ".join(html.escape(p) for p in phases if p) + ")" if len(phases) > 1 else ""}, '
                   f'each with its own go and roll-back lines. {len(oneway)} of them cannot be undone.</p><ol class="prose">{steps}</ol>'
                   + see("cutover", "Each gate's card")))
        dated = [g for g in gates if str(f_(g).get("opens on") or "")[:1].isdigit()]
        nxt = next((g for g in gates if not any(isinstance(e, dict) and e.get("outcome") for e in g.get("evidence", []))), None)
        waits = m.out(nxt, "blocked-by") if nxt else []
        open_w = [t for t in waits if m.by.get(t, {}).get("state") not in ("agreed", "recorded") and not (m.by.get(t, {}).get("kind") == "unit" and f_(m.by[t]).get("ships in"))]
        when = (", ".join(f'{html.escape(nice(g["id"]))} on {html.escape(str(f_(g)["opens on"]))}' for g in dated) + "." if dated
                else "No gate has a day yet.")
        qa.append(("When does it happen?",
                   f'<p>{when}' + (f' The next step, {html.escape(nice(nxt["id"]))}, waits on {len(open_w)} of {len(waits)} things still open.' if nxt else "") + '</p>'
                   + see("status", "Where it stands")))
        rehearsed = [g for g in gates if f_(g).get("rollback tested on")]
        qa.append(("Can we roll it back?",
                   f'<p>{len(gates) - len(oneway)} of {len(gates)} steps can be rolled back; {len(rehearsed)} of those roll-backs have been rehearsed.'
                   + (" The one-way steps (" + ", ".join(html.escape(nice(g["id"])) for g in oneway) + ") need a backup and a tested restore first." if oneway else "") + '</p>'
                   + see("cutover", "Roll-back on each card")))
    vens, deps = m.kind("vendor or dependency"), m.kind("dependency")
    if vens or deps:
        body = ""
        if vens:
            body += '<p>Services it relies on:</p><ul class="prose">' + "".join(
                f'<li>{inline(v.get("title", ""))}' + (f' <span class="muted small">· {inline(f_(v)["plan"])}</span>' if f_(v).get("plan") and f_(v)["plan"] != "unknown" else "") + '</li>' for v in vens) + '</ul>'
        if deps:
            body += '<p>What it needs from other people:</p><ul class="prose">' + "".join(
                f'<li>{inline(d.get("title", ""))} <span class="muted small">· from {inline(f_(d).get("provides", "someone not named"))}'
                + (f', needed by {html.escape(nice(f_(d)["need by"]))}' if f_(d).get("need by") else "") + f', {html.escape(f_(d).get("status") or d.get("state", ""))}</span></li>' for d in deps) + '</ul>'
        qa.append(("What does it depend on?", body + see("raid", "Dependencies and what is at risk")))
    ifcs, brk = m.kind("interface"), m.kind("breaking change")
    if ifcs or brk:
        ext = [i for i in ifcs if f_(i).get("scope") == "external"]
        body = (f'<p>{len(ifcs)} interfaces change, {len(ext)} of them seen from outside the service'
                + (f', and {len(brk)} change breaks a caller' if brk else ', and none is filed as breaking a caller') + '.</p><ul class="prose">'
                + "".join(f'<li>{inline(i.get("title", ""))} <span class="muted small">· {html.escape(f_(i).get("change", ""))}, {html.escape(f_(i).get("scope", ""))}</span></li>' for i in ifcs)
                + "".join(f'<li class="warn">{inline(b.get("title", ""))} <span class="muted small">· breaks {inline(f_(b).get("who", "callers not named"))}</span></li>' for b in brk) + '</ul>')
        qa.append(("What changes for callers and other services?", body + see("design", "The interfaces in the design")))
    lv = {"high": 3, "medium": 2, "low": 1}
    risks = sorted([r for r in m.kind("risk") if f_(r).get("status") in (None, "open") and f_(r).get("direction", "downside") == "downside"],
                   key=lambda r: -(lv.get(f_(r).get("probability"), 0) * lv.get(f_(r).get("impact"), 0)))[:3]
    if risks:
        qa.append(("How could this fail?",
                   '<ul class="prose">' + "".join(
                       f'<li><b>If {inline(f_(r).get("if") or r.get("title", ""))}</b>, then {inline(f_(r).get("then") or "")}. '
                       f'<span class="muted small">{html.escape(f_(r).get("probability") or "?")} likely, {html.escape(f_(r).get("impact") or "?")} impact; '
                       + (f'if it happens: {inline(f_(r)["contingency"])}' if f_(r).get("contingency") else f'response: {html.escape(f_(r).get("response") or "none")}') + f' ({r["id"]})</span></li>' for r in risks)
                   + '</ul>' + see("raid", "Every risk")))
    open_q = [q for q in m.kind("question") if q.get("state") in ("open", "lean")]
    if open_q:
        top = sorted(open_q, key=lambda q: -len(m.into(q["id"], "blocked-by")))[:3]
        qa.append(("What is still undecided?",
                   f'<p>{len(open_q)} questions are open. The ones the most work waits on:</p><ul class="prose">'
                   + "".join(f'<li>{inline(q.get("title", ""))} <span class="muted small">· {html.escape(q["id"])}, {"decided by " + html.escape(str((q.get("fields") or {}).get("decider"))) if (q.get("fields") or {}).get("decider") else "nobody named to decide"}</span></li>' for q in top)
                   + '</ul>' + see("register", "Every open question")))
    return "".join(f'<details class="req qa"><summary><i class="st"></i><span class="id">ask</span><span class="shall">{html.escape(q)}</span><span></span></summary>'
                   f'<div class="more">{a}</div></details>' for q, a in qa)


def faq_html(m):
    f_ = lambda i: i.get("fields") or {}
    faqs = m.kind("answer")
    pending = [a for a in faqs if any(m.by.get(q, {}).get("state") in ("open", "lean") for q in m.out(a, "rests-on"))]
    out = [insights_html([("ask", f'{len(pending)} of {len(faqs)} answers rest on a question still open, so they may change.')] if pending else []),
           '<section data-view="search"><input class="filter" type="search" placeholder="Search the questions" aria-label="Search the questions">']
    gen = faq_computed(m)
    if gen:
        out.append(f'<h3 class="sub">What everyone asks first</h3><div class="reqs">{gen}</div>')
    for aud in ("external", "internal"):
        xs = [a for a in faqs if f_(a).get("audience") == aud]
        if not xs:
            continue
        rows = []
        for a in xs:
            f = f_(a)
            open_q = [q for q in m.out(a, "rests-on") if m.by.get(q, {}).get("state") in ("open", "lean", "deferred")]
            prov = ", ".join(x for x in (
                ("asked by " + inline(f["asked by"])) if f.get("asked by") else "",
                ("asked " + html.escape(fmt_day(str(f["asked"])))) if f.get("asked") else "",
                ("answered " + html.escape(fmt_day(str(f["answered"])))) if f.get("answered") else "") if x)
            body = (f'<p>{inline(f.get("answer", ""))}</p>' + (f'<p class="muted small">{prov[:1].upper() + prov[1:]}.</p>' if prov else "")
                    + (f'<div class="muted small">{body_html(a)}</div>' if body_html(a) else "")
                    + (f'<p class="small">May change: waits on ' + " ".join(f'<a class="id" href="{tab("register")}">{q}</a>' for q in open_q) + '.</p>' if open_q else ""))
            rows.append(xrow(a, cell("may change" if open_q else ("settled" if a.get("state") == "agreed" else "proposed")), body))
        out.append(f'<h3 class="sub">{"For customers and support" if aud == "external" else "For the team"}</h3><div class="reqs">' + "".join(rows) + '</div>')
    out.append('</section>')
    return "".join(out)


def glossary_html(m):
    """Our words and the vendor's apart; each term with what it means, the words to avoid, and the items that use it, linked."""
    f_ = lambda i: i.get("fields") or {}
    terms = sorted(m.kind("term"), key=lambda t: t.get("title", "").lower())
    where = {"requirement": "requirements", "acceptance criterion": "requirements", "question": "register", "decision": "adrs",
             "risk": "raid", "issue": "raid", "assumption": "raid", "dependency": "raid", "gate": "cutover", "metric": "cutover",
             "design section": "design", "interface": "design", "slice": "design", "threat": "threats", "privacy threat": "threats",
             "answer": "faq", "unit": "map"}
    def used(t):
        pats = [re.compile(r"(?<![\w-])" + re.escape(w) + r"s?(?![\w-])", 0 if w != w.lower() else re.I)
                for w in [t.get("title", "")] + list(f_(t).get("aliases") or []) if w]
        return [i for i in m.items if i["id"] != t["id"] and i.get("kind") != "term"
                and any(pt.search(i.get("title", "") + " " + body_only(i)) for pt in pats)]
    avoid = [t for t in terms if f_(t).get("avoid")]
    ours = [t for t in terms if f_(t).get("origin") not in ("vendor", "both")]
    theirs = [t for t in terms if f_(t).get("origin") in ("vendor", "both")]
    unused = [t for t in terms if not used(t)]
    ins = [("next", f'{len(terms)} terms: {len(ours)} of ours, {len(theirs)} the vendor\'s or shared with it.')]
    if avoid:
        ins.append(("ask", f'{len(avoid)} have words to avoid, because those mean something else here: ' + ", ".join(inline(t.get("title", "")) for t in avoid) + '.'))
    if unused:
        ins.append(("ask", f'{len(unused)} are defined but used nowhere in the document: ' + ", ".join(inline(t.get("title", "")) for t in unused) + '.'))
    def row(t):
        f = f_(t)
        us = used(t)
        links = " ".join(f'<a class="id" href="{(tab(where[i["kind"]]) + ("" if i["kind"] == "interface" else "#" + i["id"])) if i.get("kind") in where else "#"}" title="{html.escape(i.get("title", ""))}">{i["id"]}</a>' for i in us[:10])
        return (f'<div class="term" id="{t["id"]}"><dt>{inline(t.get("title", ""))}'
                + (f'<span class="chip c-unchecked">shared</span>' if f.get("origin") == "both" else "") + '</dt>'
                f'<dd><p>{inline(f.get("meaning", "") or body_only(t) or "No meaning written yet.")}</p>'
                + (f'<p class="small"><b>Not to be confused with</b> {inline(", ".join(f["avoid"]))}</p>' if f.get("avoid") else "")
                + (f'<p class="small muted">Used in {len(us)}: {links}{" …" if len(us) > 10 else ""}</p>' if us else '<p class="small muted">Not used anywhere yet.</p>')
                + '</dd></div>')
    out = [insights_html(ins), '<section data-view="search"><input class="filter" type="search" placeholder="Search the glossary" aria-label="Search the glossary">']
    for head, xs, sub in (("Our words", ours, "What we call things in this change."), ("The vendor's words", theirs, "Terms the vendor's documentation uses, as it means them.")):
        if xs:
            out.append(f'<h3 class="sub">{head}</h3><p class="muted small">{sub}</p><dl class="glossary">{"".join(row(t) for t in xs)}</dl>')
    out.append('</section>')
    return "".join(out)


def safe_json(d):
    return json.dumps(d, ensure_ascii=False).replace("</", "<" + chr(92) + "/")



FAILS = ("fails", "failed", "fail")


def paused_html(m):
    """What is paused: each deferred item, why, what brings it back, and what waits on it."""
    f_ = lambda i: i.get("fields") or {}
    its = [i for i in m.items if i.get("state") == "deferred"]
    if not its:
        return ""
    cards = []
    for i in its:
        paras = [b["p"] for b in i.get("body") or [] if isinstance(b, dict) and b.get("p")]
        why = paras[-1] if paras else ""
        waits = m.into(i["id"], "blocked-by")
        cards.append(f'<article class="pcard paused" id="{i["id"]}"><p class="pk"><span class="id">{i["id"]}</span><span class="chip c-unsettled">paused</span>'
                     + (f'<span class="muted small">{inline(f_(i).get("decider") or i.get("owner") or "")}</span>' if (f_(i).get("decider") or i.get("owner")) else "") + '</p>'
                     f'<h3>{inline(i.get("title", ""))}</h3>'
                     + (f'<p>{inline(why)}</p>' if why else '<p><span class="chip c-open">why and what brings it back not written</span></p>')
                     + (f'<p class="small"><b>Waiting on it:</b> {ids(waits)}</p>' if waits else "") + '</article>')
    return '<h3 class="sub">What is paused</h3><div class="pcards">' + "".join(cards) + '</div>'


def failed_checks_html(m):
    """Where a check failed: the latest verification of a requirement, a criterion or a test that fails, and the requirement it fails."""
    rows = []
    for i in m.items:
        if i.get("kind") not in ("requirement", "acceptance criterion", "test") or i.get("state") in ("superseded", "withdrawn"):
            continue
        ev = sorted([e for e in i.get("evidence", []) if isinstance(e, dict) and e.get("outcome")], key=lambda e: str(e.get("when") or ""))
        if not ev or str(ev[-1].get("outcome")).lower() not in FAILS:
            continue
        e = ev[-1]
        if i["kind"] == "requirement":
            reqs = [i["id"]]
        elif i["kind"] == "acceptance criterion":
            reqs = m.out(i, "serves", "requirement")
        else:
            reqs = sorted({r for x in m.out(i, "verifies") for r in ([x] if m.by.get(x, {}).get("kind") == "requirement" else m.out(m.by.get(x, {}), "serves", "requirement"))})
        rows.append((str(e.get("when") or ""), i, e, reqs))
    if not rows:
        return ""
    rows.sort(key=lambda r: r[0], reverse=True)
    body = "".join(
        f'<li class="bad"><b>{html.escape(fmt_day(w))}</b> · <span class="id">{i["id"]}</span> {inline(i.get("title", ""))}'
        + (f' · {inline(e.get("what") or "")}' if e.get("what") else "")
        + (f' <a href="{html.escape(e["link"])}">source</a>' if str(e.get("link") or "").startswith("http") else "")
        + f'<br><span class="small">Fails {ids(reqs)}</span></li>' for w, i, e, reqs in rows)
    return f'<h3 class="sub">Where a check failed</h3><ul class="checks-list failed">{body}</ul>'


def changed_reach_html(m):
    """What a changed requirement reaches: each requirement whose content differs from what an agreement last covered, and the items that rest on it, two steps out."""
    def agreed_content(rid):
        last = None
        for a in m.agreements:
            for st in a.get("settled", []):
                if st.get("id") == rid and st.get("content"):
                    last = (a.get("id"), st["content"])
        return last
    out = []
    for r in m.kind("requirement"):
        got = agreed_content(r["id"])
        if not got:
            continue
        agr, content = got
        now = {"title": r.get("title"), "fields": r.get("fields") or {}, "body": r.get("body") or []}
        diff = [k for k, v in content.items() if now.get(k, (r.get("fields") or {}).get(k)) != v]
        if not diff:
            continue
        first = sorted({x for (to, _), xs in m.rev.items() if to == r["id"] for x in xs})
        second = sorted({x for f in first for (to, _), xs in m.rev.items() if to == f for x in xs} - set(first) - {r["id"]})
        out.append(f'<div class="reach"><p class="pk"><span class="id">{r["id"]}</span><b>{inline(r.get("title", ""))}</b>'
                   f'<span class="chip c-unsettled">changed since {html.escape(str(agr))}</span></p>'
                   + (f'<p class="small"><b>Agreed as:</b> {inline(str(content["title"]))}</p>' if "title" in diff else "")
                   + (f'<p class="small muted">Also changed: {html.escape(", ".join(k for k in diff if k != "title"))}</p>' if [k for k in diff if k != "title"] else "")
                   + f'<p class="small"><b>Rests on it:</b> {ids(first)}</p>' + (f'<p class="small"><b>And on those:</b> {ids(second)}</p>' if second else "")
                   + '<p class="small muted">Checks taken before the change rest on the earlier wording.</p></div>')
    return ('<h3 class="sub">What a changed requirement reaches</h3>' + "".join(out)) if out else ""


def orphans_html(m):
    """What carries no requirement: a test that verifies nothing and protects no gate, and a gate no test protects."""
    f_ = lambda i: i.get("fields") or {}
    tests = m.kind("test")
    loose = [t for t in tests if not m.out(t, "verifies") and (f_(t).get("purpose") in (None, "", "requirement") or not m.out(t, "serves", "gate"))]
    bare = [g for g in gates_in_order(m) if not m.into(g["id"], "serves", "test") and not any(g["id"] == f_(t).get("before") for t in tests)]
    if not loose and not bare:
        return ""
    out = '<h3 class="sub">What carries no requirement</h3><div class="wcols">'
    if loose:
        out += ('<div class="wcol"><h4>Tests that check nothing filed</h4><ul class="wlist">' + "".join(
            f'<li class="w"><i></i><span class="id">{t["id"]}</span><span class="wt">{inline(t.get("title", ""))}</span><span class="wr">{html.escape(f_(t).get("purpose") or "no purpose")}</span></li>' for t in loose)
            + '</ul><p class="caption">Either the work is unneeded or a requirement is missing.</p></div>')
    if bare:
        out += ('<div class="wcol"><h4>Gates no test protects</h4><ul class="wlist">' + "".join(
            f'<li class="w"><i></i><span class="id">{html.escape((g.get("title", "").split(" · ")[0]) or g["id"])}</span><span class="wt">{inline(g.get("title", "").split(" · ", 1)[-1])}</span></li>' for g in bare)
            + '</ul></div>')
    return out + '</div>'


def pull_apart_html(m):
    """Where security and privacy pull apart: a repudiation threat and a non-repudiation privacy threat sharing a mitigation or an element."""
    f_ = lambda i: i.get("fields") or {}
    rep = [t for t in m.kind("threat") if f_(t).get("category") == "repudiation"]
    nrep = [t for t in m.kind("privacy threat") if f_(t).get("category") == "non-repudiation"]
    pairs = []
    for a in rep:
        for b in nrep:
            mits = sorted(set(m.into(a["id"], "covers", "mitigation")) & set(m.into(b["id"], "covers", "mitigation")))
            els = sorted(set(f_(a).get("elements") or []) & set(f_(b).get("elements") or []))
            if mits or els:
                pairs.append((a, b, mits, els))
    if not pairs:
        return ""
    def side(t, label):
        return (f'<div class="side"><span class="tools-label">{label}</span><p class="pk"><span class="id">{t["id"]}</span></p>'
                f'<p>{inline(t.get("title", ""))}</p></div>')
    rows = []
    for a, b, mits, els in pairs:
        decs = sorted({d for x in (a["id"], b["id"]) for d in m.into(x, "answers", "decision") + m.into(x, "serves", "decision")})
        rows.append('<div class="pull">' + side(a, "Security wants a record") + '<div class="pullmid"><span>pulls against</span>'
                    + (f'<p class="small">through {ids(mits)}</p>' if mits else "") + (f'<p class="small">on {ids(els)}</p>' if els else "") + '</div>'
                    + side(b, "Privacy wants none") + '</div>'
                    + (f'<p class="small">Settled by {ids(decs)}</p>' if decs else '<p class="small muted">Not settled here: choosing between them is a decision for the register.</p>'))
    return '<h3 class="sub">Where security and privacy pull apart</h3>' + "".join(rows)


def regulator_html(m):
    """Must the regulator be consulted first: a DPIA owed and a privacy threat whose residual risk is high."""
    f_ = lambda i: i.get("fields") or {}
    scr = m.kind("screening criterion")
    yes = [c for c in scr if f_(c).get("met") == "yes"]
    unsure = [c for c in scr if f_(c).get("met") == "unsure"]
    high = [t for t in m.kind("privacy threat") if str(f_(t).get("residual") or "").lower() == "high"]
    if not high or len(yes) + len(unsure) < 2:
        return ""
    owed = len(yes) >= 2
    return (f'<div class="banner {"open" if owed else "warn"}"><b>{"The regulator must be consulted before this processing starts." if owed else "The regulator may have to be consulted first."}</b> '
            f'{"A DPIA is owed" if owed else "A DPIA may be owed"} and {len(high)} privacy threat{"s stay" if len(high) != 1 else " stays"} high after {"their responses" if len(high) != 1 else "its response"}: {ids([t["id"] for t in high])}. '
            'A high residual risk under a DPIA means prior consultation with the supervisory authority.</div>')


def libraries_html(m):
    """Which libraries it adds: each vendor that is a library, with version, licence, provenance and provider."""
    f_ = lambda i: i.get("fields") or {}
    libs = [v for v in m.kind("vendor or dependency") if f_(v).get("kind") == "library"]
    if not libs:
        return ""
    return ('<h3 class="sub">Which libraries it adds</h3>' + table_html(["Library", "Version", "Licence", "Where it comes from", "Provider"],
            [[f'{v["id"]} {v.get("title", "")}', f_(v).get("version") or "unknown", f_(v).get("licence") or "unknown", f_(v).get("provenance") or "unknown", f_(v).get("provider") or "unknown"] for v in libs]))


EXTRAS = {"register": (paused_html,), "trace": (failed_checks_html, changed_reach_html, orphans_html),
          "threats": (pull_apart_html,), "data": (regulator_html, libraries_html)}


def instrument_html(name, m, opts=None):
    return _instrument_html(name, m, opts) + "".join(fn(m) for fn in EXTRAS.get(name, ()))


def _instrument_html(name, m, opts=None):
    opts = opts or {}
    if name == "trace":
        d = trace_data(m)
        n = {k: sum(1 for r in d["reqs"] if r["status"] == k) for k in ("met", "partly", "not yet")}
        nowork = [r["id"] for r in d["reqs"] if not any(l[1] == r["id"] for l in d["links"])]
        ins = [("next", f'{n["met"]} of {len(d["reqs"])} requirements are met; {n["partly"]} partly; {n["not yet"]} not yet.')]
        if nowork:
            ins.append(("ask", f'{len(nowork)} requirements have no work planned to carry them: {" ".join(nowork[:8])}{"…" if len(nowork) > 8 else ""}.'))
        return insights_html(ins) + (f'<div class="legend"><span><i class="st st-met"></i> met: built and verified</span><span><i class="st st-partly"></i> partly</span>'
                f'<span><i class="st st-notyet"></i> not yet</span><span class="muted">{n["met"]} met · {n["partly"]} partly · {n["not yet"]} not yet</span></div>'
                f'<div class="trace"><div class="trace-graph" id="trace-graph" tabindex="0"></div><aside class="panel" id="trace-panel">'
                f'<p class="muted">Select a piece of work, a requirement or a gate to see its whole chain. A requirement shows what it must do, how it is accepted, and the evidence so far.</p></aside></div>'
                f'<script type="application/json" id="trace-data">{safe_json(d)}</script>' + testing_html(m))
    for nm, fn in (("raid", raid_html), ("threats", threats_html), ("data", data_html), ("adrs", adrs_html), ("faq", faq_html), ("glossary", glossary_html)):
        if name == nm:
            return fn(m)
    if name == "design":
        return design_html(m, tab("requirements"))
    if name == "runbook":
        return runbook_html(m)
    if name == "status":
        return status_html(m, {"cutover": tab("cutover"), "register": tab("register"), "requirements": tab("requirements")})
    if name == "map":
        return map_html(m)
    if name == "cutover":
        return cutover_html(m) + metrics_html(m) + people_html(m)
    if name == "register":
        return register_html(m, tab("trace"))
    if name == "requirements":
        return requirements_html(m, tab("trace"))
    raise ValueError(f"unknown instrument {name!r}")


def block_html(b, views, opts):
    if "h" in b:
        return f"<h3>{inline(b['h'])}</h3>"
    if "p" in b:
        return f"<p>{inline(b['p'])}</p>"
    if "ul" in b:
        return '<ul class="prose">' + "".join(f"<li>{inline(x)}</li>" for x in b["ul"]) + "</ul>"
    if "ol" in b:
        return '<ol class="prose steps">' + "".join(f"<li>{inline(x)}</li>" for x in b["ol"]) + "</ol>"
    if "callout" in b:
        return f'<div class="callout"><p>{inline(b["callout"])}</p></div>'
    if "tiles" in b:
        return '<div class="tiles">' + "".join(
            f'<div class="tile"><b>{html.escape(str(t.get("value", "")))}</b><span>{inline(t.get("label", ""))}</span>'
            + (f'<em>{inline(t["note"])}</em>' if t.get("note") else "") + "</div>" for t in b["tiles"]) + "</div>"
    if "table" in b:
        return table_html(b["table"]["header"], b["table"]["rows"])
    if "code" in b:
        return f"<pre><code>{html.escape(b['code'])}</code></pre>"
    if "quote" in b:
        return f"<blockquote>{inline(b['quote'])}</blockquote>"
    if "figure" in b:
        f = b["figure"]
        lines = "".join(f'<p class="figline">{inline(x)}</p>' for x in f.get("lines", []))
        return f'<figure data-block="diagram"><figcaption>{inline(f.get("caption", ""))}</figcaption><div class="fig">{f.get("svg", "")}</div>{lines}</figure>'
    if "instrument" in b:
        return instrument_html(b["instrument"], MODEL[0], b)
    if "image" in b:
        im = b["image"]
        src = os.path.relpath(im.get("src", ""), HERE[0] or ".").replace(os.sep, "/")
        return (f'<figure data-block="image"><img src="{html.escape(src)}" alt="{html.escape(im.get("alt", ""))}">'
                f'<figcaption>{inline(im.get("caption", ""))}</figcaption>' + (f'<p class="figline">{inline(im["provenance"])}</p>' if im.get("provenance") else "") + '</figure>')
    if "view" in b:
        key = (b["view"].get("page"), b["view"].get("position"))
        v = views[key]
        return f'<section data-view="{html.escape(str(key[0]))} {key[1]}">{view_html(v, opts.get(key, {}))}</section>'
    raise ValueError(f"unknown block {list(b)}")


def sources_key(srcs):
    """The Sources key: every outside source the site names, with what it is and its address."""
    rows = []
    for k, (u, t) in srcs:
        name = f'<a href="{html.escape(u, quote=True)}" target="_blank" rel="noopener">{html.escape(k)}</a>' if u else html.escape(k)
        what = html.escape(t) if t else '<span class="muted">what it is isn\'t said</span>'
        rows.append(f'<dt>{name}</dt><dd>{what}{"" if u else " <span class=" + chr(34) + "muted" + chr(34) + ">(no link)</span>"}</dd>')
    return '<details class="codes sources"><summary>Sources</summary><dl>' + "".join(rows) + '</dl></details>'


def bar(site, page, pages, rel):
    def link(p):
        cur = ' aria-current="page"' if p is page else ""
        return f'<a href="{rel(p["path"])}"{cur}>{html.escape(p["label"])}</a>'
    home = pages[0]
    groups = []
    if page.get("part") == "records":
        recs = [p for p in pages if p.get("part") == "records"]
        tabs_ = {p.get("label"): p.get("part") for p in pages if p.get("part") in ("now", "plan")}
        full = {"now": [], "plan": []}
        rounds, history = [], []
        for p in recs:
            base = p.get("label", "")[:-len(", as filed")] if p.get("label", "").endswith(", as filed") else None
            if base is not None and base in tabs_:
                full[tabs_[base]].append((p, base))
            elif p.get("label", "").lower().startswith("round"):
                rounds.append(p)
            else:
                history.append(p)
        short = lambda p, words: (f'<a href="{rel(p["path"])}"' + (' aria-current="page"' if p is page else "") + f'>{html.escape(words)}</a>')
        groups.append(f'<div class="navgroup"><span>&nbsp;</span><nav><a href="{rel(home["path"])}">← The documentation</a></nav></div>')
        for title, xs in (("Rounds", [(p, p["label"].replace("Rounds and working records", "All rounds")) for p in rounds]),
                          ("History", [(p, p["label"]) for p in history]),
                          ("Now, as filed", full["now"]), ("The plan, as filed", full["plan"])):
            if xs:
                first_full = title == "Now, as filed" or (title == "The plan, as filed" and not full["now"])
                groups.append(('<i class="navbreak"></i>' if first_full else "")
                              + f'<div class="navgroup{" rowstart" if first_full else ""}"><span>{title}</span><nav>{"".join(short(p, w) for p, w in xs)}</nav></div>')
    else:
        for part in ("now", "plan"):
            ps = [p for p in pages if p.get("part") == part]
            if ps:
                groups.append(f'<div class="navgroup"><span>{PARTS[part]}</span><nav>{"".join(link(p) for p in ps)}</nav></div>')
        recs = [p for p in pages if p.get("part") == "records"]
        if recs:
            groups.append(f'<div class="navgroup"><span>&nbsp;</span><nav><a href="{rel(recs[0]["path"])}">Work records →</a></nav></div>')
    used = sorted({i["id"].split("-")[0] for i in (MODEL[0].items if MODEL[0] else []) if "-" in i.get("id", "")} & set(KIND_WORDS) - {"GATE", "SLC"})
    key = ('<details class="codes"><summary>Codes</summary><dl>' + "".join(f'<dt>{k}</dt><dd>{html.escape(KIND_WORDS[k].lower())}</dd>' for k in used)
           + '<dt>B1, C1…</dt><dd>a step of the rollout: its gate and slice</dd></dl></details>') if used else ""
    srcs = sorted(USED_REFS.items(), key=lambda kv: kv[0].lower())
    if srcs:
        key = sources_key(srcs) + key
    return (f'<header class="bar"><div class="toprow"><a class="home" href="{rel(home["path"])}"><span class="mark"></span>'
            f'{html.escape(site.get("home") or site["title"])}</a>{key}</div>{"".join(groups)}</header>')


def page_html(site, page, pages, views, opts):
    here = os.path.dirname(page["path"])
    HERE[0] = here
    page = dict(page, label=page.get("label") or page.get("title") or page["path"], headline=page.get("headline") or page.get("label") or page.get("title") or "")

    def rel(path):
        return os.path.relpath(path, here or ".").replace(os.sep, "/")

    secs = page.get("sections", [])
    chips = "".join(f'<a href="#{slug(s["heading"])}">{html.escape(s.get("short") or s["heading"])}</a>' for s in secs if s.get("heading")) if len(secs) > 2 else ""
    badge = f'<span class="badge">{html.escape(page["badge"])}</span>' if page.get("badge") else ""
    meta = f'<div class="meta">{badge}<span>{inline(page.get("meta", ""))}</span></div>' if badge or page.get("meta") else ""
    hero = (f'<section class="hero"><span class="eyebrow">{html.escape(page.get("kicker", ""))}</span>'
            f'<h1>{inline(page["headline"])}</h1>{meta}'
            + (f'<p class="lead">{inline(status_lead(MODEL[0]) if page["lead"] == {"auto": "status"} else fix_counts(page["lead"], page))}</p>' if page.get("lead") else "")
            + (f'<div class="onpage"><span>On this page</span>{chips}</div>' if chips else "") + "</section>")
    def sec_html(k, s):
        sid = slug(s.get("heading") or "s" + str(k))
        if s.get("design") == "note":
            return (f'<section class="tabnote" id="{sid}"><h2>{inline(s["heading"])}</h2>'
                    + "".join(block_html(b, views, opts) for b in s.get("blocks", [])) + '</section>')
        return (f'<section id="{sid}"' + (' data-unplaced="1"' if s.get("unplaced") else "") + '>' + (f'<h2>{inline(s["heading"])}</h2>' if s.get("heading") else "")
                + "".join(block_html(b, views, opts) for b in s.get("blocks", [])) + "</section>")
    body = "".join(sec_html(k, s) for k, s in enumerate(secs))
    checks = ""
    if page.get("checks") or page.get("review"):
        rows = "".join(f'<li>{cell(c.get("state", ""))}<span>{inline(c.get("text", ""))}</span></li>' for c in page.get("checks", []))
        rows += "".join(f'<li>{cell(r.get("state", "review")) if isinstance(r, dict) else chr(60) + "span class=" + chr(34) + "chip c-unchecked" + chr(34) + ">review</span>"}<span>{inline(r.get("text", "") if isinstance(r, dict) else r)}</span></li>' for r in page.get("review", []))
        checks = f'<section class="checks"><h2>Checks on this page</h2><ul>{rows}</ul></section>'
    foot = f'<footer class="foot">{inline(site.get("foot", ""))}</footer>' if site.get("foot") else ""
    name = html.escape(site.get("home") or site["title"])
    title = name if page["path"] == "index.html" else f"{html.escape(page['label'])} · {name}"
    head = (f'<meta charset="utf-8"><title>{title}</title><meta name="claude:viewport-fit-sides" content="cover">'
            f'<link rel="stylesheet" href="{FONTS}"><style>{ASSET["site.css"]}</style>')
    entry = dict(page, pages=[p["path"] for p in pages]) if page["path"] == "index.html" else page
    names = {i["id"]: nice(i["id"]) for i in (MODEL[0].items if MODEL[0] else [])}
    content = (link_refs(name_ids(f'{bar(site, page, pages, rel)}<main>{hero}{body}{checks}</main>{foot}'))
               + f'<script type="application/json" id="praxis-names">{safe_json(names)}</script><script>{ASSET["site.js"]}</script>'
               f'<script type="application/json" id="praxis-page">{safe_json(entry)}</script>')
    if page["path"] == "index.html":
        return head + content
    return ('<!doctype html><html lang="en"><head>'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
            f'{head}</head><body>{content}</body></html>')


ASSET = {}
MODEL = [None]
RECORDED = set()
SECS = {}  # hosted sections' blocks by heading, for the instruments that draw them ("into")


def sec_paras(h):
    return [b["p"] for b in SECS.get(h, []) if "p" in b]


def sec_list(h):
    return [x for b in SECS.get(h, []) if "ul" in b for x in b["ul"]]


def sec_table(h):
    return next((b["table"] for b in SECS.get(h, []) if "table" in b), None)  # decisions whose record the site files as its own section
HERE = [""]


def tab(name):
    """Relative link from the page being rendered to a reader tab, named by its instrument."""
    target = "index.html" if name == "status" else f"pages/{name}.html"
    return os.path.relpath(target, HERE[0] or ".").replace(os.sep, "/")


# Each tab's design (the spec of record; reader-tabs.md points here): which hosted sections, by their heading in their
# type file's Sections list, go under the head ("before"), into the instrument ("into"), after the instrument as their own sections
# ("after"), or only to the tab's page as filed ("raw", by reader-tabs' filed-only test). A heading in none of these is flagged as
# unplaced.
# The tab design lives in the document skill's rule, tab-design.md; this renderer draws from it and keeps no copy.
TAB_DESIGN_RULE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "document", "rules", "tab-design.md")
PLACEMENTS = {"Under the head": "before", "In the instrument": "into", "After the instrument": "after", "Only as filed": "raw"}


def load_tab_design(path=TAB_DESIGN_RULE):
    """Read the per-tab placements and the kept-on-its-own-tab pairs from the tab-design rule."""
    design, shown, tab, where, part = {}, {}, None, None, None
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith("## "):
                part = line[3:].strip()
                continue
            if part == "Tabs" and line.startswith("### "):
                tab, where = line[4:].strip(), None
                design[tab] = {}
                continue
            mm = re.match(r"- \*\*(.+?):\*\*$", line)
            if part == "Tabs" and tab and mm:
                where = PLACEMENTS[mm.group(1)]
                continue
            mm = re.match(r"  - (.+)$", line)
            if part == "Tabs" and tab and where and mm:
                pre = re.match(r"any heading that starts `(.+)`$", mm.group(1))
                key = where + "_prefix" if pre else where
                design[tab].setdefault(key, []).append(pre.group(1) if pre else mm.group(1))
                continue
            mm = re.match(r"- (.+?), \*(.+)\*: when the site has no (.+) tab$", line)
            if part == "Kept on its own tab" and mm:
                shown[(mm.group(1), mm.group(2))] = mm.group(3)
    return design, shown


TAB_DESIGN, SHOWN_BY = load_tab_design()

def placed(label, heading, tabs=None):
    if tabs is not None and (label, heading) in SHOWN_BY and SHOWN_BY[(label, heading)] not in tabs:
        return "after"
    d = TAB_DESIGN.get(label, {})
    for where in ("before", "after", "into"):
        if heading in d.get(where, []):
            return where
    if any(heading.startswith(x) for x in d.get("into_prefix", [])):
        return "into"
    if heading in d.get("raw", []) or any(heading.startswith(x) for x in d.get("raw_prefix", [])):
        return "raw"
    return None


def split_tabs(pages):
    """A reader tab carries its head, the sections its design names, and its instrument. Every other section, its checks and
    review lines go, as filed, to a records page of the tab's documents, which the tab links to at its end."""
    out, extra = [], []
    tabs = {p.get("label") for p in pages if p.get("part") in ("now", "plan")}
    for p in pages:
        secs = p.get("sections", [])
        has_inst = any("instrument" in b for sec in secs for b in sec.get("blocks", []))
        if p.get("part") not in ("now", "plan") or not has_inst:
            out.append(p)
            continue
        label = p.get("label", "")
        inst = [{"blocks": [b for b in sec.get("blocks", []) if "instrument" in b]} for sec in secs if any("instrument" in b for b in sec.get("blocks", []))]
        rest = [sec for sec in secs if not any("instrument" in b for b in sec.get("blocks", [])) and sec.get("heading")]
        for sec in rest:
            SECS[sec["heading"]] = sec.get("blocks", [])
        before = [dict(sec, design="note") for sec in rest if placed(label, sec["heading"], tabs) == "before"]
        after = [sec for sec in rest if placed(label, sec["heading"], tabs) == "after"]
        src_dir = os.path.dirname(p["path"]) or "."

        def rebase(v):
            if isinstance(v, str):
                return re.sub(r"\]\(([^)#:\s]+)(#[^)]*)?\)", lambda mm: "](" + os.path.relpath(os.path.normpath(os.path.join(src_dir, mm.group(1))), "records").replace(os.sep, "/") + (mm.group(2) or "") + ")", v)
            if isinstance(v, list):
                return [rebase(x) for x in v]
            if isinstance(v, dict):
                return {k: rebase(x) for k, x in v.items()}
            return v
        filed = [dict(rebase(sec), unplaced=True) if placed(label, sec["heading"]) is None else rebase(sec) for sec in rest]
        if label == "ADRs" and MODEL[0]:
            missing = [d["id"] for d in MODEL[0].kind("decision") if d["id"] not in RECORDED and owes_record(d)]
            if missing:
                filed.insert(0, {"blocks": [{"p": f'{len(missing)} decisions that earn a record have none written yet: ' + ", ".join(missing) + '. Other two-way decisions keep only their register entry.'}]})
        slug_ = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")
        full = f"records/{slug_}-as-filed.html"
        held = [b["p"] for sec in rest if placed(label, sec["heading"], tabs) == "raw" for b in sec.get("blocks", [])
                if "p" in b and re.match(r"\d+ restricted items?: ask ", str(b["p"]))]
        inst = inst + ([{"blocks": [{"p": " ".join(dict.fromkeys(held)) + " (held apart from this copy)."}]}] if held else [])
        keep = before + inst + after  # a section placed after the instrument draws as its own section
        if filed or p.get("checks") or p.get("review"):
            keep.append({"blocks": [{"p": f'[The documents behind this tab, as filed]({os.path.relpath(full, os.path.dirname(p["path"]) or ".")})'}]})
            extra.append({"path": full, "label": f'{label}, as filed', "part": "records", "kicker": p.get("kicker", ""),
                          "headline": f'{label}: its documents as filed, unedited', "sections": filed,
                          "checks": p.get("checks", []), "review": p.get("review", [])})
        out.append(dict(p, sections=keep, checks=[], review=[]))
    return out + extra


def main(argv):
    if len(argv) not in (4, 5):
        print(__doc__, file=sys.stderr)
        return 2
    site = json.load(open(argv[1], encoding="utf-8"))
    resolved = json.load(open(argv[2], encoding="utf-8"))
    views = {(v["page"], v["position"]): v for v in resolved.get("views", [])}
    opts = {(v["page"], v["position"]): v.get("render", {}) for v in resolved.get("views", [])}
    pages = site.get("pages", [])
    errors = []
    if not pages or pages[0].get("path") != "index.html":
        errors.append("the first page must be index.html")
    for p in pages:
        if p.get("part") not in PARTS:
            errors.append(f"page {p.get('path')!r}: part {p.get('part')!r} isn't now, plan or records")
        for s in p.get("sections", []):
            for b in s.get("blocks", []):
                if "view" in b and (b["view"].get("page"), b["view"].get("position")) not in views:
                    errors.append(f"page {p.get('path')!r}: view {b['view']} isn't in the views file")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    for name in ("site.css", "site.js"):
        with open(os.path.join(ASSETS, name), encoding="utf-8") as fh:
            ASSET[name] = fh.read()
    REFS[0].update(site.get("refs") or {})
    REFS[1].extend(site.get("ref_patterns") or [])
    rx_ = ref_rx()
    if rx_:
        for mm in rx_.finditer(json.dumps(site.get("pages", []), ensure_ascii=False)):
            USED_REFS[mm.group(0)] = ref_for(mm.group(0))
    MODEL[0] = Model(json.load(open(argv[4], encoding="utf-8")) if len(argv) == 5 else {})
    RECORDED.update(re.match(r"(DEC-\d+)", sec["heading"]).group(1) for p in pages for sec in p.get("sections", [])
                    if re.match(r"DEC-\d+", sec.get("heading") or ""))
    pages = split_tabs(pages)
    out = argv[3]
    written = []
    for p in pages:
        path = os.path.join(out, p["path"])
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(page_html(site, p, pages, views, opts))
        written.append(path)
    if len(argv) == 5:
        shutil.copyfile(argv[4], os.path.join(out, "items.json"))
        written.append(os.path.join(out, "items.json"))
    print("\n".join(written))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
