# tidy (`--tidy`)

Activated by `--tidy`, referenced from [SKILL.md](../SKILL.md).

The base run routes a request to an act and runs it. This module runs no act: it finds what finished or idle tasks left in this repository — worktrees, environments, and the shared images and caches no task uses any more — and offers to clear it. Deletion test: without it, leftovers stay until each task is resumed and closed, or the user clears them by hand; no act changes. `(basis: maintainer, 2026-10-13 — "I have to open a session every now and then to check for stale worktrees")`

## Gather

Through [workspace](../../workspace/SKILL.md), with no task key: *list the task worktrees* (with the integration line), *list every task's environment*, and *list the unused shared pieces*. Read each task's state from the main checkout: its act marker in `.claude/praxis/acts/` ([keep-the-act-marker](../rules/keep-the-act-marker.md)), live when written within the marker idle time, and its memory entry `task-<key>` ([keep-the-task-memory-entry](../rules/keep-the-task-memory-entry.md)), its `status`, `updated`, `links` and `at`. A worktree or environment belongs to the task whose key the workspace made its name from, a `<key>-baseline` one to `<key>`. One that matches no entry is **unknown**: a lone step's, a standalone review's, one the harness or the user made in the same folder, or a task's whose entry is gone. `--task=<key>` narrows all of this to that task.

Never listed: this session's own task, and anything of a task whose marker is live — another session is working on it.

## Sort

- **Worktrees to remove** — no marker records it, and its task is closed, or its branch merged, since a merged branch loses nothing and resuming the task makes its worktree again `(basis: maintainer, 2026-10-14)`. Whether the branch's review request merged is read through [vcs](../../vcs/SKILL.md) from the entry's `links`. A detached worktree is offered only when its head is the entry's `at`, passed as the commit it was made at, or is contained in the integration line's remote head, as a baseline's is; any other head may hold commits on no branch, so it is held. An unknown worktree is never offered: nothing says it is praxis's. One the workspace would refuse is listed with the reason it returns, and not offered.
- **Environments to tear down** — its task is closed, or it is unknown, has no worktree, and nothing wrote to it within the marker idle time: no task can resume it, since work resumes a task by its entry. `(basis: derived)` With it goes the task's runs folder, which in host mode is all a task leaves.
- **Environments to stop, keeping their data** — running, its task open with no live marker: idle between sessions, or left by a session that ended mid-act. `(basis: maintainer, 2026-10-14 — an idle task's environment is stopped, never torn down)`
- **Shared pieces to remove** — the images and dependency caches the workspace reports no task uses.

Each item shows why it is listed: the task closed on its `updated` date, its branch merged, idle since its marker or environment was last written, or unused.

## Offer, then clear

Show the four lists and ask once which to clear: all of them, a whole list, or named items. Nothing is cleared unasked; in a run with no one to answer, show the lists and stop. Under `--dry-run`, show them and stop.

Clear in this order, through the workspace: tear down, then stop, then remove worktrees, since a task's environment goes before its worktree, then the chosen shared pieces. Never force anything, and report each item's outcome; a refusal or partial result names what stayed and why.

In host mode there are no environments or shared pieces, and the workspace can't tear down: tidy lists the closed tasks' folders under the main checkout's `.claude/praxis/runs/` beside the worktrees, and removes each chosen one itself.
