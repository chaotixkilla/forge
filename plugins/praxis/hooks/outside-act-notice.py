#!/usr/bin/env python3
"""praxis PostToolUse hook: outside-act notice.

When a praxis step skill is invoked in a project set up for praxis and no act is
running, adds a note for the model: once the step finishes, offer to file its
result into a task — an open one, or a new one — so the work leaves a record.
It never blocks; on any error it stays silent.
"""
import json
import os
import sys

ROOT = os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Skills that aren't steps: the orchestrator, documentation, setup and the ports.
NOT_STEPS = {"work", "document", "init", "vcs", "ci", "knowledge", "project-mgmt", "communication",
             "telemetry", "artifacts", "gather"}
NOTE = ("This praxis step is running outside an act, so its result won't be filed anywhere. When it "
        "finishes, offer to file the result into a task: an open one (work --task=<key>) or a new one.")


def plugin_name():
    try:
        with open(os.path.join(ROOT, ".claude-plugin", "plugin.json"), encoding="utf-8") as f:
            return json.load(f).get("name") or "praxis"
    except (OSError, ValueError):
        return "praxis"


def main():
    event = json.load(sys.stdin)
    if event.get("tool_name") != "Skill":
        return
    project = os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or os.getcwd()
    if not os.path.isfile(os.path.join(project, ".claude", "praxis.json")):
        return
    if os.path.isfile(os.path.join(project, ".claude", "praxis-act.json")):
        return
    skill = str((event.get("tool_input") or {}).get("skill") or "")
    prefix = plugin_name() + ":"
    if not skill.startswith(prefix):
        return
    name = skill[len(prefix):]
    if name in NOT_STEPS or not os.path.isdir(os.path.join(ROOT, "skills", name)):
        return
    json.dump({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": NOTE}}, sys.stdout)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
