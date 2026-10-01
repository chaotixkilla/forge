Starting from the code [phase 01](01-locate-and-baseline.md) located, map everything it touches and grade the change *before* an edit is made. The miss this prevents is underestimated reach: a "local" edit that turns out to be an exported contract, a "dead" branch a downstream job depends on, a refactor that a persisted format outlives.

## Map what depends on the target

Trace outward from the located code (**judgment** — depth follows the reach you keep finding):

- **Callers** — who invokes it, directly and transitively, in this repo and (for an exported symbol) beyond it.
- **Contracts** — public/exported interfaces, serialized or persisted formats, database schemas, wire/API shapes, config keys, and observable behavior consumers rely on. Mark each; a change to one is governed by [preserve-the-contract](../../../craft/engineering/preserve-the-contract.md).
- **Data** — what reads or writes the state the change touches, and whether existing data was written under the old assumption.
- **Downstream consumers** — jobs, services, or clients that would observe the change at a distance.

## Pull prior gotchas — delegate to gather

Has this been changed before, and what bit last time? Recruit the cross-lane evidence step by delegating to the [gather](../../gather/SKILL.md) skill — it runs the explorer fleet (including the repository and knowledge-base lenses) and returns a weighted picture of prior art and known gotchas around this code. **Without fan-out**, apply the lens yourself: read the change history and prior reverts for the target directly (an ambient version-control-history read), and any linked discussion via the [project-mgmt](../../project-mgmt/SKILL.md) skill, before trusting your map. This also feeds the [decode-intent-from-history](../../../craft/engineering/decode-intent-from-history.md) check when the map turns up code whose purpose isn't self-evident. Recruit only as [fan-out-only-when-it-pays](../../gather/rules/fan-out-only-when-it-pays.md) allows.

## Stress the map with future-self

Recruit the [future-self](../../../agents/critics/future-self.md) critic to ask the questions the author skips: *when this change goes wrong six months from now, what breaks, and can it be backed out?* Hand it [change-risk-scale](../../../craft/engineering/change-risk-scale.md) with the recruit, so its answer comes back on the tiers' own reach-and-reversibility axes and anchors rather than in loose prose. Fold its findings into the reach map and the reversibility read. **Without fan-out**, apply the lens yourself — walk the change forward: if it fails in production, what's the blast radius, and is the rollback a clean revert or a data-stranding mess?

## Grade the change

First **fix the intended shape** of the change. Where more than one shape solves the task — keep a facade vs. rewrite callers, add a field vs. repurpose one, guard vs. replace — the shape decides the tier, so choose it *here*, biased to the lowest-reach shape that fully solves the task ([smallest-reversible-change](../../../craft/engineering/smallest-reversible-change.md)), and grade *that* shape rather than an undecided verb. A refactor that can keep its callers' contract intact is planned and graded that way (`contained`), not as a needless caller-rewrite (`bounded`).

Then assign the change its risk tier (**contained / bounded / exposed**) on [change-risk-scale](../../../craft/engineering/change-risk-scale.md): the *worse* of its reach and reversibility, graded against the rule's assignment tests, anchors, and uncertainty rule. The tier is the phase's load-bearing output, and it carries a mandatory action into [phase 03](03-make-the-change.md).

## Output

The phase produces: the reach map (callers, contracts, data, consumers), the contract surfaces flagged, and the **risk tier with the action it forces**. That triple is the input [phase 03](03-make-the-change.md) acts on.

## Degraded and edge cases

- **Nothing outside the diff observes a difference** (a private, behavior-preserving change — even one with in-repo callers you rewrite mechanically, and even with no tests: coverage isn't a tier axis) → `contained`; proceed to direct change. Confirm it via the touched-contract test, don't assume it.
- **The consumer set can't be fully enumerated** (an exported symbol with unknown external importers, a format with data already written), **or a consumer this change actually moves deploys on its own schedule** (a separate service or a published library, *even in this repo*, that ships independently) → these are the marks of an `exposed`-tier change: you can't move all consumers under your control. Grade up, don't grade on the optimistic assumption — uncertainty about reach resolves *toward* higher risk..)
- **gather unavailable** → build the map from the local code and history via the fallback above, and note that the prior-art picture is reduced — a lower-confidence map argues for grading conservatively.
