The single most expensive mistake in maintenance is changing something whose reach you underestimated — a "local" edit that turns out to be an exported contract, a "dead" branch a downstream job depends on, a refactor that a persisted format outlives. This phase maps the reach *before* an edit is made and converts that map into a **risk grade** that decides how the change is allowed to land in [phase 03](03-make-the-change.md). It is the counterpart to [phase 01](01-locate-and-reproduce.md): phase 01 found the code; this phase finds everything the code touches.

## Map what depends on the target

Trace outward from the located code (**judgment** — depth follows the reach you keep finding):

- **Callers** — who invokes it, directly and transitively, in this repo and (for an exported symbol) beyond it.
- **Contracts** — public/exported interfaces, serialized or persisted formats, database schemas, wire/API shapes, config keys, and observable behavior consumers rely on. Mark each; a change to one is governed by [preserve-the-contract](../rules/preserve-the-contract.md).
- **Data** — what reads or writes the state the change touches, and whether existing data was written under the old assumption.
- **Downstream consumers** — jobs, services, or clients that would observe the change at a distance.

## Pull prior gotchas — delegate to gather

Has this been changed before, and what bit last time? Recruit the cross-lane evidence step by delegating to the [gather](../../gather/SKILL.md) skill — it runs the explorer fleet (including the repository and knowledge-base lenses) and returns a weighted picture of prior art and known gotchas around this code. **Without fan-out**, apply the lens yourself: read the change history and prior reverts for the target directly (an ambient version-control-history read), and any linked discussion via the [project-mgmt](../../project-mgmt/SKILL.md) skill, before trusting your map. This also feeds the [decode-intent-from-history](../rules/decode-intent-from-history.md) check when the map turns up code whose purpose isn't self-evident.

## Stress the map with future-self

Recruit the [future-self](../../../agents/critics/future-self.md) critic to ask the questions the author skips: *when this change goes wrong six months from now, what breaks, and can it be backed out?* Hand it [change-risk-scale](../rules/change-risk-scale.md) with the recruit, so its answer comes back on the tiers' own reach-and-reversibility axes and anchors rather than in loose prose. Fold its findings into the reach map and the reversibility read. **Without fan-out**, apply the lens yourself — walk the change forward: if it fails in production, what's the blast radius, and is the rollback a clean revert or a data-stranding mess?

## Grade the change

First **fix the intended shape** of the change. Where more than one shape solves the task — keep a facade vs. rewrite callers, add a field vs. repurpose one, guard vs. replace — the shape decides the tier, so choose it *here*, biased to the lowest-reach shape that fully solves the task ([smallest-reversible-change](../rules/smallest-reversible-change.md)), and grade *that* shape rather than an undecided verb. A refactor that can keep its callers' contract intact is planned and graded that way (`contained`), not as a needless caller-rewrite (`bounded`).

Then assign the change its risk tier on the defined scale — this is the phase's load-bearing output ([change-risk-scale](../rules/change-risk-scale.md)). The tier (**contained / bounded / exposed**) is the *worse* of the change's reach and reversibility, and it carries a mandatory action into [phase 03](03-make-the-change.md): a `contained` change may be made directly; a `bounded` one is staged behind a guard, or — when its full consumer set is enumerable, movable under your control, and fits one atomic diff — updated in that same diff; an `exposed` one requires a migration path rather than a flag-day switch. Grade honestly against the assignment tests and anchors in the rule; when two tiers seem to fit and the reach is *known*, the higher wins unless you can name concretely why the reach is bounded — and when the reach is *uncertain*, it resolves to the higher tier regardless (the rule's uncertainty rule; don't let "probably fine" pull a change back down).

## Output

The phase produces: the reach map (callers, contracts, data, consumers), the contract surfaces flagged, and the **risk tier with the action it forces**. That triple is the input [phase 03](03-make-the-change.md) acts on.

## Degraded and edge cases

- **Nothing outside the diff observes a difference** (a private, behavior-preserving change — even one with in-repo callers you rewrite mechanically, and even with no tests: coverage isn't a tier axis) → `contained`; proceed to direct change. Confirm it via the touched-contract test, don't assume it.
- **The consumer set can't be fully enumerated** (an exported symbol with unknown external importers, a format with data already written), **or a consumer this change actually moves deploys on its own schedule** (a separate service or a published library, *even in this repo*, that ships independently) → these are the marks of an `exposed`-tier change: you can't move all consumers under your control. Grade up, don't grade on the optimistic assumption — uncertainty about reach resolves *toward* higher risk. (For a *dependency upgrade*, whether a co-importer even counts as a consumer this change moves turns on the resolution topology — see *Grading a dependency upgrade* in [change-risk-scale](../rules/change-risk-scale.md).)
- **gather unavailable** → build the map from the local code and history via the fallback above, and note that the prior-art picture is reduced — a lower-confidence map argues for grading conservatively.
