# read-only-boundary (`--read-only`)

Activated by `--read-only`, referenced from [trace-the-behavior](../phases/03-trace-the-behavior.md).

Deletion test: remove this module and understand still runs read-only against shared state; the flag exists to forbid the ephemeral execution the default allows, for a caller who cannot tolerate *any* side effect (a production system, an unfamiliar path that looks destructive).

## The boundary: mutation vs. safe observation
The line both postures are defined against — what counts as a mutation:

`(basis: derived from understand's read-only role and the observer-visibility test below; awaiting maintainer ratification)`

- **A mutation** is any action that changes state another observer could later see: writing a file in the tree, a commit, a write query, a state-changing call to a real service, sending a message, mutating shared or persistent state, or running a suite/app that does any of these against a real backend.
- **Safe observation** is any action whose only effect is on ephemeral, self-created state you discard: reading files, a read-only query against a copy or read replica, executing a path in a scratch directory or throwaway process, reading logs. The effect must not outlive the observation or be visible outside it.

The discriminator between them is **visibility to another observer**: if the action leaves a trace someone else, or a later run, could observe, it is a mutation; if its every effect dies with your process, it is safe observation.

## What each posture allows
- **Default (flag absent):** safe observation is *permitted* — including running the suite or app *if hermetic* (it writes only ephemeral state). understand *uses* it under the trigger in [trace-the-behavior](../phases/03-trace-the-behavior.md): run to reach *observed* only when a static trace cannot settle a load-bearing claim, otherwise accept *traced*. Mutations are never allowed; understand is read-only regardless of the flag. A path that can only be exercised by mutating shared state is traced statically, not run.
- **`--read-only` (flag set):** zero execution of any kind — no runs, probes, queries, or app start, even hermetic ones. Observation is static reading only. The consequence for the map: the top achievable certainty rung drops to **traced**, because *observed* requires the execution the flag forbids ([certainty-scale](../rules/certainty-scale.md)). State that cap in the map rather than grading a static read as observed.
