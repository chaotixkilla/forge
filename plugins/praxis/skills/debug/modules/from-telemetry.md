# from-telemetry (`--from-telemetry`)

Activated by `--from-telemetry=<ref>`, referenced from [reproduce-and-frame](../phases/01-reproduce-and-frame.md) (the intake site).

Deletion test: remove it and debug still frames from the user's report or a local reproduction; seeding from a telemetry signal is optional intake a flag turns on.

## The delta

Seed the investigation from a live observability signal, read through the [telemetry](../../telemetry/SKILL.md) port (a metric, trace, error-aggregate, or dashboard by reference). Fold what it returns into framing and evidence:

- **Onset** — when the signal first appeared. A sharp onset is a regression's timestamp, and it hands [localize-the-fault](../phases/03-localize-the-fault.md) a good/bad boundary to bisect the history against.
- **Frequency and affected scope** — how often, and for which users/tenants/inputs/environments. This sizes the blast radius and separates a universal bug from an edge case.
- **Correlated signals and sample traces** — what else moved at the same time, and concrete exemplars (stack traces, trace spans) that name the failing path.

The point of the seed is to turn a **spike into a concrete reproduction target**: use the sample traces and correlated conditions to reconstruct the input/state that triggers the failure, so the run has something to make fail on demand ([reproduce-before-fixing](../rules/reproduce-before-fixing.md)) rather than a graph of aggregate pain.

debug sheds the telemetry prerequisite to the port. If telemetry isn't configured or the signal can't be read, the port reports it unavailable and this seed degrades — proceed from a local reproduction or the other evidence lanes, noting the missing signal rather than stalling.
