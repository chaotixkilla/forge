Communication is not the last step of an incident — it runs *alongside* the whole response, from the moment triage confirms an incident to the explicit resolution notice. It is placed fifth in the spine because it is easiest to describe after the response arc is clear, but in a real run it is continuous: acknowledge on declaration, update through stabilization and diagnosis, and declare the terminal outcome when [remediate-and-verify](04-remediate-and-verify.md) reaches one. The failure this phase prevents is the responder who goes heads-down on the fix and leaves stakeholders in a silence that breeds speculation, duplicate tickets, and interruptions that slow the fix itself.

## Post at the right cadence, to the right audience

Pitch frequency, detail, and audience to severity per [right-sized-status-updates](../rules/right-sized-status-updates.md): the SEV1 top rung is frequent (≤30 min, first update within ~10 min, never more than an hour of silence) and broad (responders + stakeholders + customers as warranted); SEV3 is change-based and narrow. Hold the cross-cutting rules at every severity — never go silent, commit a next-update *time* rather than a fix ETA, post immediately when impact changes, keep one canonical source, and separate the comms owner from the fix owner. Where the project's runbook defines its own audiences or escalation path, follow it per [match-the-runbook-conventions](../rules/match-the-runbook-conventions.md).

Pitch the *content* to the audience: customer/public messages are jargon-free and free of premature root-cause claims; stakeholder messages carry impact and business framing; the responder channel carries full technical detail.

## Deliver through the communication capability — and degrade

Posts go out through the [communication](../../communication/SKILL.md) port to the target named by `--notify=<target>` (absent, the configured incident channel). operate decides *what* to say, *to whom*, and *whether* to send; the port carries out the post. Under `--notify` ([notify-stakeholders](../modules/notify-stakeholders.md)), status transitions (acknowledged, mitigated, resolved) are pushed at phase boundaries; without it, this phase still composes each update and returns it.

**Degrade — communication unavailable.** If the communication backend is unconfigured, do not stall the response: compose the update and **return it for the user to send by hand**, noting that automated posting was unavailable. The incident response runs regardless of whether the status channel is wired — communication is degrade, not block.

## Declare resolution explicitly

When [remediate-and-verify](04-remediate-and-verify.md) reaches a terminal outcome, say so plainly and match the claim to the outcome — *resolved* only when the signal held at baseline; *mitigated-but-watching* when impact is contained but the fix or confirmation is still owed; *indeterminate* when the watch could not confirm stability (never dress it up as resolved). A *stood-down* triage result is communicated too, briefly, so watchers know the alert was noise, not an ignored incident. When an update or the incident summary is *published* as a durable document ([publish-incident-record](../modules/publish-incident-record.md)), the clean-export bar applies — the content and the decisions, none of operate's internal phase/critic/loop machinery.

Done-state: the current status has been communicated to the right audience at the right cadence, and — at the end of the run — the terminal outcome has been declared explicitly and truthfully.
