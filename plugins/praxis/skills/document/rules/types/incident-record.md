# Incident record

The record of a real incident, written once the service is stable.

**Reader and question.** On-call and decider: "what did this cost, why could it happen, and what stops it happening again?"

**Page.** `own page`

## Membership

The incident act's retrospective, written blamelessly ([blameless-framing](../../../../craft/writing/blameless-framing.md)). The timeline notes kept while the incident was live are [scratchpad](scratchpad.md) sections the record links. A stood-down signal files no incident record. (basis: derived from the deliverable of the act that files it)

## Items

**Outcome `OUT`.** One per page: the impact, in its body, and where the incident rests.
- Fields: `outcome` enum `resolved`, `mitigated-but-watching`, `ongoing`, `indeterminate`, one of the [five outcomes](../../../work/acts/responding-to-an-incident.md) other than stood-down; `why` text, why the record has no `resolution` event, when it has none.
- Change regime: `baseline`.
- Agreement: `none`.

**Timeline event `TL`.**
- Fields: `at` date, to the minute; `until` date, when the event spans time, empty for a point event; `phase` enum `onset`, `detection`, `mitigation`, `diagnosis`, `resolution`, `other`.
- Granularity: one thing that happened or was done, at one time.
- Change regime: `baseline`.
- Agreement: `none`.

**Contributing factor `CF`.**
- Fields: `factor` enum `trigger`, `gap`, `detection`, `recovery` — the trigger, a gap that let it reach production, or why detection or recovery was slow.
- Granularity: one factor. Incidents rarely have one cause, so a record usually has several.
- Change regime: `baseline`.
- Agreement: `none`.

**Action `ACT`.** A follow-up ([incident-retrospective](../../../communicate/rules/incident-retrospective.md)).
- Fields: `class` enum `prevent`, `detect`, `mitigate`, `repair`; `mark` enum `gating`, `advisory`; `due` when, its decide-by; `work item` text, its link once filed.
- Granularity: one concrete change, about the system. It `serves` the factors it answers.
- Change regime: `baseline`.
- Agreement: `needed`.
- Live fields: `work item state` — project-mgmt: the filed work item's status.

**Sensitivity.** Every `TL` is `restricted` by default, and so is any `CF` or `ACT` whose body shows an exploit path or personal data. Other `CF` and `ACT`, and the `OUT`, are `team`. (basis: derived from [items-and-agreements](../items-and-agreements.md)' sensitivity)

## Sections

(basis: maintainer, 2026-10-02, for the order)

1. **What happened, and where does it rest?** Always. The `OUT`: who and what was affected, since when, in numbers, without the restricted specifics, and the outcome the incident rests at.
2. **What stops it happening again?** Always. The follow-up table.
3. **Why could it happen?** Always. The factor list, then the cause chain drawn where the kit owes it.
4. **Where did we get lucky?** Always. What, had it gone otherwise, would have made it worse, in prose.
5. **What happened when?** Always. The timeline, with metric charts around it where the telemetry gave them.

## Checks

- *Computed:*
  - exactly one `OUT`;
  - every `TL` has at least one evidence link (basis: PagerDuty, every timeline entry backed by a metric or link);
  - every `ACT` has `class` and `mark`, and `serves` at least one `CF` (basis: Google SRE, owner, priority and tracking per action);
  - once the record holds any `ACT`, the actions include at least one `detect`, and at least one `prevent` or `mitigate` (basis: derived from Google SRE's action mix);
  - there is a `TL` in `detection`, and one in `resolution` or the `OUT` has `why` filled;
  - "Where did we get lucky?" says something, or says none was found.
- *Judgment:*
  - impact given without numbers;
  - a factor that names a person rather than the guard the system lacked;
  - an action such as "be more careful", or "improve monitoring" with nothing concrete to build;
  - no `gating` action for an outage users felt (basis: Google SRE);
  - a root cause that stops at the trigger;
  - end-user identifiers anywhere on the page.

## Views

- **Follow-up table** (section 2): `table` of every `ACT`, sorted by `mark` descending, then `due` ascending: class, mark, due, owner, `work item state`.
- **Factor list** (section 3): `list` of every `CF`, grouped by `factor`: what it is `served-by` (only `ACT` targets, empty marker `no action`).
- **Timeline** (section 5): `timeline` of every `TL` from `at` to `until`, a point event's empty end drawing it as a milestone.

## Minimum form

The `OUT` with the impact "not yet measured" and the outcome, "no actions yet", "no factors found yet", "not yet reviewed for luck", and the timeline's onset and detection events, with a `resolution` event unless the `OUT`'s `why` excuses it.
