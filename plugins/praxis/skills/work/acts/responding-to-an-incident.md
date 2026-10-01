# Responding to an incident

**Entry condition.** A production service is degraded or failing now — an alert is firing, an incident was declared, or users report failures — and the request is to restore it. Investigating a failure with no live impact goes to the [debug](../../debug/SKILL.md) skill directly, and judging a signal alone to [triage](../../triage/SKILL.md). (basis: maintainer, 2026-09-30)

**Done when** the incident rests at one of its four outcomes below, that outcome has been declared to the incident's audience, and, for a real incident, its retrospective is written and its follow-ups are filed. (basis: maintainer, 2026-07-11)

## Mitigate before diagnose

Restoring service comes first ([mitigate-before-diagnose](../../mitigate/rules/mitigate-before-diagnose.md)); diagnosis runs once the incident is no longer actively burning. Documentation must not slow mitigation: while the incident is live, each step's result is appended to the incident's timeline notes, and the full pages are written once the service is stable. The task key is the incident's ID. (basis: maintainer, 2026-09-30)

## The durable fix

The lasting correction is usually a code change, and it runs as its own acts in the same task: fixing a bug, then shipping. When the severity licenses fixing forward — SEV1, or SEV2 while impact is ongoing — and the change is bounded, obviously correct and reversible, those acts run as soon as debug confirms the cause, and the change ships as a hotfix. A SEV3 always waits for the normal path. Where the project's runbook sets its own fix-forward or escalation convention, it takes precedence ([match-the-runbook-conventions](../../triage/rules/match-the-runbook-conventions.md)). (basis: maintainer, 2026-07-11)

## The four outcomes

Walk these in order; each is answered from observed facts, not judgment.

1. **Did triage confirm a real incident?** No → **stood-down**.
2. **Is a durable fix in place, and has user-facing impact ended?** A *durable fix* means the offending behavior can no longer recur through normal operation: a landed correction, or a rollback, revert or permanent kill that removed the offending change. A provisional stop-gap doesn't count. *Impact ended* means the SLI is back within baseline. When a durable fix is already in place (a rollback, say), a code change still to come is the forward re-fix, a follow-up that doesn't hold the incident open. No durable fix in place → **mitigated-but-watching**: contained, with the durable fix or full confirmation still owed.
3. **Did the signal hold at baseline through the watch window?** Held → **resolved**. The window closed with the signal unsettled or too thin to judge → **indeterminate**, never rounded up to resolved, and the watch is handed off.

The severity sets how firm the confirmation must be: a SEV1 resolution warrants the full held-at-baseline window before it's declared; a SEV3 may resolve on a shorter observation. Root-cause understanding isn't a gate on resolution; it's tracked as a follow-up. A team's runbook may require the cause found and recurrence prevented before resolution; where it does, honor it, and the incident stays open until that follow-up lands. `(basis: maintainer, 2026-07-11; after Atlassian, PagerDuty and ITIL; the root-cause camp after Google SRE, "Managing Incidents", and incident.io)`

## Steps

(basis: maintainer, 2026-09-30)

| # | step | inputs | skipped by the act when |
|---|---|---|---|
| 1 | [triage](../../triage/SKILL.md), with `--from-incident=<ref>` or `--from-telemetry=<ref>` when the request names a record or a signal | the reported symptom or signal | never |
| 2 | [mitigate](../../mitigate/SKILL.md) | step 1's scope and severity, and the incident's prior actions | step 1 stood the signal down |
| 3 | [debug](../../debug/SKILL.md) `--from-incident=<the incident's record>` | the symptom, step 1's scope, step 2's actions and the evidence it captured, and the timeline notes | step 1 stood the signal down |
| 4 | [communicate](../../communicate/SKILL.md), the incident's retrospective | the timeline notes and every step's result | step 1 stood the signal down |

When step 2 ends not-mitigated, the status update says so and step 3 still runs, since diagnosis is then the way to restore service. An action step 2 returned for its owner is checked by running step 2 again once the owner reports it taken.

## Filed

While the incident is live, each step's result is appended to the task's scratchpad as the incident's timeline notes. Step 4's retrospective files as the incident record, with a decision record for each one-way-door decision the response made, such as an irreversible mitigation. (basis: derived from the document types' membership tests)

## Delivered

- **Status, at every transition.** Post through [communication](../../communication/SKILL.md) when step 1 confirms the incident (acknowledged), when step 2 ends (mitigated, or not), on any severity change, and at close-out with the outcome, pitched per [right-sized-status-updates](../rules/right-sized-status-updates.md). The target is the one the request names; without one, the incident channel praxis settings record (`tools.communication.channels.incident`); with neither, the update is returned for hand delivery. A stood-down signal gets one brief note, so watchers know the alert was noise. Declare the outcome explicitly: *resolved* only when the signal held at baseline, *mitigated-but-watching* while the fix or confirmation is owed, *indeterminate* when the watch couldn't confirm stability.
- **Follow-ups.** File each follow-up the retrospective names through [project-mgmt](../../project-mgmt/SKILL.md), with its owner and its gating or advisory mark: the durable fix among them when the task hasn't run it yet.
