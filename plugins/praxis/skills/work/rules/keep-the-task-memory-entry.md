# Keep the task's memory entry

Each task keeps one entry in the harness's persistent memory, so a later session can find the work and pick it up. The entry is a pointer, not the record: the task's documentation holds the truth, and when the two disagree the documentation wins and the entry is corrected.

## The entry

One memory file per task, named `task-<key>`, in the memory's own file format; a stack's changes and every round share it. Its body holds these fields and nothing else, each as a `<field>: <value>` line: the task (its key and title), its owner (the user running the task, by their version-control name; an entry with none reads as the session's user), its status (starting with `open` or `closed`, then what it's waiting on, a wait on review naming each request, `open · awaiting review on review requests 405, 406`), its act, its next step, its docs (the task record's location), its links (the ticket, and the change, or every change of a stack, base-most first, each review request of an act that authors a change followed by the head it was last delivered at, as below), its rounds (latest first, each `<n> · <change>`, its number and the change it works on, and for an act that authors a change `<n> · <kind> · <change>`, with its kind, followed by the act it runs in parentheses when that isn't the task's own, its change as the review requests it takes up, the branch it builds on when it opens its own, or, for a round opened only to file a finding, the change the finding is about), the commit it last worked at, and the date it was last updated, as YYYY-MM-DD. (basis: maintainer, 2026-09-30; rounds, maintainer, 2026-10-02; owner and round kinds, maintainer, 2026-10-07) The status and the commit are the latest round's. A round's line is written when it opens, or when its fold lands ([open-the-task](../phases/02-open-the-task.md)), and nothing else maintains it. A round's kind is `build`, `rework after peer review`, `follow-ups` or `ship` ([open-the-task](../phases/02-open-the-task.md)). An entry with no `rounds` reads as one round, round 1, on the base-most change its links name, and an authored change's round line with no kind reads as `build`. A review request in the links with no head reads as delivered at the entry's `at`, or at the documentation commit a delivery made on top of it, and a wait on review that names no request waits on every open request the links name. (basis: derived — an entry written before heads existed was delivered at its `at`, or at the documentation commit its delivery added on top) (basis: derived — every round written before kinds existed was a first round's work) (basis: derived from a stack's task being keyed by its base-most change)

    task:    review-230 · invoice export (PROJ-88)
    owner:   Ana Ribeiro
    status:  open · delivery pending
    act:     reviewing
    next:    post the review on review request 231
    docs:    the task record's location
    links:   ticket PROJ-88 · review requests 230, 231
    rounds:  2 · review request 231; 1 · review request 230
    at:      9ab12cd
    updated: 2026-10-02

An authored change's links and rounds read, for example:

    links:   ticket PROJ-88 · review requests 405 at 3e5f7a1, 406 at 8d2c4b6
    rounds:  3 · follow-ups (fixing-a-bug) · branch PROJ-88-round-3; 2 · rework after peer review · review request 405; 1 · build · branch PROJ-88

## The index line

While the task is open, one line in the memory index points to the entry, its link text prefixed `task:` so it can be told from other memories: `- [task: review-230 · invoice export](task-review-230.md) — open, delivery pending`. Each status change rewrites the line's status text. Close-out removes the line when the task closes, and praxis's session-start hook removes a line idle past the idle period. Only the line goes: the entry file stays, searching memory still finds it, and resuming the task restores the line. Nothing praxis runs removes a line it didn't prefix. (basis: maintainer, 2026-09-30) (routed to maintainer: an idle period of 14 days, long enough to survive a holiday.)

## A record of what was true, not of what is

An entry records what was true at its `at` commit, never the present: memory is user-global and unversioned, so nothing in it can be trusted the way a versioned file can, and the failure it invites isn't forgetting but remembering something that stopped being true — an empty memory prompts a look, a stale one prevents it. So a later session treats the entry as a **lead to verify against the repository as it now stands**, never as current fact ([open-the-task](../phases/02-open-the-task.md) re-runs a round's steps when the change has moved past the entry's commit). An entry with no `at` commit can't be checked, and is treated as stale. The entry is rewritten on every status change, never added to, so one task never has two entries to choose between. Only the task's entry carries status across sessions: a step writes no status memory of its own. (basis: maintainer, 2026-09-02)

Cited by [open-the-task](../phases/02-open-the-task.md) and [close-out](../phases/04-close-out.md).
