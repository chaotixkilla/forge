#!/usr/bin/env python3
"""praxis Stop hook: context-sync check.

While an act is running (its marker, .claude/praxis-act.json, exists), blocks
the end of a turn when a step ran but its result was neither filed in the
task's documentation nor recorded as unfiled with a reason. Work that isn't in
the documentation is work the next session can't see. It blocks once per turn:
when the harness is already continuing because of a stop hook, the turn ends.
On any error the turn ends too.
"""
import json
import os
import sys


def unsynced(steps):
    found = []
    for i, step in enumerate(steps):
        if step.get("outcome") != "ran":
            continue
        name = step.get("step") or f"step {i + 1}"
        filed = step.get("filed")
        if filed is True:
            continue
        if filed is False and str(step.get("unfiled") or "").strip():
            continue
        found.append(name)
    return found


def main():
    event = json.load(sys.stdin)
    if event.get("stop_hook_active"):
        return
    project = os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or os.getcwd()
    marker = os.path.join(project, ".claude", "praxis-act.json")
    if not os.path.isfile(marker):
        return
    with open(marker, encoding="utf-8") as f:
        found = unsynced(json.load(f).get("steps") or [])
    if found:
        reason = ("These steps ran, but their results aren't in the task's documentation: "
                  + ", ".join(found) + ". Hand each result to document, or record why it couldn't be "
                  "filed, so the task's documentation matches what was done.")
        json.dump({"decision": "block", "reason": reason}, sys.stdout)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
