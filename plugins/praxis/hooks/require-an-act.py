#!/usr/bin/env python3
"""praxis PreToolUse hook: require an act.

In a project set up for praxis, code changes happen inside an act whose proposal is
settled. When this session runs no act (no readable marker at
.claude/praxis/acts/<session-id>.json in the repository's main checkout), this denies a file edit inside any checkout of the repository, the main one or a
worktree wherever it lives, and a git commit, with a message that says how to start one:
a change with no behavior change and no new interface runs the developing act's
small-change path (develop, then verify). When the marker records no answer to the act's
proposal yet, it denies them with a message that the proposal isn't settled yet. This
session's answered act unlocks edits in every checkout of the repository; another
session's marker never unlocks this one. Edits outside every checkout, inside a
checkout's own .claude/ (a worktree nested under it is a checkout of its own), and inside
a local documentation directory (the artifacts home's, or a local audience space's) are
never blocked. On any error, when git doesn't answer in time, and when the event names no
usable session id, the change goes ahead: a guard that can't read its inputs must not
stop the user's work.
"""
import json
import os
import re
import subprocess
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

def checkouts(project):
    """Every checkout of the repository: the main one and each worktree, wherever it lives."""
    try:
        listing = subprocess.run(["git", "-C", project, "worktree", "list", "--porcelain"],
                                 capture_output=True, text=True, timeout=5).stdout
    except (OSError, subprocess.SubprocessError):
        listing = ""
    roots = [os.path.realpath(line[len("worktree "):]) for line in listing.splitlines()
             if line.startswith("worktree ")]
    return roots or [project]


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
    marker = read_marker(own)
    if marker:
        return (f"This session's act for {str(marker['task']).strip()} has no answer to its proposal recorded, "
                "so this code change is blocked: no step runs and no code changes until the act's proposal is "
                "settled (its steps shown, and its one question answered when it has one) and the marker's "
                "answered records when.")
    parts = [REASON, f"This session's id is {session}: an act run in it keeps its marker at {own}."]
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
    """The local documentation directories, which edits may always reach, as the config names them:
    relative to a checkout's root, or absolute."""
    dirs = []
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
            dirs.append(home)
    except (AttributeError, TypeError):
        pass
    for space in audiences if isinstance(audiences, list) else []:
        try:
            if is_file_backed(space) and space.get("destination"):
                dirs.append(space["destination"])
        except (AttributeError, TypeError):
            continue
    return dirs


def inside(path, root):
    return path == root or path.startswith(root.rstrip(os.sep) + os.sep)


def exempt(target, project, cwd):
    target = os.path.realpath(target if os.path.isabs(target) else os.path.join(cwd, target))
    owners = [root for root in checkouts(project) if inside(target, root)]
    if not owners:
        return True
    # A worktree nested in another checkout's folder owns its own files.
    owner = max(owners, key=len)
    if inside(target, os.path.join(owner, ".claude")):
        return True
    return any(inside(target, os.path.realpath(os.path.join(owner, d))) for d in documentation_dirs(project))


def main():
    event = json.load(sys.stdin)
    session = str(event.get("session_id") or "")
    if not SESSION.match(session):
        return
    tool = event.get("tool_name")
    payload = event.get("tool_input") or {}
    target = ""
    if tool in EDIT_TOOLS:
        target = payload.get("file_path") or payload.get("notebook_path") or ""
        if not target:
            return
    elif tool != "Bash" or not COMMIT.search(str(payload.get("command") or "")):
        return
    start = os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or os.getcwd()
    root = state_root(start)
    if root is None:
        return
    project = os.path.realpath(root)
    if not os.path.isfile(os.path.join(project, ".claude", "praxis.json")):
        return
    marker = read_marker(os.path.join(acts_dir(project), session + ".json"))
    if marker and str(marker.get("answered") or "").strip():
        return
    if target and exempt(target, project, event.get("cwd") or start):
        return
    json.dump({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                      "permissionDecisionReason": denial(project, session)}}, sys.stdout)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
