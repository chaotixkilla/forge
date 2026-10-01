# Keep the task's memory entry

Each task keeps one entry in the harness's persistent memory, so a later session can find the work and pick it up. The entry is a pointer, not the record: the task's documentation holds the truth, and when the two disagree the documentation wins and the entry is corrected.

## The entry

One memory file per task, named `task-<key>`, in the memory's own file format. Its body holds these fields and nothing else, each as a `<field>: <value>` line: the task (its key and title), its status (starting with `open` or `closed`, then what it's waiting on), its act, its next step, its docs (the task record's location), its links (the change and the ticket), the commit it last worked at, and the date it was last updated, as YYYY-MM-DD. (basis: maintainer, 2026-09-30)

    task:    review-pr-230 · invoice export (PROJ-88)
    status:  open · delivery pending
    act:     reviewing
    next:    post the review on pull request 230
    docs:    the task record's location
    links:   ticket PROJ-88 · pull request 230
    at:      3f9c2e1
    updated: 2026-10-02

## The index line

While the task is open, one line in the memory index points to the entry, its link text prefixed `task:` so it can be told from other memories: `- [task: review-pr-230 · invoice export](task-review-pr-230.md) — open, delivery pending`. Each status change rewrites the line's status text. Close-out removes the line when the task closes, and praxis's session-start hook removes a line idle past the idle period. Only the line goes: the entry file stays, searching memory still finds it, and resuming the task restores the line. Nothing praxis runs removes a line it didn't prefix. (basis: maintainer, 2026-09-30) (routed to maintainer: an idle period of 14 days, long enough to survive a holiday.)

## A record of what was true, not of what is

An entry records what was true at its `at` commit, never the present: memory is user-global and unversioned, so nothing in it can be trusted the way a versioned file can, and the failure it invites isn't forgetting but remembering something that stopped being true — an empty memory prompts a look, a stale one prevents it. So a later session treats the entry as a **lead to verify against the repository as it now stands**, never as current fact ([open-the-task](../phases/02-open-the-task.md) re-runs the act when the change has moved past the entry's commit). An entry with no `at` commit can't be checked, and is treated as stale. The entry is rewritten on every status change, never added to, so one task never has two entries to choose between. Only the task's entry carries status across sessions: a step writes no status memory of its own. (basis: maintainer, 2026-09-02)

Cited by [open-the-task](../phases/02-open-the-task.md) and [close-out](../phases/04-close-out.md).
