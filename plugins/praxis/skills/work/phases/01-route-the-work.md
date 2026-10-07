## Does it need a task?

First, the outcome. When what the request asks for *is* a write-up or a message for someone other than the asker to read — a summary, a status update, a decision record, an explanation pitched to a named reader — it is communicate's outcome: run it as one step's outcome (below), with no task. Any other request goes through the task test and the acts, and a summary it posts is its act's delivery at close-out — so "summarize how the export job works for Ana" is a write-up, while "research how teams version APIs and post a summary" is research. `(basis: maintainer, 2026-10-01)`

Then apply [when-work-needs-a-task](../rules/when-work-needs-a-task.md). If it doesn't need one, answer the request directly and stop: no task, no act, nothing written. With `--task=<key>`, skip this section and the next: the task exists, and its memory entry names its act; or the act its open round's line names, a ship round's being shipping, or, for a rework after peer review it opens, the act open-the-task's Rounds gives it; or shipping, when the request is to ship a change its act authored and the task has closed, an open round being taken under its own act first; or, for other work on a closed task of an act that authors a change, the act Which act? below matches. A request to file a finding about an existing task goes to [open-the-task](02-open-the-task.md)'s route for a finding.

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

`--act=<name>` replaces the match; a name with no act file is an error — say which acts exist and stop. When it's unclear whether the request fits an act, take the act: the proposal in [run-the-act](03-run-the-act.md) then asks before anything runs. When two acts fit, ask the user which, now. (routed to maintainer: both defaults, since the proposal shown before anything runs makes taking an act cheap to undo, while a wrong guess between two acts isn't.)

## When no act fits

Don't force one. The discriminator is the outcome the request asks for:

- **One step's outcome** — a review of this diff, the cause of this failure, a map of this module, a write-up of this change for the product manager: invoke that step's skill with the request, and open no task. Before invoking it, check that the ports its delivery would use are configured — the home's destination set where the backend uses one, and an audience space when the request names a reader [choose-form-and-channel](../../communicate/phases/03-choose-form-and-channel.md) places in one — and ask for what's missing then, as [run-the-act](03-run-the-act.md)'s proposal does. When the step hands back something meant to go somewhere — communicate's artifact, with its destination — deliver it by [deliver-through-the-ports](../rules/deliver-through-the-ports.md): publish a durable document, and post a message only when the request asks for it to reach someone — send, share, post, tell, notify and the like; naming a reader ("for Ana") says who it's for, not to send it. `(basis: maintainer, 2026-10-01)`
- **An outcome that takes several steps** — build this feature, fix the flaky export test (find the cause, then change the code): name the step skills it takes, in the order their outcomes feed each other, and stop, until an act exists for it.

The output is a direct answer, a step's skill invoked, the fitting steps named, or one chosen act for [open-the-task](02-open-the-task.md). Under `--dry-run`, routing runs in full and [dry-run](../modules/dry-run.md) governs the rest.
