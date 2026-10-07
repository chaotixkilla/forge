#!/usr/bin/env python3
"""praxis PostToolUse hook: outside-act notice.

In a project set up for praxis, when a praxis skill is invoked and this session runs
no act (it has no readable marker at .claude/praxis/acts/<session-id>.json: a JSON
object naming its task), adds a note for the model. After a step skill, the note
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
import sys

ROOT = os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Skills that aren't steps: the orchestrator, documentation, setup and the ports.
NOT_STEPS = {"work", "document", "init", "vcs", "ci", "knowledge", "project-mgmt", "communication",
             "telemetry", "artifacts", "gather"}
SESSION = re.compile(r"^[A-Za-z0-9_-]+$")
NOTE = ("This praxis step is running outside an act, so its result won't be filed anywhere. When it "
        "finishes, offer to file the result into a task: an open one (work --task=<key>) or a new one.")
UNREADABLE = ("This session's act marker, .claude/praxis/acts/{0}.json, exists but can't be read as a marker, "
              "so no act counts as running in this session. Resume its task with work --task=<key> to write "
              "it again, or remove it.")
SESSION_ID = "This session's id is {0}: an act run in it keeps its marker at .claude/praxis/acts/{0}.json."
UNANSWERED = ("This session's act for {0} has no answer to its proposal recorded, and {1} is one of its steps: "
              "no step runs before the proposal is settled. Show the act's steps, asking only when run-the-act's list "
              "calls for it (a rework always asks), and record when in the marker's answered before running any step.")


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
    project = os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or os.getcwd()
    if not os.path.isfile(os.path.join(project, ".claude", "praxis.json")):
        return
    session = str(event.get("session_id") or "")
    if not SESSION.match(session):
        return
    marker = os.path.join(project, ".claude", "praxis", "acts", session + ".json")
    skill = str((event.get("tool_input") or {}).get("skill") or "")
    prefix = plugin_name() + ":"
    if not skill.startswith(prefix):
        return
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
        parts.append(UNREADABLE.format(session))
    elif step:
        parts.append(NOTE)
    parts.append(SESSION_ID.format(session))
    json.dump({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": " ".join(parts)}},
              sys.stdout)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
