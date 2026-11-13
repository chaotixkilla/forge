#!/usr/bin/env python3
"""Check a rendered claude-artifacts site against what can be computed of design-reader-instruments.

Usage: check_site.py <out-dir> <items.json>

Reads every page render_site.py wrote and reports:
- a page without its embedded tree entry (`praxis-page`), which a fetch could not read back;
- raw data or a placeholder in a reader's text, a section that renders nothing, and a link to an anchor its page lacks;
- a step code heading two gates, or cited with no gate or slice carrying it, and a question and a decision stating one thing unlinked;
- a reader tab (part now or plan, the main page aside) without its headline strip;
- a relative link to a page or file the site doesn't hold;
- a section a tab's design neither shows nor names as filed-only;
- a source named by an id (a tracker key not of this store's prefixes, a review request, a playbook) with no link and not marked (no link),
  and one the site links or names with no title saying what it is;
  documents and threads named in words, and a source's ids sharing this store's prefixes, are not seen and are the run's to link;
- an item the store holds that no page shows, by its id or its full title, outside scripts.

Prints {"findings": [...]} with {"page", "check", "detail"} each, and exits 1 when there is any.
"""
import json
import os
import re
import sys

NOT_SHOWN_ALONE = {"overview"}
LEAK = re.compile(r"\{'\w+':|\{\"\w+\":|\bundefined\b|\[object \w+\]|\bNaN\b|\bTODO\b|\bFIXME\b|lorem ipsum")  # read into the main page's lead, never listed
# A mention that reads as an outside source: a tracker key not of this store's prefixes, a review request number, a playbook.
OUTSIDE = re.compile(r"(?<![\w#/-])(?:[A-Z]{2,}(?:-[A-Z]+)?-\d+|PR #\d+|#\d{3,}|[Rr]eview request \d+|[Pp]laybooks? \d+)(?![\w-])")


def main(argv):
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    out, store = argv[1], json.load(open(argv[2], encoding="utf-8"))
    pages = {}
    for root, _, files in os.walk(out):
        for f in files:
            if f.endswith(".html"):
                path = os.path.relpath(os.path.join(root, f), out).replace(os.sep, "/")
                pages[path] = open(os.path.join(root, f), encoding="utf-8").read()
    findings = []
    own = {i["id"].split("-")[0] for i in store.get("items", []) if "-" in i.get("id", "")} | {"AGR"}

    def find(page, check, detail):
        findings.append({"page": page, "check": check, "detail": detail})

    for path, html in sorted(pages.items()):
        m = re.search(r'<script type="application/json" id="praxis-page">(.*?)</script>', html, re.S)
        if not m:
            find(path, "read-back", "no embedded tree entry")
            continue
        entry = json.loads(m.group(1).replace("<\\/", "</"))
        has_instrument = any("instrument" in b for sec in entry.get("sections", []) for b in sec.get("blocks", []))
        if has_instrument and path != "index.html" and 'class="insights"' not in html:
            find(path, "headlines", "a reader tab without its headline strip")
        main = re.sub(r"<header\b.*?</header>|<script\b.*?</script>", "", html, flags=re.S)
        for ref in sorted(set(re.findall(r'<(?:a class="ext"|span class="src")(?![^>]*title=)[^>]*>([^<]+)<', main)))[:20]:
            find(path, "untitled", f"'{ref}' names a source without saying what it is: give its refs entry a title")
        for mm in re.finditer(r'<span class="src"[^>]*>([^<]+)</span>', main):
            if not re.sub(r"<[^>]+>", "", main[mm.end():mm.end() + 60]).lstrip().startswith("(no link)"):
                find(path, "unlinked", f"'{mm.group(1)}' has a title but no address and no (no link) after it")
        bare = re.sub(r"<(script|style|a|code|pre|svg)\b.*?</\1>|<span class=\"src\".*?</span>", "", main, flags=re.S)
        bare = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", bare))
        refs_ = sorted({mm.group(0) for mm in OUTSIDE.finditer(bare) if mm.group(0).split("-")[0] not in own
                        and not bare[mm.end():mm.end() + 12].lstrip().startswith("(no link)")})
        for ref in refs_[:20]:
            find(path, "unlinked", f"'{ref}' names a source with no link: add it to site.json's refs or ref_patterns, mark it (no link), or write a non-source as code")
        for leak in sorted(set(LEAK.findall(bare)))[:5]:
            find(path, "leak", f"'{leak}' reads as raw data or a placeholder, not words for a reader")
        for heading in re.findall(r'<section id="[^"]*"[^>]*><h2>([^<]*)</h2>\s*</section>', main):
            find(path, "empty", f"section '{heading}' renders nothing under its heading")
        for heading in re.findall(r'<section id="[^"]*" data-unplaced="1"><h2>(.*?)</h2>', html):
            find(path, "unplaced", f"section '{heading}' is neither designed into its tab nor named as filed-only")
        for href in re.findall(r'href="([^"#:?]+)(?:#[^"]*)?"', re.sub(r"<script.*?</script>", "", html, flags=re.S)):
            if href.startswith(("http", "mailto", "//")):
                continue
            target = os.path.normpath(os.path.join(os.path.dirname(path), href)).replace(os.sep, "/")
            if target not in pages and not os.path.exists(os.path.join(out, target)):
                find(path, "link", f"{href} leads nowhere")
        for href, frag in re.findall(r'href="([^"#:?]*)#([^"]+)"', re.sub(r"<script.*?</script>", "", html, flags=re.S)):
            if href.startswith(("http", "//")):
                continue
            target = os.path.normpath(os.path.join(os.path.dirname(path), href)).replace(os.sep, "/") if href else path
            if target in pages and not re.search(r'\bid="' + re.escape(frag) + '"', pages[target]) and not re.search(r'"id":\s*"' + re.escape(frag) + '"', pages[target]):
                find(path, "anchor", f"{href}#{frag} points at nothing on {target}")
    import html as _html
    text = " ".join(re.sub(r"<script.*?</script>", "", h, flags=re.S) for h in pages.values())
    kinds = {}
    for item in store.get("items", []):
        if item.get("state") in ("superseded", "withdrawn") or item.get("sensitivity") == "restricted":
            continue
        kinds.setdefault(item.get("kind"), []).append(item)
    for kind, items in sorted(kinds.items()):
        if kind in NOT_SHOWN_ALONE:
            continue
        def shown(i):
            if re.search(r"\b" + re.escape(i["id"]) + r"\b", text):
                return True
            title = _html.escape(i.get("title", ""), quote=False)
            return len(title) >= 12 and title in text
        missing = [i["id"] for i in items if not shown(i)]
        if missing:
            find("(site)", "unshown items", f"{kind}: {len(missing)} of {len(items)} appear on no page ({' '.join(missing[:8])}{'…' if len(missing) > 8 else ''})")
    # step codes: one per step, and none cited that no gate or slice carries
    live = [i for i in store.get("items", []) if i.get("state") not in ("superseded", "withdrawn")]
    coded = {}
    for i in live:
        if i.get("kind") in ("gate", "slice") and " · " in i.get("title", ""):
            coded.setdefault((i["kind"], i["title"].split(" · ")[0]), []).append(i["id"])
    for (k, c), xs in sorted(coded.items()):
        if len(xs) > 1 and k == "gate":  # slices share the code of the gate that first exposes them
            find("(site)", "code reused", f"{c} heads {len(xs)} {k}s ({' '.join(xs)}); a step code names one step")
    codes = {c for _, c in coded}
    if codes:
        letters = "".join(sorted({c[0] for c in codes}))
        cited = set(re.findall(r"(?<![\w-])([" + letters + r"]\d{1,2})(?![\w-])", re.sub(r"<[^>]+>", " ", text)))
        for c in sorted(cited - codes)[:10]:
            find("(site)", "dangling code", f"{c} is cited but no gate or slice carries it")
    # one fact in two items: a question and a decision about the same thing, neither linked to the other
    words = lambda t: {w for w in re.findall(r"[a-z]{4,}", t.lower())} - {"does", "this", "that", "with", "change", "when", "what", "which", "from", "owes", "owed"}
    qs = [i for i in live if i.get("kind") == "question"]
    ds = [i for i in live if i.get("kind") == "decision"]
    for q in qs:
        for d in ds:
            a, b = words(q.get("title", "")), words(d.get("title", ""))
            linked = any(l.get("to") in (q["id"], d["id"]) for l in q.get("links", []) + d.get("links", []))
            if a and b and len(a & b) / min(len(a), len(b)) >= 0.6 and not linked:
                find("(site)", "same fact twice", f"{q['id']} and {d['id']} state the same thing unlinked: one item, or a link saying which settles which")
    print(json.dumps({"findings": findings}, indent=2, ensure_ascii=False))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
