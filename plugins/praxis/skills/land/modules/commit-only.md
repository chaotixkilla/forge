# commit-only (`--commit`)

Activated by `--commit`, referenced from [prepare-the-increment](../phases/02-prepare-the-increment.md) and [merge](../phases/04-merge.md).

The base run carries the change all the way to merged. This module truncates the run: record coherent local commits and stop — push nothing, merge nothing. Deletion test: remove this module and land runs the full path; stopping at local commits is an opt-in early terminus a flag selects, which is why it is a module.

## The delta — stop after committing

- **Run phases 1–2 only.** [assess-the-change](../phases/01-assess-the-change.md) and [prepare-the-increment](../phases/02-prepare-the-increment.md) run as normal — the work is assessed, staged into coherent commits ([one-coherent-change-per-unit](../rules/one-coherent-change-per-unit.md)), and messaged ([commits-tell-the-why](../../../craft/engineering/commits-tell-the-why.md)). Then the run **terminates** with the *committed-only* outcome.
- **Do not push, gate or merge.** The target reconcile in [prepare-the-increment](../phases/02-prepare-the-increment.md) doesn't run — the commits are recorded on the current branch as it stands — the push, the pre-merge gate and the merge do **not** run — nothing leaves the machine.
- **Report what was recorded.** Return the commits written (their refs and messages) and state plainly that nothing was pushed or landed, so the caller knows the change is local-only and what the follow-up (a plain `land` run) would do.

## Mutual exclusion — refuse, don't ignore

`--commit` stops before anything leaves the machine, so **`--gate`**, which acts on the pre-merge gate, is meaningless with it. Refuse the combination up front with a clear message ("`--commit` records locally and runs no gate"), rather than silently ignoring the other flag — a silent ignore leaves the caller believing a gate ran when it didn't. `(basis: derived from the artifacts port's up-front refusal of contradictory flags)`
