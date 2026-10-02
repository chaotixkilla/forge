#!/usr/bin/env python3
"""praxis Stop hook: context-sync check.

While this session runs an act (its marker, .claude/praxis/acts/<session-id>.json,
is a JSON object naming its task, the test the edit guard uses), blocks the end of
a turn when work isn't in the task's documentation: a step ran but its result was
neither filed nor written to the task's unfiled directory, or close-out delivered
something but the record of where it went was neither filed nor written there. An
unfiled entry counts only when it names its own file, as work's keep-the-act-marker
rule names it, and that file exists: <row>-<skill>.md in .claude/praxis/unfiled/<task>/
for a step keyed "<row>:<skill>", and delivery.md there for the delivery. Other
sessions' markers are never read. Work that isn't in the documentation is work
the next session can't see. It blocks once per turn: when the harness is already
continuing because of a stop hook, the turn ends. On any error, an unreadable
marker or an event with no usable session id included, the turn ends too.
"""
import json
import os
import re
import sys

SESSION = re.compile(r"^[A-Za-z0-9_-]+$")


def read_marker(path):
    """The marker at path when it is a JSON object naming its task, else None."""
    try:
        with open(path, encoding="utf-8") as f:
            marker = json.load(f)
    except (OSError, ValueError):
        return None
    if isinstance(marker, dict) and str(marker.get("task") or "").strip():
        return marker
    return None


def own_file(project, task, name):
    """The real path of the unfiled file named name in this task's unfiled directory, else ''.
    A step keyed "1:understand" files as 1-understand.md, and the delivery as delivery.md."""
    name = str(name or "").replace(":", "-")
    root = os.path.realpath(os.path.join(project, ".claude", "praxis", "unfiled"))
    folder = os.path.realpath(os.path.join(root, task))
    if not name or os.sep in name or not folder.startswith(root + os.sep):
        return ""
    return os.path.join(folder, name + ".md")


def unfiled_own(project, task, name, value):
    """True when value names this entry's own unfiled file and that file exists."""
    value = str(value or "").strip()
    expected = own_file(project, task, name)
    if not value or not expected:
        return False
    return os.path.isfile(expected) and os.path.realpath(os.path.join(project, value)) == os.path.realpath(expected)


def recorded(project, task, name, entry):
    return entry.get("filed") is True or unfiled_own(project, task, name, entry.get("unfiled"))


def unsynced(project, marker):
    task = str(marker["task"]).strip()
    folder = f".claude/praxis/unfiled/{task}/"
    found = []
    steps = marker.get("steps")
    for i, step in enumerate(steps if isinstance(steps, list) else []):
        if step.get("outcome") != "ran" or recorded(project, task, step.get("step"), step):
            continue
        name = step.get("step") or f"step {i + 1}"
        if str(step.get("unfiled") or "").strip():
            own = str(step.get("step") or "").replace(":", "-")
            found.append(f"{name}: its unfiled entry names no existing {folder}{own or '<row>-<skill>'}.md, "
                         "the step's own file")
        else:
            found.append(f"{name}: its result is neither filed nor written to {folder}")
    delivery = marker.get("delivery") or {}
    if delivery.get("channels") and not recorded(project, task, "delivery", delivery):
        if str(delivery.get("unfiled") or "").strip():
            found.append(f"the delivery: its unfiled entry names no existing {folder}delivery.md, "
                         "the delivery's own file")
        else:
            found.append("the delivery: close-out delivered, but where each part went is neither filed in the "
                         f"task's record nor written to {folder}")
    return found


def main():
    event = json.load(sys.stdin)
    if event.get("stop_hook_active"):
        return
    session = str(event.get("session_id") or "")
    if not SESSION.match(session):
        return
    project = os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or os.getcwd()
    marker = read_marker(os.path.join(project, ".claude", "praxis", "acts", session + ".json"))
    if not marker:
        return
    found = unsynced(project, marker)
    if found:
        reason = ("This act's work isn't all in the task's documentation:\n- " + "\n- ".join(found)
                  + "\nHand each to document. When document can't file it, write what it hands back to the "
                  "task's unfiled directory and record that path in the marker, so the next session can "
                  "file it.")
        json.dump({"decision": "block", "reason": reason}, sys.stdout)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
