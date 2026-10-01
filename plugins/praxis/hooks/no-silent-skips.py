#!/usr/bin/env python3
"""praxis Stop hook: no silent skips.

While an act is running (its marker, .claude/praxis-act.json, exists), blocks
the end of a turn when a step was passed over without an honest outcome: a step
still pending while a later step has run, an outcome that isn't one of the
three, or a skip with no reason recorded. It blocks once per turn: when the
harness is already continuing because of a stop hook, the turn ends. On any
error the turn ends too.
"""
import json
import os
import sys

# The outcomes of the skip-only-with-a-reason rule, plus the state before a step runs.
OUTCOMES = {"pending", "ran", "skipped-by-act", "skipped-by-user"}


def problems(steps):
    last_done = max((i for i, s in enumerate(steps) if s.get("outcome", "pending") != "pending"), default=-1)
    found = []
    for i, step in enumerate(steps):
        name = step.get("step") or f"step {i + 1}"
        outcome = step.get("outcome", "pending")
        if outcome not in OUTCOMES:
            found.append(f"{name}: '{outcome}' isn't an outcome (ran, skipped-by-act or skipped-by-user)")
        elif outcome == "pending" and i < last_done:
            found.append(f"{name} has no outcome, but a later step has run")
        elif outcome.startswith("skipped") and not str(step.get("reason") or "").strip():
            found.append(f"{name} was skipped with no reason recorded")
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
        found = problems(json.load(f).get("steps") or [])
    if found:
        reason = ("The running act's checklist has steps without an honest outcome:\n- " + "\n- ".join(found)
                  + "\nRun each one, or record why it was skipped: the condition the act file names, "
                  "or the user's own reason. A step is never skipped silently.")
        json.dump({"decision": "block", "reason": reason}, sys.stdout)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
