# watch-the-pipeline (`--watch`)

Activated by `--watch`, referenced from [confirm-healthy](../phases/03-confirm-healthy.md).

Base behavior: roll-out promotes and returns the *immediate* result — the promotion was accepted, the signals read once. This module keeps roll-out **attached** until the deploy run and the post-ship signals actually **settle**, then returns the settled verdict rather than firing and forgetting. Deletion test: remove this module and roll-out still promotes and returns the immediate outcome; the sustained watch is additive, so it is a module.

## The delta — stay attached until it settles

- **Await the deploy run.** Instead of returning when the pipeline is *triggered*, block on the [ci](../../ci/SKILL.md) capability's *await a run* operation until the run reaches a terminal verdict within its timeout. A timeout with the run still in flight is reported as *not-yet-settled* (retryable), never silently treated as a pass.
- **Watch the post-ship signals.** After the rollout, read the post-ship signals through the [telemetry](../../telemetry/SKILL.md) capability across the watch window and apply the health verdict pinned in [confirm-healthy](../phases/03-confirm-healthy.md) — don't return "rolled out, healthy" the instant the promotion is accepted; a rollout can be accepted and then degrade.
- **Return the settled verdict.** Return the outcome — the deploy run's pass/fail and the post-ship health verdict (healthy / needs-rollback / indeterminate) — as the run's result, so the caller acts on what settled, not on what was merely started.

## Composition

- **With `--on-fail`** ([failure-policy](failure-policy.md)): if the watched run or rollout settles to a failure, the `--on-fail` policy fires on the settled failure — this is exactly the point of watching, so a `rollback` policy can act while roll-out is still attached rather than after the caller has walked away. An `ask` policy acts as `abort` here, since nobody is waiting to answer: the result lists the decisions `ask` would have offered, for the user to make on their return.
- **With `--target`**: the watch spans the promotion and its signal window.

## Prerequisite and degrade

The await goes through the [ci](../../ci/SKILL.md) capability and the signal watch through the [telemetry](../../telemetry/SKILL.md) capability (each owns its own prerequisite — doer-owns-prerequisites; roll-out declares none). Degrade **per capability**: if `tools.ci` is unavailable, the deploy run can't be awaited — return the immediate outcome and that the run couldn't be watched; if `tools.telemetry` is unavailable, the rollout still stands but post-ship health can't be judged — report *indeterminate* health and say why. A missing watch backend narrows what can be *observed*; it never undoes the rollout. `(basis: per-capability degrade; mirrors debug's --from-telemetry degrade)`

While watching, decide and record instead of asking ([ask-while-the-user-is-here](../../gather/rules/ask-while-the-user-is-here.md)).
