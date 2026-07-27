#!/usr/bin/env python3
"""Measures what a plugin's skills actually cost to load, layer by layer.

The contract audit asks whether every file *can* load. This asks the opposite question: given that
they can, how much becomes reachable, and from where. Both matter, and neither substitutes for the
other — a skill can be perfectly wired and still make 30,000 tokens reachable from one paragraph.

The metric that does the work here is **fan-out**: for each file, the weight its own citations make
reachable in ONE hop, over its own weight, together with how many files that is. Both halves are
needed. Ratio alone flags a short module that cites five heavy rules, which is ordinary and fine.
Count alone flags a spine, whose whole job is to cite every phase. It is the conjunction — many
citations, carrying many times this file's own weight, from one place — that identifies a *roster*:
a list the executor must triage by filename, where it will either read all of it or guess.

Fan-out is not itself a defect, which is why this reports rather than forbids. A deliberate routing
index has high fan-out by design and is correct; the difference between an index and a roster is
whether each link carries a firing condition, and that is a reading, not a measurement. So this
locates the sites and the audit reads them.

What this script does NOT judge: whether a citation carries a trigger, whether a rule earns its keep,
whether the prose is derivable. Those are readings, and they stay with the audit and its critics.

Usage:
    measure_context.py <plugin-dir> [...] [--json] [--top=N]
                       [--max-amplification=N] [--max-resident=N] [--max-closure=N]

Exit status:
    0  within every budget
    1  a budget exceeded
    2  bad invocation

Token figures are chars/4 — a rough, stable estimate, used only for comparison between files
measured the same way. Stdlib only, by design: it ships inside a plugin.
"""

from __future__ import annotations

import json
import os
import re
import sys

LINK = re.compile(r"\[[^\]]*\]\(\s*(?!https?://|mailto:|#)([^)\s#]+)")
PLACEHOLDER = re.compile(r"[<>]|(?:^|/)(?:name|NN-name)\.md$")
SPINE_STEP = re.compile(r"^\s*\d+\.\s")

# Proposed budgets. These are the one genuinely contestable part of this script: they are thresholds,
# and a threshold with no owner is the open standard anvil's own audits exist to catch. They ship as
# defaults so the check is runnable today, overridable per invocation, and are recorded as
# PROPOSED — pending maintainer ratification — in the rule that documents this check. Do not read
# them as house standard until that marker changes.
DEFAULTS = {
    "max_amplification": 12.0,  # direct-cited weight over own weight, for one file
    "max_citations": 12,        # direct citations from one file; breaches need BOTH this and the ratio
    "max_resident": 3500,       # always-resident tokens per plugin (skill + agent descriptions)
    "max_closure": 25000,       # tokens a no-flag run of one skill can reach
}


def read(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def strip_code(text: str) -> str:
    text = re.sub(r"```.*?```", lambda m: " " * len(m.group(0)), text, flags=re.S)
    return re.sub(r"(`+)(?:(?!\1)[^\n])*\1", lambda m: " " * len(m.group(0)), text)


def toks(text: str) -> int:
    return round(len(text) / 4)


def frontmatter_split(text: str) -> tuple[dict, str]:
    """Return (top-level scalar keys, body-after-frontmatter)."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm: dict = {}
    for line in text[3:end].splitlines():
        if not line.strip() or line.startswith("#") or line[:1].isspace():
            continue
        k, sep, v = line.partition(":")
        if sep and k.strip():
            fm[k.strip()] = v.strip()
    return fm, text[end + 4 :]


def citations(path: str) -> list[str]:
    """Resolved, existing markdown-link targets from one file."""
    base = os.path.dirname(path)
    out = []
    for t in LINK.findall(strip_code(read(path))):
        if PLACEHOLDER.search(t):
            continue
        r = os.path.normpath(os.path.join(base, t))
        if os.path.isfile(r):
            out.append(r)
    return out


def skill_root(path: str) -> str | None:
    """The skills/<name> directory containing `path`, if any."""
    marker = f"{os.sep}skills{os.sep}"
    i = path.find(marker)
    if i == -1:
        return None
    rest = path[i + len(marker):]
    name = rest.split(os.sep, 1)[0]
    return path[: i + len(marker)] + name


def crosses_boundary(node: str, home: str | None) -> bool:
    """True where the load path stops expanding.

    Two seams end a context rather than extending it, and conflating them with an ordinary citation
    is what turns this metric into noise:

      * a sibling SKILL.md — a delegation is an *invocation*. The sibling runs its own procedure in
        its own window; its phases and rules are not pulled into this one. Reading the spine to make
        the call is a real cost, so the file counts for one hop, but expanding through it would make
        every file in a well-connected skill "reach" the entire plugin.
      * an agent body — explorers and critics run in a forked context. Same logic: the recruit costs
        the caller nothing of the agent's own body.
    """
    if f"{os.sep}agents{os.sep}" in node:
        return True
    return skill_root(node) != home


def closure(start: str, weights: dict[str, int], edges: dict[str, list[str]]) -> tuple[int, int]:
    """Reachable weight from `start`, excluding `start`, stopping at each context boundary.

    Boundary files are counted once (you pay to read the spine you invoke) but never expanded.
    """
    home = skill_root(start)
    seen = {start}
    stack = list(edges.get(start, []))
    total = 0
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        total += weights.get(node, 0)
        if not crosses_boundary(node, home):
            stack.extend(edges.get(node, []))
    return total, len(seen) - 1


def measure(plugin_dir: str) -> dict:
    plugin_dir = os.path.abspath(plugin_dir.rstrip(os.sep))
    plugin = os.path.basename(plugin_dir)
    parent = os.path.dirname(plugin_dir)

    def rel(p: str) -> str:
        return os.path.relpath(p, parent)

    all_md = []
    for dirpath, _d, filenames in os.walk(plugin_dir):
        for fn in filenames:
            if fn.endswith(".md"):
                all_md.append(os.path.join(dirpath, fn))
    all_md.sort()

    weights = {p: toks(read(p)) for p in all_md}
    edges = {p: citations(p) for p in all_md}

    # ---- layer 0: what is resident on every request, whether or not a skill is invoked ----------
    resident = 0
    resident_parts = []
    for p in all_md:
        is_skill = os.path.basename(p) == "SKILL.md" and f"{os.sep}skills{os.sep}" in p
        is_agent = f"{os.sep}agents{os.sep}" in p
        if not (is_skill or is_agent):
            continue
        fm, _ = frontmatter_split(read(p))
        cost = toks(fm.get("name", "") + " " + fm.get("description", ""))
        resident += cost
        resident_parts.append({"file": rel(p), "tokens": cost, "kind": "skill" if is_skill else "agent"})
    resident_parts.sort(key=lambda r: -r["tokens"])

    # ---- per-skill layers ----------------------------------------------------------------------
    skills = []
    skills_root = os.path.join(plugin_dir, "skills")
    if os.path.isdir(skills_root):
        for name in sorted(os.listdir(skills_root)):
            sdir = os.path.join(skills_root, name)
            smd = os.path.join(sdir, "SKILL.md")
            if not os.path.isfile(smd):
                continue

            def slot_weight(slot: str) -> tuple[int, int]:
                d = os.path.join(sdir, slot)
                files = [p for p in all_md if p.startswith(d + os.sep)]
                return sum(weights[p] for p in files), len(files)

            ph_w, ph_n = slot_weight("phases")
            ru_w, ru_n = slot_weight("rules")
            mo_w, mo_n = slot_weight("modules")
            ad_w, ad_n = slot_weight("adapters")
            usage = os.path.join(sdir, "usage.md")
            us_w = weights.get(usage, 0)
            spine_w = weights[smd]

            # a no-flag run: spine + usage (pointed at from body line 1) + every phase + whatever
            # those phases transitively reach. modules are excluded: they are flag-gated.
            phase_files = [p for p in all_md if p.startswith(os.path.join(sdir, "phases") + os.sep)]
            reach: set[str] = set()
            for pf in phase_files:
                stack = list(edges.get(pf, []))
                while stack:
                    n = stack.pop()
                    if n in reach or n in phase_files or n == smd:
                        continue
                    reach.add(n)
                    if not crosses_boundary(n, sdir):
                        stack.extend(edges.get(n, []))
            reach.discard(usage)
            # modules are flag-gated; a phase citing one does not load it on a no-flag run
            reach = {p for p in reach if f"{os.sep}modules{os.sep}" not in p}
            reachable_w = sum(weights.get(p, 0) for p in reach)

            skills.append({
                "skill": name,
                "spine": spine_w,
                "usage": us_w,
                "phases": {"tokens": ph_w, "files": ph_n},
                "rules": {"tokens": ru_w, "files": ru_n},
                "modules": {"tokens": mo_w, "files": mo_n, "note": "flag-gated"},
                "adapters": {"tokens": ad_w, "files": ad_n},
                "no_flag_ceiling": spine_w + us_w + ph_w + reachable_w,
                "disclosure_ratio": round((spine_w + us_w + ph_w + ru_w + mo_w + ad_w) / spine_w, 1) if spine_w else 0,
            })

    # ---- amplification, per citing file --------------------------------------------------------
    # Amplification is measured on DIRECT citations — one hop — not on the transitive closure.
    # The transitive figure is the wrong instrument for locating a roster: rules in this kit
    # cross-link densely, so every file in a well-connected skill transitively reaches that skill's
    # whole library, and a 275-token leaf scores higher than the roster you are hunting. Direct
    # fan-out is what separates the two: a phase that cites 37 rules in one bullet list carries the
    # weight of 37 rules at one decision point, whereas a leaf citing two siblings carries two.
    hotspots = []
    for p in all_md:
        own = weights[p]
        direct = sorted(set(edges.get(p, [])))
        if own < 40 or not direct:
            continue
        direct_w = sum(weights.get(t, 0) for t in direct)
        if not direct_w:
            continue
        reach_w, reach_n = closure(p, weights, edges)
        # A SKILL.md spine is an index by design — being a high-fan-out pointer is its job, and the
        # contract requires it to cite every phase. Measured and reported, never flagged.
        is_spine = os.path.basename(p) == "SKILL.md"
        hotspots.append({
            "file": rel(p),
            "own_tokens": own,
            "direct_citations": len(direct),
            "direct_tokens": direct_w,
            "amplification": round(direct_w / own, 1),
            "transitive_tokens": reach_w,
            "transitive_files": reach_n,
            "exempt": is_spine,
        })
    hotspots.sort(key=lambda h: -h["amplification"])

    corpus = sum(weights.values())
    return {
        "plugin": plugin,
        "corpus_tokens": corpus,
        "always_resident_tokens": resident,
        "resident_share": round(100 * resident / corpus, 2) if corpus else 0,
        "resident_parts": resident_parts,
        "skills": skills,
        "hotspots": hotspots,
    }


def main(argv: list[str]) -> int:
    opts = dict(DEFAULTS)
    top = 12
    as_json = "--json" in argv
    targets = []
    for a in argv[1:]:
        if a.startswith("--max-amplification="):
            opts["max_amplification"] = float(a.split("=", 1)[1])
        elif a.startswith("--max-citations="):
            opts["max_citations"] = int(a.split("=", 1)[1])
        elif a.startswith("--max-resident="):
            opts["max_resident"] = int(a.split("=", 1)[1])
        elif a.startswith("--max-closure="):
            opts["max_closure"] = int(a.split("=", 1)[1])
        elif a.startswith("--top="):
            top = int(a.split("=", 1)[1])
        elif not a.startswith("--"):
            targets.append(a)
    if not targets:
        sys.stderr.write(__doc__ or "")
        return 2

    reports, breaches = [], []
    for t in targets:
        if not os.path.isdir(t):
            sys.stderr.write(f"not a directory: {t}\n")
            return 2
        r = measure(t)
        reports.append(r)
        if r["always_resident_tokens"] > opts["max_resident"]:
            breaches.append(
                f"{r['plugin']}: always-resident {r['always_resident_tokens']} tok "
                f"exceeds budget {opts['max_resident']}"
            )
        for h in r["hotspots"]:
            if h["exempt"]:
                continue
            if h["amplification"] <= opts["max_amplification"] or h["direct_citations"] <= opts["max_citations"]:
                continue
            breaches.append(
                f"{h['file']}: fan-out {h['amplification']}x — {h['own_tokens']} tok cites "
                f"{h['direct_tokens']} tok across {h['direct_citations']} files in one hop "
                f"(budget {opts['max_amplification']}x AND {opts['max_citations']} citations) "
                f"— read this site for a firing condition per link"
            )
        for s in r["skills"]:
            if s["no_flag_ceiling"] > opts["max_closure"]:
                breaches.append(
                    f"{r['plugin']}/{s['skill']}: no-flag ceiling {s['no_flag_ceiling']} tok "
                    f"exceeds {opts['max_closure']}"
                )

    if as_json:
        print(json.dumps({"budgets": opts, "reports": reports, "breaches": breaches}, indent=2))
        return 1 if breaches else 0

    for r in reports:
        print(f"\n{'='*78}\n{r['plugin']}  —  corpus {r['corpus_tokens']:,} tok\n{'='*78}")
        print(f"always resident : {r['always_resident_tokens']:,} tok  ({r['resident_share']}% of corpus)")
        print(f"                  the name+description of every skill and agent, paid on every request")
        print(f"\n{'skill':<18}{'spine':>7}{'usage':>7}{'phases':>8}{'rules':>8}{'mods':>7}{'ceiling':>9}{'ratio':>7}")
        print("-" * 78)
        for s in sorted(r["skills"], key=lambda x: -x["no_flag_ceiling"]):
            print(
                f"{s['skill']:<18}{s['spine']:>7,}{s['usage']:>7,}{s['phases']['tokens']:>8,}"
                f"{s['rules']['tokens']:>8,}{s['modules']['tokens']:>7,}"
                f"{s['no_flag_ceiling']:>9,}{s['disclosure_ratio']:>6}x"
            )
        print(f"\n  ceiling = spine + usage + all phases + everything they transitively reach")
        print(f"            (modules excluded — flag-gated, so they cost nothing by default)")
        print(f"  ratio   = corpus governed by the spine, per token of spine")

        print(f"\nfan-out hotspots — most weight cited from one file in a single hop:")
        print(f"\n{'file':<56}{'own':>6}{'cites':>7}{'tok':>8}{'x':>7}")
        print("-" * 84)
        for h in r["hotspots"][:top]:
            if h["exempt"]:
                flag = "  (spine — index by design)"
            elif h["amplification"] > opts["max_amplification"]:
                flag = "  <-- over budget"
            else:
                flag = ""
            print(
                f"{h['file']:<56}{h['own_tokens']:>6,}{h['direct_citations']:>7}"
                f"{h['direct_tokens']:>8,}{h['amplification']:>6}x{flag}"
            )

    if breaches:
        print(f"\n{len(breaches)} budget breach(es):\n")
        for b in breaches:
            print(f"  - {b}")
        print("\nA fan-out breach is a hotspot, not a verdict: read the citation site and decide")
        print("whether each link carries a firing condition. A routing index is allowed to be high;")
        print("a bare roster the executor must triage by filename is what this points at.")
    else:
        print("\nwithin every budget")
    return 1 if breaches else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
