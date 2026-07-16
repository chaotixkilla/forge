Triage is where the response is shaped: everything downstream — how hard you mitigate, how often you communicate, what "resolved" will require — keys off two judgments made here. First, *is this a real incident at all?* Second, *how bad is it?* Get the first wrong and you either burn a night on a flapping alert or miss a live outage; get the second wrong and the whole response runs at the wrong tempo. This phase confirms the signal, scopes the blast radius, and sets severity — and it can legitimately end the run before any of that if the signal turns out to be noise.

## Establish the signal — confirm it is real before responding

Pull the current picture before reacting to the alarm. Read the firing signal and its surrounding context through the [telemetry](../../telemetry/SKILL.md) port — the metric's onset, rate, affected scope, and correlated signals — and recruit the [repository explorer](../../../agents/explorers/repository.md) for what changed recently near the symptom. Without fan-out, read the signal through the port and inspect recent history yourself before proceeding.

Then apply [real-signal-vs-flapping](../rules/real-signal-vs-flapping.md): weigh persistence, symptom-mapping, corroboration, and known-flappy history together. A signal that is sustained, maps to a user-facing symptom, and is corroborated is a real incident — **engage**. A signal that oscillates, fires from a lone internal probe with no user impact, and self-clears is noise — **stand down**: record it, route the noisy alert to be tuned, and end the run at the *stood-down* terminal outcome ([remediate-and-verify](04-remediate-and-verify.md) owns the outcome set). Standing down on noise is a correct, valuable result — not a failure to respond.

When a `--from-incident` ([from-incident](../modules/from-incident.md)) or `--from-telemetry` ([from-telemetry](../modules/from-telemetry.md)) seed is in play, its intake has already pulled the reported symptom/signal — fold it in here, but treat the report as a *claim to reconcile* against what the live signal actually shows, not ground truth (the reported blast radius and the observed one often differ, and the gap is itself evidence).

## Scope the blast radius

For a confirmed incident, establish *what* is affected and *how widely*: which capability or flow is degraded, how many users or what fraction, which services/regions, and whether it is spreading or steady. This scope is the input both to severity and to the audience decision in [communicate-status](05-communicate-status.md). Anchor it in the signal, not assumption — "logins failing for all users in EU" is scope; "logins seem broken" is not.

## Set the severity

With the incident confirmed and scoped, assign severity per [severity-scale](../rules/severity-scale.md) — the 3-level SEV1/SEV2/SEV3 ladder, placed by functional impact, blast radius, and user impact, rounding up when two levels both fit and you can name the impact that justifies the higher one. First check whether the project's runbook defines its own severity vocabulary; if it does, use it, per [match-the-runbook-conventions](../rules/match-the-runbook-conventions.md) — do not impose the house ladder over an established one. Severity is the *current* rung, not a permanent label: [severity-scale](../rules/severity-scale.md) re-assesses it as duration and blast radius change.

## Degrade and done-state

- **Degrade — telemetry unavailable.** operate cannot triage blind. If the telemetry backend is unconfigured *and* no signal or incident was seeded, halt and guide the user to `init:telemetry` — there is no honest triage without a signal to read. If a signal *was* seeded (`--from-telemetry`/`--from-incident`) but live telemetry is unavailable, proceed from the seed and note that the live picture could not be confirmed.
- **Done-state.** Either a confirmed incident carrying a severity and a scope — proceed to [stabilize-first](02-stabilize-first.md) — or a *stood-down* result with the reason and the noisy alert flagged for tuning, which ends the run.
