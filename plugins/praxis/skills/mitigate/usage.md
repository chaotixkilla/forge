# mitigate — usage

Restore a degraded production service before anyone knows why it broke: choose the fastest safe, reversible action, capture the evidence that action would erase, apply it, and confirm the signal is back at baseline and holding.

## When to use
- A real incident is under way and users are hurting now, so stopping the harm comes before understanding it.
- You want the mitigation's kind on record — durable (the offending change is gone) or provisional (a stop-gap, the real fix still owed) — so nobody mistakes a stop-gap for a resolution.

## Not for / use instead
- Deciding whether a signal is a real incident, and how severe → **triage**.
- Driving the whole response — triage, mitigate, diagnose, communicate → the incident act in **work**.
- Finding the cause → **debug**. mitigate restores service; it doesn't explain the failure.
- The durable code fix → the fixing-a-bug act in **work**. mitigate never changes code.
- Rolling a merged change out → **roll-out**.

## Examples
`mitigate` — choose, capture, apply and confirm, reading the signal once at the end.
`mitigate --watch` — stay attached until the signal holds at baseline through its hold window: the one the caller names, else the signal's own.

## Gotchas
- **mitigate needs no configuration of its own.** Pipeline actions go through `ci`, which owns `tools.ci`, and the signal through `telemetry`, which owns `tools.telemetry`. Without `tools.ci`, a rollback is returned as the recommended action; without `tools.telemetry`, the signal can't be read, so the result is not checked ([results-and-certainty](../../craft/evidence/results-and-certainty.md)), with that reason.
- **Reversible first.** An irreversible mitigation is taken only with your confirmation, asked with what it can't undo; with no one to answer, it's returned as the recommendation and not taken.
- **Some actions aren't praxis's to take.** A failover or a scaling change that only its owner can make is returned in its exact form, and a later run checks whether it held.
- **A mitigation that holds hasn't resolved the incident.** A provisional stop-gap leaves the real fix owed.
