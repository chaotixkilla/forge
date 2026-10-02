# read-only-boundary (`--read-only`)

Activated by `--read-only`, referenced from [trace-the-behavior](../phases/03-trace-the-behavior.md).

Deletion test: remove this module and understand still runs read-only against shared state; the flag exists to forbid the ephemeral execution the default allows, for a caller who cannot tolerate *any* side effect (a production system, an unfamiliar path that looks destructive).

## The delta

The line between a mutation and safe observation is [mutation-vs-observation](../rules/mutation-vs-observation.md), and it holds on every run. This module narrows what the run may do on the safe side of it:

- **`--read-only` (flag set):** zero execution of any kind — no runs, probes, queries, or app start, even hermetic ones. Observation is static reading only. The consequence for the map: the top achievable certainty rung drops to **traced**, because *observed* requires the execution the flag forbids ([certainty-scale](../rules/certainty-scale.md)). State that cap in the map rather than grading a static read as observed.
