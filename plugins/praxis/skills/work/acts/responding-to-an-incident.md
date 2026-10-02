# Responding to an incident

**Entry condition.** A production service is degraded or failing now — an alert is firing, an incident was declared, or users report failures — and the request is to restore it. Investigating a failure with no live impact goes to the [debug](../../debug/SKILL.md) skill directly, and judging a signal alone to [triage](../../triage/SKILL.md). (basis: maintainer, 2026-09-30)

**Done when** the incident rests at one of its five outcomes below, that outcome has been declared to the incident's audience, and, for a real incident, its retrospective is written and its follow-ups are filed. A gating follow-up holds the incident record open until it lands, not the task. An *ongoing* or *indeterminate* incident isn't done: the recommended action, or what would settle it, is the task's next step. (basis: maintainer, 2026-07-11)

## Mitigate before diagnose

Restoring service comes first ([mitigate-before-diagnose](../../mitigate/rules/mitigate-before-diagnose.md)); diagnosis runs once the incident is no longer actively burning. Documentation must not slow mitigation: while the incident is live, each step's result is appended to the incident's timeline notes, and the full pages are written once the service is stable. The task key is the incident's ID. (basis: maintainer, 2026-09-30)

## The durable fix

The lasting correction is usually a code change, and it runs as its own acts in the same task: fixing a bug, then shipping. When the severity licenses fixing forward — SEV1, or SEV2 while impact is ongoing — and the change is safe to rush — debug confirmed its mechanism, it sits in [change-risk-scale](../../../craft/engineering/change-risk-scale.md)'s *contained* tier, and it backs out with a single clean revert — those acts run as soon as debug confirms the cause, and the change ships as a hotfix. A SEV3 always waits for the normal path. Where the project's runbook sets its own fix-forward or escalation convention, it takes precedence ([match-the-runbook-conventions](../../../craft/engineering/match-the-runbook-conventions.md)). (basis: maintainer, 2026-07-11)

## The five outcomes

Walk these in order; each is answered from observed facts, not judgment.

1. **Did triage confirm a real incident?** Triage stood the signal down, or found a lead with no user-facing symptom (*investigate*) → **stood-down**; an investigate lead is carried in the report as a follow-up. Triage halted — no telemetry and nothing seeded — → **indeterminate**: nothing was confirmed either way, and the report names what would settle it.
2. **Has user-facing impact ended?** Read off step 2's outcome. *Mitigated* → yes. *Not-mitigated* → no → **ongoing**: the incident isn't contained, and mitigate's recommended action, with its owner, is the task's next step. *Indeterminate* → **indeterminate**, the watch handed off.
3. **Is a durable fix in place?** A *durable fix* means the offending behavior can no longer recur through normal operation: a landed correction, or a rollback, revert or permanent kill that removed the offending change. A provisional stop-gap doesn't count. When a durable fix is already in place (a rollback, say), a code change still to come is the forward re-fix, a follow-up that doesn't hold the incident open. No → **mitigated-but-watching**: contained, with the durable fix or full confirmation still owed.
4. **Did the signal hold at baseline through the watch window?** Step 2's `--watch` holds the window; for a durable fix this task shipped, the shipping act's health verdict does. Held → **resolved**. The window closed with the signal unsettled, too thin to judge, or unreadable → **indeterminate**, never rounded up to resolved, and the watch is handed off.

Every run lands in exactly one: each question is asked only once the ones before it are answered, and every answer a step can return is listed with the outcome it ends at. `(basis: derived)`

The severity sets how firm the confirmation must be: a SEV1 or SEV2 resolution warrants the full held-at-baseline window before it's declared; a SEV3 resolves once the signal has held for half of it (routed to maintainer: half the window for SEV3, since a SEV3's bounded impact makes the shorter confirmation an acceptable risk). Root-cause understanding isn't a gate on resolution; it's tracked as a follow-up. A team's runbook may require the cause found and recurrence prevented before resolution; where it does, honor it, and the incident stays open until that follow-up lands. `(basis: maintainer, 2026-07-11; after Atlassian's Incident Management Handbook, PagerDuty's incident-response guide and ITIL; the root-cause camp after Google SRE, "Managing Incidents", and incident.io's incident guide)`

## Steps

(basis: maintainer, 2026-09-30)

| # | step | inputs | skipped by the act when |
|---|---|---|---|
| 1 | [triage](../../triage/SKILL.md), with `--from-incident=<ref>` or `--from-telemetry=<ref>` when the request names a record or a signal | the reported symptom or signal | never |
| 2 | [mitigate](../../mitigate/SKILL.md) `--watch` | step 1's scope and severity, the firing signal's telemetry reference, and the incident's prior actions | step 1 didn't confirm an incident |
| 3 | [debug](../../debug/SKILL.md) `--from-incident=<the incident's record>` | the symptom, step 1's scope, step 2's actions and the evidence it captured, and the timeline notes | step 1 didn't confirm an incident |
| 4 | [communicate](../../communicate/SKILL.md), the incident's retrospective | the timeline notes and every step's result | step 1 didn't confirm an incident |

When step 2 ends not-mitigated, the status update says so and step 3 still runs, since diagnosis is then the way to restore service. An action step 2 returned for its owner is checked by running step 2 again once the owner reports it taken.

## Filed

While the incident is live, each step's result is appended to the task's scratchpad as the incident's timeline notes. Step 4's retrospective files as the incident record, with a decision record for each one-way-door decision the response made, such as an irreversible mitigation. (basis: derived from the document types' membership tests)

## Delivered

- **Status, at every transition.** Post through [communication](../../communication/SKILL.md) when step 1 confirms the incident (acknowledged), when step 2 ends (mitigated, or not), on any severity change, and at close-out with the outcome, pitched and timed per [right-sized-status-updates](../rules/right-sized-status-updates.md): at every transition, and between them on its severity's cadence, never silent past it. The target is the one the request names; without one, the incident channel praxis settings record (`tools.communication.channels.incident`); with neither, the update is returned for hand delivery. A stood-down run gets one brief note, so watchers know the alert was noise, or, for an investigate lead, that users weren't affected. Declare the outcome explicitly: *resolved* only when the signal held at baseline, *ongoing* while impact continues, *mitigated-but-watching* while the fix or confirmation is owed, *indeterminate* when the watch couldn't confirm stability.
- **Follow-ups.** File each follow-up the retrospective names through [project-mgmt](../../project-mgmt/SKILL.md), with its owner and its gating or advisory mark: the durable fix among them when the task hasn't run it yet.
