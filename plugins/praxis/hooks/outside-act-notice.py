#!/usr/bin/env python3
"""praxis PostToolUse hook: outside-act notice.

In a project set up for praxis, when a praxis skill is invoked and this session runs
no act (it has no readable marker, a JSON object naming its task, at
.claude/praxis/acts/<session-id>.json in the repository's main checkout), adds a note for the model. After a step skill, the note
offers to file the step's result into a task, an open one or a new one, so the work
leaves a record. After work, and after a step, it states this session's id, under
which an act writes its marker, so the act can write one when session start stated
none. When the marker file exists but can't be read as one, the note says so instead
of the offer. When this session's act marker records no answer to the act's proposal
and the skill is one of its steps, the note says no step runs before it's
settled. It never blocks; on any error, and when the event names no usable
session id, it stays silent.
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Skills that aren't steps: the orchestrator, documentation, setup and the ports.
NOT_STEPS = {"work", "document", "init", "vcs", "ci", "knowledge", "project-mgmt", "communication",
             "telemetry", "artifacts", "gather"}
SESSION = re.compile(r"^[A-Za-z0-9_-]+$")
NOTE = ("This praxis step is running outside an act, so its result won't be filed anywhere. When it "
        "finishes, offer to file the result into a task: an open one (work --task=<key>) or a new one.")
UNREADABLE = ("This session's act marker, {0}, exists but can't be read as a marker, "
              "so no act counts as running in this session. Resume its task with work --task=<key> to write "
              "it again, or remove it.")
SESSION_ID = "This session's id is {0}: an act run in it keeps its marker at {1}."
UNANSWERED = ("This session's act for {0} has no answer to its proposal recorded, and {1} is one of its steps: "
              "no step runs before the proposal is settled. Show the act's steps, asking only when run-the-act's list "
              "calls for it (a rework always asks; a revision of one doesn't), and record when in the marker's answered before running any step.")


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

def plugin_name():
    try:
        with open(os.path.join(ROOT, ".claude-plugin", "plugin.json"), encoding="utf-8") as f:
            return json.load(f).get("name") or "praxis"
    except (OSError, ValueError):
        return "praxis"


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


def main():
    event = json.load(sys.stdin)
    if event.get("tool_name") != "Skill":
        return
    session = str(event.get("session_id") or "")
    if not SESSION.match(session):
        return
    skill = str((event.get("tool_input") or {}).get("skill") or "")
    prefix = plugin_name() + ":"
    if not skill.startswith(prefix):
        return
    root = state_root(os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or os.getcwd())
    if root is None:
        return
    project = os.path.realpath(root)
    if not os.path.isfile(os.path.join(project, ".claude", "praxis.json")):
        return
    marker = os.path.join(project, ".claude", "praxis", "acts", session + ".json")
    name = skill[len(prefix):]
    running = read_marker(marker)
    if running:
        steps = running.get("steps") if isinstance(running.get("steps"), list) else []
        mine = any(str(s.get("step") or "").split(":", 1)[-1] == name for s in steps if isinstance(s, dict))
        if mine and not str(running.get("answered") or "").strip():
            note = UNANSWERED.format(str(running["task"]).strip(), plugin_name() + ":" + name)
            json.dump({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": note}},
                      sys.stdout)
        return
    step = name not in NOT_STEPS and os.path.isdir(os.path.join(ROOT, "skills", name))
    if name != "work" and not step:
        return
    parts = []
    if os.path.exists(marker):
        parts.append(UNREADABLE.format(marker))
    elif step:
        parts.append(NOTE)
    parts.append(SESSION_ID.format(session, marker))
    json.dump({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": " ".join(parts)}},
              sys.stdout)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
