# Close-out record

What an epic built against what it meant to, who watches whether it worked once the work has closed, and where its documentation stands from then on.

## Reader and question

A decider who owns the outcome, and a maintainer later: "What did we end up with, and who keeps checking it worked?" (basis: IPA, benefits monitored after the project closes)

## Page

`own page`.

## Membership

One per task, filed once by the round that closes the task out ([documentation-plan](../../../../craft/writing/documentation-plan.md)), and filed again only to correct it. What happened round by round stays in the task history; the metrics themselves are the [cutover plan](cutover-plan.md)'s.

## Items

**Close-out `CLO`.** The page's own content, one per task.
- Fields:
  - `closed`: date;
  - `outcome owner`: text, the one person who watches the outcome metrics after close, who may differ from the item's owner, the one who answers for this page;
  - `outcome judged`: date, when the outcome is next judged against its targets.
- Granularity: one per task.
- Agreement: `none`.

## Sections

1. **Did we build what we meant to?** — always. The built view, then in prose where what was built departs from what the intent asked.
2. **What changed from the plan along the way?** — present when any requirement was `superseded`, `withdrawn` or `deferred`. The changes view; each item carries why.
3. **How will we know it worked, and who checks?** — always. The outcome owner, when the outcome is next judged, and the metrics view. (basis: IPA; Microsoft ExP, a named owner after the epic closes)
4. **What is still owed?** — always. Follow-ups the work hands on, as prose, each with who takes it; their items live in the [RAID log](raid-log.md) or the [incident record](incident-record.md).
5. **Where does the documentation stand now?** — always. Which living sections froze at close-out, and which operational pages stay under review, each with its owner. (basis: maintainer, 2026-11-11, operational documents switch to a calendar review after close-out)

## Checks

*Computed:*
- The close-out names an outcome owner and a judged date later than its closed date.
- Every requirement not `superseded` or `withdrawn` is `verified-by` a `TEST` ([test-plan](test-plan.md)), directly or through one of its acceptance criteria, whose latest verification holds; or, when no test plan is owed, carries a verification in its own evidence that holds; or is `deferred`. (basis: NASA SWE-052)
- Every item of an operational type carries a next review. (basis: maintainer, 2026-11-11)

*Judgment:*
- An outcome metric that counts activity rather than an outcome. (basis: OKRs, Google re:Work)
- An outcome owner who doesn't run the part of the system the metric watches.
- A goal metric with no guardrail beside it. (basis: Grove; Microsoft ExP)
- A built-against-intended account that passes over what was dropped.
- A follow-up nobody takes.
- A requirement closed on a failed verification.

## Views

- **Built:** `table` of every `REQ` not `superseded` or `withdrawn`: title, state, `verified-by` and `serves`.
- **Changes:** `table` of every `REQ` that is `superseded`, `withdrawn` or `deferred`: title, its state with its reason, and `superseded-by`.
- **Metrics:** `table` of every `goal` and `guardrail` `MET`: definition, baseline, target, direction, cadence and owner after close, and its `value` as observed.

## Minimum form

Filed only at close, so every section has content; one with nothing to report says so in a line, such as "nothing was dropped".
