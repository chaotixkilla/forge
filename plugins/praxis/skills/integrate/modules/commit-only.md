# commit-only (`--commit`)

Activated by `--commit`, referenced from [land-it](../phases/04-land-it.md).

The base run carries the change all the way to landed (and, with a target, shipped). This module truncates the run: record coherent local commits and stop — push nothing, open nothing, merge nothing. Deletion test: remove this module and integrate runs the full land/ship path; stopping at local commits is an opt-in early terminus a flag selects, which is why it is a module.

## The delta — stop after committing

- **Run phases 1–2 only.** [assess-the-change](../phases/01-assess-the-change.md) and [prepare-the-increment](../phases/02-prepare-the-increment.md) run as normal — the work is assessed, staged into coherent commits ([one-coherent-change-per-unit](../rules/one-coherent-change-per-unit.md)), and messaged ([commits-tell-the-why](../rules/commits-tell-the-why.md)). Then the run **terminates** with the *committed-only* outcome.
- **Do not reconcile, gate, land, or ship.** The target reconcile in [prepare-the-increment](../phases/02-prepare-the-increment.md) still runs *only if* it is needed to produce clean commits on the current branch; the push, the pre-merge gate, the merge/PR, and any rollout do **not** run — nothing leaves the machine.
- **Report what was recorded.** Return the commits written (their refs and messages) and state plainly that nothing was pushed or landed, so the caller knows the change is local-only and what the follow-up (a plain `integrate` run) would do.

## Mutual exclusion — refuse, don't ignore

`--commit` stops before anything leaves the machine, so the flags that act *upstream* are meaningless with it: **`--pr`, `--target`, `--watch`, and `--gate`** each require pushing/landing/shipping that `--commit` forbids. Refuse the contradictory combination up front with a clear message (e.g. "`--commit` records locally and cannot also `--pr`/ship"), rather than silently ignoring the other flag — a silent ignore leaves the caller believing a PR was opened or a deploy happened when it wasn't. `(basis: publish-artifact rejects contradictory invocations (e.g. --idempotent with --version) up front rather than silently resolving them — the same fail-loud-on-contradiction discipline.)`
