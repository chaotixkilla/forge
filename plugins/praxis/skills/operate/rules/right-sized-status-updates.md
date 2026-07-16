# Right-sized status updates

During an incident, silence is the enemy: a gap with no update pulls stakeholders into speculation, duplicate tickets, and DMs to responders asking "is it fixed yet?" — which pulls responders off the fix. But a rigid 15-minute heartbeat on a low-severity, slow-burning incident is just noise that trains readers to ignore the channel. The right cadence and depth are *keyed to severity and audience*, not fixed. "Communicate regularly" is not a codified bar — two responders reading it will post on wildly different clocks. This rule pins the matrix [communicate-status](../phases/05-communicate-status.md) posts against, keyed to the severity set by [severity-scale](severity-scale.md).

## The cadence matrix

Frequency, detail, and audience by severity. The rungs are anchored top (SEV1) and bottom (SEV3); SEV2 interpolates.

| Severity | Frequency | Audience | Detail |
|---|---|---|---|
| **SEV1** (top) | first update within ~10 min of declaring; then **every ≤30 min** while impact persists — **never more than 1 hour** between updates | responders + stakeholders/execs + customers/public status page as the incident warrants | short impact summary in plain language + what is being done + the *time* of the next update. **No premature root-cause claims.** |
| **SEV2** | roughly **every 2–4 hours** while active | responders + affected stakeholders | impact + progress + next-update time; business framing for stakeholders |
| **SEV3** (bottom) | **change-based** / business-hours — post on a state change, not a fixed clock | the owning team channel | acknowledgement + updates when status changes |

`(basis: Atlassian Incident Management Handbook — the hard ceiling "never go more than one hour without an update" while customers are affected; incident.io — the per-severity matrix shape (SEV1 20-30 min → SEV2 ~4h → SEV3 business-hours); PagerDuty — a ~20-minute floor and first-comms within minutes. Google SRE deliberately sets no interval, so the numbers are vendor convention, not an SRE-universal — the *shape* and the 1-hour ceiling are the well-corroborated parts.)`

`(basis: ratified by the maintainer, 2026-07-11 — the SEV1 top-rung interval is ≤30 min, with the 1h hard ceiling and a first update within ~10 min. The sourced cluster was 15-30 min (Atlassian's 1h ceiling + incident.io/PagerDuty); 15 min was offered for a top-tier public outage and not adopted. Google SRE sets no number, so this is a house standard.)`

## The cross-cutting rules — these hold at every severity

These are the parts the authorities agree on most tightly; they are not severity-keyed.

- **Never go silent.** Post on the cadence even when there is no news — but say so explicitly ("still investigating, no new information, next update by HH:MM") rather than copy-pasting an identical placeholder. When genuinely in a long mitigation with nothing to report, **lengthen the interval and announce the new cadence**, don't hold a tight clock producing noise. `(basis: incident.io / Atlassian heartbeat guidance + the practitioner refinement — Hosted Graphite, iamevan.me — that repetitive placeholders train readers to ignore the channel.)`
- **Commit to a next-update *time*, not a fix ETA.** Promise when the next *update* lands, never when the fix ships — it lets stakeholders point people at a known time without exposing a repair deadline you may miss. `(basis: Atlassian Statuspage tips, Rootly, Hosted Graphite — corroborated across independent sources.)`
- **An impact change overrides the clock.** Post immediately when the blast radius or severity changes materially; the interval is a floor for silence, not a cap on updates.
- **Separate the comms owner from the fix owner.** Above SEV3, one person owns communication and a different person owns the fix — "the moment the conductor picks up a violin, nobody's conducting." `(basis: Google SRE (Communications Lead distinct from Incident Commander); PagerDuty Internal/Customer Liaison roles.)` When operate runs as the **sole responder** (a single agent, no human team to split the roles), it cannot hand comms to a second role — instead it surfaces the recommended split to the user and keeps posting updates on cadence itself rather than dropping them to focus on the fix.
- **One canonical source.** Route all updates through a single agreed channel/source so customers, support, and execs never get three conflicting stories.
- **Pitch detail to the audience.** Public/customer messages are jargon-free and free of root-cause speculation; stakeholder messages carry impact and business framing; the responder channel carries full technical detail. When an update is *published* as a durable document ([publish-incident-record](../modules/publish-incident-record.md)), the clean-export bar applies — content, not machinery.
- **Defer to the runbook's own cadence and audience.** Where the project's runbook or status-page policy already sets an update cadence or audience routing, follow it per [match-the-runbook-conventions](match-the-runbook-conventions.md); this matrix is the house default for when none exists.

## Anchors

- *Top (SEV1):* a public status-page post within 10 minutes of declaring — "We're aware of errors affecting logins for all users; we're investigating; next update by 14:20" — then a fresh post every 20–30 minutes until impact ends, and a distinct resolution post.
- *Bottom (SEV3):* an acknowledgement in the team channel, then a note when the state changes (mitigated, resolved) — no fixed clock.
