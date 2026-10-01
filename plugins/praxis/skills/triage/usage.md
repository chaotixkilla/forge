# triage — usage

Decide whether a production signal is a real incident and how bad it is: confirm it isn't a flapping alert, scope what it affects, and set its severity on the house ladder or the runbook's own.

## When to use
- An alert is firing, an incident was declared, or users report failures, and you need to know whether it's real and how severe before anyone acts.
- You want to start from where the alarm already lives: an incident record (`--from-incident`) or a telemetry signal (`--from-telemetry`), with the report treated as a claim to check against the live signal.

## Not for / use instead
- Driving the whole response — mitigate, diagnose, communicate, learn → the incident act in **work**, which runs triage first.
- Restoring service once an incident is confirmed → **mitigate**.
- Finding why a defect happened → **debug**.
- Reading a signal or an incident record without judging it → the **telemetry** or **project-mgmt** port.

## Examples
`triage --from-telemetry=<signal-ref>` — start from a firing signal: confirm it's real, scope it, set its severity.
`triage --from-incident=<incident-ref>` — start from a declared incident record, reconciling its reported symptom and severity against the live signal.

## Gotchas
- **triage needs no configuration of its own.** Live signals come through `telemetry`, which owns `tools.telemetry`. With no telemetry and no seed, triage can't run blind: it stops and points to `init:telemetry`. With a seed but no live telemetry, it proceeds from the seed and says the live picture wasn't confirmed.
- **A flapping alert is not an incident.** Standing a signal down, with the noisy alert flagged for tuning, is a valid outcome.
- **Severity is the current rung, not a label for life.** It is re-assessed as the incident's duration and reach change.
