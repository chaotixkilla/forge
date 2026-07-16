# Know when to stop

Fan-out can always run one more query; the discipline is stopping when the *answer* stops changing, not when the queries run out. Over-gathering burns budget and buries the signal under restatement; under-gathering ships a thin picture as if it were complete. The judgment is telling the two stops apart — real saturation versus a thin-evidence dead end — and naming which you hit. Cited from [gather-evidence](../phases/03-gather-evidence.md).

## The saturation test

Stop chasing a sub-question when a further round of new sources adds no new load-bearing claim and shifts no claim's confidence grade ([claim-confidence-scale](claim-confidence-scale.md)) — the answer has stopped moving, measured against the *answer*, not a query count. New sources that only restate claims already captured are the signal to stop, not to keep going.

## Saturation vs. a thin-evidence dead end — the discriminator

The two stops look identical (new sources stop changing the answer) but mean opposite things, so name which:

- **Saturated** — the answer stopped moving because *independent origins converge* on it ([triangulate-before-trusting](triangulate-before-trusting.md)). A strong stop; the claim is as established as the evidence allows.
- **Thin dead end** — the answer stopped moving because you keep finding the *same one or few origins* echoed, or nothing at all. A weak stop the caller must see: the answer rests on thin or circular evidence, delivered at low confidence, never as if it were saturated. Say where you searched, so the thinness is auditable.

Collapsing these two into one "I stopped finding new things" is the defect — it lets a dead end ship with the confidence of a saturated answer.

`(basis: ratified by the maintainer, 2026-07-13. The stop bar: one full round of new sources across the sub-question's lanes adds no new load-bearing claim and shifts no confidence grade; the saturated/dead-end split turns on independent-origin count (≥2 independent origins = saturated, ≤1 = thin). Ratified as the house standard — "the answer stopped moving" needs a concrete round-and-origin threshold or two cold runs stop at different points. A --budget/--timebox cap can force a stop before this bar — when it does, the stop is reported as budget-bound, not saturation.)`
