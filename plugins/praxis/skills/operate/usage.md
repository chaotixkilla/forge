# operate — usage

Run and respond to a production incident end-to-end: confirm and triage a live signal, mitigate to restore service, diagnose the true cause, remediate durably and verify the signal holds at baseline, communicate at a severity-right cadence, and turn the incident into prevention.

## When to use
- Production is degraded or down and someone has to drive the response: a telemetry signal is firing, an incident was declared, or users are reporting failures. operate carries the incident authority to **mitigate** — to restore service before the cause is understood — which a plain investigation does not.
- You want to start from where the alarm already lives: an incident record (`--from-incident`) or a telemetry signal (`--from-telemetry`), and have triage anchor on it instead of starting cold.
- You want the response to hold the whole arc — triage → stabilize → diagnose → remediate → communicate → learn — not just the fix, so the signal is verified back to baseline, stakeholders are kept informed, and the incident becomes a guardrail rather than a repeat.
- You want to stay attached after the fix until the signal is provably stable (`--watch`), or detach and be re-engaged only on a state change (`--background`).

## Not for / use instead
- Root-causing a specific defect that already bit, with no live incident and no authority to mitigate → **debug**. debug fixes the mechanism (cause-only by default) and will not patch a symptom from its own read of production; operate runs *under* a declared incident and mitigate-first is its default. (debug explicitly defers the mitigate branch to a declared incident — that is this skill.)
- Shipping a change and watching its rollout settle → **integrate** (`--watch` there watches a *deploy*; operate responds when a shipped change *degrades* production).
- Proactive tech-debt paydown, dependency upgrades, or scoped refactors with no incident → **maintain**.
- Reading a live signal, posting a status message, reading an incident record, or publishing a document → the capability ports (**telemetry**, **communication**, **project-mgmt**, **publish-artifact**). operate *decides* what the signal means and what to do; the ports carry out the read/post/publish it hands them.
- Authoring or running tests to confirm intended behavior → **test** / **verify**. operate confirms a signal returned to *baseline*, not that a feature is correct.

## Examples
`operate --from-telemetry=<signal-ref>` — start from a firing signal: triage confirms it is a real incident (not a flapping alert), scopes it, and sets severity, then drives the response.
`operate --from-incident=<incident-ref>` — start from a declared incident record: triage seeds from its reported symptom, severity, and prior actions rather than cold.
`--watch` — after remediation, hold the run open and re-read the signal until it stays at baseline for the signal's stability window before declaring resolved (a timeout with the signal unsettled reports *indeterminate*, never resolved).
`--notify` — push status transitions (acknowledged, mitigated, resolved) over the communication capability at phase boundaries; pair with `--channel=<ref>` to override the target.
`--background` — detach the loop so watching/diagnosis continues across turns, re-engaging only on a state change or threshold breach.
`--publish` — publish the incident record / postmortem as a durable team-facing document via the artifacts capability.

## Gotchas
- **operate mitigates; that is what separates it from debug.** Under a live incident, restoring service comes before understanding — but a mitigation (rollback, failover, restart) can destroy the evidence root-cause needs. operate prefers the fastest *reversible* mitigation and snapshots volatile, non-reproducible evidence first when the mitigation would erase it.
- **operate needs no configuration of its own.** It delegates every backend to a port. If telemetry isn't configured and no signal was seeded, triage cannot run blind — it halts and guides you to `init:telemetry`. If communication isn't configured, status updates degrade to being returned for you to send by hand; the response still runs.
- **operate does not carry the durable code fix.** The lasting correction is usually a code change — operate hands it to **develop** / **debug --fix** and tracks it as a follow-up, carrying the change itself only for a genuine hotfix under high severity. A resolved incident may still owe a *forward* code fix: when the durable fix was a rollback that removed the offending change, re-landing the feature correctly is a tracked follow-up, not an open incident.
- **"Resolved" is a real threshold, not the moment the alert clears.** operate declares resolved only when impact has ended, a durable fix (not a transient mitigation) is in place, and the signal has held at baseline through the watch window; short of that the state is *mitigated-but-watching*.
- **`--channel` needs a messaging path.** It only sets the target for `--notify`/status posts; on its own, with no notification being sent, it does nothing.
- **A flapping alert is not an incident.** Triage will stand the run down if the signal is transient/self-clearing and maps to no user-facing symptom — a valid, valuable outcome, not a failure to respond.
