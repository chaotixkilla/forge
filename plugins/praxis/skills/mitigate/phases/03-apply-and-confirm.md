A mitigation isn't done when it's applied, and the alert clearing is the *start* of confirming it, not the end.

## Apply it through the path that owns it

mitigate decides what to do and applies it where a praxis capability owns the path: a rollback or redeploy of the last good version is a promotion of that version's ref through [ci](../../ci/SKILL.md)'s *promote to an environment*; without ci, it is returned as the recommended action. The last-good ref is the caller's when it names one, else the target line's previous release — its most recent release tag before this change, an ambient read. With neither, there is no ref to promote: the reversal is returned as the action owed, naming the ref it needs. `(basis: derived from a release tag being the version an environment last ran on a tagged line)` An action no praxis port performs — a failover, scaling, load shedding, a config revert, any feature switch — is returned as the recommended action, in its exact form, for the owner to take; a later mitigate run confirms it. mitigate never changes code: a code hotfix is a change to the code, so it is returned as the recommended action too.

Record what was done and when, the evidence [preserve-the-evidence](02-preserve-the-evidence.md) captured, and the mitigation's kind, durable or provisional, by [mitigate-before-diagnose](../rules/mitigate-before-diagnose.md)'s one test. Don't blanket-label a durable rollback as provisional.

## Confirm: signal back to baseline, and holding

Confirm the mitigation worked by the signal, not by assertion: a cleared alert or a success status is the system's claim about itself, not the effect ([observation-over-inference](../../../craft/evidence/observation-over-inference.md)). **Baseline** is defined, not eyeballed, by [confirm-the-signal-holds](../../../craft/evidence/confirm-the-signal-holds.md): the user-facing SLI or symptom metric back within its pre-incident range — its range over the same span before onset that the watch will hold for, the project's SLO band where one is set (routed to maintainer: the pre-onset span equal to the hold window, since a range sampled over the span the watch holds for compares like with like), and — where the signal is SLO-based — the burn rate below threshold on *all* configured windows, not merely the instantaneous rate dipping under the paging line.

The signal is the one the caller names by its telemetry reference — the incident's firing signal or symptom SLI. With none named, it can't be read, as without telemetry.

How long it must **hold** is the watch window. Under `--watch`, [watch-until-stable](../modules/watch-until-stable.md) holds the run open and re-reads until the signal stays at baseline for the signal's stability window; without `--watch`, read the signal once through the [telemetry](../../telemetry/SKILL.md) port and report it as of now — often not yet settled for a fresh mitigation, said honestly. Without telemetry, the signal can't be read, which the outcome below names. The hold comes from the signal's own evaluation window, by the same standard; the module carries mitigate's fallback.

## The outcome

Every run ends in exactly one of three outcomes, read off two facts: *was a mitigation applied* — by this run, or, in a confirming run, by its owner before it, as the caller states — and *is the signal back within baseline — yes, no, or can't tell yet?*

- **mitigated** — applied, and the signal is back within baseline. Returned with the actions and their times, the evidence captured, the kind (durable or provisional), and the signal's hold: held through the window.
- **indeterminate** — applied, but the signal can't yet say: still decaying, too thin to judge, unsettled when the window ended, or unreadable. Returned with the last observed state and what would settle it; never rounded up to mitigated.
- **not-mitigated** — nothing was applied, or the applied mitigation didn't bring the signal back. Returned with why and the recommended next action: no safe mitigation was available, the user declined or couldn't confirm an irreversible one, the action is its owner's to take, or the applied mitigation didn't bring the signal back. Service still down is a state worth reporting, never a reason to force an unsafe action. `(basis: derived — the incident act already expects indeterminate)`

A mitigated incident isn't resolved: a provisional mitigation leaves the real fix owed, and even a durable one resolves the incident only once its hold is confirmed. That call belongs to whoever runs the response, not to mitigate.
