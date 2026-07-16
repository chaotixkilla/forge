# watch-until-stable (`--watch`)

Activated by `--watch`, referenced from [remediate-and-verify](../phases/04-remediate-and-verify.md).

Base behavior: [remediate-and-verify](../phases/04-remediate-and-verify.md) reads the signal once and reports the verdict as of now — often *indeterminate* for a fresh fix, said honestly. This module keeps operate **attached**, re-reading until the signal is provably stable, before a *resolved* declaration is allowed. Deletion test: remove it and remediate-and-verify still reads once and reports; the sustained hold is additive — so it is a module.

## The delta — hold open until the signal holds at baseline

Re-read the signal through the [telemetry](../../telemetry/SKILL.md) port — at least once per the signal's **refresh interval** (its scrape/update cadence; polling faster than the signal refreshes only re-reads jitter, polling slower than it can miss a mid-watch regression) — and keep the run open until it stays at **baseline** for the signal's **stability window** (the hold duration defined below — a distinct quantity from the refresh interval). Holding at baseline clears the *stability* gate for a resolved declaration; it is not the whole gate — [remediate-and-verify](../phases/04-remediate-and-verify.md) also requires a durable fix in place, so a held window resolves the incident only when the cause is gone, not merely because the signal is quiet.

- **Baseline** — the user-facing SLI/symptom metric back within its pre-incident range, and — where the signal is SLO-based — the burn rate below threshold on *all* configured windows (not the instantaneous rate dipping under the paging line once). `(basis: Google SRE "Alerting on SLOs" — a single sample back under threshold is the classic false recovery; the long window only clears well after errors stop.)`
- **Stability window** — how long baseline must hold. **Derive it from the signal's own evaluation window** — its configured hold-for duration (the pre-fire soak the signal itself requires), the burn-rate long window, or the recheck count that defines the signal — so the hold matches what the signal itself considers settled. This is the authoritatively-defensible bar and avoids inventing a number. `(basis: only the alerting layer (Prometheus for:/keep_firing_for, SRE burn-rate windows, Nagios max_check_attempts) defines a hold duration; no incident-process authority sets a wall-clock, so derive from the signal rather than fiat a minute count.)`
- **Fallback window** — when no evaluation window is derivable from the signal `(basis: ratified by the maintainer, 2026-07-11 — ~30 minutes at baseline for a steady signal, or one representative traffic cycle for a slow / load / time-triggered failure whose recurrence only shows under a full cycle. No incident-process authority sets a wall-clock, so this is a house standard; a signal that defines its own window always overrides it.)`.

## The verdicts it produces

- Signal holds at baseline through the window → clears the *resolved* gate.
- Window elapses / times out with the signal **unsettled or too thin to judge** → **indeterminate**, never rounded up to resolved: keep watching, widen the window, or hand off the watch.
- Signal regresses during the watch → back to [stabilize-first](../phases/02-stabilize-first.md) / [diagnose-root-cause](../phases/03-diagnose-root-cause.md); the fix didn't hold.

## Relation to the harness loop, and to `--background`

`--watch` stays **attached** and polls within the run — it does not reimplement scheduling, and it is the operational analogue of integrate's `--watch` (stay attached until signals settle). Detaching the watch across turns is `--background`'s job ([run-in-background](run-in-background.md)); this module only defines *what stable means* and *how long to hold*. Prerequisite: the re-reads go through the telemetry port (doer-owns-prerequisites; operate declares none) — if telemetry becomes unavailable mid-watch, report the last observed state as *indeterminate* and say the watch could not continue, rather than declaring resolved.
