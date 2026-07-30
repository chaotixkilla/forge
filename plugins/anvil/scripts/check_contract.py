#!/usr/bin/env python3
"""Deterministic half of anvil's plugin contract audit.

The contract audit asks two kinds of question. Most are judgment: is this piece in the slot that
matches its altitude, is this bar closed, is this capability a disguised tool. A few are not — they
are mechanical facts about the files, with exactly one right answer and no reading required:

  * does every relative markdown link resolve to a file that exists
  * is every phase reachable from its SKILL.md spine, and every rule reachable from some body file
  * does every frontmatter `name` obey the charset and match its own directory or filename

Those three are what this script owns. It exists because a model hand-executing a link-resolution
sweep over a few hundred files is slower, costs context, and — per the kit's own dogfood record —
gets the subdirectory-relative cases wrong in a way a resolver never does. The audit still reads the
judgment checks itself; this replaces the counting, not the thinking.

Usage:
    check_contract.py <plugin-dir> [<plugin-dir> ...] [--json] [--quiet]

Exit status:
    0  no findings
    1  findings present
    2  bad invocation (no such directory, nothing auditable)

Stdlib only, by design: it ships inside a plugin, so it may not assume an install step.
"""

from __future__ import annotations

import json
import os
import re
import sys

# A markdown inline link whose target is not a URL or a bare anchor. Group 1 is the target, with any
# #fragment already excluded so `file.md#L12` resolves against `file.md`.
LINK = re.compile(r"\[[^\]]*\]\(\s*(?!https?://|mailto:|#)([^)\s#]+)")

# An agent carrying no `tools:` allowlist is normally a defect: nothing at the interface holds it
# read-only. One case is legitimate and cannot be fixed by writing a better allowlist — a lane whose
# sources are reachable *only* through tools an allowlist categorically cannot admit, which must then
# carry the boundary as stated discipline. That exemption is earned by documenting it, never by
# omission: a `(basis: …)` marker that speaks to the envelope. An agent with no allowlist and no such
# note is still a finding, so silence never buys the exemption — only an argument the next maintainer
# can read and contest does.
ENVELOPE_BASIS = re.compile(r"\(basis:.{0,600}?\b(allowlist|envelope)\b", re.IGNORECASE | re.DOTALL)

# Authoring debris: fragments of the tool-call envelope an authoring session runs inside, left at the
# tail of a file when a write was captured with its wrapper. Every one of these shipped to consumers
# in this marketplace at least once — 21 files, one of them an always-resident SKILL.md — and passed
# every other check, because the files are structurally perfect and the junk is semantically inert.
# That is exactly why it needs a mechanical check: nothing about it looks wrong while reading.
DEBRIS = re.compile(
    r"^\s*</?(?:content|invoke|function_calls|function_results|antml:\w+)\b[^>]*>\s*$",
    re.IGNORECASE,
)

# Frontmatter `name:` values are dispatch identifiers, so the charset is narrow on purpose.
NAME_OK = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# Some of this kit's files document the citation form itself, and they do it by writing an example
# link. Those targets are meant to be unresolvable — they are shapes, not references — so flagging
# them would mean the checker reports its own documentation. A checker that cries wolf teaches the
# audit to ignore it, which is worse than not shipping one. Two markers make a target a shape:
# an angle-bracket slot (`<kind>`, `<skill>`, `<family>`), or one of the kit's literal placeholder
# stems (`name.md`, `NN-name.md`). Anything else that fails to resolve is a real finding — notably a
# plausible-looking filename that simply is not in this plugin, which is exactly the case a human
# reviewer misses and a resolver does not.
PLACEHOLDER = re.compile(r"[<>]|(?:^|/)(?:name|NN-name)\.md$")

# A numbered spine step in a SKILL.md body: "1. Do the thing — see [phases/01-x.md](...)"
SPINE_STEP = re.compile(r"^\s*\d+\.\s")

BODY_SLOTS = ("phases", "rules", "modules", "adapters")


class Finding:
    __slots__ = ("severity", "kind", "where", "detail")

    def __init__(self, severity: str, kind: str, where: str, detail: str) -> None:
        self.severity = severity
        self.kind = kind
        self.where = where
        self.detail = detail

    def as_dict(self) -> dict:
        return {"severity": self.severity, "kind": self.kind, "where": self.where, "detail": self.detail}


def read(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def frontmatter(text: str) -> dict:
    """Parse the top-level scalar keys of a leading --- fenced block. Nested blocks are ignored;
    this only needs `name`, `description`, and `tools`, all of which are top-level scalars."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    out: dict = {}
    for line in text[3:end].splitlines():
        if not line.strip() or line.startswith("#") or line[:1].isspace():
            continue
        key, sep, val = line.partition(":")
        if sep and key.strip():
            out[key.strip()] = val.strip()
    return out


def md_files(root: str) -> list[str]:
    found = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for fn in filenames:
            if fn.endswith(".md"):
                found.append(os.path.join(dirpath, fn))
    return sorted(found)


def strip_code(text: str) -> str:
    """Blank out fenced blocks and inline code spans.

    This mirrors the kit's own stated convention: a backticked path is *prose*, not a citation — the
    loader never follows it. So a link written inside backticks is an illustration of citation form,
    and treating it as a citation would make the checker flag the very files that document the rule.
    Spans are replaced with equal-length blanks so any offsets stay honest.
    """
    text = re.sub(r"```.*?```", lambda m: " " * len(m.group(0)), text, flags=re.S)
    # An inline span never crosses a line break. Anchoring it to one line matters: a pattern allowed
    # to span newlines will pair an unmatched backtick with the next one paragraphs away and blank
    # out every real citation in between — silently turning the checker into one that always passes.
    return re.sub(r"(`+)(?:(?!\1)[^\n])*\1", lambda m: " " * len(m.group(0)), text)


def links_in(path: str) -> list[str]:
    return LINK.findall(strip_code(read(path)))


def spine_of(skill_md: str) -> tuple[set[str], set[str]]:
    """Return (targets cited on numbered spine steps, targets cited anywhere in the body).

    The split matters: a phase must be reachable from the *spine* (the harness loads SKILL.md on
    trigger, and an uncited phase never loads), whereas usage.md must be reachable from the body but
    NOT from the spine — it is caller documentation, not a step the executor runs.
    """
    text = read(skill_md)
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            body = text[end + 4 :]
    spine: set[str] = set()
    everywhere: set[str] = set()
    for line in body.splitlines():
        targets = LINK.findall(line)
        everywhere.update(targets)
        if SPINE_STEP.match(line):
            spine.update(targets)
    return spine, everywhere


def audit_plugin(plugin_dir: str, findings: list[Finding]) -> dict:
    plugin_dir = os.path.abspath(plugin_dir.rstrip(os.sep))
    plugin = os.path.basename(plugin_dir)
    stats = {"plugin": plugin, "skills": 0, "agents": 0, "files": 0, "links": 0}

    def rel(p: str) -> str:
        return os.path.relpath(p, os.path.dirname(plugin_dir))

    # ---- link resolution, over every markdown file the plugin ships -------------------------
    all_md = md_files(plugin_dir)
    stats["files"] = len(all_md)
    for path in all_md:
        # authoring debris, checked on the raw text — it lives outside markdown structure, so the
        # code-stripping and placeholder rules below must not get a chance to excuse it
        for lineno, line in enumerate(read(path).splitlines(), 1):
            if DEBRIS.match(line):
                findings.append(
                    Finding(
                        "high",
                        "authoring-debris",
                        f"{rel(path)}:{lineno}",
                        f"tool-call envelope fragment left in a shipped file: {line.strip()!r}",
                    )
                )
        base = os.path.dirname(path)
        for target in links_in(path):
            if PLACEHOLDER.search(target):
                stats["placeholders"] = stats.get("placeholders", 0) + 1
                continue
            stats["links"] += 1
            resolved = os.path.normpath(os.path.join(base, target))
            if not os.path.exists(resolved):
                findings.append(
                    Finding(
                        "high",
                        "dangling-link",
                        rel(path),
                        f"link target does not resolve: {target!r} -> {rel(resolved)}",
                    )
                )

    # ---- per-skill reachability and frontmatter ---------------------------------------------
    skills_root = os.path.join(plugin_dir, "skills")
    if os.path.isdir(skills_root):
        for name in sorted(os.listdir(skills_root)):
            sdir = os.path.join(skills_root, name)
            skill_md = os.path.join(sdir, "SKILL.md")
            if not os.path.isdir(sdir) or not os.path.isfile(skill_md):
                if os.path.isdir(sdir):
                    findings.append(Finding("high", "missing-skill-md", rel(sdir), "no SKILL.md"))
                continue
            stats["skills"] += 1

            fm = frontmatter(read(skill_md))
            declared = fm.get("name", "")
            if not declared:
                findings.append(Finding("high", "frontmatter", rel(skill_md), "no `name` in frontmatter"))
            elif declared != name:
                findings.append(
                    Finding("high", "frontmatter", rel(skill_md), f"name {declared!r} != directory {name!r}")
                )
            elif not NAME_OK.match(declared):
                findings.append(
                    Finding("medium", "frontmatter", rel(skill_md), f"name {declared!r} is not lower-kebab-case")
                )
            if not fm.get("description"):
                findings.append(Finding("high", "frontmatter", rel(skill_md), "no `description` in frontmatter"))

            spine, everywhere = spine_of(skill_md)

            def cited(target_rel: str, pool: set[str]) -> bool:
                """A citation counts only if it resolves to this exact file from the SKILL.md dir."""
                want = os.path.normpath(os.path.join(sdir, target_rel))
                return any(os.path.normpath(os.path.join(sdir, t)) == want for t in pool)

            # phases: reachable from the spine, or they never load
            phase_dir = os.path.join(sdir, "phases")
            if os.path.isdir(phase_dir):
                for pf in sorted(os.listdir(phase_dir)):
                    if not pf.endswith(".md"):
                        continue
                    if not cited(os.path.join("phases", pf), spine):
                        where = rel(os.path.join(phase_dir, pf))
                        if cited(os.path.join("phases", pf), everywhere):
                            findings.append(
                                Finding("medium", "phase-off-spine", where, "cited in the body but not on a numbered spine step")
                            )
                        else:
                            findings.append(
                                Finding("high", "unreferenced-phase", where, "no SKILL.md citation — this phase never loads")
                            )

            # rules and modules: reachable from any body file in the skill
            body_pool = [skill_md]
            for slot in BODY_SLOTS:
                d = os.path.join(sdir, slot)
                if os.path.isdir(d):
                    body_pool.extend(md_files(d))
            inbound: set[str] = set()
            for bf in body_pool:
                bbase = os.path.dirname(bf)
                for t in links_in(bf):
                    inbound.add(os.path.normpath(os.path.join(bbase, t)))

            for slot, kind in (("rules", "orphaned-rule"), ("modules", "orphaned-module")):
                d = os.path.join(sdir, slot)
                if not os.path.isdir(d):
                    continue
                for rf in md_files(d):
                    if os.path.normpath(rf) not in inbound:
                        findings.append(
                            Finding("medium", kind, rel(rf), f"no citation from any body file in {name} — never loads")
                        )

            # usage.md: present, referenced off-spine, never as a spine step
            usage = os.path.join(sdir, "usage.md")
            if not os.path.isfile(usage):
                findings.append(Finding("medium", "missing-usage", rel(sdir), "skill ships no usage.md"))
            else:
                on_spine = cited("usage.md", spine)
                anywhere = cited("usage.md", everywhere)
                if on_spine:
                    findings.append(
                        Finding("medium", "usage-on-spine", rel(skill_md), "usage.md cited as a numbered spine step; it is caller docs, not a phase")
                    )
                elif not anywhere:
                    findings.append(
                        Finding("medium", "usage-unreferenced", rel(skill_md), "no non-spine pointer to usage.md")
                    )

    # ---- agents: name matches filename, tools declared --------------------------------------
    agents_root = os.path.join(plugin_dir, "agents")
    if os.path.isdir(agents_root):
        for af in md_files(agents_root):
            stats["agents"] += 1
            body = read(af)
            fm = frontmatter(body)
            stem = os.path.splitext(os.path.basename(af))[0]
            declared = fm.get("name", "")
            if not declared:
                findings.append(Finding("high", "frontmatter", rel(af), "agent has no `name`"))
            elif declared != stem:
                findings.append(Finding("high", "frontmatter", rel(af), f"name {declared!r} != filename stem {stem!r}"))
            if not fm.get("description"):
                findings.append(Finding("high", "frontmatter", rel(af), "agent has no `description`"))
            if not fm.get("tools") and not ENVELOPE_BASIS.search(body):
                findings.append(
                    Finding(
                        "medium",
                        "agent-envelope",
                        rel(af),
                        "no `tools:` allowlist and no `(basis: …)` note addressing the envelope — "
                        "the read-only boundary is neither enforced nor argued for",
                    )
                )
    return stats


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    as_json = "--json" in argv
    quiet = "--quiet" in argv
    if not args:
        sys.stderr.write(__doc__ or "")
        return 2

    findings: list[Finding] = []
    all_stats = []
    for target in args:
        if not os.path.isdir(target):
            sys.stderr.write(f"not a directory: {target}\n")
            return 2
        all_stats.append(audit_plugin(target, findings))

    order = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda f: (order.get(f.severity, 9), f.kind, f.where))

    if as_json:
        print(json.dumps({"stats": all_stats, "findings": [f.as_dict() for f in findings]}, indent=2))
    elif not quiet:
        for s in all_stats:
            print(
                f"{s['plugin']}: {s['skills']} skills, {s['agents']} agents, "
                f"{s['files']} md files, {s['links']} links checked"
            )
        if not findings:
            print("\nno findings — links resolve, every body file is reachable, frontmatter is well-formed")
        else:
            print(f"\n{len(findings)} finding(s):\n")
            for f in findings:
                print(f"  [{f.severity:6}] {f.kind:20} {f.where}")
                print(f"           {f.detail}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
