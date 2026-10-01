Everything downstream — how hard the response mitigates, how often it communicates, what "resolved" will require — keys off two judgments triage makes: *is this a real incident at all?* and *how bad is it?* This phase makes the first.

## Establish the signal — confirm it is real before responding

Pull the current picture before reacting to the alarm. Read the firing signal and its surrounding context through the [telemetry](../../telemetry/SKILL.md) port — the metric's onset, rate, affected scope, and correlated signals — and recruit the [repository explorer](../../../agents/explorers/repository.md) for what changed recently near the symptom. Without fan-out, read the signal through the port and inspect recent history yourself before proceeding. Recruit only as [fan-out-only-when-it-pays](../../gather/rules/fan-out-only-when-it-pays.md) allows.

Then apply [real-signal-vs-flapping](../rules/real-signal-vs-flapping.md): weigh persistence, symptom-mapping, corroboration, and known-flappy history together. A signal that is sustained, maps to a user-facing symptom, and is corroborated is a real incident — **engage**. A signal that oscillates, fires from a lone internal probe with no user impact, and self-clears is noise — **stand down**: record it, flag the noisy alert for tuning, and end the run at the *stood-down* outcome ([scope-and-grade](02-scope-and-grade.md) holds the outcomes).

When a `--from-incident` ([from-incident](../modules/from-incident.md)) or `--from-telemetry` ([from-telemetry](../modules/from-telemetry.md)) seed is in play, its intake has already pulled the reported symptom/signal — fold it in here, but treat the report as a *claim to reconcile* against what the live signal actually shows, not ground truth — and the gap between reported and observed is itself evidence.

## Degrade and done-state

- **Degrade — telemetry unavailable.** triage cannot run blind. If the telemetry backend is unconfigured *and* no signal or incident was seeded, halt and guide the user to `init:telemetry`. If a signal *was* seeded (`--from-telemetry`/`--from-incident`) but live telemetry is unavailable, proceed from the seed and note that the live picture could not be confirmed.
- **Done-state.** Either a confirmed incident — go on to [scope-and-grade](02-scope-and-grade.md) — or a *stood-down* result with the reason and the noisy alert flagged for tuning, which ends the run.
