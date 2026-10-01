# Check coverage and hand off

This is the closure gate, and then the exit: nothing is emitted until the units are proven to *cover* the source.

## Prove coverage against the source

Check the unit set against the source in both directions — no orphans (every source element owned by at least one unit) and no overlaps (each owned by at most one) — so the units form an exactly-one-owner partition of the source ([leave-no-orphans](../rules/leave-no-orphans.md)). Walk the source's elements explicitly and mark each with its owning unit; unmarked elements are dropped work and doubly-marked ones are double-ownership, each resolved before handoff (add the missing unit or record the deliberate out-of-scope; merge or re-cut the colliding pair). Confirm every cross-unit dependency surfaced in [size-and-sequence](03-size-and-sequence.md) is recorded as an explicit link ([make-dependencies-explicit](../rules/make-dependencies-explicit.md)), not left implicit in the order.

Recruit the **completeness-auditor** critic to attack the source→units direction — *what did you drop?* — and the **adversary** critic to attack the units→source direction — *where do two units collide, and where is a claimed owner not actually delivering its element?* Fold surviving objections back in. Without fan-out, run both passes yourself: read source-to-units for gaps, then units-to-source for collisions, before declaring coverage.

## Flag residual risk

Coverage can hold on paper and the breakdown can still rest on an unretired unknown. Surface the risks that remain — an approach not yet proven, a fact not yet known — and carve each into a timeboxed spike to run *before* the units that depend on it ([size-the-unknowns-as-spikes](../rules/size-the-unknowns-as-spikes.md)). A spike is sequenced early by the risk pass of [order-by-dependency-then-risk](../rules/order-by-dependency-then-risk.md).

## Return it in the requested form

Return the covered, ordered unit set to the caller:

- **The base:** present the decomposition — the ordered units, each with its done-condition, dependencies, and just-enough context. decompose emits nothing external: filing the units as tracked work-items is the caller's delivery. `(basis: maintainer, 2026-07-10)`
- **`--checklist`:** render the units as one ordered checklist instead — see [emit-checklist](../modules/emit-checklist.md).

## Before it goes out, read it as its reader

Put the finished report through [deliver-at-the-readers-register](../../../craft/writing/deliver-at-the-readers-register.md) before delivering it, applying its honesty floor item by item from the rule, not from memory.

## The terminal outcome

This phase completes the run's terminal-outcome partition opened in [ingest-the-source](01-ingest-the-source.md): a run that reached here resolves to **`decomposed`** — the covered, ordered unit set, emitted to a sink (the requested one, or its fallback if the requested one degraded; the degrade is noted, but the outcome is still `decomposed`). The only other terminal outcome, **`routed-back`**, is reached earlier, at the readiness gate, and never here — by the time a run reaches coverage it has units to deliver. The two outcomes are exhaustive (every run either had a decomposable source and lands `decomposed`, or did not and was `routed-back` at ingest) and mutually exclusive (a run stopped at the readiness gate never reaches this phase).
