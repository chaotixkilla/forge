#!/usr/bin/env python3
"""praxis SessionStart hook.

In a project with praxis settings (.claude/praxis.json), removes the task lines
from the memory index whose task is closed or has been idle past the idle
period, then gives the session praxis's guidance. It never blocks: on any
error it exits 0, and the session starts as it would without praxis.
"""
import datetime
import json
import os
import re
import sys

# The idle period from the keep-the-task-memory-entry rule (routed to the maintainer).
IDLE_DAYS = 14

GUIDANCE = (
    "praxis is set up in this project. For software engineering work (building, fixing, "
    "reviewing, shipping, responding to incidents, maintaining, researching, prototyping, "
    "auditing, learning), start with the praxis work skill. When the "
    "work asks for one specific step, such as reviewing a diff or debugging a failure, use that "
    "praxis skill directly. Either way, a skill's phase files and rules are the procedure: follow "
    "them instead of working from memory, and don't skip a step without recording why. Quick "
    "questions that produce nothing to review or keep can be answered directly."
)

# The standing posture for code comments, from output.comments (craft's report-style-settings rule),
# stated here because most comments are written outside a praxis run.
COMMENTS = {
    "why-only": "Code comments in this project: write one only where the code cannot carry the meaning itself.",
    "match-codebase": "Code comments in this project: follow the comment density of the surrounding file.",
}


def postures(cwd):
    """The standing postures the config sets for work outside a praxis run; the default when unreadable."""
    value = "why-only"
    try:
        with open(os.path.join(cwd, ".claude", "praxis.json"), encoding="utf-8") as f:
            value = (json.load(f).get("output") or {}).get("comments") or value
    except (OSError, ValueError, AttributeError):
        pass
    return COMMENTS.get(str(value), COMMENTS["why-only"])


TASK_LINE = re.compile(r"^\s*-\s*\[task:[^\]]*\]\(([^)]+)\)")
FIELD = re.compile(r"^\s*(status|updated):\s*(.+?)\s*$", re.M)


def stale(entry_path, today):
    """A task is stale when it's closed or was last updated more than IDLE_DAYS ago.
    An entry that can't be read or dated is left alone."""
    try:
        with open(entry_path, encoding="utf-8") as f:
            fields = dict(FIELD.findall(f.read()))
    except OSError:
        return False
    if fields.get("status", "").lower().startswith("closed"):
        return True
    try:
        updated = datetime.date.fromisoformat(fields.get("updated", "")[:10])
    except ValueError:
        return False
    return (today - updated).days > IDLE_DAYS


def trim_task_lines(memory_dir, today):
    index = os.path.join(memory_dir, "MEMORY.md")
    if not os.path.isfile(index):
        return
    with open(index, encoding="utf-8") as f:
        lines = f.readlines()
    kept = [line for line in lines
            if not ((m := TASK_LINE.match(line)) and stale(os.path.join(memory_dir, m.group(1)), today))]
    if len(kept) != len(lines):
        tmp = index + ".praxis-tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.writelines(kept)
        os.replace(tmp, index)


def main():
    try:
        event = json.load(sys.stdin)
    except ValueError:
        event = {}
    cwd = os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or os.getcwd()
    if not os.path.isfile(os.path.join(cwd, ".claude", "praxis.json")):
        return
    transcript = event.get("transcript_path") or ""
    if transcript:
        # The harness keeps a project's memory beside its session transcripts.
        try:
            trim_task_lines(os.path.join(os.path.dirname(transcript), "memory"), datetime.date.today())
        except OSError:
            pass
    context = GUIDANCE + " " + postures(cwd)
    json.dump({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}}, sys.stdout)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
