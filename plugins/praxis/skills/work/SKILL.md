---
name: work
description: Start or resume a piece of engineering work — work out which kind of work it is, run that act's steps in the act's order, keep the task's documentation and memory entry current, and deliver the results. The entry point for engineering work in a praxis project; for one specific step on its own, use that step's skill directly.
metadata:
  flags:
    --task=<key>: resume the named task instead of working out which task the request belongs to (a phase input, not a behavior module)
    --act=<name>: run the named act instead of routing the work to one (a phase input, not a behavior module)
    --dry-run: show the act, the steps it would propose and what would be recorded, without running a step or writing anything — activates the dry-run module
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies. work owns no backend of its own: it delivers through the ports and hands results to [document](../document/SKILL.md), each the doer that owns its own prerequisite, so it declares no `config_requires`.

`--dry-run` changes the whole run — every phase computes, none writes: see [modules/dry-run.md](modules/dry-run.md).

1. Route the work: decide whether it needs a task at all, and which act it is  — see [phases/01-route-the-work.md](phases/01-route-the-work.md)
2. Open the task: find or create it, re-read its intent, and record which act is running  — see [phases/02-open-the-task.md](phases/02-open-the-task.md)
3. Run the act: propose its steps, run each with its inputs in the act's order, and hand each result on  — see [phases/03-run-the-act.md](phases/03-run-the-act.md)
4. Close out: check the act's done-condition, deliver, and leave the task ready to resume  — see [phases/04-close-out.md](phases/04-close-out.md)
