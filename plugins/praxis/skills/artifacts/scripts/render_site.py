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


def stream_ids(m):
    """Each requirement stream's anchor, unique over every stream in the store, so Status and the Requirements tab agree
    and two names that slug alike never share one."""
    out, used = {}, set()
    for r in m.kind("requirement"):
        g = (r.get("fields") or {}).get("stream") or "Other"
        if g not in out:
            base = "stream-" + slug(g)
            sid, k = base, 2
            while sid in used:
                sid, k = f"{base}-{k}", k + 1
            out[g] = sid
            used.add(sid)
    return out


def requirements_html(m, trace=None):
    reqs = m.kind("requirement")
    groups = {}
    for r in cut(m, "requirements", reqs):
        groups.setdefault((r.get("fields") or {}).get("stream") or "Other", []).append(r)
    verifs = sorted({(r.get("fields") or {}).get("verification") for r in reqs} - {None})
    types = sorted({(r.get("fields") or {}).get("type") for r in reqs} - {None})
    chips = lambda name, vals: (f'<div class="chipset" data-filter="{name}"><span>{label(name)}</span>'
                                 f'<button aria-pressed="true" data-v="">All</button>'
                                 + "".join(f'<button aria-pressed="false" data-v="{html.escape(v)}">{html.escape(v)}</button>' for v in vals) + "</div>")
    sids = stream_ids(m)
    jump = "".join(f'<a href="#{sids[g]}">{inline(g)}</a>' for g in groups)
    noac = [r["id"] for r in reqs if not m.into(r["id"], "serves", "acceptance criterion")]
    tbr = [r["id"] for r in reqs if m.out(r, "blocked-by")]
    one = len(groups) == 1 and "Other" in groups
    streams = {(r.get("fields") or {}).get("stream") or "Other" for r in reqs}  # over every requirement, not only those the tab draws
    ins = [("next", f'{len(reqs)} requirements{"" if streams == {"Other"} else " in " + str(len(streams)) + (" stream" if len(streams) == 1 else " streams")}; {sum(1 for r in reqs if m.req_status(r) == "met")} met so far.')]
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
        out.append(f'<section class="stream" id="{sids[g]}">' + ("" if one else f'<h2><span class="sn">{gi:02d}</span>{inline(g)}</h2>') + '<div class="reqs">')
        for r in rs:
            f = r.get("fields") or {}
            st = m.req_status(r)
            acs_all = [m.by[a] for a in m.into(r["id"], "serves", "acceptance criterion")]
            acs = cut(m, "requirements", acs_all)
            threats = [t for mit in m.out(r, "serves", "mitigation") for t in m.out(m.by[mit], "covers")]
            design = m.into(r["id"], "serves", "design section")
            waits = m.out(r, "blocked-by")
            own = m.verdicts(r)[-1] if m.verdicts(r) else None
            acc = "".join(ac_html(m, a) for a in acs) or (f'<p class="muted"><a href="{as_filed_link()}#{acs_all[0]["id"]}">{len(acs_all)} criteria, as filed</a></p>' if acs_all else None) or (
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
    # a stream the reader cut left with nothing drawn keeps its anchor, so a link to it lands on where its requirements are
    for g in sorted({(r.get("fields") or {}).get("stream") or "Other" for r in reqs} - set(groups)):
        n = sum(1 for r in reqs if ((r.get("fields") or {}).get("stream") or "Other") == g)
        out.append(f'<section class="stream" id="{sids[g]}"><h2>{inline(g)}</h2><p class="muted">Its {n} requirement{"s are" if n != 1 else " is"} '
                   f'<a href="{as_filed_link()}">on the page as filed</a>; none needs a reader\'s action now.</p></section>')
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
        brief = cut(m, "register", [m.by[b] for b in m.into(i["id"], "serves", "brief")])
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
        items = cut(m, "register", [i for i in waiting if (i.get("fields") or {}).get("tier") == tier])
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
    decided = cut(m, "register", decided)
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
    can = [n for n in nodes if n in open_ and all(p not in open_ for p in preds.get(n, []))]  # filed order, so a render is repeatable
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
        insights.append({"id": nxt["id"], "kind": "next", "text": f'Start with {nxt["id"]}.', "title": nxt["title"],
                         "more": "It can start now" + (", it is on the critical path" if nxt["crit"] else "") + f', and {nxt["down"]} thing{"s" if nxt["down"] != 1 else ""} follow{"" if nxt["down"] != 1 else "s"} from it.'})
    open_preds = lambda n: [p for p in preds.get(n, []) if p in open_]
    merges = [o for o in live if o["kind"] in ("step", "gate") and len([p for p in open_preds(o["id"]) if nodes[p].get("kind") == "unit"]) >= 2]
    if merges:
        c = max(merges, key=lambda o: (o["down"] > 0, o["down"], len(open_preds(o["id"]))))
        lines = [p for p in open_preds(c["id"]) if nodes[p].get("kind") == "unit"]
        insights.append({"id": c["id"], "kind": "bottleneck", "text": f'{c["id"]} is where the work converges.', "title": c["title"],
                         "more": f'It waits on {" and ".join(lines)}, and {c["down"]} thing{"s" if c["down"] != 1 else ""} follow{"" if c["down"] != 1 else "s"} it.'})
    asks = [o for o in live if o["kind"] == "ask"]
    if asks:
        q = max(asks, key=lambda o: (o["down"], o["gates"]))
        if q["down"] >= 2:
            insights.append({"id": q["id"], "kind": "ask", "text": f'{q["id"]} holds up {q["down"]} things until it is answered.', "title": q["title"], "more": ""})
    orphans = [i for i in m.items if i.get("kind") in ("question", "decision") and i.get("state") in ("open", "lean", "proposed")
               and (i.get("fields") or {}).get("tier") == "1" and not (i.get("fields") or {}).get("decider")]
    for o_ in orphans[:1]:
        blocks = m.into(o_["id"], "blocked-by")
        gates_hit = sorted({g for b_ in blocks for g in ([b_] if m.by[b_].get("kind") == "gate" else [])})
        named = [m.by[b_].get("title", b_) for b_ in blocks if m.by[b_].get("kind") in ("slice", "gate", "unit")] or [b_ for b_ in blocks]
        what = "; ".join(named[:3]) + ("…" if len(named) > 3 else "")
        insights.append({"id": o_["id"], "kind": "ask", "text": f'{o_["id"]} is tier 1, and nobody is named to decide it.', "title": o_.get("title", ""),
                         "more": f'It blocks {what or "nothing filed yet"}.'})
    ranked = sorted(live, key=lambda o: -o["down"])
    keyset = {o["id"] for o in ranked[:8]} | {i["id"] for i in insights} | {o["id"] for o in out if o["kind"] == "gate"}
    for o in out:
        o["key"] = o["id"] in keyset
    return {"nodes": out, "edges": edges, "crit": crit, "can": can, "open": len(open_), "insights": insights}


def map_html(m):
    d = map_data(m)
    first = next((n for n in d["crit"] if n in d["can"]), d["crit"][0] if d["crit"] else "")
    kinds_can = [x["kind"] for x in d["nodes"] if x["id"] in d["can"]]
    lead = (f'<span><b>{len(d["can"])}</b> things can start now.</span><span class="muted small">'  # the claim, then quiet detail
            f'{kinds_can.count("step")} pieces of work and {len(kinds_can) - kinds_can.count("step")} questions, decisions or dependencies. The critical path runs through '
            f'{sum(1 for n in d["crit"] if any(x["id"] == n and not x["done"] for x in d["nodes"]))} unfinished steps'
            + (f', starting with <span class="id">{first}</span>' if first else "") + '.</span>')
    modes = ('<div class="chipset modes" role="group" aria-label="Show"><span>Show</span>'
             '<button aria-pressed="true" data-mode="all">Everything</button><button aria-pressed="false" data-mode="crit">Critical path</button>'
             '<button aria-pressed="false" data-mode="can">Can start now</button>'
             '<label class="ctl">Owner <select id="map-owner"><option value="">anyone</option></select></label>'
             '<label class="ctl"><input type="checkbox" id="map-done" checked> done steps</label>'
             '<label class="ctl"><input type="checkbox" id="map-asks" checked> questions and decisions</label></div>')
    key = ('<div class="key"><span><i class="kd"></i> work</span><span><i class="kd done"></i> done</span><span><i class="kq"></i> question or decision</span>'
           '<span><i class="kg"></i> gate</span><span><i class="kc"></i> critical path</span></div>')
    marks = {"bottleneck": "!", "ask": "?", "next": "→"}
    # the map's findings, the most pressing first as its conclusion, as insights_html orders every other instrument's
    # each finding's claim first, within the reader-tabs headline limits, then its detail and the item's title, quieter
    rows = [("next", lead)] + [(i["kind"], f'<span>{inline(i["text"])}</span><span class="muted small">{inline(i.get("more", ""))} {inline(i["title"])}</span>'
                                f'<button class="ref" data-show="{i["id"]}">show</button>') for i in d.get("insights", [])]
    rows.sort(key=lambda r: {"bottleneck": 0, "ask": 1}.get(r[0], 2))
    rest = "".join(f'<li class="ins {k}"><b>{marks[k]}</b>{t}</li>' for k, t in rows[1:])
    lead = f'<p class="conclusion {rows[0][0]}"><b>{marks[rows[0][0]]}</b>{rows[0][1]}</p>' + (f'<ul class="insights">{rest}</ul>' if rest else "")
    key = key.replace('</div>', '<span><i class="ksz"></i> bigger: more waits on it</span></div>', 1)
    # one control row under the lead: the modes and filters, the key behind a disclosure, and a slot time travel fills
    ctl = f'<div class="mapctl">{modes}<details class="mapkey"><summary>Key</summary>{key}</details><div class="ttslot"></div></div>'
    return (lead + ctl + f'<div class="trace wide"><div class="trace-graph mapgraph" id="map-graph"></div><aside class="panel" id="map-panel" data-cutover="{tab("cutover")}" data-register="{tab("register")}">'
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
        items = cut(m, "design", [d for d in m.kind("design section") if (d.get("fields") or {}).get("aspect") in aspects])
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
        for o in cut(m, "runbook", slos):
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
        notes.append(("bottleneck", f'None of the {len(alerts)} alerts exists in monitoring yet. The entry for each is the playbook it will carry once it is defined.'))
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
        for a in cut(m, "runbook", alerts):
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
        if cards:  # the reader cut can leave none; its count line then says where they are, under no empty heading
            out.append(f'<h3 class="sub">When an alert fires</h3><div class="acards">{"".join(cards)}</div>')
    procs = m.kind("procedure")
    if procs:
        cards = "".join(
            f'<article class="pcard" id="{p["id"]}"><p class="pk"><span class="id">{p["id"]}</span><span class="muted small">when {inline((p.get("fields") or {}).get("when", ""))}</span></p>'
            f'<h3>{inline(p.get("title", ""))}</h3>{body_html(p)}'
            f'<p><b>Check it worked.</b> {inline((p.get("fields") or {}).get("verify", "not stated"))}</p>'
            f'<p class="muted"><b>Undo.</b> {inline((p.get("fields") or {}).get("undo", "not stated"))}</p></article>' for p in cut(m, "runbook", procs))
        if cards:
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
        bars.append(f'<a class="sbar" href="{links.get("requirements", "pages/requirements.html")}#{stream_ids(m)[st]}"><span class="sname">{inline(st)}</span>'
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
    """An instrument's computed findings, the most pressing stated first as its conclusion, the rest as quiet rows whose
    mark alone carries the state colour."""
    if not rows:
        return ""
    marks = {"bottleneck": "!", "ask": "?", "next": "→", "ok": "✓"}
    # design-reader-instruments' order: what nobody owns or blocks a step, then what is unsettled, then where to start
    rows = sorted(rows, key=lambda r: {"bottleneck": 0, "ask": 1}.get(r[0], 2))
    (k0, t0), rest = rows[0], "".join(f'<li class="ins {k}"><b>{marks.get(k, "!")}</b><span>{t}</span></li>' for k, t in rows[1:])
    return f'<p class="conclusion {k0}"><b>{marks.get(k0, "!")}</b><span>{t0}</span></p>' + (f'<ul class="insights">{rest}</ul>' if rest else "")


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
        out.append('<h3 class="sub">Risks</h3><div class="reqs">' + "".join(xrow(r, chipr(r), body(r)) for r in cut(m, "raid", sorted(risks, key=score, reverse=True))) + '</div>')
    if issues:
        out.append('<h3 class="sub">What has already happened</h3><div class="reqs">' + "".join(
            xrow(i, cell(f_(i).get("impact", "")), f'<p><b>Until it is fixed.</b> {inline(f_(i).get("workaround") or "no workaround")}</p><p class="muted">Must be fixed by {inline(str(f_(i).get("target date") or "a day not set"))}</p>') for i in cut(m, "raid", issues)) + '</div>')
    if asms:
        out.append('<h3 class="sub">What we are taking for granted</h3><div class="reqs">' + "".join(
            xrow(a, cell(f_(a).get("status", "")), f'<p><b>If it is false.</b> {inline(f_(a).get("if false", ""))}</p><p><b>How we check.</b> {inline(f_(a).get("validation", ""))} <span class="muted">by {inline(str(f_(a).get("validate by") or "—"))}</span></p>') for a in cut(m, "raid", asms)) + '</div>')
    if deps:
        out.append('<h3 class="sub">Whom we are waiting on</h3><div class="reqs">' + "".join(
            xrow(d, cell("met" if f_(d).get("status") in ("met", "closed") else "open"), f'<dl class="refs"><div><dt>We need</dt><dd>{inline(f_(d).get("needs", ""))}</dd></div><div><dt>From</dt><dd>{inline(f_(d).get("provides", ""))}</dd></div><div><dt>Needed by</dt><dd>{inline(str(f_(d).get("need by") or "not set"))}</dd></div></dl>') for d in cut(m, "raid", deps)) + '</div>')
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
        keep = {i["id"] for i in cut(m, "threats", [r[0] for r in rs])}
        for t, mits, reqs in [r for r in rs if r[0]["id"] in keep]:
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
        # side by side, "kept: …" has the box's last 143px, about 18 monospace characters, and a region half the box;
        # either running longer stacks the lines, for every recipient, so the rows keep one height
        wide_reg = any(len(str(f_(v).get("region") or "")) > 25 or len("kept: " + str(f_(v).get("retention") or "unknown")) > 18 for v in recips)
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
                def wrap52(text, most):  # stacked lines of at most 52 monospace characters, the last cut short when there are more
                    ls, cur_ = [], ""
                    for w_ in text.split():
                        if cur_ and len(cur_) + 1 + len(w_) > 52:
                            ls.append(cur_)
                            cur_ = w_
                        else:
                            cur_ = (cur_ + " " + w_).strip()
                    ls.append(cur_)
                    return ls if len(ls) <= most else ls[:most - 1] + [ls[most - 1][:49] + "…"]
                kl = wrap52("kept: " + ret, 2)
                rl = wrap52("region: " + reg, 4 - len(kl))
                rows_ = [(t, reg.lower() in ("unknown", "")) for t in rl] + [(t, ret.lower() in ("unknown", "")) for t in kl]
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
            + '</article>' for v in cut(m, "data", vens))
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
    for d in cut(m, "adrs", order):
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
        for a in cut(m, "faq", xs):
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
    # An answered question has no place in the register, so a link to it goes to the decision that answered it.
    answered = {l.get("to"): d["id"] for d in m.kind("decision") if d.get("state") == "agreed"
                for l in d.get("links", []) if l.get("link") == "answers"}

    def target(i):
        if i.get("kind") == "question" and i["id"] in answered:
            return tab("adrs") + "#" + answered[i["id"]]
        if i.get("kind") not in where:
            return "#"
        return tab(where[i["kind"]]) + ("" if i["kind"] == "interface" else "#" + i["id"])
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
        links = " ".join(f'<a class="id" href="{target(i)}" title="{html.escape(i.get("title", ""))}">{i["id"]}</a>' for i in us[:10])
        return (f'<div class="term" id="{t["id"]}"><dt>{inline(t.get("title", ""))}'
                + (f'<span class="chip c-unchecked">shared</span>' if f.get("origin") == "both" else "") + '</dt>'
                f'<dd><p>{inline(f.get("meaning", "") or body_only(t) or "No meaning written yet.")}</p>'
                + (f'<p class="small"><b>Not to be confused with</b> {inline(", ".join(f["avoid"]))}</p>' if f.get("avoid") else "")
                + (f'<p class="small muted">Used in {len(us)}: {links}{" …" if len(us) > 10 else ""}</p>' if us else '<p class="small muted">Not used anywhere yet.</p>')
                + '</dd></div>')
    out = [insights_html(ins), '<section data-view="search"><input class="filter" type="search" placeholder="Search the glossary" aria-label="Search the glossary">']
    for head, xs, sub in (("Our words", ours, "What we call things in this change."), ("The vendor's words", theirs, "Terms the vendor's documentation uses, as it means them.")):
        if xs:
            out.append(f'<h3 class="sub">{head}</h3><p class="muted small">{sub}</p><dl class="glossary">{"".join(row(t) for t in cut(m, "glossary", xs))}</dl>')
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


# The visual library (the artifacts skill's visual-library rule): every visual a tab may show, the instrument body it draws
# with ("of" names the tab instruments it serves when that is not its own body alone), and the two tests that decide it. "needs" makes a visual eligible from the set's own data; among the eligible
# candidates the tab design lists, in its order, the first whose "wins" holds is shown first, and "why" says so on the page.
# A tab with two or more eligible candidates gets a picker of at most four.
MAPDATA = {}


def _map(m):
    if id(m) not in MAPDATA:
        MAPDATA[id(m)] = map_data(m) if m else {"nodes": [], "edges": []}
    return MAPDATA[id(m)]


def _gates(m):
    return [n for n in _map(m)["nodes"] if n["kind"] == "gate"]


def _shallow(m):
    """Twelve or more items besides gates, three quarters at depth 0 or 1, so columns by depth stack them into one tall strip."""
    nodes = [n for n in _map(m)["nodes"] if n["kind"] != "gate"]
    return len(nodes) >= 12 and sum(1 for n in nodes if n.get("layer", 0) <= 1) >= .75 * len(nodes)


VISUALS = {
    "map-web": {"body": "map", "layout": "web", "label": "Web",
                "needs": lambda m: len(_gates(m)) >= 1 and bool(_map(m)["edges"]), "wins": lambda m: len(_gates(m)) >= 2,
                "why": "the set has several gates, and the web shows what clusters around each and the threads between them"},
    "map-gates": {"body": "map", "layout": "gates", "label": "Gates in a row",
                  "needs": lambda m: len(_gates(m)) >= 2, "wins": lambda m: len(_gates(m)) >= 2 and _shallow(m),
                  "why": "most items wait on little or nothing, so columns by depth would stack them; the gates read best in a row"},
    "map-lanes": {"body": "map", "layout": "lanes", "label": "Lanes",
                  "needs": lambda m: True, "wins": lambda m: True,
                  "why": "the work runs several steps deep, so columns by depth show the order"},
}
CUR_LABEL = [""]


def views_html(name, m, b=None):
    """An instrument drawn with the tab's eligible candidate visuals, the first that wins shown first, and a picker when
    two or more are eligible. A tab whose design lists fewer than two candidates draws its instrument alone."""
    cands = [c for c in TAB_DESIGN.get(CUR_LABEL[0], {}).get("visuals", []) if c in VISUALS and name in VISUALS[c].get("of", (VISUALS[c]["body"],))]
    elig = [c for c in cands if VISUALS[c]["needs"](m)][:4]
    if len(elig) < 2:
        return instrument_html(name, m, b)
    first = next((c for c in elig if VISUALS[c]["wins"](m)), elig[0])
    btns = "".join(f'<button type="button" data-v="{c}" data-body="{VISUALS[c]["body"]}" data-layout="{VISUALS[c].get("layout", "")}" aria-pressed="{"true" if c == first else "false"}">'
                   f'{html.escape(VISUALS[c]["label"])}</button>' for c in elig)
    shown = VISUALS[first]["body"]  # only the first visual's body shows until the picker swaps it, so a page without scripts draws one
    bodies = "".join(f'<div class="viewbody" data-body="{bd}"{"" if bd == shown else " hidden"}>{instrument_html(bd, m, b)}</div>'
                     for bd in dict.fromkeys(VISUALS[c]["body"] for c in elig))
    return (f'<div class="views" data-tab="{slug(CUR_LABEL[0])}" data-default="{first}" data-layout="{VISUALS[first].get("layout", "")}">'
            f'<div class="pickrow"><div class="picker" role="group" aria-label="View">{btns}</div>'
            f'<span class="why" data-first="{first}">Shown first: {html.escape(VISUALS[first]["why"])}.</span></div>{bodies}</div>')


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
        return views_html(b["instrument"], MODEL[0], b)
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
    CUR_LABEL[0] = page.get("label") or ""
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
PLACEMENTS = {"Under the head": "before", "In the instrument": "into", "After the instrument": "after", "Only as filed": "raw",
              "Visuals": "visuals"}


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


# --- visuals: ws1 status & decisions ---
# Bodies a tab's picker can swap in (the visual-library rule), each answering its tab's question from the item store alone.
WS1_BODIES = {}


def people_in(text):
    """The people a decider or owner field names: it may name several, "A and B" or "A, B"."""
    return list(dict.fromkeys(p_ for p_ in re.split(r",\s*|\s+and\s+", text or "") if p_))


def id_order(x):
    pre, _, n = x.rpartition("-")
    return (pre, int(n) if n.isdigit() else 0)


def gate_columns(m):
    """Each gate on the map in rollout order (gates_in_order) with the unfinished items, by the map's done test, it waits on
    directly or through items that aren't gates, that no earlier gate waits on; and how many of those it waits on are done."""
    d = _map(m)
    by = {n["id"]: n for n in d["nodes"]}
    preds = {}
    for a, b_ in d["edges"]:
        preds.setdefault(b_, []).append(a)
    claimed, cols = set(), []
    for g in [g for g in gates_in_order(m) if g["id"] in by]:
        up, st = set(), [g["id"]]
        while st:
            for p_ in preds.get(st.pop(), []):
                if p_ not in up and by.get(p_, {}).get("kind") != "gate":
                    up.add(p_)
                    st.append(p_)
        waits = [x for x in up if not by[x]["done"] and x not in claimed]
        done = len([x for x in up if by[x]["done"] and x not in claimed])
        claimed |= up
        cols.append((g, waits, done, g["id"] in d["crit"]))
    return cols


def gateboard_html(m):
    cols = gate_columns(m)
    by = {n["id"]: n for n in _map(m)["nodes"]}
    ran = lambda g: any(isinstance(e, dict) and e.get("outcome") for e in g.get("evidence", []))
    code = lambda g: g.get("title", "").split(" · ")[0] if " · " in g.get("title", "") else g["id"]
    word = {"step": "work", "ask": "question", "dep": "dependency"}
    asks_ = lambda w: [x for x in w if by[x]["kind"] == "ask"]
    nxt = next((c for c in cols if not ran(c[0])), None)
    ins = []
    if nxt:
        g, w, _, _ = nxt
        who = sorted({p_ for x in asks_(w) for p_ in people_in(by[x]["owner"])})
        ins.append(("next", f'{html.escape(code(g))}, the next gate, waits on {len(w)} unfinished item{"s" if len(w) != 1 else ""}'
                    + (f': {len(asks_(w))} of them are answers from {html.escape(", ".join(who))}' if who else "") + '.' if w else
                    f'{html.escape(code(g))}, the next gate, waits on nothing unfinished.'))
    most = max(cols, key=lambda c: len(c[1]), default=None)
    if most and most is not nxt and len(most[1]) > (len(nxt[1]) if nxt else 0):
        ins.append(("bottleneck", f'{html.escape(code(most[0]))} waits on the most: {len(most[1])} unfinished items.'))
    nobody = [x for c in cols for x in asks_(c[1]) if not by[x]["owner"]]
    if nobody:
        ins.append(("ask", f'{len(nobody)} question{"s" if len(nobody) != 1 else ""} on the board name{"s" if len(nobody) == 1 else ""} nobody to decide: {" ".join(nobody[:6])}{"…" if len(nobody) > 6 else ""}.'))
    rank = {"ask": 0, "dep": 1, "step": 2}
    out = []
    for g, w, done, crit in cols:
        st = "ran" if ran(g) else (f"waits on {len(w)}" if w else "nothing left")
        tone_ = "c-holds" if ran(g) or not w else ("c-open" if crit else "c-unsettled")
        cards = []
        for x in sorted(w, key=lambda x: (rank.get(by[x]["kind"], 3), str(by[x]["when"] or "~"), x)):
            n = by[x]
            if n["kind"] == "ask":
                who = f'[{html.escape(n["owner"])}]' if n["owner"] else '<span class="nobody">[nobody named]</span>'
                st_ = "leaning" if n["state"] == "lean" else "to decide"
            else:
                who = html.escape(n["owner"]) if n["owner"] else ""
                st_ = "can start" if n["can"] else "waiting"
            due = f' · due {html.escape(fmt_day(n["when"]))}' if str(n["when"])[:1].isdigit() else ""
            cards.append(f'<li class="gbcard"><div class="gbmeta"><span class="id">{x}</span><span>{word.get(n["kind"], n["kind"])}</span>'
                         f'<span class="gbst">{st_}</span></div><p>{inline(n["title"])}</p><p class="gbwho">{who}{due}</p></li>')
        out.append(f'<section class="gbcol{" crit" if crit and not ran(g) else ""}" aria-label="{html.escape(code(g))}"><header><div class="gbtop">'
                   f'<span class="id">{html.escape(code(g))}</span><span class="chip {tone_}">{st}</span></div>'
                   f'<h3>{inline(g.get("title", "").split(" · ", 1)[-1])}</h3>'
                   + ('<p class="gbsub">on the critical path</p>' if crit and not ran(g) else "") + '</header>'
                   f'<ol class="gbcards">{"".join(cards)}</ol><p class="gbdone">{done} done</p></section>')
    return insights_html(ins) + f'<div class="gboard">{"".join(out)}</div>'


WS1_BODIES["gateboard"] = gateboard_html
VISUALS["gate-board"] = {"body": "gateboard", "of": ("map",), "label": "Gate board",
                         "needs": lambda m: len(_gates(m)) >= 2 and any(c[1] for c in gate_columns(m)),
                         "wins": lambda m: False,
                         "why": "the board reads the map gate by gate, each column what that gate still waits on"}


def _day(v):
    import datetime
    try:
        return datetime.date.fromisoformat(str(v)[:10])
    except ValueError:
        return None


def due_day(m, i):
    """An item's due point as a day: its decide-by when that is a date, else the opens-on date of the gate it names."""
    d = i.get("decide_by")
    g = m.by.get(d) if isinstance(d, str) else None
    return _day(d) or (_day((g.get("fields") or {}).get("opens on")) if g and g.get("kind") == "gate" else None)


def ageing_rows(m):
    """The register's waiting set (questions and decisions open, leaning or proposed, not restricted): days open since
    first filed, and days late or left against the due point."""
    import datetime
    today = datetime.date.today()
    rows = []
    for i in m.items:
        if i.get("kind") not in ("question", "decision") or i.get("state") not in ("open", "lean", "proposed") or i.get("sensitivity") == "restricted":
            continue
        filed, due = _day(i.get("first_filed")), due_day(m, i)
        rows.append({"item": i, "open": (today - filed).days if filed else None, "due": (due - filed).days if due and filed else None,
                     "late": (today - due).days if due and due < today else 0, "left": (due - today).days if due and due >= today else None})
    return rows


def ageing_html(m):
    rows = sorted(ageing_rows(m), key=lambda r: (-r["late"], r["left"] if r["left"] is not None else 10 ** 6, r["item"]["id"]))
    late = [r for r in rows if r["late"]]
    who = lambda r: (r["item"].get("fields") or {}).get("decider") or ""
    if late:
        names = sorted({p_ for r in late for p_ in people_in(who(r))})
        ins = [("bottleneck", f'{len(late)} answer{"s are" if len(late) != 1 else " is"} past due' + (f', waiting on {html.escape(", ".join(names))}' if names else "")
                + f'; the most overdue is {late[0]["item"]["id"]}, {late[0]["late"]} day{"s" if late[0]["late"] != 1 else ""} late.')]
    else:
        soon = next((r for r in rows if r["left"] is not None), None)
        ins = [("next", "No answer is past due" + (f'; the nearest is {soon["item"]["id"]}, due in {soon["left"]} day{"s" if soon["left"] != 1 else ""}.' if soon else "."))]
    undated = sorted((r["item"]["id"] for r in rows if r["due"] is None), key=id_order)  # no dated due point, or no filed date to age from
    rows = [r for r in rows if r["due"] is not None]
    span = max([1] + [max(r["open"], r["due"]) for r in rows])
    out = []
    for r in rows:
        i = r["item"]
        tone_ = "late" if r["late"] else ""
        note = f'{r["open"]} days open · ' + (f'{r["late"]} late' if r["late"] else f'due in {r["left"]}')
        tick = f'<i class="agdue" style="left:{r["due"] / span * 100:.1f}%" title="due"></i>'
        out.append(f'<li class="agrow {tone_}"><span class="id">{i["id"]}</span><div class="agbar"><i class="agopen" style="width:{max(r["open"], 0) / span * 100:.1f}%"></i>{tick}'
                   f'<span class="agnote">{note}</span></div><p>{inline(i.get("title", ""))} <span class="muted">{"[" + html.escape(who(r)) + "]" if who(r) else "[nobody named]"}</span></p></li>')
    rest = (f'<p class="muted small">{len(undated)} more waiting, with no dated due point or filed date to draw from: {" ".join(undated)}.</p>' if undated else "")
    return (insights_html(ins) + f'<ol class="ageing">{"".join(out)}</ol>' + rest
            + '<div class="key"><span><i class="agk"></i> days open</span><span><i class="agk due"></i> due point</span><span><i class="agk late"></i> past due</span></div>')


WS1_BODIES["ageing"] = ageing_html
VISUALS["decision-cards"] = {"body": "register", "label": "Decision cards", "needs": lambda m: True, "wins": lambda m: True,
                             "why": "no waiting answer is past its due point, so the cards lead with what needs whose answer"}
VISUALS["question-ageing"] = {"body": "ageing", "of": ("register",), "label": "Ageing",
                              "needs": lambda m: sum(1 for r in ageing_rows(m) if r["due"] is not None) >= 2,
                              "wins": lambda m: any(r["late"] for r in ageing_rows(m)),
                              "why": "a waiting answer is past its due point, so the ages come first"}
EXTRAS["ageing"] = EXTRAS["register"]  # the tab's in-instrument sections, such as what is paused, show under either body



def gate_ran(g):
    return any(isinstance(e, dict) and e.get("outcome") for e in g.get("evidence", []))


def gate_code(g):
    return g.get("title", "").split(" · ")[0] if " · " in g.get("title", "") else g["id"]


def merged_on(u):
    """The day a piece of work merged: the dated evidence whose link names its review request's number as a whole number."""
    pr = str((u.get("fields") or {}).get("ships in") or "").lstrip("#")
    hit = lambda link: bool(pr) and re.search(r"(?<!\d)" + re.escape(pr) + r"(?!\d)", str(link or "")) is not None
    return next((_day(e["when"]) for e in u.get("evidence", []) if isinstance(e, dict) and hit(e.get("link")) and _day(e.get("when"))), None)


def forecast_data(m):
    """The first gate in rollout order not yet run, when it has a dated opens-on and needs pieces of work (those it and
    every earlier gate are blocked-by): how many of them are merged, and the day the rest land at the team's pace, the
    mean of merges per full week since the first merge's week (the running week left out), and at the slowest and fastest
    of the last four full weeks, or of every full week when there are fewer."""
    import datetime
    today = datetime.date.today()
    units = m.kind("unit")
    days = sorted(d for d in (merged_on(u) for u in units) if d)
    if not days:
        return None
    monday = lambda d: d - datetime.timedelta(days=d.weekday())
    weeks, w = [], monday(days[0])
    while w <= monday(today):
        weeks.append((w, sum(1 for d in days if monday(d) == w)))
        w += datetime.timedelta(days=7)
    gates = gates_in_order(m)
    nxt = next((g for g in gates if not gate_ran(g)), None)
    when = _day((nxt.get("fields") or {}).get("opens on")) if nxt else None
    need = sorted({u for g in gates[:gates.index(nxt) + 1] for u in m.out(g, "blocked-by", "unit")}) if nxt else []
    if len(weeks) < 3 or not when or not need:  # weeks counted from the first merge's week through this one, both ends in
        return {"weeks": weeks, "gate": None}
    full = [n for _, n in weeks[:-1]]
    recent = full[-4:]
    pace = {"mean": sum(full) / len(full), "slow": min(recent), "fast": max(recent)}
    merged = sorted(d for d in (merged_on(m.by[u]) for u in need) if d)
    left = len(need) - len(merged)
    land = {k: (today + datetime.timedelta(days=round(left / v * 7)) if v else None) for k, v in pace.items()}
    return {"weeks": weeks, "gate": nxt, "when": when, "need": len(need), "merged": merged, "left": left, "pace": pace, "land": land, "today": today}


def forecast_html(m):
    import datetime
    d = forecast_data(m)
    g, when, land, today = d["gate"], d["when"], d["land"], d["today"]
    c = html.escape(gate_code(g))
    if not d["left"]:
        ins = [("next", f'Every piece {c} needs is merged' + (f'; its date, {fmt_day(when)}, has passed and it has not run.' if when < today else f'; it can open on its date, {fmt_day(when)}.'))]
    elif when < today:
        ins = [("bottleneck", f'{c}\'s date, {fmt_day(when)}, has passed: {d["left"]} of its {d["need"]} pieces are still to merge'
                + (f'; at this pace they land by {fmt_day(land["mean"])}.' if land["mean"] else "."))]
    else:
        late = (land["mean"] - when).days
        say = (f'about {late} day{"s" if late != 1 else ""} after its date' if late > 0 else
               f'about {-late} day{"s" if late != -1 else ""} before its date' if late < 0 else "on its date")
        ins = [("bottleneck" if late > 0 else "next", f'{c}\'s pieces land {say}: '
                f'{d["left"]} of {d["need"]} still to merge at {d["pace"]["mean"]:.1f} a week, by {fmt_day(land["mean"])}, against {fmt_day(when)}.')]
    W, H, L, T, B = 640, 220, 44, 18, 30
    x0 = min(d["weeks"][0][0], when)
    end = max([when, today] + [x for x in land.values() if x]) + datetime.timedelta(days=3)
    span = max(1, (end - x0).days)
    X = lambda day: L + (day - x0).days / span * (W - L - 12)
    top = d["need"]
    Y = lambda n: H - B - n / top * (H - B - T)
    done = len(d["merged"])
    pts = [f"{X(x0):.1f},{Y(0):.1f}"] + [f"{X(day):.1f},{Y(k):.1f}" for k, day in enumerate(d["merged"], 1)] + [f"{X(today):.1f},{Y(done):.1f}"]
    svg = [f'<line class="fcgrid" x1="{L}" x2="{W - 12}" y1="{Y(0):.1f}" y2="{Y(0):.1f}"/>',
           f'<line class="fcscope" x1="{L}" x2="{W - 12}" y1="{Y(top):.1f}" y2="{Y(top):.1f}"/>'
           f'<text class="fclab" x="{W - 12}" y="{Y(top) - 5:.1f}" text-anchor="end">{c} needs {top}</text>']
    band = ""
    if d["left"] and land["fast"]:
        slow_x = X(land["slow"]) if land["slow"] else W - 12
        svg.append(f'<path class="fcband" d="M{X(today):.1f},{Y(done):.1f} L{X(land["fast"]):.1f},{Y(top):.1f} L{slow_x:.1f},{Y(top):.1f} Z"/>')
        band = (" Band: the slowest and fastest of the last four full weeks" + ("; the slowest merged nothing, so it runs off the chart." if not land["slow"] else "."))
    if d["left"] and land["mean"]:
        svg.append(f'<line class="fcproj" x1="{X(today):.1f}" y1="{Y(done):.1f}" x2="{X(land["mean"]):.1f}" y2="{Y(top):.1f}"/>')
    svg.append(f'<polyline class="fcline" points="{" ".join(pts)}"/>')
    svg.append(f'<line class="fcgate" x1="{X(when):.1f}" x2="{X(when):.1f}" y1="{T}" y2="{H - B}"/><text class="fclab gate" x="{X(when) + 4:.1f}" y="{T + 10}">{c} date</text>')
    svg.append(f'<text class="fclab" x="{L}" y="{H - 10}">{fmt_day(x0)}</text><text class="fclab" x="{X(today):.1f}" y="{H - 10}" text-anchor="middle">today</text>'
               f'<text class="fclab" x="{L - 6}" y="{Y(0) + 4:.1f}" text-anchor="end">0</text><text class="fclab" x="{L - 6}" y="{Y(top) + 4:.1f}" text-anchor="end">{top}</text>')
    label = f'The {top} pieces of work {gate_code(g)} needs, merged over time, projected to its date at the team\'s pace.'
    return (insights_html(ins) + f'<figure class="forecast"><svg viewBox="0 0 {W} {H}" role="img" aria-label="{html.escape(label)}">{"".join(svg)}</svg>'
            f'<figcaption class="muted small">Line: {c}\'s pieces merged so far, {done} of {top}. Dashed: the team\'s mean pace per full week since its first merge.{band}</figcaption></figure>')


def rollout_data(m):
    gates = gates_in_order(m)
    stages = []
    for g in gates:
        f = g.get("fields") or {}
        outs = [e for e in g.get("evidence", []) if isinstance(e, dict) and e.get("outcome")]
        health = []
        for x in m.out(g, "rests-on", "metric"):
            mf = m.by[x].get("fields") or {}
            try:
                val, tgt = float(mf.get("value")), float(mf.get("target"))
            except (TypeError, ValueError):
                continue
            ok = val <= tgt if mf.get("direction") == "down" else val >= tgt if mf.get("direction") == "up" else None
            health.append({"id": x, "title": m.by[x].get("title", ""), "value": val, "target": tgt, "ok": ok})
        stages.append({"gate": g, "ran": bool(outs), "fails": any(e.get("outcome") == "fails" for e in outs), "health": health,
                       "exposure": f.get("exposure", ""), "decides": f.get("decides", "")})
    return stages


def mid_rollout(m):
    st = rollout_data(m)
    return any(s["ran"] for s in st) and not all(s["ran"] for s in st)


def rollout_html(m):
    st = rollout_data(m)
    ran = [s for s in st if s["ran"]]
    nxt = next((s for s in st if not s["ran"]), None)
    now = ran[-1] if ran else None
    bad = [h for s in ran for h in s["health"] if h["ok"] is False] + ([{"id": gate_code(s["gate"])} for s in ran if s["fails"]])
    scored = [h for s in ran for h in s["health"] if h["ok"] is not None]
    if now:
        lead = (f'{html.escape(gate_code(now["gate"]))} is out and ' + ("not healthy" if bad else "healthy" if scored else "its health is not stated")
                + f': it reaches {inline(now["exposure"] or "a reach not stated")}'
                + (f', and {" ".join(h["id"] for h in bad[:2])} {"is" if len(bad) == 1 else "are"} off target or failed' if bad
                   else "" if scored else ", and no metric it rests on has a direction, value and target"))
        lead += (f'; {html.escape(gate_code(nxt["gate"]))} waits on a go from {html.escape(nxt["decides"])}.' if nxt and nxt["decides"] else
                 f'; nobody is named to give {html.escape(gate_code(nxt["gate"]))} its go.' if nxt else "; every gate has run.")
        ins = [("bottleneck" if bad or (nxt and not nxt["decides"]) else "next", lead)]
    else:
        ins = []
    cells = []
    for s in st:
        cls = "fails" if s["fails"] else "ran" if s["ran"] else "next" if s is nxt else "later"
        word = {"fails": "failed", "ran": "done", "next": "next", "later": "later"}[cls]
        who = (f'go from {html.escape(s["decides"])}' if s["decides"] else "nobody named to give the go") if s is nxt else ""
        hs = "".join(f'<li class="{"ok" if h["ok"] else "bad" if h["ok"] is False else ""}"><b>{h["value"]:g}</b> {inline(h["title"])} <span class="muted">· target {h["target"]:g}</span></li>'
                     for h in s["health"])
        cells.append(f'<li class="rstage {cls}"><div class="rhead"><span class="id">{html.escape(gate_code(s["gate"]))}</span><span class="rword">{word}</span></div>'
                     f'<p>{inline(s["exposure"] or s["gate"].get("title", "").split(" · ", 1)[-1])}</p>'
                     + (f'<p class="rwho">{who}</p>' if who else "") + (f'<ul class="rhealth">{hs}</ul>' if hs and s["ran"] else "") + '</li>')
    return insights_html(ins) + f'<ol class="rollout">{"".join(cells)}</ol>'


def since_events(m):
    """Every dated change the store holds, newest first: (day, what, id, title)."""
    ev = []
    for a in m.agreements:
        if _day(a.get("date")):
            for x in a.get("settled", []):
                if x.get("id") in m.by:
                    ev.append((_day(a["date"]), "withdrawn" if "withdrawn" in (x.get("content") or {}) else "decided", x["id"]))
    first = min((_day(i.get("first_filed")) for i in m.items if _day(i.get("first_filed"))), default=None)
    for i in m.items:
        f = _day(i.get("first_filed"))
        if f and first and f > first:
            ev.append((f, "raised", i["id"]))  # the first filing is the set's start, not a change
        if i.get("kind") == "unit" and merged_on(i):
            ev.append((merged_on(i), "merged", i["id"]))
        for e in i.get("evidence", []):
            if isinstance(e, dict) and e.get("outcome") in ("holds", "fails") and _day(e.get("when")):
                ev.append((_day(e["when"]), "failed" if e["outcome"] == "fails" else "checked", i["id"]))
    seen, out = set(), []
    for e in sorted(ev, key=lambda e: (e[0], e[2]), reverse=True):
        if e not in seen and m.by[e[2]].get("sensitivity") != "restricted":
            seen.add(e)
            out.append(e)
    return out


SINCE_WORDS = {"decided": "decided", "withdrawn": "withdrawn", "raised": "raised", "merged": "merged", "checked": "checked and held", "failed": "failed a check"}


def since_html(m):
    import datetime
    ev = since_events(m)
    since = ev[0][0] - datetime.timedelta(days=7)  # without a recorded visit, the week before the latest change: about one gap between visits
    tone_ = {"decided": "c-holds", "withdrawn": "c-unchecked", "raised": "c-open", "merged": "c-holds", "checked": "c-holds", "failed": "c-open"}
    rows = "".join(f'<li data-when="{d.isoformat()}"{"" if d > since else " hidden"}><time>{fmt_day(d)}</time><span class="chip {tone_[w]}">{w}</span>'
                   f'<span class="id">{x}</span><span>{inline(m.by[x].get("title", ""))}</span></li>' for d, w, x in ev)
    counts = {}
    for d, w, _ in ev:
        if d > since:
            counts[w] = counts.get(w, 0) + 1
    head = f'Since {fmt_day(since)}: ' + ", ".join(f'{n} {SINCE_WORDS[w]}' for w, n in counts.items()) + "."
    return (f'<div class="since-visit" data-default="{since.isoformat()}" data-words="{html.escape(json.dumps(SINCE_WORDS))}">'
            f'<ul class="insights"><li class="ins next"><b>→</b><span class="sv-head">{head}</span></li></ul>'
            f'<p class="muted small sv-note">Counted from the week before the latest change. Once you have visited, it counts from your last visit on this device.</p>'
            f'<ol class="sv-list">{rows}</ol><p class="muted small sv-none" hidden>Nothing has changed since your last visit.</p></div>')


WS1_BODIES.update({"forecast": forecast_html, "rollout": rollout_html, "since": since_html})
VISUALS["status-briefing"] = {"body": "status", "label": "Briefing", "needs": lambda m: True, "wins": lambda m: not mid_rollout(m),
                              "why": "no rollout is part-way, so the briefing reads the whole state at once"}
VISUALS["forecast"] = {"body": "forecast", "of": ("status",), "label": "Forecast",
                       "needs": lambda m: bool((forecast_data(m) or {}).get("gate")), "wins": lambda m: False,
                       "why": "the forecast shows whether the next gate's pieces merge by its date"}
VISUALS["rollout-stages"] = {"body": "rollout", "of": ("status", "cutover"), "label": "Rollout",
                             "needs": lambda m: len(m.kind("gate")) >= 2 and any(gate_ran(g) for g in m.kind("gate")), "wins": mid_rollout,
                             "why": "the rollout is under way, so how far out it is and whether it is healthy come first"}
VISUALS["since-you-last-looked"] = {"body": "since", "of": ("status",), "label": "Since you last looked",
                                    "needs": lambda m: bool(since_events(m)), "wins": lambda m: False,
                                    "why": "it lists what changed since your last visit"}
VISUALS["cutover-rail"] = {"body": "cutover", "label": "Cutover rail", "needs": lambda m: True, "wins": lambda m: True,
                           "why": "no rollout is part-way, so the rail shows each gate's card in order"}


_instrument_before_ws1 = _instrument_html


def _instrument_html(name, m, opts=None):
    return WS1_BODIES[name](m) if name in WS1_BODIES else _instrument_before_ws1(name, m, opts)
# --- end visuals: ws1 ---


# --- visuals: ws2 design & diagnosis ---
# An incident's timeline and its contributing factors, as Status candidates; a design's sequences and states, drawn from
# diagram blocks that carry their form and elements in the portable tree's shape. Each tests only the set it is given.
WS2_BODIES = {}
KIND_WORDS.update({"OUT": "Outcome", "TL": "Timeline event", "CF": "Contributing factor", "ACT": "Action"})
ID_PAT = re.compile(r"\b(" + "|".join(sorted(KIND_WORDS, key=len, reverse=True)) + r")-(\d+)\b")


def _when(v):
    """A timeline event's time, read as ISO 8601; one with a zone is taken to UTC, so times with and without one compare."""
    import datetime
    try:
        t = datetime.datetime.fromisoformat(str(v or "").strip().replace(" ", "T").replace("Z", "+00:00"))
    except ValueError:
        return None
    return t.astimezone(datetime.timezone.utc).replace(tzinfo=None) if t.tzinfo else t


def _span(a, b):
    """The time between two moments, in words: 6 minutes, 2 hours 10 minutes, 3 days."""
    mins = max(int((b - a).total_seconds() // 60), 0)
    if mins < 60:
        return f"{mins} minute{'s' if mins != 1 else ''}"
    if mins < 48 * 60:
        h, mm = divmod(mins, 60)
        return f"{h} hour{'s' if h != 1 else ''}" + (f" {mm} minute{'s' if mm != 1 else ''}" if mm else "")
    return f"{mins // 1440} days"


INCIDENT_PHASES = (("onset", "began"), ("detection", "found"), ("mitigation", "contained"), ("resolution", "fixed"))
PHASE_TONE = {"onset": "open", "detection": "unsettled", "mitigation": "quiet", "resolution": "holds"}


def incident_events(m):
    """The incident's timeline events that carry a readable time, in time order, and the first event of each phase."""
    evs = sorted(((t, i) for i in m.kind("timeline event") for t in [_when((i.get("fields") or {}).get("at"))] if t), key=lambda x: x[0])
    firsts = {}
    for t, i in evs:
        ph = (i.get("fields") or {}).get("phase")
        if ph in PHASE_TONE and ph not in firsts:
            # contained once the first mitigation has taken hold, at its end where the event spans time
            end = _when((i.get("fields") or {}).get("until")) if ph == "mitigation" else None
            firsts[ph] = (end if end and end > t else t, i)
    return evs, firsts


def incident_timeline_html(m):
    evs, f = incident_events(m)
    t0, t1 = evs[0][0], evs[-1][0]
    total = max((t1 - t0).total_seconds(), 1)
    # durations count from the onset; with none recorded, from when it was found, and the line says so
    base = "onset" if "onset" in f else "detection"
    said = [f"{w} in {_span(f[base][0], f[ph][0])}" for ph, w in INCIDENT_PHASES[1:] if ph in f and ph != base]
    # the furthest the response got leads, within a headline's length; the earlier phases follow as its detail
    last, rest = said[-1], said[:-1]
    head = (last[0].upper() + last[1:] + (f"; {' and '.join(rest)}." if rest else ".") if base == "onset"
            else f"{last[0].upper() + last[1:]} after it was found; its onset isn't recorded" + (f", and it was {' and '.join(rest)}." if rest else "."))
    stamp = (lambda t: f"{t.day} {t:%b %H:%M}") if (t1 - t0).days >= 1 else (lambda t: f"{t:%H:%M}")
    out_ = (m.kind("outcome") or [{}])[0]
    if "resolution" not in f:
        head += {"resolved": " No resolution event is recorded.", "mitigated-but-watching": " It is contained and being watched.",
                 "indeterminate": " How it ended couldn't be settled."}.get((out_.get("fields") or {}).get("outcome"), " It isn't fixed yet.")
    pos = lambda t: 100 * (t - t0).total_seconds() / total
    cuts = [(ph, f[ph][0]) for ph, _ in INCIDENT_PHASES if ph in f] + [("end", t1)]
    segs = "".join(f'<span class="seg-{PHASE_TONE[a[0]] if a[0] != "onset" else "open"}" style="left:{pos(a[1]):.2f}%;width:{max(pos(b[1]) - pos(a[1]), .5):.2f}%"></span>'
                   for a, b in zip(cuts, cuts[1:]) if a[0] != "resolution")
    ticks = "".join(f'<li class="t-{PHASE_TONE[ph]}{" up" if n % 2 else ""}" style="left:{pos(f[ph][0]):.2f}%"><b>{stamp(f[ph][0])}</b>'
                    f'<span>{w}</span></li>' for n, (ph, w) in enumerate(INCIDENT_PHASES) if ph in f)
    rows = "".join(f'<li><span class="when">{t.day} {t:%b %H:%M}</span>'
                   f'<span class="muted small">{html.escape((i.get("fields") or {}).get("phase") or "other")}</span>'
                   f'<span class="id">{i["id"]}</span><span>{inline(i.get("title", ""))}</span></li>' for t, i in evs)
    rests = "".join(f'<p class="pk"><span class="id">{o["id"]}</span><span class="chip c-{"holds" if (o.get("fields") or {}).get("outcome") == "resolved" else "unsettled"}">'
                    f'{html.escape((o.get("fields") or {}).get("outcome") or "outcome not recorded")}</span><span>{inline(o.get("title", ""))}</span></p>' for o in m.kind("outcome"))
    done = "resolution" in f or (out_.get("fields") or {}).get("outcome") == "resolved"
    return (insights_html([("ok" if done else "bottleneck", head)]) + rests
            + f'<div class="itl"><div class="itl-bar">{segs}</div><ol class="itl-ticks">{ticks}</ol></div>'
            '<div class="legend"><span><i class="kseg seg-open"></i> not yet found</span><span><i class="kseg seg-unsettled"></i> found, not contained</span>'
            '<span><i class="kseg seg-quiet"></i> contained, not fixed</span></div>'
            f'<details class="itl-all"><summary>Every event, in order ({len(evs)})</summary><ol class="itl-list">{rows}</ol></details>')


FACTOR_ORDER = ("trigger", "gap", "detection", "recovery")
FACTOR_WORDS = {"trigger": "Trigger", "gap": "Let it through", "detection": "Slow to find", "recovery": "Slow to recover"}
# results-and-certainty's grades: only an observed cause holds; traced, inferred and unverified are all still unsettled
CERTAINTY_TONE = {"observed": "holds", "traced": "unsettled", "inferred": "unsettled", "unverified": "unsettled"}


def _factors(m):
    rank = lambda c: FACTOR_ORDER.index((c.get("fields") or {}).get("factor")) if (c.get("fields") or {}).get("factor") in FACTOR_ORDER else len(FACTOR_ORDER)
    return sorted(m.kind("contributing factor"), key=lambda c: (rank(c), id_num(c["id"])))


def id_num(iid):
    mm = re.search(r"(\d+)$", iid)
    return int(mm.group(1)) if mm else 0


def cause_chain_html(m):
    """The contributing factors as one chain, trigger first, each with the actions that answer it. Certainty is shown only
    where a factor carries it; the store holds none by default, and none is guessed."""
    cfs = _factors(m)
    acts = {c["id"]: m.into(c["id"], "serves", "action") for c in cfs}
    bare = [c["id"] for c in cfs if not acts[c["id"]]]
    head = (f'{len(bare)} of {len(cfs)} factors that let this happen {"has" if len(bare) == 1 else "have"} no action yet: {" ".join(bare)}.'
            if bare else f'Every one of the {len(cfs)} factors that let this happen has an action.')
    rows = "".join(
        f'<li class="cc" id="{c["id"]}"><span class="role">{html.escape(FACTOR_WORDS.get((c.get("fields") or {}).get("factor"), "Factor"))}</span>'
        f'<div class="cc-body"><p class="pk"><span class="id">{c["id"]}</span>'
        + (f'<span class="chip c-{CERTAINTY_TONE.get(cert, "unchecked")}">{html.escape(cert)}</span>' if (cert := (c.get("fields") or {}).get("certainty")) else "")
        + (f'<span class="muted small">answered by {ids(acts[c["id"]])}</span>' if acts[c["id"]] else '<span class="chip c-open">no action</span>')
        + f'</p><b>{inline(c.get("title", ""))}</b></div></li>' for c in cfs)
    return insights_html([("bottleneck" if bare else "ok", head)]) + f'<ol class="cchain">{rows}</ol>'


# Diagrams the renderer draws itself, from a figure block's form and elements; a drawing from the elements replaces any
# hand-drawn svg the block also carries, so a stale drawing never shows. Marks take the accent for added, the unsettled tone
# for changed, dashed and quiet for removed, each also written as a word on the element.
MARK_WORD = {"added": "new", "changed": "changed", "removed": "removed"}
CH = 7.2  # a 12px label's width per character: the adapter's geometry check counts 0.6 of the font size


def _fit(text, room, px=12):
    n = max(int(room // (.6 * px + (.6 if px > 12 else 0))), 4)
    return text if len(text) <= n else text[:n - 1] + "…"


def _tip(text):
    """An element's full label, kept as its tooltip, so a label cut to fit never loses its words."""
    return f'<title>{html.escape(text)}</title>' if text else ""


def _marked(e):
    mk = e.get("mark")
    return (f' mk-{mk}' if mk in MARK_WORD else ""), (f' · {MARK_WORD[mk]}' if mk in MARK_WORD else "")


def sequence_svg(fig):
    parts, msgs = fig.get("participants") or [], fig.get("messages") or []
    pid = lambda p: p.get("id") if isinstance(p, dict) else str(p)
    plabel = lambda p: (p.get("label") or p.get("id")) if isinstance(p, dict) else str(p)
    col = {pid(p): k for k, p in enumerate(parts)}
    # too small to be a sequence, or a message naming no participant: left to the hand-drawn path, or listed (block_html)
    if len(parts) < 2 or not msgs or None in col or any(ms.get("from") not in col or ms.get("to") not in col for ms in msgs):
        return ""
    W, top, step = 230, 64, 40
    x = lambda k: 20 + W / 2 + k * W
    width, height = 40 + len(parts) * W, top + len(msgs) * step + 24
    out = [f'<svg class="sq" role="img" viewBox="0 0 {width} {height}" width="{width}" height="{height}"><title>{html.escape(fig.get("caption", ""))}</title>'
           f'<desc>{html.escape(fig.get("finding", fig.get("caption", "")))}</desc>']
    for k, p in enumerate(parts):
        cls, word = _marked(p) if isinstance(p, dict) else ("", "")
        out.append(f'<g class="pt{cls}">{_tip(plabel(p) + word)}<rect x="{x(k) - 80}" y="8" width="160" height="34" rx="8"/><text x="{x(k)}" y="30" text-anchor="middle">{html.escape(_fit(plabel(p) + word, 150, 13))}</text>'
                   f'<line class="ll" x1="{x(k)}" y1="42" x2="{x(k)}" y2="{height - 8}"/></g>')
    for n, ms in enumerate(msgs):
        y = top + n * step + 14
        a, b = col[ms["from"]], col[ms["to"]]
        cls, word = _marked(ms)
        kind = ms.get("kind") or "call"
        label = (ms.get("label") or "") + word
        if kind == "note":
            lo, hi = min(a, b), max(a, b)
            out.append(f'<g class="note{cls}">{_tip(label)}<rect x="{x(lo) - 70}" y="{y - 18}" width="{x(hi) - x(lo) + 140}" height="26" rx="5"/>'
                       f'<text x="{(x(lo) + x(hi)) / 2}" y="{y}" text-anchor="middle">{html.escape(_fit(label, x(hi) - x(lo) + 130))}</text></g>')
            continue
        dash = ' stroke-dasharray="5 4"' if kind == "reply" else ""
        if a == b:
            out.append(f'<g class="msg {kind}{cls}">{_tip(label)}<path d="M{x(a)},{y - 8} h34 v16 h-34"{dash} fill="none"/><polygon points="{x(a)},{y + 8} {x(a) + 8},{y + 4} {x(a) + 8},{y + 12}"/>'
                       f'<text x="{x(a) + 42}" y="{y + 4}">{html.escape(_fit(label, W - 20))}</text></g>')
            continue
        d = 1 if b > a else -1
        x1, x2 = x(a), x(b) - d * 2
        head = f'{x2},{y} {x2 - d * 9},{y - 5} {x2 - d * 9},{y + 5}' if kind != "async" else f'{x2 - d * 9},{y - 5} {x2},{y} {x2 - d * 9},{y + 5}'
        out.append(f'<g class="msg {kind}{cls}">{_tip(label)}<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}"{dash}/>'
                   + (f'<polygon points="{head}"/>' if kind != "async" else f'<polyline points="{head}" fill="none"/>')
                   + f'<text x="{(x1 + x2) / 2}" y="{y - 6}" text-anchor="middle">{html.escape(_fit(label, abs(x2 - x1) - 12))}</text></g>')
    return "".join(out) + "</svg>"


def state_parts(fig):
    """A state diagram's states and moves. A terminal state is one no move leaves; a move into the diagram's end, its final
    pseudo-state, doesn't count, since it only says the thing stops there."""
    nodes, edges = fig.get("nodes") or [], fig.get("edges") or []
    finals = {n["id"] for n in nodes if pseudo_kind(n) == "final"}
    states = [n for n in nodes if not pseudo_kind(n)]
    leaves = {e.get("from") for e in edges if e.get("to") not in finals}
    terminal = [n["id"] for n in states if n["id"] not in leaves]
    return states, edges, terminal


def pseudo_kind(n):
    """"initial" or "final" for a state diagram's start or end, by kind, or by id as the portable tree names them
    (`initial`, `final`, or `<group>-initial` inside a group); else None."""
    i = str(n.get("id") or "")
    for k in ("initial", "final"):
        if n.get("kind") == k or i == k or i.endswith("-" + k):
            return k
    return None


def state_svg(fig):
    nodes, edges = fig.get("nodes") or [], fig.get("edges") or []
    states, _, terminal = state_parts(fig)
    ids_ = [n.get("id") for n in nodes]
    # composite states, too few states or moves, or a move naming no state: left to the hand-drawn path, or listed
    if fig.get("groups") or len(states) < 2 or not edges or None in ids_ or any(e.get("from") not in ids_ or e.get("to") not in ids_ for e in edges):
        return ""
    out_of = {}
    for e in edges:
        out_of.setdefault(e.get("from"), []).append(e.get("to"))
    starts = [n["id"] for n in nodes if pseudo_kind(n) == "initial"] or [ids_[0]]
    depth, queue = {s: 0 for s in starts}, list(starts)
    while queue:
        cur = queue.pop(0)
        for nx in out_of.get(cur, []):
            if nx in ids_ and nx not in depth:
                depth[nx] = depth[cur] + 1
                queue.append(nx)
    for i in ids_:
        depth.setdefault(i, max(depth.values(), default=0) + 1)
    cols = {}
    for i in ids_:
        cols.setdefault(depth[i], []).append(i)
    by = {n["id"]: n for n in nodes}
    small = lambda i: bool(pseudo_kind(by[i]))
    wide = lambda i: 18 if small(i) else min(max(96, CH * len((by[i].get("label") or i) + _marked(by[i])[1]) + 30), 200)
    CW, RH = 230, 74
    back = any(e.get("from") in depth and e.get("to") in depth and depth[e["to"]] <= depth[e["from"]] for e in edges)
    top = 96 if back else 40  # room above the states for a move that runs back, its curve and its label
    pos = {i: (40 + d * CW, top + r * RH) for d, col in cols.items() for r, i in enumerate(col)}
    width = 80 + max(cols) * CW + 200
    height = top + 10 + max(len(c) for c in cols.values()) * RH
    out = [f'<svg class="stm" role="img" viewBox="0 0 {width} {height}" width="{width}" height="{height}"><title>{html.escape(fig.get("caption", ""))}</title>'
           f'<desc>{html.escape(fig.get("finding", fig.get("caption", "")))}</desc>']
    for e in edges:
        a, b = e.get("from"), e.get("to")
        (ax, ay), (bx, by_) = pos[a], pos[b]
        cls, word = _marked(e)
        sx, ex = ax + wide(a) / 2, bx - wide(b) / 2 - 3
        if bx > ax:
            path, lx, ly = f'M{sx},{ay} C{(sx + ex) / 2},{ay} {(sx + ex) / 2},{by_} {ex},{by_}', (sx + ex) / 2, (ay + by_) / 2 - 6
            tip = f'{ex},{by_} {ex - 9},{by_ - 5} {ex - 9},{by_ + 5}'
        else:
            lift = min(34 + abs(ay - by_) / 3, 60)
            sx2, ex2 = ax, bx
            path = f'M{sx2},{ay - 15} C{sx2},{ay - 15 - lift} {ex2},{by_ - 15 - lift} {ex2},{by_ - 17}'
            lx, ly = (sx2 + ex2) / 2, min(ay, by_) - 25 - lift * .75
            tip = f'{ex2},{by_ - 15} {ex2 - 5},{by_ - 24} {ex2 + 5},{by_ - 24}'
        label = (e.get("label") or "") + word
        out.append(f'<g class="mv{cls}">{_tip(label)}<path d="{path}" fill="none"/><polygon points="{tip}"/>'
                   + (f'<text x="{lx}" y="{ly}" text-anchor="middle">{html.escape(_fit(label, CW - 40))}</text>' if label else "") + '</g>')
    for i, (cx, cy) in pos.items():
        n = by[i]
        if small(i):
            fin = pseudo_kind(n) == "final"
            out.append(f'<g class="pseudo"><circle cx="{cx}" cy="{cy}" r="8"/>' + (f'<circle class="ring" cx="{cx}" cy="{cy}" r="12"/>' if fin else "") + '</g>')
            continue
        cls, word = _marked(n)
        term = " terminal" if i in terminal else ""
        w = wide(i)
        out.append(f'<g class="st{cls}{term}">{_tip((n.get("label") or i) + word)}<rect x="{cx - w / 2}" y="{cy - 15}" width="{w}" height="30" rx="15"/>'
                   + (f'<rect class="ring" x="{cx - w / 2 - 4}" y="{cy - 19}" width="{w + 8}" height="38" rx="19"/>' if term else "")
                   + f'<text x="{cx}" y="{cy + 4}" text-anchor="middle">{html.escape(_fit((n.get("label") or i) + word, w - 16))}</text></g>')
    return "".join(out) + "</svg>"


DRAWN = {"sequence": sequence_svg, "state": state_svg}
FIGS = {}  # each reader tab's diagram blocks that carry their form and elements, by tab label, gathered before the tabs split


def _figures(blocks):
    for b in blocks or []:
        if "figure" in b and b["figure"].get("form") in DRAWN:
            yield b["figure"]
        for k in ("blocks", "sections"):
            yield from _figures(b.get(k))


_split_tabs_before_ws2 = split_tabs


def split_tabs(pages):
    for p in pages:
        if p.get("part") in ("now", "plan"):
            FIGS.setdefault(p.get("label") or "", []).extend(f for s in p.get("sections", []) for f in _figures(s.get("blocks")))
    return _split_tabs_before_ws2(pages)


_block_html_before_ws2 = block_html


def block_html(b, views, opts):
    f = b.get("figure")
    if f and f.get("form") in DRAWN:
        drawn = DRAWN[f["form"]](f)
        if drawn:
            b = dict(b, figure=dict(f, svg=drawn))
        elif not f.get("svg"):  # one the renderer can't draw and nobody drew degrades to its elements, never an empty frame
            b = dict(b, figure=dict(f, svg=_elements_html(f)))
    return _block_html_before_ws2(b, views, opts)


def _elements_html(f):
    say = lambda e: html.escape(str((e.get("label") or e.get("id") or "") if isinstance(e, dict) else e) + (_marked(e)[1] if isinstance(e, dict) else ""))
    verb = lambda e: html.escape((e.get("label") or "") + _marked(e)[1]) or "moves to"
    if f.get("form") == "sequence":
        rows = [say(p) for p in f.get("participants") or []] + [f'{html.escape(str(ms.get("from")))} → {html.escape(str(ms.get("to")))}: {verb(ms)}' for ms in f.get("messages") or []]
    else:
        rows = [say(n) for n in f.get("nodes") or [] if not pseudo_kind(n)] + [f'{html.escape(str(e.get("from")))} → {html.escape(str(e.get("to")))}: {verb(e)}' for e in f.get("edges") or []]
    return '<ul class="prose">' + "".join(f"<li>{r}</li>" for r in rows) + '</ul>' 


def tab_figures(form):
    return [f for f in FIGS.get(CUR_LABEL[0], []) if f.get("form") == form and DRAWN[form](f)]


def _marks_in(f, keys):
    return [e for k in keys for e in (f.get(k) or []) if isinstance(e, dict) and e.get("mark") in ("added", "changed")]


def _fig_html(f):
    return (f'<figure data-block="diagram"><figcaption>{inline(f.get("caption", ""))}</figcaption><div class="fig">{DRAWN[f["form"]](f)}</div>'
            + "".join(f'<p class="figline">{inline(x)}</p>' for x in (f.get("lines") or []) if isinstance(x, str)) + '</figure>')


MARK_KEY = ('<div class="legend"><span><i class="kmk mk-added"></i> new in this change</span><span><i class="kmk mk-changed"></i> changed</span>'
            '<span><i class="kmk mk-removed"></i> removed</span></div>')


def sequence_html(m):
    figs = tab_figures("sequence")
    steps = [ms for f in figs for ms in f.get("messages") or [] if ms.get("kind") != "note"]
    new = sum(1 for ms in steps if ms.get("mark") == "added")
    chg = sum(1 for ms in steps if ms.get("mark") == "changed")
    parts = len({(p.get("id") if isinstance(p, dict) else p) for f in figs for p in f.get("participants") or []})
    said = [w for w in (f"{new} added" if new else "", f"{chg} changed" if chg else "") if w]
    head = (f'{len(figs)} flow{"s" if len(figs) != 1 else ""}: {len(steps)} steps across {parts} parts'
            + (f', {" and ".join(said)} by this change.' if said else '; no step is marked as changed.'))
    return insights_html([("next", head)]) + "".join(_fig_html(f) for f in figs) + MARK_KEY


def states_html(m):
    figs = tab_figures("state")
    parts = [state_parts(f) for f in figs]
    n = sum(len(s) for s, _, _ in parts)
    few = lambda xs: ", ".join(xs[:4]) + ("…" if len(xs) > 4 else "")
    new = [(n_.get("label") or n_["id"]) for s, _, _ in parts for n_ in s if n_.get("mark") == "added"]
    chg = [(n_.get("label") or n_["id"]) for s, _, _ in parts for n_ in s if n_.get("mark") == "changed"]
    moved = sum(1 for f in figs for e in f.get("edges") or [] if e.get("mark") in ("added", "changed"))
    ends = [(next((x.get("label") for x in s if x["id"] == t), t) or t) for s, _, term in parts for t in term]
    head = (f'{n} states' + (f', {len(new)} new ({few(new)})' if new else '') + (f', {len(chg)} changed ({few(chg)})' if chg else '')
            + (f', {moved} moves new or changed' if moved else '') + '; '
            + (f'it ends in {" or ".join(ends[:4])}{"…" if len(ends) > 4 else ""}.' if ends else 'every state can move on; none is final.'))
    return (insights_html([("next", head)]) + "".join(_fig_html(f) for f in figs)
            + MARK_KEY.replace('</div>', '<span><i class="kmk terminal"></i> terminal: no move leaves it but to the end</span></div>', 1))


WS2_BODIES.update({"incident-timeline": incident_timeline_html, "cause-chain": cause_chain_html, "sequence": sequence_html, "states": states_html})

VISUALS["incident-timeline"] = {
    "body": "incident-timeline", "of": ("status",), "label": "Timeline",
    "needs": lambda m: bool(m) and "detection" in incident_events(m)[1] and any(p in incident_events(m)[1] for p in ("mitigation", "resolution")),
    "wins": lambda m: bool(m) and bool(m.kind("outcome")),
    "why": "the set records an incident, so how long it took to find, contain and fix comes first"}
VISUALS["cause-chain"] = {
    "body": "cause-chain", "of": ("status",), "label": "Cause chain",
    "needs": lambda m: bool(m) and len(m.kind("contributing factor")) >= 2,
    "wins": lambda m: bool(m) and any(not m.into(c["id"], "serves", "action") for c in m.kind("contributing factor")),
    "why": "a factor that let the incident happen has no action yet"}
VISUALS["design-sequence"] = {
    "body": "sequence", "of": ("design",), "label": "Sequence",
    "needs": lambda m: bool(tab_figures("sequence")),
    "wins": lambda m: any(_marks_in(f, ("participants", "messages")) for f in tab_figures("sequence")),
    "why": "this change adds or changes steps in a flow, so the flow comes first with them marked"}
VISUALS["design-states"] = {
    "body": "states", "of": ("design", "data"), "label": "States",
    "needs": lambda m: bool(tab_figures("state")),
    "wins": lambda m: any(_marks_in(f, ("nodes", "edges")) for f in tab_figures("state")),
    "why": "this change adds or changes states or moves, so the states come first with them marked"}
VISUALS["design-slices"] = {"body": "design", "label": "Slices", "needs": lambda m: True, "wins": lambda m: True,
                            "why": "no diagram marks a change and no scored decision is open, so the slices come first"}
VISUALS["data-chips"] = {"body": "data", "label": "Data", "needs": lambda m: True, "wins": lambda m: True,
                         "why": "no diagram on this tab marks a change, so what is processed and kept comes first"}


# Review rounds: each round's verdict, one per review record, with its standing findings by grade as counted when it was
# filed, so a clean round counts as zero and a finding withdrawn in its own round never counts.
KIND_WORDS.update({"FND": "Finding", "ASK": "Question for the author", "VRD": "Verdict", "COV": "Coverage reading"})
ID_PAT = re.compile(r"\b(" + "|".join(sorted(KIND_WORDS, key=len, reverse=True)) + r")-(\d+)\b")
GRADES = ("critical", "high", "medium", "low", "info")
GRADE_TONE = {"critical": "open", "high": "open", "medium": "unsettled", "low": "quiet", "info": "quiet"}


def _ws2_num(v):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None


def review_rounds(m):
    """Round number -> its verdict's counts by grade, in round order; a verdict without a readable round is left out."""
    out = {}
    # the verdict of a round's review record filed last stands for the round
    for v in sorted(m.kind("verdict"), key=lambda v: (str(v.get("first_filed") or ""), id_num(v["id"]))):
        f = v.get("fields") or {}
        r = _ws2_num(f.get("round"))
        if r is not None:
            out[r] = dict({g: _ws2_num(f.get(g)) or 0 for g in GRADES}, id=v["id"])
    return dict(sorted(out.items()))


def _total(g):
    return sum(g[k] for k in GRADES)


def review_converging(m):
    rr = list(review_rounds(m).values())
    block = lambda g: g["critical"] + g["high"]
    return len(rr) < 2 or (_total(rr[-1]) < _total(rr[-2]) and block(rr[-1]) <= block(rr[-2]))


def review_rounds_html(m):
    rounds = list(review_rounds(m).items())
    (pn, pg), (ln, lg) = rounds[-2:]
    pt, lt = _total(pg), _total(lg)
    if review_converging(m):
        head, kind = f'The review is converging: round {ln} found {lt} standing findings, down from {pt} in round {pn}.', "ok"
    else:
        rose = next((g for g in GRADES if lg[g] > pg[g]), None) or next((g for g in GRADES if lg[g] and lg[g] == pg[g]), None)
        head = (f"The review isn't converging: round {ln} found {lt} standing findings to round {pn}'s {pt}"
                + (f"; {rose} findings went from {pg[rose]} to {lg[rose]}." if rose and lg[rose] > pg[rose] else
                   f"; {lg[rose]} {rose} still stand." if rose else "."))
        kind = "bottleneck"
    top = max(_total(g) for _, g in rounds) or 1
    rows = "".join(
        f'<li id="{g["id"]}"><span class="rr-n">Round {n} <span class="id">{g["id"]}</span></span><div class="rr-bar">'
        + "".join(f'<span class="rr-{GRADE_TONE[k]}" style="width:{100 * g[k] / top:.2f}%" title="{g[k]} {k}"></span>' for k in GRADES if g[k])
        + f'</div><span class="rr-c">{_total(g)}</span><span class="muted small">{" · ".join(f"{g[k]} {k}" for k in GRADES if g[k]) or "no findings"}</span></li>'
        for n, g in rounds)
    key = ('<div class="legend"><span><i class="kseg rr-open"></i> critical or high</span><span><i class="kseg rr-unsettled"></i> medium</span>'
           '<span><i class="kseg rr-quiet"></i> low or info</span></div>')
    return insights_html([(kind, head)]) + f'<ol class="rrounds">{rows}</ol>' + key


WS2_BODIES["review-rounds"] = review_rounds_html
VISUALS["review-rounds"] = {
    "body": "review-rounds", "of": ("status",), "label": "Review rounds",
    "needs": lambda m: bool(m) and len(review_rounds(m)) >= 2,
    "wins": lambda m: bool(m) and not review_converging(m),
    "why": "the latest review round found no fewer standing findings than the one before, or more that block a merge, so the review isn't converging"}


# Change footprint: how much of the change's new lines each area's tests ran, from the test plan's coverage readings, a
# later reading of an area superseding the earlier. A diagnostic: it locates untested code and sets no verdict.
def footprint(m):
    rows = {}
    for c in m.kind("coverage reading"):
        f = c.get("fields") or {}
        rows[f.get("area") or "(all)"] = {"id": c["id"], "new": _ws2_num(f.get("new lines")), "run": _ws2_num(f.get("run")),
                                          "at": f.get("at") or "", "why": f.get("not measured") or "",
                                          "part": f.get("scope") == "part of the suite"}
    return rows


def _measured(r):
    return not r["why"] and r["new"] is not None and r["run"] is not None and r["new"] > 0


def change_footprint_html(m):
    rows = footprint(m)
    meas = sorted(((a, r) for a, r in rows.items() if _measured(r)), key=lambda x: (x[1]["run"] / x[1]["new"], -x[1]["new"]))
    new, run = sum(r["new"] for _, r in meas), sum(r["run"] for _, r in meas)
    # a reading from part of the suite is a floor: under half there is unclear, never a gap on its own
    low = [a for a, r in meas if r["run"] * 2 < r["new"] and not r["part"]]
    unclear = [a for a, r in meas if r["run"] * 2 < r["new"] and r["part"]]
    floor = "at least " if any(r["part"] for _, r in meas) else ""
    head = (f'The tests run {floor}{run} of {new} new lines'
            + (f'; {" and ".join(low[:2])}{"…" if len(low) > 2 else ""} run{"s" if len(low) == 1 else ""} under half.' if low else
               f'; {len(unclear)} area{"s are" if len(unclear) != 1 else " is"} unclear.' if unclear else '; every area runs at least half.'))
    top = max(r["new"] for _, r in meas)
    out = []
    for a, r in meas:
        w, f_ = 100 * r["new"] / top, 100 * r["run"] / r["new"]
        out.append(f'<li id="{r["id"]}"><span class="fp-a">{html.escape(a)} <span class="id">{r["id"]}</span></span><div class="fp-track"><div class="fp-bar{" low" if a in low else ""}" style="width:{w:.2f}%">'
                   f'<span style="width:{f_:.2f}%"></span></div></div><span class="fp-n">{r["run"]} / {r["new"]}</span>'
                   + ('<span class="chip c-open">under half run</span>' if a in low else '<span class="chip c-unsettled">unclear</span>' if a in unclear
                      else f'<span class="muted small">{"at least " if r["part"] else ""}{round(f_)}%</span>')
                   + ('<span class="muted small fp-part">from a run of part of the suite</span>' if r["part"] else "") + '</li>')
    out += [f'<li id="{r["id"]}" class="fp-none"><span class="fp-a">{html.escape(a)} <span class="id">{r["id"]}</span></span><span class="muted small">not measured: {inline(r["why"] or "no reading")}</span></li>'
            for a, r in rows.items() if not _measured(r)]
    ats = sorted({r["at"] for _, r in meas if r["at"]})
    key = ('<div class="legend"><span><i class="kseg fp-run"></i> new lines the tests run</span><span><i class="kseg fp-unrun"></i> new lines they don\'t</span>'
           f'<span class="muted">bar length: how many new lines the area holds{" · at " + ", ".join(ats) if ats else ""}</span></div>')
    return insights_html([("ask" if low or unclear else "ok", head)]) + f'<ol class="fprint">{"".join(out)}</ol>' + key


WS2_BODIES["change-footprint"] = change_footprint_html
VISUALS["change-footprint"] = {
    "body": "change-footprint", "of": ("trace",), "label": "Footprint",
    "needs": lambda m: bool(m) and any(_measured(r) for r in footprint(m).values()),
    "wins": lambda m: bool(m) and any(_measured(r) and not r["part"] and r["run"] * 2 < r["new"] for r in footprint(m).values()),
    "why": "the tests run under half the new lines of some part of the change, so where comes first"}
VISUALS["trace-graph"] = {"body": "trace", "label": "Trace", "needs": lambda m: bool(m) and bool(m.kind("requirement")), "wins": lambda m: True,
                          "why": "the trace from work to requirement and its checks is the tab's own view"}



# Assumption grid: the open assumptions placed by how sure the work is of each and what it would cost if wrong, as the
# raid log grades them; the corner of low confidence and high cost is where a validation is owed first.
LEVELS = ("high", "medium", "low")


def open_assumptions(m):
    return [a for a in m.kind("assumption") if (a.get("fields") or {}).get("status") == "open"]


def _graded(a):
    f = a.get("fields") or {}
    return f.get("confidence") in LEVELS and f.get("cost if wrong") in LEVELS


def assumption_grid_html(m):
    asm = open_assumptions(m)
    graded = [a for a in asm if _graded(a)]
    g = lambda a, k: (a.get("fields") or {}).get(k)
    worst = [a["id"] for a in graded if g(a, "confidence") == "low" and g(a, "cost if wrong") == "high"]
    head = (f'{len(worst)} open assumption{"s are" if len(worst) != 1 else " is"} a costly guess: {" ".join(worst)}.'
            if worst else f'No open assumption is a costly guess; {len(graded)} are graded.')
    # cost first, as plan ranks the riskiest: a costly guess is red, a costly or middling assumption not yet shown is amber;
    # one the code or data already shows owes no validation first, whatever its cost
    tone = {("low", "high"): "act", ("medium", "high"): "watch", ("low", "medium"): "watch"}
    cells = []
    for conf in ("low", "medium", "high"):
        cells.append(f'<span class="ag-row">{conf} confidence</span>')
        for cost in ("low", "medium", "high"):
            here = [a for a in graded if g(a, "confidence") == conf and g(a, "cost if wrong") == cost]
            chips = "".join(f'<span class="id" title="{html.escape(a.get("title", ""))}">{a["id"]}</span>' for a in here)
            cells.append(f'<div class="ag-cell ag-{tone.get((conf, cost), "plain")}">{chips}</div>')
    ungraded = [a["id"] for a in asm if not _graded(a)]
    return (insights_html([("bottleneck" if worst else "ok", head)])
            + '<div class="agrid"><span></span>' + "".join(f'<span class="ag-col">{c} cost if wrong</span>' for c in ("low", "medium", "high"))
            + "".join(cells) + '</div>'
            + (f'<p class="muted small">Not yet graded: {" ".join(ungraded)}</p>' if ungraded else ""))


WS2_BODIES["assumption-grid"] = assumption_grid_html
VISUALS["assumption-grid"] = {
    "body": "assumption-grid", "of": ("raid",), "label": "Assumptions",
    "needs": lambda m: bool(m) and any(_graded(a) for a in open_assumptions(m)),
    "wins": lambda m: bool(m) and any(_graded(a) and (a.get("fields") or {}).get("confidence") == "low"
                                      and (a.get("fields") or {}).get("cost if wrong") == "high" for a in open_assumptions(m)),
    "why": "an open assumption is a guess the work can't afford to get wrong, so where each stands comes first"}
VISUALS["raid-board"] = {"body": "raid", "label": "RAID", "needs": lambda m: True, "wins": lambda m: True,
                         "why": "the log's risks, issues and dependencies by when each could hit are the tab's own view"}



# Before and after: each goal and guardrail metric's latest reading against its baseline, read by the direction it was
# meant to move; a metric with no baseline or no reading yet says so rather than draw a move.
def _f(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def metric_moves(m):
    out = []
    for x in m.kind("metric"):
        f = x.get("fields") or {}
        if f.get("role") not in ("goal", "guardrail"):
            continue
        base, val, tol = _f(f.get("baseline")), _f(f.get("value")), _f(f.get("tolerance"))
        d = f.get("direction")
        why = ("no baseline yet" if base is None else "no reading yet" if val is None else "no direction" if d not in ("up", "down", "hold")
               else "no tolerance" if d == "hold" and tol is None else "")
        if why:
            out.append({"m": x, "move": "unread", "base": base, "val": val, "why": why})
            continue
        if d == "hold":
            move = "held" if abs(val - base) <= tol else "broke"
        else:
            delta = (val - base) * (1 if d == "up" else -1)
            # any move counts, the gate's go-when judging its size; a guardrail that hasn't moved has held
            move = "toward" if delta > 0 else "away" if delta < 0 else "held" if f.get("role") == "guardrail" else "flat"
        out.append({"m": x, "move": move, "base": base, "val": val, "why": ""})
    return out


MOVE_WORD = {"toward": ("moved as meant", "holds"), "held": ("held", "holds"), "flat": ("hasn't moved", "unsettled"),
             "away": ("moved the wrong way", "open"), "broke": ("left its tolerance", "open"), "unread": ("no reading yet", "unchecked")}


def _fmt(v):
    return "–" if v is None or v != v or v in (float("inf"), float("-inf")) else (str(int(v)) if v == int(v) else f"{v:g}")


def before_after_html(m):
    mv = metric_moves(m)
    bad = [r["m"]["id"] for r in mv if r["move"] in ("away", "broke")]
    read = [r for r in mv if r["move"] != "unread"]
    good = sum(1 for r in read if r["move"] in ("toward", "held"))
    head = (f'{len(bad)} metric{"s" if len(bad) != 1 else ""} moved the wrong way: {" ".join(bad)}.' if bad
            else f'{good} of {len(read)} read metrics moved as meant.' if read else 'No metric has a reading since its baseline yet.')
    rows = []
    for r in mv:
        f, (word, tone) = r["m"].get("fields") or {}, MOVE_WORD[r["move"]]
        word = r["why"] or word
        arrow = {"up": "↑", "down": "↓", "hold": "↔"}.get(f.get("direction"), "")
        rows.append(f'<li id="{r["m"]["id"]}"><span class="ba-t"><span class="id">{r["m"]["id"]}</span> {inline(r["m"].get("title", ""))}'
                    f'<span class="muted small">{html.escape(f.get("role", ""))} · meant {arrow} · target {_fmt(_f(f.get("target")))}</span></span>'
                    f'<span class="ba-n">{_fmt(r["base"])}<i>→</i><b>{_fmt(r["val"])}</b></span><span class="chip c-{tone}">{word}</span></li>')
    return insights_html([("bottleneck" if bad else "ok" if read else "next", head)]) + f'<ol class="bafter">{"".join(rows)}</ol>'


WS2_BODIES["before-after"] = before_after_html
VISUALS["before-after"] = {
    "body": "before-after", "of": ("cutover",), "label": "Before and after",
    "needs": lambda m: bool(m) and any(r["move"] != "unread" for r in metric_moves(m)),
    "wins": lambda m: bool(m) and any(r["move"] in ("away", "broke") for r in metric_moves(m)),
    "why": "a goal or guardrail metric moved the wrong way since its baseline, so the moves come first"}



# Option scoring: a decision's options on plan's approach scale, from its `scores` lines; a failed MUST rules an option out
# whatever else it scores, and the axes read in plan's priority order.
AXES = (("fit", ("strong", "partial", "poor")), ("cost", ("low", "moderate", "high")), ("reversibility", ("two-way", "partial", "one-way")),
        ("blast", ("contained", "bounded", "wide")), ("operability", ("turnkey", "standard", "demanding")))
# colour only where a reader must act (design-reader-instruments, point 2): a failed MUST and a one-way door are red;
# every other rung is a settled grade and stays plain, the chosen row standing out by weight
RUNG_ACT = {"one-way"}


def parse_scores(d):
    """Each `scores` line as a row; a line the form doesn't fit stays a row that says so, never dropped."""
    rows = []
    for line in (d.get("fields") or {}).get("scores") or []:
        name, sep, rest = re.sub(r"\s+(?:—|--?)\s+", " — ", str(line), count=1).partition(" — ")
        rest = rest.strip().lower()
        if not sep or not name.strip():
            rows.append({"name": str(line)[:40], "bad": True})
            continue
        if rest.startswith("fails"):
            rows.append({"name": name.strip(), "fails": rest[5:].strip() or "a MUST not named"})
            continue
        got = {}
        for part in re.split(r"\s*[·,;]\s*", rest):
            words = part.replace(" door", "").replace("blast radius", "blast").split(" ", 1)
            if len(words) == 2:
                got[words[0]] = words[1].strip()
        rungs = {ax: got.get(ax) for ax, _ in AXES}
        if all(rungs[ax] in levels for ax, levels in AXES):
            rows.append({"name": name.strip(), "rungs": rungs})
        else:
            rows.append({"name": name.strip(), "bad": True})
    return rows


def scored_decisions(m):
    return [(d, r) for d in m.kind("decision") for r in [parse_scores(d)] if len(r) >= 2]


def option_scoring_html(m):
    decs = scored_decisions(m)
    out, heads = [], []
    for d, rows in decs:
        chosen = (d.get("fields") or {}).get("chosen") or (d.get("fields") or {}).get("lean") or ""
        # the scored option whose name `chosen` names, the longest such name when one holds another; never one that failed a MUST
        hits = [r["name"] for r in rows if "rungs" in r and r["name"].lower() in chosen.lower()]
        pick = max(hits, key=len) if hits else None
        failed = [r["name"] for r in rows if "fails" in r]
        heads.append((pick, failed, d))
        head_row = '<span></span>' + "".join(f'<span class="os-ax">{ax}</span>' for ax, _ in AXES)
        body = ""
        for r in rows:
            cls = " chosen" if r["name"] == pick else ""
            if r.get("bad"):
                body += f'<span class="os-n">{inline(r["name"])}</span><span class="os-fail os-bad">its scores line doesn\'t fit the form</span>'
            elif "fails" in r:
                body += f'<span class="os-n{cls}">{inline(r["name"])}</span><span class="os-fail">fails {inline(r["fails"])}</span>'
            else:
                body += f'<span class="os-n{cls}">{inline(r["name"])}{" · chosen" if cls else ""}</span>' + "".join(
                    f'<span class="os-c{" c-open" if r["rungs"][ax] in RUNG_ACT else ""}">{html.escape(r["rungs"][ax])}</span>' for ax, levels in AXES)
        out.append(f'<section class="osc" id="{d["id"]}-scores"><h3 class="sub"><span class="id">{d["id"]}</span> {inline(d.get("title", ""))}</h3>'
                   f'<div class="ogrid">{head_row}{body}</div></section>')
    # lead with a decision still open, the one that makes this view win, else the first
    pick, failed, d = next((h for h in heads if h[2].get("state") in ("open", "lean", "proposed")), heads[0])
    verb = "won" if d.get("state") in ("agreed", "recorded") else "leads"
    head = (f'{pick} {verb} {d["id"]} on the approach scale' if pick else f'{d["id"]} names no scored option as chosen')
    head += (f"; {len(failed)} option{'s' if len(failed) != 1 else ''} failed a MUST." if failed else ".")
    if len(heads) > 1:
        head = f'{len(heads)} decisions were weighed on the approach scale; ' + head[0].lower() + head[1:]
    key = ('<div class="legend"><span><i class="kseg rr-open"></i> a failed MUST or a one-way door</span>'
           '<span class="muted">axes in plan\'s priority order, best rung first</span></div>')
    return insights_html([("next", head)]) + "".join(out) + key


WS2_BODIES["option-scoring"] = option_scoring_html
VISUALS["option-scoring"] = {
    "body": "option-scoring", "of": ("design", "adrs"), "label": "Options",
    "needs": lambda m: bool(m) and bool(scored_decisions(m)),
    "wins": lambda m: bool(m) and any(d.get("state") in ("open", "lean", "proposed") for d, _ in scored_decisions(m)),
    "why": "a decision weighed on the approach scale is still open, so how its options scored comes first"}
VISUALS["adr-records"] = {"body": "adrs", "label": "Records", "needs": lambda m: True, "wins": lambda m: True,
                          "why": "the decision records are the tab's own view"}



# Reach rings: how far a fixed bug's cause reaches, from the task record's reach items: its callers on the inner ring,
# the entry points and stores beyond them on the outer; an entry point anyone may call, or none tests, is red.
KIND_WORDS.update({"RCH": "Reach"})
ID_PAT = re.compile(r"\b(" + "|".join(sorted(KIND_WORDS, key=len, reverse=True)) + r")-(\d+)\b")


def reach_items(m):
    return [r for r in m.kind("reach") if (r.get("fields") or {}).get("ring") in ("caller", "entry point", "data", "input")]


def _still_wrong(f):
    c = str(f.get("count") or "").strip().lower()
    return f.get("ring") == "data" and not re.match(r"^0\b|^none\b", c)


def _reach_tone(r):
    """Red for data still wrong, a failure to repair; amber for an entry point no test runs; public is said, not coloured
    (design-reader-instruments, point 2)."""
    f = r.get("fields") or {}
    if _still_wrong(f):
        return "act"
    return "watch" if f.get("ring") == "entry point" and f.get("tested") in ("no", "unknown") else "plain"


def reach_rings_html(m):
    import math
    rs = reach_items(m)
    ring = lambda r: (r.get("fields") or {}).get("ring")
    entries = [r for r in rs if ring(r) == "entry point"]
    pub = [r for r in entries if (r.get("fields") or {}).get("who may call") == "public"]
    untested = [r for r in entries if (r.get("fields") or {}).get("tested") in ("no", "unknown")]
    wrong = [r for r in rs if _still_wrong(r.get("fields") or {})]
    head = (f'{len(entries)} entry point{"s reach" if len(entries) != 1 else " reaches"} the fault, {len(pub)} public'
            + (f'; {len(untested)} untested' if untested else '') + (f'; data still wrong in {len(wrong)}' if wrong else '') + '.')
    W, H, cx, cy = 720, 360, 360, 180
    out = [f'<svg class="rchmap" role="img" viewBox="0 0 {W} {H}"><title>How far the fault reaches</title><desc>{html.escape(head)}</desc>',
           f'<circle class="rch-ring" cx="{cx}" cy="{cy}" r="160"/><circle class="rch-ring" cx="{cx}" cy="{cy}" r="92"/>',
           f'<circle class="rch-core" cx="{cx}" cy="{cy}" r="34"/><text class="rch-core-t" x="{cx}" y="{cy + 4}" text-anchor="middle">the fault</text>']
    for k, (radius, group) in enumerate(((92, [r for r in rs if ring(r) == "caller"]), (160, [r for r in rs if ring(r) != "caller"]))):
        shown = group[:10]
        for n, r in enumerate(shown):
            a = -math.pi / 2 + (2 * math.pi * n / max(len(shown), 1)) + (k * .3)
            x, y = cx + radius * math.cos(a), cy + radius * .95 * math.sin(a)
            label = _fit(f'{r["id"]} {r.get("title", "")}', 150)
            w = min(len(label) * 6.6 + 16, 170)
            pubcls = " rch-pub" if (r.get("fields") or {}).get("who may call") == "public" else ""
            out.append(f'<g class="rch rch-{_reach_tone(r)}{pubcls}"><title>{html.escape(r.get("title", ""))}</title><rect x="{x - w / 2:.1f}" y="{y - 11:.1f}" width="{w:.1f}" height="22" rx="6"/>'
                       f'<text x="{x:.1f}" y="{y + 4:.1f}" text-anchor="middle">{html.escape(label)}</text></g>')
    out.append('</svg>')
    def facts(r):
        f = r.get("fields") or {}
        bits = [html.escape(ring(r))]
        if ring(r) == "entry point":
            bits.append(f'<b>{html.escape(f.get("who may call"))}</b>' if f.get("who may call") else "who may call not recorded")
            bits.append({"no": '<span class="chip c-unsettled">no test</span>', "unknown": '<span class="chip c-unsettled">test unknown</span>'}.get(f.get("tested"), "tested" if f.get("tested") == "yes" else "testing not recorded"))
        if ring(r) == "data":
            bits.append(f'<span class="chip c-open">{html.escape(str(f.get("count") or "not counted"))} still wrong</span>' if _still_wrong(f) else "repaired")
        return " · ".join(bits)
    rows = "".join(f'<li id="{r["id"]}"><span class="id">{r["id"]}</span><span>{inline(r.get("title", ""))}</span><span class="muted small">{facts(r)}</span></li>' for r in rs)
    key = ('<div class="legend"><span>inner ring: callers</span><span>outer ring: entry points, data and inputs</span>'
           '<span><i class="kseg ag-act"></i> data still wrong</span><span><i class="kseg ag-watch"></i> entry point no test runs</span><span><b>bold</b>: public</span></div>')
    return insights_html([("bottleneck" if wrong else "ask" if untested else "ok", head)]) + f'<div class="fig">{"".join(out)}</div>' + key + f'<ol class="reachl">{rows}</ol>'


WS2_BODIES["reach-rings"] = reach_rings_html
VISUALS["reach-rings"] = {
    "body": "reach-rings", "of": ("status",), "label": "Reach",
    "needs": lambda m: bool(m) and any((r.get("fields") or {}).get("ring") == "entry point" for r in reach_items(m)),
    "wins": lambda m: bool(m) and any(_reach_tone(r) != "plain" for r in reach_items(m)),
    "why": "data the fault reached is still wrong, or no test runs it through an entry point"}


_instrument_before_ws2 = _instrument_html


def _instrument_html(name, m, opts=None):
    return WS2_BODIES[name](m) if name in WS2_BODIES else _instrument_before_ws2(name, m, opts)
# --- end visuals: ws2 ---

# --- reading: ws1 ---
# The reading features (the artifacts skill's reading-features rule): every page carries one card per item, which hover
# previews, search and the printed brief read, so a page needs no fetch and works opened from disk.
def page_instrument(p):
    return next((b["instrument"] for sec in p.get("sections", []) for b in sec.get("blocks", []) if "instrument" in b), None)


READ_HOME = {"gate": "cutover"}


def travel_dates(m, i, settled):
    """The dates time travel reads, each ISO or empty: filed; then the day the item turned done by its kind's own event,
    as the map counts done: a question or decision first settled by an agreement, a piece of work merged, a gate's first
    run that held."""
    iso = lambda d: d.isoformat() if d else ""
    k = i.get("kind")
    agreed = min((_day(c.get("date")) for c in i.get("state_changes") or [] if c.get("state") in ("agreed", "recorded") and _day(c.get("date"))), default=None)
    if agreed and (settled.get(i["id"]) is None or agreed < settled[i["id"]]):
        settled = dict(settled, **{i["id"]: agreed})  # a dated change to agreed counts as settling, the earlier of the two
    ran = min((_day(e.get("when")) for e in i.get("evidence", []) if isinstance(e, dict) and e.get("outcome") == "holds" and _day(e.get("when"))), default=None)
    since = {f'{i["id"]}>{l["to"]}': _day(l["since"]).isoformat() for l in i.get("links", []) if l.get("link") == "blocked-by" and _day(l.get("since"))}
    return [iso(_day(i.get("first_filed"))), iso(settled.get(i["id"]) if k in ("question", "decision") else None),
            iso(merged_on(i) if k == "unit" else None), iso(ran if k == "gate" else None), since]


def reading_cards(page, pages):
    """The page's cards: each item's kind, title, state, who decides or owns it, its due point, a short excerpt of its body,
    how many items it waits on and unlocks, and the tab it lives on, as a link relative to this page. That tab is the one
    whose instrument holds its kind and the fewest other kinds, the earlier in navigation order on a tie, except that a
    kind READ_HOME names lives on that tab: a gate on the cutover tab, where its card is."""
    here = os.path.dirname(page["path"]) or "."
    tabs, home = [], {}
    for p in pages:
        inst = page_instrument(p)
        if inst and p.get("part") != "records":  # a record is history, never an item's home
            tabs.append([p.get("label") or p["path"], os.path.relpath(p["path"], here).replace(os.sep, "/")])
            for k in TAB_KINDS.get(inst, ()):
                fit = (inst != READ_HOME.get(k), len(TAB_KINDS[inst]))  # the named home first, then the tab holding fewest kinds
                if k not in home or fit < home[k][1]:
                    home[k] = (len(tabs) - 1, fit)
    home = {k: v[0] for k, v in home.items()}
    m = MODEL[0]
    cards, held = [], 0
    settled = {}
    for ag in (m.agreements if m else []):
        if _day(ag.get("date")):
            for x in ag.get("settled", []):
                if "withdrawn" not in (x.get("content") or {}):
                    settled[x.get("id")] = min(settled.get(x.get("id"), _day(ag["date"])), _day(ag["date"]))
    for i in (m.items if m else []):
        if i.get("sensitivity") == "restricted":
            held += 1
            continue
        f = i.get("fields") or {}
        txt = re.sub(r"\s+", " ", body_text(i) or "").strip()
        mm = ID_PAT.fullmatch(i["id"])
        cards.append([i["id"], KIND_WORDS.get(mm.group(1), i.get("kind", "")) if mm else i.get("kind", ""), i.get("title", ""), i.get("state", ""),
                      f.get("decider") or f.get("decides") or i.get("owner") or "", str(i.get("decide_by") or ""),
                      txt[:200] + ("…" if len(txt) > 200 else ""), len(m.out(i, "blocked-by")), len(m.into(i["id"], "blocked-by")),
                      home.get(i.get("kind"), -1), (due_day(m, i) or "") and due_day(m, i).isoformat()] + travel_dates(m, i, settled))
    return {"tabs": tabs, "cards": cards, "restricted": held}


def brief_html(m, page, site):
    """The one-page brief printed from the status tab: its headline, three numbers (pieces merged, tier-1 answers waiting,
    the next gate), what needs an answer, and the risk the RAID tab's lead names as the biggest."""
    import datetime
    f_ = lambda i: i.get("fields") or {}
    units = m.kind("unit")
    merged = [u for u in units if f_(u).get("ships in")]
    waiting = [i for i in m.items if i.get("kind") in ("question", "decision") and i.get("state") in ("open", "lean", "proposed")]
    today = datetime.date.today()
    t1 = [i for i in waiting if f_(i).get("tier") == "1"]  # counted as the status tab's own tile counts them
    late = [i for i in t1 if (due_day(m, i) or today) < today]
    gates = gates_in_order(m)
    nxt = next((g for g in gates if not gate_ran(g)), None)
    nb = [t for t in m.out(nxt, "blocked-by") if m.by.get(t, {}).get("state") not in ("agreed", "recorded") and not f_(m.by.get(t, {})).get("ships in")] if nxt else []
    nums = [(f"{len(merged)} / {len(units)}", "pieces of work merged", ""),
            (str(len(t1)), "tier-1 answers waiting" + (f", {len(late)} past due" if late else ""), "late" if late else ""),
            (gate_code(nxt) if nxt else "none", f"next gate, waiting on {len(nb)}" if nxt else "every gate has run", "")]
    far = datetime.date.max
    asks = sorted([i for i in waiting if i.get("sensitivity") != "restricted"], key=lambda i: (f_(i).get("tier") or "9", due_day(m, i) or far, id_order(i["id"])))[:5]
    rows = "".join(f'<li><b>{i["id"]}</b> {inline(i.get("title", ""))} <span>— {html.escape(f_(i).get("decider") or "nobody named")}'
                   + (f' · due {fmt_day(due_day(m, i))}' if due_day(m, i) else "") + '</span></li>' for i in asks)
    lvl = {"high": 3, "medium": 2, "low": 1}
    risks = m.kind("risk")  # the population and order the RAID tab's lead ranks, so both name the same risk
    top = max(risks, key=lambda r: lvl.get(f_(r).get("probability"), 0) * 10 + lvl.get(f_(r).get("impact"), 0)) if risks else None
    risk = (f'<p><b>{top["id"]}</b> {inline(top.get("title", ""))} <span>— {html.escape(f_(top).get("probability", "?"))} probability, '
            f'{html.escape(f_(top).get("impact", "?"))} impact' + (f'; response: {inline(f_(top)["response"])}' if f_(top).get("response") else "; no response yet")
            + '</span></p>') if top else '<p>No open risk is filed.</p>'
    return (f'<section class="brief" aria-label="One-page brief"><div class="bhead"><span>{html.escape(site.get("home") or site.get("title") or "")} · status brief</span>'
            f'<span>printed {fmt_day(today)}</span></div><h2>{inline(page.get("headline") or "")}</h2>'
            '<div class="bnums">' + "".join(f'<div class="{c}"><b>{html.escape(v)}</b><span>{html.escape(l)}</span></div>' for v, l, c in nums) + '</div>'
            f'<h3>Needs an answer</h3>' + (f'<ol>{rows}</ol>' if rows else '<p>Nothing is waiting on an answer.</p>')
            + f'<h3>Top risk</h3>{risk}<p class="bfoot">The full record and live state are on the site. Printed from the status tab.</p></section>')


_views_before_reading = views_html


def views_html(name, m, b=None):
    """The instrument with its "Explain this" control, hidden until the page learns it can ask Claude for the viewer."""
    return (f'<div class="xhost" data-instrument="{html.escape(name)}"><div class="xbar"><button type="button" class="sbtn xbtn" hidden>Explain this</button></div>'
            f'{_views_before_reading(name, m, b)}<div class="xout" hidden aria-live="polite"></div></div>')


# Reader lenses: the status tab re-ranked for one kind of reader, each saying what it leaves out.
LENSES = (("decider", "Decider"), ("engineer", "Engineer"), ("reviewer", "Reviewer"), ("newcomer", "Newcomer"))


def lens_card(tag, tone_, iid, meta, title, sub="", hot=False):
    return (f'<li class="lcard{" hot" if hot else ""}"><div class="lmeta"><span class="chip {tone_}">{html.escape(tag)}</span>'
            + (f'<span class="id">{html.escape(iid)}</span>' if iid else "") + f'<span class="muted">{inline(meta)}</span></div>'
            f'<b>{inline(title)}</b>' + (f'<p>{inline(sub)}</p>' if sub else "") + '</li>')


def lens_panels(m):
    """One panel per lens: its headline, its lead, its blocks of cards, and what it leaves out, all computed from the store."""
    import datetime
    f_ = lambda i: i.get("fields") or {}
    d = _map(m)
    node = {n["id"]: n for n in d["nodes"]}
    waiting = [i for i in m.items if i.get("kind") in ("question", "decision") and i.get("state") in ("open", "lean", "proposed")
               and i.get("sensitivity") != "restricted"]
    today = datetime.date.today()
    shown = lambda i: i.get("sensitivity") != "restricted"  # every lens holds restricted items apart, as every view does
    units = [u for u in m.kind("unit") if shown(u)]
    panels = {}

    def unlocks(i):
        n = node.get(i["id"])
        if not n or not n["down"]:
            return "unlocks nothing filed yet"
        return (f'unlocks {n["down"]} item{"s" if n["down"] != 1 else ""}'
                + ("" if not n["gates"] else ", a gate among them" if n["gates"] == 1 else f', {n["gates"]} gates among them'))

    # Decider: who must answer what, the most-waited-on first, and what each answer unlocks.
    people = {}
    for i in waiting:
        for p_ in people_in(f_(i).get("decider")) or ["nobody named"]:
            people.setdefault(p_, []).append(i)
    named = sorted((p_ for p_ in people if p_ != "nobody named"), key=lambda p_: (-len(people[p_]), p_))
    order = named[:4] + (["nobody named"] if "nobody named" in people else [])
    late = [i for i in waiting if (due_day(m, i) or today) < today]
    blocks = []
    for p_ in order:
        its = sorted(people[p_], key=lambda i: (f_(i).get("tier") or "9", due_day(m, i) or datetime.date.max, id_order(i["id"])))
        blocks.append((f"Waiting on {p_}", [lens_card("leaning" if i.get("state") == "lean" else "decide", "c-unsettled" if i.get("state") == "lean" else "c-open", i["id"],
                       " · ".join(x for x in (f'tier {f_(i)["tier"]}' if f_(i).get("tier") else "", f'due {fmt_day(due_day(m, i))}' if due_day(m, i) else "",
                                               f_(i).get("reversibility", "")) if x), i.get("title", ""), unlocks(i).capitalize() + ".",
                       hot=(due_day(m, i) or today) < today) for i in its[:4]]))
    latest = {}
    for a in m.agreements:
        for x in a.get("settled", []):
            i = m.by.get(x.get("id"))
            if _day(a.get("date")) and i and shown(i) and i.get("state") not in ("superseded", "withdrawn"):
                latest[i["id"]] = max(latest.get(i["id"], _day(a["date"])), _day(a["date"]))
    recent = sorted(((dd, x) for x, dd in latest.items()), key=lambda t: (t[0], id_order(t[1])), reverse=True)[:3]
    if recent:
        blocks.append(("Decided lately", [lens_card("agreed", "c-holds", x, fmt_day(dd), m.by[x].get("title", "")) for dd, x in recent]))
    panels["decider"] = (f'{len(waiting)} answers wait on {len([p_ for p_ in people if p_ != "nobody named"])} deciders' + (f', {len(late)} past due' if late else ""),
                         f'Each card says what its answer unlocks. {len(people.get("nobody named", []))} have nobody named to decide.' if people.get("nobody named") else "Each card says what its answer unlocks.",
                         blocks, "the work, the risks, review requests and the design")

    # Engineer: what can be built now, what is blocked and on what, and the risks that reach the work.
    open_units = [u for u in units if not f_(u).get("ships in")]
    ready = [u for u in open_units if u["id"] not in node or node[u["id"]]["can"]]  # a piece with no waits can start
    blocked = [u for u in open_units if u not in ready]
    lvl = {"high": 3, "medium": 2, "low": 1}
    risks = sorted([r for r in m.kind("risk") if f_(r).get("status") != "closed" and shown(r)],
                   key=lambda r: -(lvl.get(f_(r).get("probability"), 0) * 10 + lvl.get(f_(r).get("impact"), 0)))
    waits = lambda u: [x for x in m.out(u, "blocked-by") if x in node and not node[x]["done"] and node[x]["kind"] != "gate"]
    blocks = []
    if ready:
        blocks.append(("Can start now", [lens_card("ready", "c-holds", u["id"], "on the critical path" if node.get(u["id"], {}).get("crit") else "", u.get("title", "")) for u in ready[:4]]))
    if blocked:
        blocks.append(("Blocked, and on what", [lens_card("waiting", "c-unsettled", u["id"], "after " + " ".join(waits(u)[:3]) if waits(u) else "after an earlier gate", u.get("title", "")) for u in blocked[:4]]))
    if risks:
        blocks.append(("Risks to watch", [lens_card(f'{f_(r).get("probability") or "?"} · {f_(r).get("impact") or "?"}', "c-open", r["id"], f_(r).get("response") or "no response yet", r.get("title", "")) for r in risks[:3]]))
    panels["engineer"] = (f'{len(ready)} pieces can start now; {len(blocked)} wait on something', "Each blocked piece names what it waits on.",
                          blocks, "decisions already made, deciders, the glossary and the gates")

    # Reviewer: the work merged, newest first, and the requirements built but not yet verified. Merged is what the status
    # tab counts as merged: work whose review request is named.
    merged = sorted([u for u in units if f_(u).get("ships in")], key=lambda u: (merged_on(u) or datetime.date.min, id_order(u["id"])), reverse=True)
    partly = [r for r in m.kind("requirement") if m.req_status(r) == "partly" and shown(r)]
    blocks = []
    if merged:
        blocks.append(("Merged, newest first", [lens_card(str(f_(u)["ships in"]), "c-holds", u["id"], " · ".join(x for x in (fmt_day(merged_on(u)) if merged_on(u) else "", "serves " + " ".join(m.out(u, "serves")[:4]) if m.out(u, "serves") else "") if x), u.get("title", "")) for u in merged[:6]]))
    if partly:
        blocks.append(("Built, not yet verified", [lens_card("partly met", "c-unsettled", r["id"], "", r.get("title", "")) for r in partly[:4]]))
    panels["reviewer"] = (f'{len(merged)} of {len(units)} pieces are merged' + (f'; {len(partly)} requirement{"s are" if len(partly) != 1 else " is"} built but not yet verified' if partly else ""),
                          "Each merged piece names what it serves, so a review can start from the requirement.", blocks,
                          "gates, deciders and forecasts")

    # Newcomer: what this is, the decisions everything rests on, the words it uses, and whom to ask.
    ovw = next(iter(m.kind("overview")), None)
    settled = sorted([i for i in m.kind("decision") if i.get("state") in ("agreed", "recorded") and shown(i)],
                     key=lambda i: -len(m.into(i["id"], "rests-on")) - len(m.into(i["id"], "blocked-by")))  # ties keep the store's order
    terms = sorted([t for t in m.kind("term") if shown(t)], key=lambda t: id_order(t["id"]))
    owners = {}
    for i in waiting:
        for p_ in people_in(f_(i).get("decider")):
            owners.setdefault(p_, []).append(i["id"])
    blocks = []
    if settled or terms:
        blocks.append(("Read these first", [lens_card("decided", "c-holds", i["id"], "decision", i.get("title", "")) for i in settled[:3]]
                       + [lens_card("term", "c-unchecked", t["id"], "glossary", t.get("title", "")) for t in terms[:2]]))
    if owners:
        blocks.append(("Who to ask", [lens_card("decides", "c-unchecked", "", f'{len(v)} open', p_, "Decides " + " ".join(sorted(v, key=id_order)[:5]) + ("…" if len(v) > 5 else "")) for p_, v in sorted(owners.items(), key=lambda kv: -len(kv[1]))[:4]]))
    panels["newcomer"] = ((ovw.get("title") if ovw else "Start here"), (body_text(ovw)[:300] if ovw else "What the work is, the decisions it rests on, and whom to ask."),
                          blocks, "the work list, review requests and risks, which read better after the design")
    out = []
    for key, label in LENSES:
        head, lead, blocks, hides = panels[key]
        body = "".join(f'<h3 class="sub">{html.escape(t)}</h3><ul class="lcards">{"".join(cs)}</ul>' for t, cs in blocks if cs) or '<p class="muted">Nothing on this set is for this lens yet.</p>'
        out.append(f'<section class="lens" data-lens="{key}" hidden aria-label="{label} lens"><span class="eyebrow">Reading as {label.lower()}</span>'
                   f'<h2>{inline(head)}</h2><p class="lead">{inline(lead)}</p>{body}'
                   f'<p class="lfold">Left out for this lens: {html.escape(hides)}. <button type="button" class="sbtn lall">Show everything</button></p></section>')
    return "".join(out)


_page_before_reading = page_html


def page_html(site, page, pages, views, opts):
    out = _page_before_reading(site, page, pages, views, opts)
    if page["path"] == "index.html" and MODEL[0] and MODEL[0].items:
        # inserted after the page's own pass, so they take the same naming and source links themselves
        out = out.replace("</main>", link_refs(name_ids(brief_html(MODEL[0], page, site))) + "</main>", 1)
        h = out.find('<section class="hero">')
        e = out.find("</section>", h) + len("</section>") if h >= 0 else -1
        if e > 0:
            out = out[:e] + link_refs(name_ids(lens_panels(MODEL[0]))) + out[e:]
    tag = f'<script type="application/json" id="praxis-cards">{safe_json(reading_cards(page, pages))}</script>'
    return out.replace("</body></html>", tag + "</body></html>") if out.endswith("</body></html>") else out + tag
# --- end reading: ws1 ---


# --- reader cut: ws3 ---
# What a reader tab draws in full (the document skill's reader-tabs rule, "What a tab draws in full"): every instrument that
# gives items as text passes its list through cut(), which keeps every item passing one of the rule's five tests, in the
# rule's rank order, with no cap. Every other item of a kind an instrument cut is counted in one line after the instrument,
# linking its entry on the tab's page as filed, where each item carries an anchor. Marks in a picture are not cut.
# The words a tab writes are advised, never cut: check_site reads these from here and reports denser text as advice. Hosted
# sections shown on a tab are as filed and take no advice.
HEADLINE_WORDS = 14          # a headline: one claim or one question
SENTENCE_WORDS = 25          # a sentence of the words a tab writes itself
SENTENCE_CODES = 2           # item codes one such sentence names
# The kinds each instrument gives as text, in its tab's table order; the first is the tab's subject (test 5). Kinds an
# instrument draws only as marks, such as Design's slices or Threats' parts, are neither ranked nor counted.
TEXT_KINDS = {"register": ("question", "decision", "brief"), "requirements": ("requirement", "acceptance criterion"),
              "raid": ("risk", "issue", "assumption", "dependency"), "threats": ("threat", "privacy threat"), "adrs": ("decision",),
              "faq": ("answer",), "design": ("design section",), "data": ("vendor or dependency",),
              "runbook": ("objective", "alert", "procedure"), "glossary": ("term",)}
FILED = [None]  # the page being rendered's own page as filed, when it has one; without one a tab draws everything
PAGE_CUT = {}   # page path -> (ids its tab no longer draws, its page as filed), for relink_cut
CUTS = {}      # instrument -> {"full": ids drawn in full, "items": the tab's items, "test": id -> lowest test passed}
CUT_USED = {}  # instrument -> kinds an instrument cut while drawing, for its count lines
PLURAL = {"acceptance criterion": "acceptance criteria", "screening criterion": "screening criteria", "vendor or dependency": "vendors or dependencies",
          "dependency": "dependencies", "privacy threat": "privacy threats", "design section": "design sections", "restore path": "restore paths"}


def _ws3_overdue(i):
    import datetime
    d = str(i.get("decide_by") or "")
    return d[:1].isdigit() and d[:10] < datetime.date.today().isoformat() and i.get("state") != "agreed"


def _ws3_is_ask(m, i):
    """Test 1: an open ask. A decide-by naming a gate or a milestone never counts as passed."""
    k, st = i.get("kind"), i.get("state")
    if (k == "question" and st in ("open", "lean")) or (k == "decision" and st == "proposed") or _ws3_overdue(i):
        return True
    return k == "brief" and any(_ws3_is_ask(m, m.by[x]) for x in m.out(i, "serves") if x in m.by and m.by[x].get("kind") != "brief")


def _ws3_red(m, i):
    """Test 4: what design-reader-instruments marks as needing an action: unowned or undecided, failing, one-way."""
    f = i.get("fields") or {}
    v = m.verdicts(i)
    return (not i.get("owner") or (i.get("kind") in ("question", "decision") and not f.get("decider"))
            or (bool(v) and v[-1].get("outcome") not in ("holds", None)) or f.get("reversibility") == "one-way"
            or f.get("aspect") == "inconsistency")  # a design and its code disagreeing is failing


def cut_test(m, i, instrument):
    """The lowest-numbered test of the rule's five an item passes, or None."""
    f = i.get("fields") or {}
    if _ws3_is_ask(m, i):
        return 1
    if i.get("kind") in ("question", "decision") and (f.get("tier") == "1" or f.get("reach") == "beyond the change"):
        return 2
    if any(x in m.by and _ws3_is_ask(m, m.by[x]) for x in m.out(i, "blocked-by")):
        return 3
    if _ws3_red(m, i):
        return 4
    return 5 if i.get("kind") == TEXT_KINDS.get(instrument, (None,))[0] else None


def _ws3_rank(i, t):
    f = i.get("fields") or {}
    tier = {"1": 0, "2": 1}.get(str(f.get("tier")), 2)
    d = str(i.get("decide_by") or "")
    g = re.match(r"GATE-(\d+)$", d)
    due = (0, d[:10], 0) if d[:1].isdigit() else (1, "", int(g.group(1))) if g else (2, "", 0) if d else (3, "", 0)
    return (t, tier, due)


def reader_cut(m, instrument):
    if instrument not in CUTS:
        items = [i for i in m.items if i.get("kind") in TEXT_KINDS.get(instrument, ())
                 and i.get("state") not in ("superseded", "withdrawn") and i.get("sensitivity") != "restricted"]
        test = {i["id"]: cut_test(m, i, instrument) for i in items}
        passing = [i for i in items if test[i["id"]]]
        CUTS[instrument] = {"full": {i["id"] for i in passing}, "items": items, "test": test,
                            "rank": {i["id"]: _ws3_rank(i, test[i["id"]]) for i in passing}}
    return CUTS[instrument]


def cut(m, instrument, items):
    """The items of a list an instrument gives as text that its tab draws in full; the rest go to the count lines."""
    if not FILED[0]:
        return items
    c = reader_cut(m, instrument)
    CUT_USED.setdefault(instrument, set()).update(i.get("kind") for i in items)
    return sorted((i for i in items if i["id"] in c["full"]), key=lambda i: c["rank"][i["id"]])  # stable: ties keep the instrument's order


def as_filed_link():
    return os.path.relpath(FILED[0], HERE[0] or ".").replace(os.sep, "/")


def count_lines(m, instrument):
    c, used = CUTS.get(instrument), CUT_USED.get(instrument)
    if not c or not used:
        return ""
    href, out = as_filed_link(), []
    for k in TEXT_KINDS.get(instrument, ()):
        rest = [i for i in c["items"] if i.get("kind") == k and i["id"] not in c["full"]]
        if k not in used or not rest:
            continue
        word = PLURAL.get(k, k + "s") if len(rest) != 1 else k
        out.append(f'<p class="caption cutline"><a href="{href}#{rest[0]["id"]}">{len(rest)} more {html.escape(word)}, '
                   'none open</a></p>')
    return "".join(out)


def anchor_items(markup):
    """Each item's first appearance on a page as filed carries its id as an anchor: its row, else its code."""
    parts = re.split(r"(<script\b.*?</script>)", markup, flags=re.S)
    seen = set(re.findall(r'\bid="([A-Z]{1,5}-\d+)"', markup))

    def once(mm, pre, post):
        iid = mm.group(1)
        if iid in seen:
            return mm.group(0)
        seen.add(iid)
        return f'{pre}id="{iid}" {post}{iid}'
    for n, p in enumerate(parts):
        if n % 2 == 0:
            p = re.sub(r'data-item="([A-Z]{1,5}-\d+)', lambda mm: once(mm, "", 'data-item="'), p)
            p = re.sub(r'<abbr title="([A-Z]{1,5}-\d+)(?= ·)', lambda mm: once(mm, "<abbr ", 'title="'), p)
            parts[n] = p
    return "".join(parts)


_instrument_before_ws3 = _instrument_html


def _instrument_html(name, m, opts=None):
    CUTS.pop(name, None)
    CUT_USED.pop(name, None)
    body = _instrument_before_ws3(name, m, opts)
    c = CUTS.get(name)
    if c:  # a mark linking an item the tab no longer draws opens its entry as filed
        gone = {i["id"] for i in c["items"] if i.get("kind") in CUT_USED.get(name, ())} - c["full"]
        PAGE_CUT.setdefault(CURPATH[0], (set(), FILED[0]))[0].update(gone)
        gone -= set(re.findall(r'\bid="([A-Z]{1,5}-\d+)"', body))
        body = re.sub(r'href="#([A-Z]{1,5}-\d+)"', lambda mm: f'href="{as_filed_link()}#{mm.group(1)}"' if mm.group(1) in gone else mm.group(0), body)
    return body + count_lines(m, name)


_insights_before_ws3 = insights_html


def insights_html(rows):
    """An instrument headline is claim first: its first clause is the claim, and what follows its first colon or semicolon
    is the claim's detail, shown after it in quieter type. Nothing is dropped or shortened."""
    def split(t):
        depth, pos = 0, 0
        for part in re.split(r"(<[^>]+>)", t):  # only text outside every element, never inside an entity
            if part.startswith("<"):
                depth += 0 if part.endswith("/>") or re.match(r"<(br|img|wbr)\b", part) else -1 if part.startswith("</") else 1
            elif depth == 0:
                mm = re.search(r"[:;]\s+", re.sub(r"&[#\w]+;", lambda e: "\0" * len(e.group(0)), part))
                head = t[:pos + mm.start()] if mm else ""
                plain = re.sub(r"<[^>]+>", "", head)
                if re.search(r"[.!?]\s", plain):  # the first sentence has no clause break: it is the claim whole
                    return t
                if mm and len(plain.split()) >= 3:  # a claim, not a bare value such as an option's name
                    rest = t[pos + mm.end():]
                    return head + "\u2063" + rest[:1].upper() + rest[1:]
            pos += len(part)
        return t
    out = _insights_before_ws3([(k, split(t)) for k, t in rows])
    return out.replace("\u2063", '.</span><span class="muted small">')


_page_before_ws3 = page_html


CURPATH = [""]


def page_html(site, page, pages, views, opts):
    slug_ = re.sub(r"[^a-z0-9]+", "-", (page.get("label") or page.get("title") or page["path"]).lower()).strip("-")
    filed = f"records/{slug_}-as-filed.html"
    FILED[0] = filed if any(p.get("path") == filed for p in pages) else None
    CURPATH[0] = page["path"]
    out = _page_before_ws3(site, page, pages, views, opts)
    return anchor_items(out) if str(page.get("path", "")).endswith("-as-filed.html") else out
# --- end reader cut: ws3 ---


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


# --- reader cut: ws3 (links) ---
# Once every page is written, a link to an item a tab no longer draws in full opens its entry on that tab's page as filed.
_main_before_ws3 = main


def relink_cut(out):
    pages = {}
    for root, _, files in os.walk(out):
        for f in files:
            if f.endswith(".html"):
                pages[os.path.relpath(os.path.join(root, f), out).replace(os.sep, "/")] = open(os.path.join(root, f), encoding="utf-8").read()
    ids = {p: set(re.findall(r'\bid="([A-Z]{1,5}-\d+)"', h)) for p, h in pages.items()}
    for path, h in pages.items():
        here = os.path.dirname(path)

        def fix(mm):
            target = os.path.normpath(os.path.join(here, mm.group(1))).replace(os.sep, "/")
            if target.endswith("-as-filed.html") and target in pages and mm.group(2) not in ids[target]:
                return f'href="{mm.group(1)}"'  # an item its page as filed doesn't hold: the page itself
            gone, full = PAGE_CUT.get(target, (set(), None))
            if mm.group(2) not in gone or mm.group(2) in ids.get(target, ()) or mm.group(2) not in ids.get(full, ()):
                return mm.group(0)
            return f'href="{os.path.relpath(full, here or ".").replace(os.sep, "/")}#{mm.group(2)}"'
        new = re.sub(r'href="([^"#:]+\.html)#([A-Z]{1,5}-\d+)"', fix, h)
        if new != h:
            with open(os.path.join(out, path), "w", encoding="utf-8") as fh:
                fh.write(new)


def main(argv):
    rc = _main_before_ws3(argv)
    if rc == 0:
        relink_cut(argv[3])
    return rc
# --- end reader cut: ws3 (links) ---

if __name__ == "__main__":
    sys.exit(main(sys.argv))
