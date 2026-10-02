# watch-until-stable (`--watch`)

Activated by `--watch`, referenced from [apply-and-confirm](../phases/03-apply-and-confirm.md).

Base behavior: [apply-and-confirm](../phases/03-apply-and-confirm.md) reads the signal once and reports it as of now — often not yet settled for a fresh mitigation, said honestly. This module keeps mitigate **attached**, re-reading until the signal is provably stable. Deletion test: remove it and apply-and-confirm still reads once and reports; the sustained hold is additive — so it is a module.

## The delta — hold open until the signal holds at baseline

Keep the run open, re-reading the signal through the [telemetry](../../telemetry/SKILL.md) port, until it holds at baseline for the window apply-and-confirm sets — the caller's named hold, else the one [confirm-the-signal-holds](../../../craft/evidence/confirm-the-signal-holds.md) derives from the signal's own evaluation window — reading at least once per the signal's refresh interval. Holding at baseline is the *stability* half of resolving an incident, not the whole of it: the incident also needs a durable fix in place, so a held window resolves it only when the cause is gone, not merely because the signal is quiet.

- **Baseline** is that standard's, read against the incident: the user-facing SLI or symptom metric back within its pre-incident range, and the burn rate below threshold on all configured windows where the signal is SLO-based.
- **The fallback hold** — when no evaluation window is derivable from the signal: ~30 minutes at baseline for a steady signal, or one representative traffic cycle for a slow, load- or time-triggered failure whose recurrence only shows under a full cycle. `(basis: maintainer, 2026-07-11)`

## The result

The watch's result is placed by [apply-and-confirm](../phases/03-apply-and-confirm.md)'s result list.

## Relation to the harness loop

`--watch` stays **attached** and polls within the run — it does not reimplement scheduling; this module only defines *what stable means* and *how long to hold*. Prerequisite: the re-reads go through the telemetry port (doer-owns-prerequisites; mitigate declares none); if telemetry becomes unavailable mid-watch, the watch ends there and apply-and-confirm places the result.

While watching, decide and record instead of asking ([ask-while-the-user-is-here](../../gather/rules/ask-while-the-user-is-here.md)).
