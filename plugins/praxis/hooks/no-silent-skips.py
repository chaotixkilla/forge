#!/usr/bin/env python3
"""praxis Stop hook: no silent skips.

While this session runs an act (its marker in the repository's main checkout,
.claude/praxis/acts/<session-id>.json, is a JSON object naming its task), blocks the end of a turn when a step was passed
over without an honest outcome: a step still pending while a later step has run, a
step still pending whose result waits in the task's unfiled directory (it has ended,
so it must not run again), an outcome that isn't one of the three, a skip with no
reason recorded, or a step given an outcome while the marker records no answer to
the act's proposal (steps run only once it is settled). Other sessions'
markers are never read. It blocks once per turn: when the harness is already
continuing because of a stop hook, the turn ends. On any error, an unreadable marker
or an event with no usable session id included, the turn ends too.
"""
import json
import os
import re
import subprocess
import sys

# The outcomes of the skip-only-with-a-reason rule, plus the state before a step runs.
OUTCOMES = {"pending", "ran", "skipped-by-act", "skipped-by-user"}
SESSION = re.compile(r"^[A-Za-z0-9_-]+$")


def state_root(start):
    """Where praxis keeps this project's config and act markers (init's write-and-validate): the parent
    of the repository's git folder when that is named .git, so every worktree shares them. start itself
    outside a repository, when git's folder has another name (as a bare repository's, a submodule's or a
    separate git dir's usually does), or when only start holds a config, as an older praxis set up in a
    subfolder. None when git doesn't answer within five seconds (a healthy one answers in milliseconds),
    so the caller stays silent rather than read the wrong place."""
    try:
        done = subprocess.run(["git", "-C", start, "rev-parse", "--git-common-dir"],
                              capture_output=True, text=True, timeout=5)
    except subprocess.TimeoutExpired:
        return None
    except (OSError, subprocess.SubprocessError):
        return start
    common = done.stdout.strip()
    if done.returncode or not common or "\n" in common:
        return start
    common = os.path.normpath(os.path.join(start, common))
    root, config = os.path.dirname(common), os.path.join(".claude", "praxis.json")
    if os.path.basename(common) != ".git" or (not os.path.isfile(os.path.join(root, config))
                                              and os.path.isfile(os.path.join(start, config))):
        return start
    return root

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


def waiting(project, task, name):
    """The project-relative path of a step's unfiled result when that file exists, else ''.
    A step keyed "1:understand" files as .claude/praxis/unfiled/<task>/1-understand.md."""
    root = os.path.realpath(os.path.join(project, ".claude", "praxis", "unfiled"))
    folder = os.path.realpath(os.path.join(root, task))
    path = os.path.join(folder, str(name).replace(":", "-") + ".md")
    if name and folder.startswith(root + os.sep) and os.sep not in str(name) and os.path.isfile(path):
        return os.path.relpath(path, os.path.realpath(project))
    return ""


def problems(project, task, steps, answered):
    last_done = max((i for i, s in enumerate(steps) if s.get("outcome", "pending") != "pending"), default=-1)
    found = []
    if last_done >= 0 and not answered:
        found.append("steps have outcomes, but the marker records no answer to the act's proposal: steps run "
                     "only once it's settled, so show the act's steps, asking only when run-the-act's list calls for it "
                     "(a rework always asks), and record when in the marker's answered")
    for i, step in enumerate(steps):
        name = step.get("step") or f"step {i + 1}"
        outcome = step.get("outcome", "pending")
        if outcome not in OUTCOMES:
            found.append(f"{name}: '{outcome}' isn't an outcome (ran, skipped-by-act or skipped-by-user)")
        elif outcome == "pending" and (copy := waiting(project, task, step.get("step") or "")):
            found.append(f"{name} has its result waiting at {os.path.join(project, copy)}, so it has ended: record "
                         f"it as ran, or as the skip that file records, with {copy} as its unfiled and its failure that "
                         "it waits from an earlier session, rather than running it again")
        elif outcome == "pending" and i < last_done:
            found.append(f"{name} has no outcome, but a later step has run")
        elif outcome.startswith("skipped") and not str(step.get("reason") or "").strip():
            found.append(f"{name} was skipped with no reason recorded")
    return found


def main():
    event = json.load(sys.stdin)
    if event.get("stop_hook_active"):
        return
    session = str(event.get("session_id") or "")
    if not SESSION.match(session):
        return
    root = state_root(os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or os.getcwd())
    if root is None:
        return
    project = os.path.realpath(root)
    marker = read_marker(os.path.join(project, ".claude", "praxis", "acts", session + ".json"))
    if not marker:
        return
    steps = marker.get("steps")
    found = problems(project, str(marker["task"]).strip(), steps if isinstance(steps, list) else [],
                     str(marker.get("answered") or "").strip())
    if found:
        reason = ("The running act's checklist has steps without an honest outcome:\n- " + "\n- ".join(found)
                  + "\nRun each step, record the outcome its waiting "
                  "result gives it, or record why it was skipped: the condition the act file names, or the "
                  "user's own reason. None is skipped silently.")
        json.dump({"decision": "block", "reason": reason}, sys.stdout)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
