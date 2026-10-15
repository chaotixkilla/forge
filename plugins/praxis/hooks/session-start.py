#!/usr/bin/env python3
"""praxis SessionStart hook.

In a project with praxis settings (.claude/praxis.json in the repository's main
checkout), removes the task lines from the memory index whose task is closed or has
been idle past the idle period, then gives the session praxis's guidance: the standing
postures, with a notice when output.comments holds a value the report-style-settings
rule doesn't define; the folder praxis keeps the project's state in; this session's
id, under which an act keeps its marker there; and each act marker another session
left with no write past the marker idle time, or that an older praxis left at
.claude/praxis-act.json. It also lists the open tasks other sessions are working on; moves the act
markers and unfiled results an older praxis left inside a worktree, idle past the marker idle time,
into the main checkout, removing the emptied folders and saying what it moved and what it left; and,
when finished or idle tasks left worktrees or environments behind, has the session offer work --tidy.
And when the installed praxis's version differs from the one init last ran under, it says so once per version. It reads only git and praxis's own files, never a container runtime. It never blocks: on any error it exits 0, and the session
starts as it would without praxis; a failed memory trim only skips the trim.
"""
import datetime
import json
import os
import re
import shutil
import subprocess
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

def memory_dir(root, transcript):
    """The project's memory folder. The harness keys memory by repository, so every worktree shares the
    main checkout's (Claude Code's memory docs). When it doesn't exist yet, the folder beside this
    session's transcript, which is the project's own when the session runs in the main checkout."""
    base = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(os.path.expanduser("~"), ".claude")
    for path in (root, os.path.realpath(root)):
        keyed = os.path.join(base, "projects", re.sub(r"[^A-Za-z0-9]", "-", path), "memory")
        if os.path.isdir(keyed):
            return keyed
    return os.path.join(os.path.dirname(transcript), "memory") if transcript else ""

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
    return (COMMENTS["why-only"] + f" output.comments in {os.path.join(cwd, '.claude', 'praxis.json')} is {json.dumps(value)}, which "
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
            lines.append(f"{path}, last written {when}, can't be read as a marker: "
                         "remove it if no act is running from it")
    legacy = os.path.join(cwd, ".claude", "praxis-act.json")
    if os.path.isfile(legacy):
        task, _ = marker_task(legacy)
        then = (f"resume its task with work --task={task}, then remove the file" if task
                else "remove it if no act is running from it")
        lines.append(f"{legacy}, a marker from an older praxis, which this one does not read: {then}")
    return lines


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


def key_name(key):
    """A task key as the workspace names its folders and resources (its own rule): lowercase, every
    character outside a-z, 0-9 and the hyphen made a hyphen."""
    return re.sub(r"[^a-z0-9-]", "-", key.lower())


def age_hours(path, now):
    try:
        written = datetime.datetime.fromtimestamp(os.path.getmtime(path), datetime.timezone.utc)
    except OSError:
        return None
    return (now - written).total_seconds() / 3600


def repair(project, now):
    """Moves what an older praxis left in a worktree's own .claude/praxis/ (act markers and unfiled
    results) into the main checkout's, and removes the folders that leaves empty. A worktree holding a
    marker written within the marker idle time is left alone, since a session may still be writing
    there. A marker the main checkout already holds is the same session's: the newer copy stays and the
    older goes. An unfiled result the main checkout already holds is left in place, since the two may
    hold different pieces. Returns what it moved and what it left, as report lines."""
    moved, left = [], []
    main = os.path.join(project, ".claude", "praxis")
    for checkout in checkouts(project):
        if checkout == project:
            continue
        base = os.path.join(checkout, ".claude", "praxis")
        if not os.path.isdir(base):
            continue
        acts = os.path.join(base, "acts")
        markers = [os.path.join(acts, n) for n in sorted(os.listdir(acts))] if os.path.isdir(acts) else []
        if any((h := age_hours(m, now)) is not None and h <= MARKER_IDLE_HOURS for m in markers):
            left.append(f"{base}, where a session wrote within {MARKER_IDLE_HOURS} hours")
            continue
        for folder, _, files in os.walk(base):
            for name in files:
                try:
                    note = move_one(os.path.join(folder, name), base, main)
                except OSError as error:
                    note = ("left", f"{os.path.join(folder, name)}, since moving it failed: {error.strerror or error}")
                if note:
                    (moved if note[0] == "moved" else left).append(note[1])
        for folder, _, _ in sorted(os.walk(base), key=lambda w: -len(w[0])):
            try:
                os.rmdir(folder)
            except OSError:
                pass
    return moved, left


def move_one(source, base, main):
    """Moves one file of a worktree's .claude/praxis/ into the main checkout's, by repair's rules.
    Returns ("moved" or "left", a report line), or None for a file outside acts/ and unfiled/."""
    relative = os.path.relpath(source, base)
    if relative.split(os.sep)[0] not in ("acts", "unfiled"):
        return None
    target = os.path.join(main, relative)
    if os.path.exists(target):
        if relative.split(os.sep)[0] != "acts":
            return "left", f"{source}, since {target} exists"
        if os.path.getmtime(source) > os.path.getmtime(target):
            os.remove(target)
            shutil.move(source, target)
            return "moved", f"{source} to {target}, replacing an older copy"
        os.remove(source)
        return "moved", f"nothing from {source}, an older copy of {target}, which it removed"
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.move(source, target)
    return "moved", f"{source} to {target}"


def task_entries(memory):
    """Each task's status and updated date from its memory entry, task-<key>.md, by the key's folder
    name. None when the memory folder can't be listed, since every task would then read as unknown."""
    entries = {}
    try:
        names = os.listdir(memory)
    except (OSError, TypeError, ValueError):
        return None
    for name in names:
        if not (name.startswith("task-") and name.endswith(".md")):
            continue
        try:
            with open(os.path.join(memory, name), encoding="utf-8") as f:
                fields = dict(FIELD.findall(f.read()))
        except OSError:
            continue
        entries[key_name(name[len("task-"):-len(".md")])] = fields
    return entries


def open_tasks(project, session, now):
    """The act markers in the main checkout: every worktree a marker records, the task keys of those
    written within the marker idle time (this session's included), and report lines for other
    sessions' among them."""
    worktrees, keys, live = set(), set(), []
    folder = os.path.join(project, ".claude", "praxis", "acts")
    try:
        names = sorted(os.listdir(folder))
    except OSError:
        names = []
    for name in names:
        path = os.path.join(folder, name)
        if not name.endswith(".json"):
            continue
        try:
            with open(path, encoding="utf-8") as f:
                marker = json.load(f)
        except (OSError, ValueError):
            continue
        if not isinstance(marker, dict):
            continue
        task = str(marker.get("task") or "").strip()
        tree = str(marker.get("worktree") or marker.get("copy") or "").strip()
        if tree:
            worktrees.add(os.path.realpath(tree))
        hours = age_hours(path, now)
        mine = name[:-len(".json")] == session
        if task and (mine or (hours is not None and hours <= MARKER_IDLE_HOURS)):
            keys.add(key_name(task))
            if not mine:
                act = str(marker.get("act") or "").strip()
                live.append(f"{task}{' (' + act + ')' if act else ''} in {tree or project}")
    return worktrees, keys, live


def leftovers(project, entries, keys, worktrees, now):
    """What finished or idle tasks left, by work --tidy's rules: praxis's worktrees no marker records
    whose task is closed; environment records of closed tasks, and of unknown ones (no memory entry) with
    no worktree and no write within the marker idle time, to tear down; and running environments of open
    tasks, to stop. A <key>-baseline name belongs to <key>; anything of a task keys holds (a live marker)
    is skipped. With entries None, only running environments untouched within the marker idle time are reported, since a fresh one may be a lone step's. Whether a branch merged needs
    the remote, so work --tidy decides that."""
    owner = lambda name: key_name(name[:-len("-baseline")] if name.endswith("-baseline") else name)
    trees, gone, idle = [], [], []
    holder = os.path.join(project, ".claude", "worktrees")
    try:
        names = sorted(os.listdir(holder)) if entries is not None else []
    except OSError:
        names = []
    for name in names:
        path = os.path.realpath(os.path.join(holder, name))
        key = owner(name)
        if (os.path.isdir(path) and path not in worktrees and key not in keys
                and entries.get(key, {}).get("status", "").lower().startswith("closed")):
            trees.append(name)
    runs = os.path.join(project, ".claude", "praxis", "runs")
    try:
        names = sorted(os.listdir(runs))
    except OSError:
        names = []
    for name in names:
        key, record = owner(name), os.path.join(runs, name, "environment.json")
        if key in keys:
            continue
        try:
            with open(record, encoding="utf-8") as f:
                state = json.load(f).get("state")
        except (OSError, ValueError, AttributeError):
            continue
        if entries is not None and key not in entries:
            hours = age_hours(record, now)
            if not os.path.isdir(os.path.join(holder, name)) and hours is not None and hours > MARKER_IDLE_HOURS:
                gone.append(name)
        elif entries is not None and entries[key].get("status", "").lower().startswith("closed"):
            gone.append(name)
        elif state == "running" and (entries is not None or (age_hours(record, now) or 0) > MARKER_IDLE_HOURS):
            idle.append(name)
    return trees, gone, idle


def version_notice(project):
    """A line saying the installed praxis differs from the version init last ran under, given once per
    installed version: the version shown is recorded in .claude/praxis/seen-version, and an equal one there
    keeps it quiet. Empty when the versions match or either can't be read."""
    try:
        with open(os.path.join(os.environ.get("CLAUDE_PLUGIN_ROOT", ""), ".claude-plugin", "plugin.json"),
                  encoding="utf-8") as f:
            installed = str(json.load(f).get("version") or "")
        with open(os.path.join(project, ".claude", "praxis.json"), encoding="utf-8") as f:
            recorded = str(json.load(f).get("praxis_version") or "")
    except (OSError, ValueError, AttributeError):
        return ""
    if not installed or installed == recorded:
        return ""
    seen = os.path.join(project, ".claude", "praxis", "seen-version")
    try:
        with open(seen, encoding="utf-8") as f:
            if f.read().strip() == installed:
                return ""
    except OSError:
        pass
    os.makedirs(os.path.dirname(seen), exist_ok=True)
    with open(seen, "w", encoding="utf-8") as f:
        f.write(installed + "\n")
    was = recorded or "an earlier version that didn't record one"
    return (f" praxis is now {installed}, and this project's setup was last reviewed under {was}: tell the user "
            "once, and suggest running /praxis:init, which reviews the setup slot by slot and offers what changed.")


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
    root = state_root(os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or os.getcwd())
    if root is None:
        return
    project = os.path.realpath(root)
    if not os.path.isfile(os.path.join(project, ".claude", "praxis.json")):
        return
    memory = ""
    try:
        memory = memory_dir(root, event.get("transcript_path") or "")
        if memory:
            trim_task_lines(memory, datetime.date.today())
    except Exception:
        pass
    context = GUIDANCE + " " + postures(project) + (f" praxis keeps this project's config and state in {project}: read .claude/praxis.json, "
                                                    "act markers and unfiled results there, whichever worktree this session runs in.")
    session = str(event.get("session_id") or "")
    if SESSION.match(session):
        context += (f" This session's id is {session}: an act run in it keeps its marker at "
                    f"{os.path.join(project, '.claude', 'praxis', 'acts', session + '.json')}.")
    else:
        session = ""
    now = datetime.datetime.now(datetime.timezone.utc)
    try:
        moved, kept = repair(project, now)
    except Exception:
        moved, kept = [], []
    try:
        left = left_markers(project, session, now)
    except Exception:
        left = []
    if left:
        context += " Act markers left without a close-out, so tell the user: " + "; ".join(left) + "."
    if moved or kept:
        context += (" praxis keeps act markers and unfiled results only in the main checkout, so tell the user "
                    "what it did with those an older version left in worktrees: "
                    + "; ".join([f"moved {m}" for m in moved] + [f"left {k}" for k in kept]) + ".")
    try:
        worktrees, keys, live = open_tasks(project, session, now)
        trees, gone, idle = leftovers(project, task_entries(memory), keys, worktrees, now)
    except Exception:
        live, trees, gone, idle = [], [], [], []
    if live:
        context += (" Other sessions are working on these open tasks; don't open a task in their worktrees: "
                    + "; ".join(live) + ".")
    found = [f"{label}: {', '.join(names)}" for label, names in (
        ("worktrees of closed tasks", trees),
        ("environments of closed or unknown tasks", gone),
        ("running environments of idle tasks", idle)) if names]
    try:
        context += version_notice(project)
    except Exception:
        pass
    if found:
        context += (" Finished or idle tasks left these behind, so in your first reply offer the user, once, to "
                    "clear them with work --tidy, which checks each before removing anything: " + "; ".join(found) + ".")
    json.dump({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}}, sys.stdout)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
