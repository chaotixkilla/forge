#!/usr/bin/env python3
"""Scan a drafted developer-mode feedback report for project details before it is written.

Usage: check_feedback.py <draft.md>

feedback-on-praxis.md's "Nothing from the project" lists what an entry may not hold. This flags
the shapes of those details mechanically, so the check doesn't rest on a reading alone:
  - key:      a ticket-key shape (ABC-123) whose prefix praxis's own files never use;
  - number:   a review-request, pull-request or issue number (#12, "request 123", "PR 123"), never
              a report's own "Seen before: <file> #<n>";
  - hash:     a commit-hash shape (7 to 40 hex characters with a digit and a letter);
  - path:     an absolute or home-relative path;
  - address:  an email address or a URL whose host isn't praxis's own;
  - name:     a capitalised word, mid-sentence, that no praxis file uses capitalised: a person,
              product, vendor or project name until shown otherwise, and a job title (CTO, VP), which
              names a person's role. All-caps acronyms, months and praxis's codes (U2) pass.
The allowlist is praxis's own vocabulary, read from the plugin's markdown, so naming a backend
praxis ships an adapter for, or a praxis term, never trips it. The header line is skipped: its
fields are praxis's own.

It can't see, and the reading still owns: a relative project path, code or quoted text from the project,
names written in lowercase (handles, field names), all-caps organization or vendor names, single-digit
request numbers, and a vendor or key prefix that praxis's own files happen to mention.

Prints {"flags": [{"line", "kind", "token"}...]} and exits 1 when anything is flagged, 0 when nothing
is, 2 on a bad invocation and 3 when the draft can't be read. A flag is resolved by rewriting the
line in praxis's terms, never by editing this allowlist.
"""
import json
import os
import re
import sys

PLUGIN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

KEY = re.compile(r"\b([A-Z][A-Z0-9]{1,9})-(\d+)\b")
NUMBER = re.compile(r"((?<!\.md )#\d{2,}\b|\b(?:request|PR|MR|pull request|issue|ticket|change)\s+#?\d{2,}\b)", re.I)
HASH = re.compile(r"\b(?=[0-9a-f]*\d)(?=[0-9a-f]*[a-f])[0-9a-f]{7,40}\b")
PATH = re.compile(r"(?<![\w.])(?:~/|/(?:Users|home|var|opt|srv|etc|tmp|private)/)\S+")
EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
URL = re.compile(r"https?://([^/\s)]+)\S*")
WORD = re.compile(r"\b[A-Z][a-zA-Z0-9]+(?:[A-Z][a-zA-Z0-9]*)*\b")
# Job titles name a person's role, which a report may not hold; other all-caps words are acronyms or headings.
ROLES = {"CTO", "CEO", "CFO", "COO", "CIO", "CISO", "CPO", "VP", "SVP", "EVP"}
MONTHS = {"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Sept", "Oct", "Nov", "Dec",
          "January", "February", "March", "April", "June", "July", "August", "September", "October",
          "November", "December"}
CODE = re.compile(r"^[A-Z]\d+$")  # praxis's step and unit codes, such as C1 or U2
OWN_HOSTS = ("claude.ai", "claude.com", "anthropic.com", "github.com/chaotixkilla/forge")


def vocabulary():
    """Capitalised words and key prefixes praxis's own markdown uses."""
    words, prefixes = set(), set()
    for root, _, files in os.walk(PLUGIN):
        for name in files:
            if not name.endswith(".md"):
                continue
            try:
                with open(os.path.join(root, name), encoding="utf-8") as f:
                    text = f.read()
            except OSError:
                continue
            words.update(WORD.findall(text))
            prefixes.update(m.group(1) for m in KEY.finditer(text))
    return words, prefixes


def sentence_start(line, at):
    """True when the word at index at opens the line, a list item, or a sentence."""
    before = line[:at].rstrip(" *`_>([\"'")
    return not before or before.endswith((".", "!", "?", "-", "—", "|", "#")) or re.fullmatch(r"\s*(\d+\.)?", before) is not None


def scan(lines, words, prefixes):
    flags = []
    for n, line in enumerate(lines, 1):
        if n == 1 and line.startswith("praxis "):
            continue  # the header: version, act, round kind, install, harness
        for m in KEY.finditer(line):
            if m.group(1) not in prefixes:
                flags.append({"line": n, "kind": "key", "token": m.group(0)})
        flags += [{"line": n, "kind": "number", "token": m.group(0)} for m in NUMBER.finditer(line)]
        flags += [{"line": n, "kind": "hash", "token": m.group(0)} for m in HASH.finditer(line)]
        flags += [{"line": n, "kind": "path", "token": m.group(0)} for m in PATH.finditer(line)]
        flags += [{"line": n, "kind": "address", "token": m.group(0)} for m in EMAIL.finditer(line)]
        for m in URL.finditer(line):
            if not any(m.group(0).split("://", 1)[1].startswith(h) for h in OWN_HOSTS):
                flags.append({"line": n, "kind": "address", "token": m.group(0)})
        for m in WORD.finditer(line):
            w = m.group(0)
            if w in ROLES:
                flags.append({"line": n, "kind": "name", "token": w})
                continue
            if w.isupper() or w in MONTHS or CODE.match(w) or w in words:
                continue
            if not sentence_start(line, m.start()):
                flags.append({"line": n, "kind": "name", "token": m.group(0)})
    return flags


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            lines = f.read().splitlines()
    except (OSError, UnicodeDecodeError) as e:
        print(f"can't read {sys.argv[1]}: {e}", file=sys.stderr)
        return 3
    words, prefixes = vocabulary()
    flags = scan(lines, words, prefixes)
    json.dump({"flags": flags}, sys.stdout, indent=1)
    print()
    return 1 if flags else 0


if __name__ == "__main__":
    sys.exit(main())
