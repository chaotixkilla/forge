# Decision register

The task's one list of questions still to settle and of the decisions that settled them, each tiered, with one decider and a date it is needed by.

## Reader and question

A decider, and a maintainer whose work waits on a decision: "What is still undecided, who decides it, by when, and what is it holding up?"

## Page

`own page`

## Membership

Every question the work has to settle and every decision it has taken, whatever their tier. The full reasoning behind a decision that earns a [decision-record](decision-record.md) is that record's; the case put to a decider on a tier-1 question is its [decision-brief](decision-brief.md)'s. A question is asked in this register only, never in a second list on another page. (basis: prototype sweep, 2026-11-11, one register of questions, never two) Its subject is the task's questions and decisions, so a task has one. It is filed again whenever a question or decision is added, changes, or changes state.

## Items

Both kinds are tiered on two axes, and both are required. (basis: maintainer, 2026-11-11, reversibility × reach, a house rule)

- `reversibility`: enum `one-way`, `two-way`, by the test in [design-for-reversibility](../../../../craft/engineering/design-for-reversibility.md).
- `reach`: enum `beyond the change`, `within the change`. Beyond when what it settles is read or called by code or people outside the task's own change: a schema others read, a contract others call.

- `tier`: enum `1`, `2`. Set from the two axes whenever they are filed, never chosen on its own: `1` when one-way and beyond the change, as the [documentation-plan](../../../../craft/writing/documentation-plan.md) defines a tier-1 question, `2` otherwise. Only the binary is anchored, so no third tier is drawn. (basis: Bezos 2015, Type 1 and Type 2 decisions)

Both also carry:

- `decider`: text. Exactly one person, the one who will settle it. When the result names several, it is missing, and one is never picked. (basis: DACI's one approver; PMI, accountability is not shared)
- `lean`: text. The answer favoured, while the item is `lean`.

**Question `Q`.** One thing the work can't settle without an answer.
- Fields, beyond the tier's, `decider` and `lean`:
  - `consulted`: list of text. Whose view is sought before it is settled.
  - `informed`: list of text. Who is told once it is.
- An escalated risk in the [raid-log](raid-log.md) opens a question: the question is `opened-by` the risk, and its decider is who the risk was escalated to.
- Change regime: `baseline`.

**Decision `DEC`.** One choice the work makes, stated actively. Its body holds the context: the problem and the forces in tension, stated neutrally.
- Fields, beyond the tier's, `decider` and `lean`:
  - `options`: list of text. Each option weighed, with its pros and cons.
  - `chosen`: text. "We will …", naming one of the options.
  - `gains` and `costs`: list of text. What the decision buys and what it costs. (basis: Nygard 2011, all consequences, not just the positive)
  - `confirmation`: text. How anyone can check that the work follows it: a test, a fitness function or a review, naming the `TEST` id when it is one. (basis: MADR 4.0, Confirmation)
  - `revisit when`: text. What would reopen it.
  - `architectural`: enum `yes`, `no`. `yes` when the choice adds, removes or replaces a part, a contract between parts, which part holds a kind of data, or an outside service the system depends on, a part being what is deployed or owned on its own: a service, a job, a data store, an outside service, a module with its own owner. `no` for a choice inside one part. A new claim two services read from a token is `yes`; which library one service parses it with is `no`. Whoever files a decision, any step or act, sets it by this test.
  - `confidence`: enum `high`, `medium`, `low`. `low` when the forces or the options are unclear, even when the choice has been verified; otherwise `high` when a spike, a test or prior use in this project has verified the choice; `medium` otherwise. (basis: Zimmermann, disclose your confidence)
- Links: it `answers` the question it settles, `serves` the requirements or needs it was taken for, and `supersedes` the decision it replaces.
- Change regime: `freeze`.

The fields an agreement records, the decider who actually settled it, consulted, informed, the date and the link to where it was settled, are the agreement's, shown beside the item, never copied into it. These kinds' checks hold wherever a question or decision is shown, so a task that owes no register still meets them on its spec page.

## Sections

1. **What needs deciding, and by when?** Always. The open-items table, then the waiting-on view. The table's key says what the tiers mean.
2. **What has been decided?** Always. The decisions table.
3. **What is paused?** When an item is `deferred`. A list of each, with why and what brings it back.
4. **What was replaced or dropped?** When an item is `superseded` or `withdrawn`. A list of each, with what replaced it or why it was dropped.

## Checks

*Computed:* each skips `superseded` and `withdrawn` items.
- Every question and decision has both `reversibility` and `reach`, and the tier they set; every decision has `architectural`. (basis: maintainer, 2026-11-11; the prototype filled them on a third of its items)
- An item that is `lean` has its lean.
- Every tier-1 question is served by a brief, at either scale. (basis: maintainer, 2026-11-11, every tier-1 question has a decision brief; [documentation-plan](../../../../craft/writing/documentation-plan.md))
- A decision's `answers` link names a question.

*Judgment:*
- A tier that misstates how hard the choice is to undo, or how far it reaches. (basis: Bezos 2015)
- A tier-2 question held up for tier-1 deliberation, the failure Bezos names.
- A question or decision not yet `agreed` with no decider: the result named several people, or none, so who decides is itself unsettled.
- A question past its decide-by with no new date and no `deferred` reason. A decide-by that names a gate falls due on that gate's `opens on`.
- A tier-1 decision whose choice the sources the work starts from show already running in production while it isn't `agreed`: the work went through a one-way door ahead of its agreement. A tier-2 decision may run first, as Bezos's rule wants. (basis: benchmark, 2026-11-12, production ran under proposed decisions with no approval trail)
- One question asked twice under two ids.
- An agreed decision whose agreement names a decider other than its own.
- A decision taken while the question it settles stayed open, with no `answers` link.
- A decision agreed with no record of where it was settled. (basis: PEP 1, Resolution)

## Views

- **Open items:** `table` of every `Q` and `DEC` that is `open`, `lean` or `proposed`, sorted by tier, descending (highest first), then by decide-by, ascending, in `when` order ([item-store-and-views](../../../artifacts/rules/item-store-and-views.md)): tier, reversibility, reach, decider, consulted, decide-by, state, lean, what it `blocks`, and its brief (`served-by`).
- **Waiting on:** `list` of the same items grouped by decider: id, title, decide-by, state.
- **Decisions:** `table` of every `agreed` `DEC`, sorted by id, descending: chosen, tier, the question it `answers`, and the covering agreement's decider, date and link.

## Minimum form

Each always-present section keeps its heading with one line: no question is open yet, or nothing has been decided yet.
