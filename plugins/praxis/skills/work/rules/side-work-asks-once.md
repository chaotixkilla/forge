# Side work asks once

Research, a probe or an explanation asked for while a task is open often serves that task. Run as a task of its own, it splits the record: the conclusion the task rests on lives in another document, and someone has to merge the two by hand later. Run silently into a task the user isn't working in, it fills that task's record with work they meant to keep apart. `(basis: maintainer, 2026-10-13)`

## What counts as side work

A request is side work for a task when it would run a step skill — understand, gather, deep-research, prototype, debug — and so needs a task of its own by [when-work-needs-a-task](when-work-needs-a-task.md).

- **The task.** It is side work for the task this session runs, unless the request names another task, which then takes the path below for no act running. With no act running, it is for the task the request names, by key, change, ticket or branch, as [open-the-task](../phases/02-open-the-task.md)'s Find the task matches them, open or closed. A request that names none is not side work, and routes on as new work.
- **What it isn't.**
  - An answer drawn from what the task has already read: it is a finding, which [run-the-act](../phases/03-run-the-act.md)'s rules for findings file.
  - The task's next step.
  - Work its rounds cover: a rework, a ship round, or follow-ups. Those are work that changes the code or reviews a new head. Research, a probe or an explanation that changes neither is side work, however it bears on the outcome. `(basis: derived from the field case, where research was misfiled as new rounds)`

Under `--task`, the check runs the same way.

## While an act runs: attach

While this session runs the task's act, side work is part of that task. It runs now and attaches, with nothing asked. Running it apart or later would leave the act working without what the user just asked for. `(basis: maintainer, 2026-10-14)`

## With no act running: ask once

When no act runs for the task in this session — it waits between rounds, or it is closed — ask one question with three answers, the recommended one first:

- **Attach it to the task.**
  - For an open task, recommended when the work serves a decision the task still has open: a question its spec, plan or review hasn't settled, or a claim a step's result leaves unsettled.
  - For a closed task, recommended when the request questions what the task concluded, since that reopens the decision it rests on.
- **A separate task, linked** — recommended otherwise. It routes on as new work. Opening it writes `related` in its own entry and in the task's: the other's key and why they were linked ([keep-the-task-memory-entry](keep-the-task-memory-entry.md)). A closed task's front page shows the link from its next filing.
- **A separate task** — routes on as new work, with no link.

An answer that picks none takes the recommended one. `--attach` and `--separate` answer before it is asked; `--separate` takes the linked form, since a link costs nothing. A run that can't ask ([ask-while-the-user-is-here](../../gather/rules/ask-while-the-user-is-here.md)) takes the linked separate task and says so: a move (below) can fold that in later, while nothing undoes an attachment. `(basis: derived)`

## Attached work

Attached work runs as the step skills its outcome takes. Research climbs [help-build-the-mental-model](help-build-the-mental-model.md)'s order, but a heavyweight run asks its cost question by [ask-before-a-heavyweight-run](../../gather/rules/ask-before-a-heavyweight-run.md), as part of answering the user's request.

Each result is filed as a result of its own, never merged into a step's, labelled `attached:` with the request in the user's words, by run-the-act's rules for findings. Side work never opens a round:

- **While an act runs,** it joins the current round.
- **On a task between rounds,** it joins the latest round.
- **On a closed task,** it joins the latest round, and the task stays closed. Document takes a filing labelled `attached:` into that round.

## Moving a separate task into another

When the user asks to move a task into another, carry it out as open-the-task's fold of earlier separate tasks: fetch both tasks' whole trees, hand the target's documents with the filing, and treat the move as all or nothing. It differs in three ways:

- **What lands where.** The moved task's pages, but for its task record and task history, file into the target's latest round as working records, carried as they stand, labelled `moved:` with its key. That round's history records the move.
- **Retire is asked, not assumed.** Once the filing lands and an open moved task's closing filing (below) has landed too, ask before retiring the moved task's documentation; when the closing filing fails, report it and don't ask. While an act runs, the question goes in close-out's report. A run that can't ask takes "no", which leaves two records.
- **No link.** Write no `related` for a move: the target's history names the moved task.

The moved task must have no act marker written within the marker idle time ([keep-the-act-marker](keep-the-act-marker.md)). If it has one, refuse the move, and say that another session may be running it. If the target has such a marker, warn as open-the-task's route for a finding does.

An open moved task then closes in a filing of its own, before the retire question:

- its status `closed · moved into <key>`;
- its index line removed, and its act marker, if one was left past the idle time;
- its environment torn down and its worktree removed as close-out does.

The moved task's memory entry stays, unlike a folded one's, so its key still resolves; a retire clears its `docs`.

When the target's filing fails, nothing else happens. When the closing filing fails, the report says so.

Cited by [route-the-work](../phases/01-route-the-work.md), [open-the-task](../phases/02-open-the-task.md), [run-the-act](../phases/03-run-the-act.md) and [keep-the-task-memory-entry](keep-the-task-memory-entry.md).
