#!/usr/bin/env python3
"""praxis PreToolUse hook: require an act.

In a project set up for praxis (it has .claude/praxis.json), code changes happen
inside an act. When this session runs no act (it has no readable marker at
.claude/praxis/acts/<session-id>.json, per work's keep-the-act-marker rule), this
denies a file edit inside the project, and a git commit, with a message that says
how to start one: a change with no behavior change and no new interface runs the
developing act's small-change path (develop, then verify). Another session's
marker never unlocks this one. Edits outside the project, inside .claude/, and
inside a local documentation directory (the artifacts home's, or a local audience
space's) are never blocked. On any error, and when the event names no usable
session id, the change goes ahead: a guard that can't read its inputs must not
stop the user's work.
"""
import json
import os
import re
import sys

EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
# git is praxis's declared ambient substrate (see skills/vcs/usage.md), so matching its commit
# command here is deliberate: accepted on record, maintainer, 2026-10-01.
COMMIT = re.compile(r"(^|[;&|]\s*|\s)git(\s+-\S+(\s+\S+)?)*\s+commit\b")
REASON = (
    "No praxis act is running in this session, so this code change is blocked. Start the work through "
    "the praxis work skill: it routes the change to its act. A change with no behavior change and no new "
    "interface runs the developing act's small-change path, develop then verify."
)
SESSION = re.compile(r"^[A-Za-z0-9_-]+$")


def acts_dir(project):
    return os.path.join(project, ".claude", "praxis", "acts")


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


def denial(project, session):
    """The deny message: how to start an act, and what this session and others have on disk."""
    own = os.path.join(acts_dir(project), session + ".json")
    parts = [REASON, f"This session's id is {session}: an act running in it keeps its marker at "
                     f".claude/praxis/acts/{session}.json."]
    if os.path.exists(own):
        parts.append("That file exists but can't be read as a marker. Resume its task with work --task=<key> "
                     "to write it again, or remove it.")
    try:
        names = sorted(os.listdir(acts_dir(project)))
    except OSError:
        names = []
    others = []
    for name in names:
        if name.endswith(".json") and name != session + ".json":
            marker = read_marker(os.path.join(acts_dir(project), name))
            if marker:
                others.append(str(marker["task"]).strip())
    if others:
        keys = ", ".join(sorted(set(others)))
        parts.append(f"Another session's act is recorded for {keys}. To carry one on here, run "
                     "work --task=<key>, which offers to take it over.")
    return " ".join(parts)


def is_file_backed(space):
    """A destination written to the filesystem: the fs transport, or the local provider of older configs."""
    return str(space.get("transport", "")).strip() == "fs" or str(space.get("provider", "")).strip() == "local"


def documentation_dirs(project):
    """The local documentation directories, which edits may always reach."""
    dirs = [os.path.join(project, "docs", "praxis")]
    try:
        with open(os.path.join(project, ".claude", "praxis.json"), encoding="utf-8") as f:
            artifacts = (json.load(f).get("tools") or {}).get("artifacts") or {}
    except (OSError, ValueError, AttributeError):
        artifacts = {}
    audiences = (artifacts.get("audiences") or []) if isinstance(artifacts, dict) else []
    try:
        # An older config keeps the home's destination as destinations.default.
        home = artifacts.get("destination") or (artifacts.get("destinations") or {}).get("default") or ""
        if is_file_backed(artifacts) and home:
            dirs.append(os.path.join(project, home))
    except (AttributeError, TypeError):
        pass
    for space in audiences if isinstance(audiences, list) else []:
        try:
            if is_file_backed(space) and space.get("destination"):
                dirs.append(os.path.join(project, space["destination"]))
        except (AttributeError, TypeError):
            continue
    return [os.path.realpath(d) for d in dirs]


def inside(path, root):
    return path == root or path.startswith(root.rstrip(os.sep) + os.sep)


def exempt(target, project):
    target = os.path.realpath(target if os.path.isabs(target) else os.path.join(project, target))
    if not inside(target, project):
        return True
    if inside(target, os.path.join(project, ".claude")):
        return True
    return any(inside(target, d) for d in documentation_dirs(project))


def main():
    event = json.load(sys.stdin)
    project = os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or os.getcwd())
    if not os.path.isfile(os.path.join(project, ".claude", "praxis.json")):
        return
    session = str(event.get("session_id") or "")
    if not SESSION.match(session):
        return
    if read_marker(os.path.join(acts_dir(project), session + ".json")):
        return
    tool = event.get("tool_name")
    payload = event.get("tool_input") or {}
    if tool in EDIT_TOOLS:
        target = payload.get("file_path") or payload.get("notebook_path") or ""
        if not target or exempt(target, project):
            return
    elif tool == "Bash":
        if not COMMIT.search(str(payload.get("command") or "")):
            return
    else:
        return
    json.dump({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                      "permissionDecisionReason": denial(project, session)}}, sys.stdout)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
