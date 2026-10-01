#!/usr/bin/env python3
"""praxis Stop hook: phase-read check.

Blocks the end of a turn when a praxis skill with phase files was invoked in
this session, as a skill call or a slash command, and none of its phase files
has been read at any point in the session: the sign of a skill run from memory
instead of from its procedure. It blocks once per turn, and on any error the
turn ends.
"""
import json
import os
import re
import sys

ROOT = os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def plugin_name():
    try:
        with open(os.path.join(ROOT, ".claude-plugin", "plugin.json"), encoding="utf-8") as f:
            return json.load(f).get("name") or "praxis"
    except (OSError, ValueError):
        return "praxis"


def tool_uses(node):
    """Every tool call in a transcript entry, however deeply it's nested."""
    if isinstance(node, dict):
        if node.get("type") == "tool_use":
            yield node.get("name"), node.get("input") or {}
        for value in node.values():
            yield from tool_uses(value)
    elif isinstance(node, list):
        for value in node:
            yield from tool_uses(value)


def reads_phases(tool, args, skill):
    text = args.get("file_path") or args.get("path") or args.get("command") or ""
    if not isinstance(text, str):
        return False
    if re.search(r"(?:^|[\s/\"'=])" + re.escape(skill) + r"/phases/", text):
        return True
    # A shell read from inside the skill's directory: `cd …/skills/<skill> && cat phases/…`.
    return tool == "Bash" and f"skills/{skill}" in text and "phases/" in text


def unread(transcript, plugin):
    command = re.compile(r"<command-name>/?" + re.escape(plugin) + r":([a-z0-9-]+)</command-name>")
    invoked, calls = set(), []
    with open(transcript, encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
            except ValueError:
                continue
            invoked.update(command.findall(line))
            for tool, args in tool_uses(entry):
                if tool == "Skill" and str(args.get("skill") or "").startswith(plugin + ":"):
                    invoked.add(str(args["skill"]).split(":", 1)[1])
                elif tool in ("Read", "Bash"):
                    calls.append((tool, args))
    return sorted(s for s in invoked
                  if os.path.isdir(os.path.join(ROOT, "skills", s, "phases"))
                  and not any(reads_phases(tool, args, s) for tool, args in calls))


def main():
    event = json.load(sys.stdin)
    if event.get("stop_hook_active"):
        return
    transcript = event.get("transcript_path") or ""
    if not os.path.isfile(transcript):
        return
    plugin = plugin_name()
    missed = unread(transcript, plugin)
    if missed:
        names = ", ".join(f"{plugin}:{s}" for s in missed)
        reason = (f"{names} ran without any of its phase files being read. A skill's phases are its "
                  "procedure: read them, and do the work as they say, instead of from memory.")
        json.dump({"decision": "block", "reason": reason}, sys.stdout)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
