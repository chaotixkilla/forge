## Does it need a task?

Apply [when-work-needs-a-task](../rules/when-work-needs-a-task.md). If it doesn't, answer the request directly and stop: no task, no act, nothing written. With `--task=<key>`, skip this section and the next: the task exists, and its memory entry names its act ([open-the-task](02-open-the-task.md)).

## Which act?

Match the request against each act's entry condition, stated at the top of its act file:

- [developing](../acts/developing.md)
- [fixing-a-bug](../acts/fixing-a-bug.md)
- [reviewing](../acts/reviewing.md)
- [shipping](../acts/shipping.md)
- [responding-to-an-incident](../acts/responding-to-an-incident.md)
- [maintaining](../acts/maintaining.md)
- [researching](../acts/researching.md)
- [prototyping](../acts/prototyping.md)
- [auditing](../acts/auditing.md)
- [learning](../acts/learning.md)

`--act=<name>` replaces the match; a name with no act file is an error — say which acts exist and stop. When it's unclear whether the request fits an act, take the act: the proposal in [run-the-act](03-run-the-act.md) shows the user what it would run before anything does. When two acts fit, ask the user which, now. (routed to maintainer: both defaults proposed.)

## When no act fits

Don't force one. The discriminator is the outcome the request asks for:

- **One step's outcome** — a review of this diff, the cause of this failure, a map of this module: invoke that step's skill with the request, and open no task.
- **An outcome that takes several steps** — build this feature, fix the flaky export test (find the cause, then change the code): name the step skills it takes, in the order their outcomes feed each other, and stop, until an act exists for it.

The output is a direct answer, a step's skill invoked, the fitting steps named, or one chosen act for [open-the-task](02-open-the-task.md). Under `--dry-run`, routing runs in full and [dry-run](../modules/dry-run.md) governs the rest.
