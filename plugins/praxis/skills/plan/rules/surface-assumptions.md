# Surface every load-bearing assumption

Every design rests on things the author believes to be true — "this is never null here", "the upstream call is idempotent", "this fits in memory", "volume stays under N". While they stay in the author's head, a reviewer cannot challenge them and a builder cannot check them; the design looks sound right up until an assumption is falsified in production, where it is most expensive to discover. This rule drags the load-bearing assumptions into the open where they can be argued with.

## State it, and state how it could be false

For each claim the design leans on, write it down as an explicit, **falsifiable** statement — one a reviewer could disagree with and a builder could test — paired with what would break if it were false. "We assume each order has exactly one payment" is surfaced; a design that silently relies on it is not. An assumption you cannot phrase as something that *could be* false is not yet stated precisely enough.

## Only the load-bearing ones — churn is the inverse defect

The discriminator: **would the design break if this assumption were false?** If yes, it is load-bearing — surface it. If the design survives either way, it is incidental — leave it out. Documenting the self-evident or the harmless is the over-correction, as much noise as the silent trap is a risk; the goal is that a reviewer sees exactly the premises the design is betting on, not a catalogue of everything true about the world.

The **single riskiest** load-bearing assumption — the one most likely to be wrong and most damaging if it is — gets a named validation step: a spike, a probe, a query against real data, before the design is committed. That named step is what [slice-and-validate](../phases/06-slice-and-validate.md)'s buildable bar checks for.

*Anchor (top):* a stated, falsifiable assumption with a named way to confirm it. *Anchor (bottom):* a silent dependency — an implicit ordering, a shared constant two places must agree on, an "always non-null" that a reachable path violates — that a maintainer breaks precisely because nothing named it (the trap the future-self critic hunts).

Cited by [mapping-to-system](../phases/01-mapping-to-system.md), [working-the-hard-parts](../phases/04-working-the-hard-parts.md), and [slice-and-validate](../phases/06-slice-and-validate.md). Related: [record-rejected-alternatives](record-rejected-alternatives.md) (an assumption is a decision's hidden premise), [follow-the-data](follow-the-data.md).
