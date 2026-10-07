#!/usr/bin/env python3
"""praxis Stop hook: context-sync check.

While this session runs an act (its marker, .claude/praxis/acts/<session-id>.json,
is a JSON object naming its task), blocks the end of a turn when work isn't in the
task's documentation: a step ended (ran or skipped) but what it hands the record was
neither filed nor written to the task's unfiled directory; a step's skill was
invoked after the act's proposal was answered (the marker's answered, against the
transcript's timestamps) while the marker still holds that step pending, so its
result reached only the conversation; or close-out delivered something but the
record of where it went was neither filed nor written there. An unfiled entry counts
only when it names its own file, as work's keep-the-act-marker rule names it, that
file exists, and the entry records the failure that put it there: <row>-<skill>.md
in .claude/praxis/unfiled/<task>/ for a step keyed "<row>:<skill>", and delivery.md
there for the delivery. Other sessions' markers are never read. Work that isn't in
the documentation is work the next session can't see. It blocks once per turn: when
the harness is already continuing because of a stop hook, the turn ends. On any
error, an unreadable marker or an event with no usable session id included, the turn
ends too; an unreadable transcript skips only the transcript check.
"""
import json
import os
import re
import sys
from datetime import datetime, timezone

SESSION = re.compile(r"^[A-Za-z0-9_-]+$")
ROOT = os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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
    if entry.get("filed") is True:
        return True
    return unfiled_own(project, task, name, entry.get("unfiled")) and bool(str(entry.get("failure") or "").strip())


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


def moment(value):
    """A UTC ISO 8601 time as a comparable datetime, or None."""
    try:
        when = datetime.fromisoformat(str(value).strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return when if when.tzinfo else when.replace(tzinfo=timezone.utc)


def invoked_since(transcript, answered, plugin):
    """How many times each of this plugin's skills was invoked through the Skill tool at or after
    the act's proposal was answered, by the transcript's own timestamps: no step runs before it,
    and a taken-over marker that records answered is stamped with the take-over's time, so an
    earlier act of the same session ran before it."""
    counts = {}
    with open(transcript, encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                entry = json.loads(line)
            except ValueError:
                continue
            when = moment(entry.get("timestamp")) if isinstance(entry, dict) else None
            if when is None or when < answered:
                continue
            for tool, args in tool_uses(entry):
                if tool == "Skill" and str(args.get("skill") or "").startswith(plugin + ":"):
                    skill = str(args["skill"]).split(":", 1)[1]
                    counts[skill] = counts.get(skill, 0) + 1
    return counts


def unrecorded_runs(steps, counts):
    """A step whose skill was invoked more times since the act began than its steps have outcomes,
    while one of its steps is still pending: the earliest such pending step, per skill."""
    found = []
    for skill, invoked in counts.items():
        mine = [s for s in steps if str(s.get("step") or "").split(":", 1)[-1] == skill]
        ended = sum(1 for s in mine if s.get("outcome", "pending") != "pending")
        pending = [s for s in mine if s.get("outcome", "pending") == "pending"]
        if pending and invoked > ended:
            found.append(f"{pending[0].get('step')}: its skill ran in this act, but the marker still holds it "
                         "pending, so its result reached only the conversation: record how it ended and hand "
                         "it to document now")
    return found


def unsynced(project, marker):
    task = str(marker["task"]).strip()
    folder = f".claude/praxis/unfiled/{task}/"
    found = []
    steps = marker.get("steps")
    for i, step in enumerate(steps if isinstance(steps, list) else []):
        if step.get("outcome", "pending") == "pending" or recorded(project, task, step.get("step"), step):
            continue
        name = step.get("step") or f"step {i + 1}"
        if str(step.get("unfiled") or "").strip() and not str(step.get("failure") or "").strip():
            found.append(f"{name}: its result was written to {folder} without a failed filing recorded; "
                         "the unfiled directory holds failed filings only, so attempt the filing")
        elif str(step.get("unfiled") or "").strip():
            own = str(step.get("step") or "").replace(":", "-")
            found.append(f"{name}: its unfiled entry names no existing {folder}{own or '<row>-<skill>'}.md, "
                         "the step's own file")
        else:
            found.append(f"{name}: what it hands the record is neither filed nor written to {folder}")
    delivery = marker.get("delivery") or {}
    if delivery.get("channels") and not recorded(project, task, "delivery", delivery):
        if str(delivery.get("unfiled") or "").strip() and not str(delivery.get("failure") or "").strip():
            found.append(f"the delivery: its record was written to {folder} without a failed filing "
                         "recorded; attempt the filing")
        elif str(delivery.get("unfiled") or "").strip():
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
    steps = marker.get("steps")
    answered = moment(marker.get("answered"))
    transcript = event.get("transcript_path") or ""
    if isinstance(steps, list) and answered and os.path.isfile(transcript):
        try:
            found += unrecorded_runs(steps, invoked_since(transcript, answered, plugin_name()))
        except Exception:
            pass
    if found:
        reason = ("This act's work isn't all in the task's documentation:\n- " + "\n- ".join(found)
                  + "\nHand each to document. Only when its filing fails, write what document hands back to "
                  "the task's unfiled directory and record that path, with the failure, in the marker, so "
                  "the next session can file it.")
        json.dump({"decision": "block", "reason": reason}, sys.stdout)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
