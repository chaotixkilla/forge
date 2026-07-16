# Check coverage and hand off

This is the closure gate, and then the exit. A decomposition can look complete — every unit sized, ordered, actionable — and still have silently dropped a requirement or double-owned an outcome, faults that surface mid-build as "who was doing this?" or a merge conflict between two units building the same thing. This phase proves the units actually *cover* the source before anything is emitted, flags the risks that a small investigation should retire first, and then delivers the breakdown in the form the caller asked for. A decomposition that skips the coverage proof is a list of plausible units; one that does it is a plan of record.

## Prove coverage against the source

Check the unit set against the source in both directions — no orphans (every source element owned by at least one unit) and no overlaps (each owned by at most one) — so the units form an exactly-one-owner partition of the source ([leave-no-orphans](../rules/leave-no-orphans.md)). Walk the source's elements explicitly and mark each with its owning unit; unmarked elements are dropped work and doubly-marked ones are double-ownership, each resolved before handoff (add the missing unit or record the deliberate out-of-scope; merge or re-cut the colliding pair). Confirm every cross-unit dependency surfaced in [size-and-sequence](03-size-and-sequence.md) is recorded as an explicit link ([make-dependencies-explicit](../rules/make-dependencies-explicit.md)), not left implicit in the order.

Recruit the **completeness-auditor** critic to attack the source→units direction — *what did you drop?* — and the **adversary** critic to attack the units→source direction — *where do two units collide, and where is a claimed owner not actually delivering its element?* Fold surviving objections back in. Without fan-out, run both passes yourself: read source-to-units for gaps, then units-to-source for collisions, before declaring coverage.

## Flag residual risk

Coverage can hold on paper and the breakdown can still rest on an unretired unknown. Surface the risks that remain — an approach not yet proven, a fact not yet known — and carve each into a timeboxed spike to run *before* the units that depend on it, rather than discovering the unknown mid-build ([size-the-unknowns-as-spikes](../rules/size-the-unknowns-as-spikes.md)). A spike is sequenced early by the risk pass of [order-by-dependency-then-risk](../rules/order-by-dependency-then-risk.md).

## Emit in the requested form

Deliver the covered, ordered unit set to the sink the caller chose — the three are mutually exclusive:

- **`--plan-only` (the base behavior, and the default when no output flag is given):** present the decomposition for review — the ordered units, each with its done-condition, dependencies, and just-enough context — and emit nothing external. This is the safe default: it produces the breakdown without mutating any tracker, and the caller opts into a side-effecting sink explicitly. `(basis: --plan-only as the default is ratified by the maintainer, 2026-07-10 — a side-effect-free presentation is the least-surprising default, mirroring how review returns findings locally unless a sink flag is given.)`
- **`--ticket`:** create one tracked work-item per unit via the project_mgmt capability — see [emit-tickets](../modules/emit-tickets.md).
- **`--checklist`:** render the units as one ordered checklist — see [emit-checklist](../modules/emit-checklist.md).

**Degraded case:** when `--ticket` is asked for but the project_mgmt backend is unavailable, do not block — fall back to `--checklist` (or, failing that, `--plan-only`) and tell the caller the requested tracker could not be reached and what was emitted instead ([emit-tickets](../modules/emit-tickets.md) owns this degrade). The decomposition still lands; only the sink narrows.

## The terminal outcome

This phase completes the run's terminal-outcome partition opened in [ingest-the-source](01-ingest-the-source.md): a run that reached here resolves to **`decomposed`** — the covered, ordered unit set, emitted to a sink (the requested one, or its fallback if the requested one degraded; the degrade is noted, but the outcome is still `decomposed`). The only other terminal outcome, **`routed-back`**, is reached earlier, at the readiness gate, and never here — by the time a run reaches coverage it has units to deliver. The two outcomes are exhaustive (every run either had a decomposable source and lands `decomposed`, or did not and was `routed-back` at ingest) and mutually exclusive (a run stopped at the readiness gate never reaches this phase).
