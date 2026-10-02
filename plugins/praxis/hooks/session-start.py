#!/usr/bin/env python3
"""praxis SessionStart hook.

In a project with praxis settings (.claude/praxis.json), removes the task lines
from the memory index whose task is closed or has been idle past the idle
period, then gives the session praxis's guidance: the standing postures, with a
notice when output.comments holds a value the report-style-settings rule doesn't
define; this session's id, under which an act keeps its marker; and each act
marker another session left with no write past the marker idle time, or that an
older praxis left at .claude/praxis-act.json. It never blocks: on any error it
exits 0, and the session starts as it would without praxis.
"""
import datetime
import json
import os
import re
import sys

# The idle period from the keep-the-task-memory-entry rule (routed to the maintainer).
IDLE_DAYS = 14
# The marker idle time from work's keep-the-act-marker rule (the maintainer's, 2026-10-02).
MARKER_IDLE_HOURS = 2
SESSION = re.compile(r"^[A-Za-z0-9_-]+$")

GUIDANCE = (
    "praxis is set up in this project. For software engineering work (building, fixing, "
    "reviewing, shipping, responding to incidents, maintaining, researching, prototyping, "
    "auditing, learning), start with the praxis work skill. When the "
    "work asks for one specific step, such as reviewing a diff or debugging a failure, use that "
    "praxis skill directly. Either way, a skill's phase files and rules are the procedure: follow "
    "them instead of working from memory, and don't skip a step without recording why. Quick "
    "questions that produce nothing to review or keep can be answered directly."
)

# The standing posture for code comments, from output.comments (craft's report-style-settings rule),
# stated here because most comments are written outside a praxis run.
COMMENTS = {
    "why-only": "Code comments in this project: write one only where the code cannot carry the meaning itself.",
    "match-codebase": "Code comments in this project: follow the comment density of the surrounding file.",
}


def postures(cwd):
    """The standing postures the config sets for work outside a praxis run. An absent or unreadable
    setting takes the default silently; a value the rule doesn't define takes it and says so."""
    value = None
    try:
        with open(os.path.join(cwd, ".claude", "praxis.json"), encoding="utf-8") as f:
            value = (json.load(f).get("output") or {}).get("comments")
    except (OSError, ValueError, AttributeError):
        pass
    if value is None or value == "":
        return COMMENTS["why-only"]
    if isinstance(value, str) and value in COMMENTS:
        return COMMENTS[value]
    return (COMMENTS["why-only"] + f" output.comments in .claude/praxis.json is {json.dumps(value)}, which "
            "isn't one of why-only or match-codebase, so the default, why-only, applies. Tell the user, so "
            "they can correct it.")


def left_markers(cwd, session, now):
    """Report lines for act markers other sessions left with no write past MARKER_IDLE_HOURS, and for
    the marker an older praxis kept at .claude/praxis-act.json."""
    lines = []
    folder = os.path.join(cwd, ".claude", "praxis", "acts")
    try:
        names = sorted(os.listdir(folder))
    except OSError:
        names = []
    for name in names:
        path = os.path.join(folder, name)
        if not name.endswith(".json") or name[:-len(".json")] == session:
            continue
        try:
            written = datetime.datetime.fromtimestamp(os.path.getmtime(path), datetime.timezone.utc)
        except OSError:
            continue
        if (now - written).total_seconds() <= MARKER_IDLE_HOURS * 3600:
            continue
        task, act = marker_task(path)
        when = written.strftime("%Y-%m-%d %H:%M UTC")
        if task:
            lines.append(f"{task}{' (' + act + ')' if act else ''}, last written {when}: resume or close it "
                         f"with work --task={task}")
        else:
            lines.append(f".claude/praxis/acts/{name}, last written {when}, can't be read as a marker: "
                         "remove it if no act is running from it")
    legacy = os.path.join(cwd, ".claude", "praxis-act.json")
    if os.path.isfile(legacy):
        task, _ = marker_task(legacy)
        then = (f"resume its task with work --task={task}, then remove the file" if task
                else "remove it if no act is running from it")
        lines.append(f".claude/praxis-act.json, a marker from an older praxis, which this one does not read: {then}")
    return lines


def marker_task(path):
    """A marker's task key and act; empty strings when it can't be read as one."""
    try:
        with open(path, encoding="utf-8") as f:
            marker = json.load(f)
    except (OSError, ValueError):
        return "", ""
    if not isinstance(marker, dict):
        return "", ""
    return str(marker.get("task") or "").strip(), str(marker.get("act") or "").strip()


TASK_LINE = re.compile(r"^\s*-\s*\[task:[^\]]*\]\(([^)]+)\)")
FIELD = re.compile(r"^\s*(status|updated):\s*(.+?)\s*$", re.M)


def stale(entry_path, today):
    """A task is stale when it's closed or was last updated more than IDLE_DAYS ago.
    An entry that can't be read or dated is left alone."""
    try:
        with open(entry_path, encoding="utf-8") as f:
            fields = dict(FIELD.findall(f.read()))
    except OSError:
        return False
    if fields.get("status", "").lower().startswith("closed"):
        return True
    try:
        updated = datetime.date.fromisoformat(fields.get("updated", "")[:10])
    except ValueError:
        return False
    return (today - updated).days > IDLE_DAYS


def trim_task_lines(memory_dir, today):
    index = os.path.join(memory_dir, "MEMORY.md")
    if not os.path.isfile(index):
        return
    with open(index, encoding="utf-8") as f:
        lines = f.readlines()
    kept = [line for line in lines
            if not ((m := TASK_LINE.match(line)) and stale(os.path.join(memory_dir, m.group(1)), today))]
    if len(kept) != len(lines):
        tmp = index + ".praxis-tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.writelines(kept)
        os.replace(tmp, index)


def main():
    try:
        event = json.load(sys.stdin)
    except ValueError:
        event = {}
    cwd = os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or os.getcwd()
    if not os.path.isfile(os.path.join(cwd, ".claude", "praxis.json")):
        return
    transcript = event.get("transcript_path") or ""
    if transcript:
        # The harness keeps a project's memory beside its session transcripts.
        try:
            trim_task_lines(os.path.join(os.path.dirname(transcript), "memory"), datetime.date.today())
        except OSError:
            pass
    context = GUIDANCE + " " + postures(cwd)
    session = str(event.get("session_id") or "")
    if SESSION.match(session):
        context += (f" This session's id is {session}: an act run in it keeps its marker at "
                    f".claude/praxis/acts/{session}.json.")
    else:
        session = ""
    try:
        left = left_markers(cwd, session, datetime.datetime.now(datetime.timezone.utc))
    except Exception:
        left = []
    if left:
        context += " Act markers left without a close-out, so tell the user: " + "; ".join(left) + "."
    json.dump({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}}, sys.stdout)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
