# Research report

The answer a researching task reached.

**Reader and question.** Decider: "what's the answer, how sure are we, and what does it mean for us?"

**Page.** `own page`

## Membership

The research step's final result. (basis: derived from the deliverable of the act that files it)

## Items

**Answer `ANS`.** One per page: the answer to the question as asked.
- Fields: `result` enum `holds`, `fails`, `unsettled`, `not checked`; `reason` text, why it is `not checked`, when it is; `support` enum `established`, `corroborated`, `contested`, `single-source` ([results-and-certainty](../../../../craft/evidence/results-and-certainty.md)); `means for us` text.
- Change regime: `baseline`.
- Agreement: `none`.

**Sub-question `SQ`.**
- Fields: `support` enum, as the answer's; `result` enum, as the answer's, only when a check was run on it; `reason` text, as the answer's; `dissent` text, the evidence against and how it was weighed; `tested` text, how hard its claims were tested.
- Granularity: one sub-question the research split the question into. The answer `rests-on` each.
- Change regime: `baseline`.
- Agreement: `none`.

## Sections

(basis: maintainer, 2026-10-02, for the order)

1. **What's the answer?** Always. `ANS`: the answer, its support and result, and what it means for the purpose.
2. **How do we know?** Always. The sub-question cards.
3. **What's still open?** Always. The weak-support table, then the unsettled table, each sub-question with what would settle it in its body, then open questions outside the split, in prose.

## Checks

- *Computed:*
  - exactly one `ANS`;
  - every `SQ` has at least one evidence link;
  - an `ANS` or `SQ` at `not checked` has `reason` filled.
- *Judgment:*
  - an answer whose support is stronger than the weakest support among the sub-questions it rests on;
  - dissent named but not weighed;
  - every source from one tier, with authority or corroboration never weighed;
  - "means for us" that restates the answer instead of applying it.

## Views

- **Sub-question cards** (section 2): `cards` of every `SQ`, in store order: support, result, dissent, tested.
- **Weak-support table** (section 3): `table` of every `SQ` whose `support` is in `contested`, `single-source`: support, result (empty marker `no check run`), dissent.
- **Unsettled table** (section 3): `table` of every `SQ` whose `result` is in `unsettled`, `not checked`: result, reason, support.

## Minimum form

The answer `not checked` with why, "no sub-questions answered yet", and the question itself as still open.
