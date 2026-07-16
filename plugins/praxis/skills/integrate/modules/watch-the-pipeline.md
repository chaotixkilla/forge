# watch-the-pipeline (`--watch`)

Activated by `--watch`, referenced from [confirm-and-report](../phases/06-confirm-and-report.md).

Base behavior: integrate fires the land/ship and reports the *immediate* result — the run was triggered, the promotion was accepted. This module keeps integrate **attached** until the run and the post-ship signals actually **settle**, then reports the settled verdict rather than firing and forgetting. Deletion test: remove this module and integrate still lands/ships and reports the immediate outcome; the sustained watch is additive, so it is a module.

## The delta — stay attached until it settles

- **Await the run.** Instead of returning when the pipeline is *triggered*, block on the [ci](../../ci/SKILL.md) capability's *await a run* operation until the run reaches a terminal verdict within its timeout. A timeout with the run still in flight is reported as *not-yet-settled* (retryable), never silently treated as a pass.
- **Watch the post-ship signals.** After a ship, read the post-ship signals through the [telemetry](../../telemetry/SKILL.md) capability across the watch window and apply the health verdict pinned in [confirm-and-report](../phases/06-confirm-and-report.md) — do not report "shipped, healthy" the instant the promotion is accepted; a rollout can be accepted and then degrade.
- **Report the settled verdict.** Return the terminal outcome — the run's pass/fail and the post-ship health verdict (healthy / needs-rollback / indeterminate) — as the run's result, so the caller acts on what settled, not on what was merely started.

## Composition

- **With `--on-fail`** ([failure-policy](failure-policy.md)): if the watched run or rollout settles to a failure, the `--on-fail` policy fires on the settled failure — this is exactly the point of watching, so a `rollback` policy can act while integrate is still attached rather than after the caller has walked away.
- **With `--target`** ([promote-to-environment](promote-to-environment.md)): the watch spans the promotion and its signal window; without a target, `--watch` still awaits the *gate/land* run to settle.

## Prerequisite and degrade

The await goes through the [ci](../../ci/SKILL.md) capability and the signal watch through the [telemetry](../../telemetry/SKILL.md) capability (each owns its own prerequisite — doer-owns-prerequisites; integrate declares none). Degrade **per capability**: if `tools.ci` is unavailable, the run can't be awaited — report the landing/immediate outcome and that the run could not be watched; if `tools.telemetry` is unavailable, the ship still stands but post-ship health can't be judged — report *indeterminate* health and say why. A missing watch backend narrows what can be *observed*; it never undoes the land or ship. `(basis: integrate's per-capability degrade posture, USING-ANVIL §2 doer-owns-prerequisites; mirrors debug's --from-telemetry degrade.)`
