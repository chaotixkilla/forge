The signal is a real incident ([confirm-the-signal](01-confirm-the-signal.md)). Now answer the second judgment: how bad is it?

## Scope the blast radius

Establish *what* is affected and *how widely*: which capability or flow is degraded, how many users or what fraction, which services or regions, and whether it is spreading or steady. This scope is the input to severity here, and to whoever decides the incident's audience. Anchor it in the signal, not assumption — "logins failing for all users in EU" is scope; "logins seem broken" is not.

## Set the severity

Assign severity per [severity-scale](../rules/severity-scale.md) — the 3-level SEV1/SEV2/SEV3 ladder, placed by functional impact, blast radius and user impact, rounding up when two levels both fit and you can name the impact that justifies the higher one. First check whether the project's runbook defines its own severity vocabulary; if it does, use it, per [match-the-runbook-conventions](../../../craft/engineering/match-the-runbook-conventions.md). Severity is the *current* rung, not a permanent label: [severity-scale](../rules/severity-scale.md) re-assesses it as duration and blast radius change.

## The outcome

Every run ends in exactly one of three outcomes, read off the first judgment:

- **real incident** — returned with its scope, its severity and the reason for each, the signal it rests on, and any gap between a seed's report and the live picture; a scope read off the live signal is `observed`, and one that rests on the seed alone is `unverified` ([confirm-the-signal](01-confirm-the-signal.md)'s degrade).
- **investigate** — a real signal but not an incident: it persists or is corroborated, yet maps to no user-facing symptom. Returned as a lead to investigate, with the signal and what to check; the alert is not flagged for tuning, since it fired correctly ([confirm-the-signal](01-confirm-the-signal.md) ends the run there).
- **stood-down** — not a real signal: it oscillates or self-clears. Returned with the reason and the noisy alert flagged for tuning ([confirm-the-signal](01-confirm-the-signal.md) ends the run there).

Every run lands in exactly one: the signal is real or not, and a real one maps to a user-facing symptom or doesn't. `(basis: derived from real-signal-vs-flapping's symptom-mapping test)`

A signal triage couldn't judge either way, because telemetry was unavailable and nothing was seeded, isn't an outcome: the run stopped before judging ([confirm-the-signal](01-confirm-the-signal.md)'s degrade).
