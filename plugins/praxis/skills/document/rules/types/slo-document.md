# SLO document

The reliability a service is held to: each objective, the indicator it rests on, why its number is what it is, and what happens when its error budget runs out.

## Reader and question

On-call, and the decider who owns the service: "What reliability do we hold this service to, and what do we do when we miss it?"

## Page

`own page`

## Membership

The objectives of each service the work runs under or creates a target for, with their error budget policy. How alerts on them are answered is the [runbook](runbook.md)'s. Its subject is the service, so a task has one per service. It is filed again when an objective or its policy changes, and at each review.

**Operational.**

## Items

**Objective `SLO`.** One indicator held to one target over one window. Its body is the rationale for the number. An objective set from observation cites in its body the reason users would feel that number, not only the baseline.

- `service`: text.
- `indicator`: id. The `MET` it rests on, a ratio of good events to valid events, whose role is `indicator`. The objective `rests-on` that metric. (basis: SRE Workbook, implementing SLOs)
- `target`: number.
- `window type`: enum `rolling`, `calendar`, and `window length`: period.
- `published target`: number. The target promised outside the team, when one is. (basis: Google SRE ch. 4)
- `set from`: enum `experiment`, `observation`. (basis: SRE Workbook, the rationale labels where its numbers came from)
- `when exhausted`: text. What stops, what takes priority, and what lets it resume. It has one trigger: the budget running out. (basis: SRE Workbook, error budget policy; one trigger rather than staged thresholds, chosen for simplicity)
- `escalate to`: text. The one person who settles a disagreement over the policy.

Live field: `budget left`, number, `telemetry: the share of the error budget left in the current window`.

Agreement `needed`, change regime `baseline`. Its decide-by is the plan's due point.

Shows `MET` (home: [cutover-plan](cutover-plan.md)).

## Sections

1. **What do we hold the service to?** Always. The objective table.
2. **How is each measured?** Always. The indicator table.
3. **What happens when the budget runs out?** Always. The policy list.

## Checks

*Computed:*
- Every objective has its indicator, target, window type, window length, set from, when exhausted and escalate to.
- Every objective `rests-on` the metric its indicator names, and that metric's role is `indicator`.
- A published target is no tighter than the target, read in the indicator's `direction`: no higher for `up`, no lower for `down`. (basis: Google SRE ch. 4)
- An objective set from observation rests on a metric with a baseline and its window. (basis: prototype sweep, 2026-11-11, a budget set before any baseline)

*Judgment:*
- An objective set from observation whose body cites only the baseline, with no reason in what users would feel.
- A target tighter than users would notice. (basis: Google SRE ch. 4)
- More objectives than the service's users would feel.
- A latency indicator taken as a mean, or mixing successes with failures. (basis: Google SRE ch. 4 and 6)
- A policy whose actions nobody would follow.
- An agreement on an objective whose decider and consulted don't include product, development and operations. (basis: SRE Workbook, approved jointly; the agreement's single decider stays, the others consulted)

## Views

- **Objective table:** `table` of `SLO` whose service is `page subject`: indicator, target, published target, window type, window length, set from, budget left, next review.
- **Indicator table:** `table` of `SLO` whose service is `page subject`: the indicator it `rests-on` (only `MET`), and that metric's definition, source, baseline and baseline window (`rests-on`, only `MET`, one named field each).
- **Policy list:** `list` of `SLO` whose service is `page subject`: when exhausted, escalate to.

## Minimum form

Each section keeps its heading with one line: no objective is set yet, and who sets it.
