#!/usr/bin/env python3
"""praxis Stop hook: phase-read check.

Blocks the end of a turn when a praxis skill with phase files was invoked since the
user's last message, as a skill call or a slash command, and its procedure wasn't
read through at any point in the session: for a skill that carries no acts, its
final phase file, the one a run that reaches its result reads, was never read; for
an orchestrator (a skill that carries acts), whose routing can end at its first
phase by handing a lone step on, none of its phase files was. Either is the sign of
a skill run from memory instead of from its procedure. A run its own procedure
stopped earlier (a dry run, a refusal, a gate, a question to the user) is blocked
once, and the reason asks the model to name the phase that stopped it; checking only
this turn's invocations keeps that to one block. For a skill without acts, a shell
command counts as a read of its final phase when it names the file, or globs the
skill's phases with anything but a listing. It blocks once per turn, and on any
error the turn ends.
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


def final_phase(skill):
    """The skill's last phase file by name, or '' for an orchestrator, which any phase read satisfies."""
    folder = os.path.join(ROOT, "skills", skill)
    if os.path.isdir(os.path.join(folder, "acts")):
        return ""
    names = sorted(n for n in os.listdir(os.path.join(folder, "phases")) if n.endswith(".md"))
    return names[-1] if names else ""


def reads_final(tool, args, skill, final):
    text = args.get("file_path") or args.get("path") or args.get("command") or ""
    if not isinstance(text, str):
        return False
    if re.search(r"(?:^|[\s/\"'=])" + re.escape(skill) + r"/phases/" + re.escape(final), text):
        return True
    if tool != "Bash" or f"skills/{skill}" not in text:
        return False
    listing = re.match(r"\s*(?:cd\s+\S+\s*(?:&&|;)\s*)?ls\b", text)
    return final in text or (bool(re.search(r"phases/\*", text)) and not listing)


def read_through(skill, calls):
    final = final_phase(skill)
    if final:
        return any(reads_final(tool, args, skill, final) for tool, args in calls)
    return any(reads_phases(tool, args, skill) for tool, args in calls)


def prompt(entry):
    """True for a message the user sent: where this turn's work begins. Tool results and the
    harness's own injected entries (a loaded skill's body, marked isMeta) aren't."""
    if not isinstance(entry, dict) or entry.get("type") != "user" or entry.get("isMeta"):
        return False
    content = (entry.get("message") or {}).get("content")
    if isinstance(content, str):
        return True
    return isinstance(content, list) and not any(
        isinstance(c, dict) and c.get("type") == "tool_result" for c in content)


def unread(transcript, plugin):
    command = re.compile(r"<command-name>/?" + re.escape(plugin) + r":([a-z0-9-]+)</command-name>")
    invoked, calls = set(), []
    with open(transcript, encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                entry = json.loads(line)
            except ValueError:
                continue
            if prompt(entry):
                invoked = set()
            invoked.update(command.findall(line))
            for tool, args in tool_uses(entry):
                if tool == "Skill" and str(args.get("skill") or "").startswith(plugin + ":"):
                    invoked.add(str(args["skill"]).split(":", 1)[1])
                elif tool in ("Read", "Bash"):
                    calls.append((tool, args))
    return sorted(s for s in invoked
                  if os.path.isdir(os.path.join(ROOT, "skills", s, "phases"))
                  and not read_through(s, calls))


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
        reason = (f"{names} ran without its procedure read through: its final phase (any phase, for an "
                  "orchestrator) was never read. A skill's phases are its procedure: read each one the run "
                  "reaches, and do the work as they say, instead of from memory. If the procedure itself "
                  "stopped the run before its final phase (a dry run, a refusal, a gate, or a question to "
                  "the user), say which phase stopped it and why; when it waits on the user's answer, end "
                  "the turn there without going on.")
        json.dump({"decision": "block", "reason": reason}, sys.stdout)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
