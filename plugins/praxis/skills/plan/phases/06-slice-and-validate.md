This is the closure gate: prove the design buildable, sliceable into units each verifiable on its own, with nothing load-bearing left open. What it catches is the "figure it out later" that detonates mid-build: an open decision from mapping never closed, a seam too loose for two developers to converge, an untested assumption the whole thing rests on.

## Slice into independently buildable units

Break the design into units that can each be built and verified on their own, in an order where each rests only on what came before. The test that the slicing is real: at least one **end-to-end function** can be traced through the units with no gap — a thin path from entry to storage and back that exercises every main component the design introduces. That walking-skeleton trace is what proves the pieces actually connect, not just that they were each named.

## The buildable / closed bar

`(basis: maintainer, 2026-07-05; after Cockburn 2004, Hunt and Thomas's tracer bullets, and Fairbanks 2010)`

A design is **closed / buildable** when all of these hold — check them explicitly, and a failure is an open, not a nit:

- **Every main component is named**, and one real end-to-end function traces through them with no gap (the walking-skeleton test above).
- **Each seam/contract is specified precisely enough that two independent developers would build the same interface** — the convergence bar from [specify-interfaces](03-specify-interfaces.md).
- **Every open decision surfaced in [mapping-to-system](01-mapping-to-system.md) is now closed** — nothing deferred to "later". (With `--from-spec`, additionally: every spec requirement is addressed by some part of the design — [from-spec](../modules/from-spec.md).)
- **Every moving part earns its place** against a constraint ([justify-every-moving-part](../../../craft/engineering/justify-every-moving-part.md)) — the closure pass is also the last chance to cut what doesn't.
- **The single riskiest assumption — chosen by the ranking in [surface-assumptions](../rules/surface-assumptions.md) — has a named validation step** — the design does not bet the build on an unchecked premise.

Do **not** substitute Scrum's Definition of Done (that is "increment shipped", downstream of this handoff) or a full IEEE-1016 design document (documentation completeness, not buildability) for this bar unless the domain contractually requires the formal artifact.

## Before it goes out, read it as its reader

Put the finished report through [deliver-at-the-readers-register](../../../craft/writing/deliver-at-the-readers-register.md) before delivering it, applying its honesty floor item by item from the rule, not from memory.

**And a visual where prose would carry it worse:** where the report describes a *structure* — a shape, a flow, a set of relationships — show it rather than describe it, per `output.diagrams` ([report-style-settings](../../../craft/writing/report-style-settings.md)) and [when-a-visual-is-owed](../../../craft/writing/when-a-visual-is-owed.md), which decides whether one is owed.

## Flag residual risk, stress-test, and hand off

Flag the known unknowns that remain and what needs a spike or throwaway prototype *before* committing to build — the design can be closed on paper and still name a risk that a small experiment should retire first. Run the final perspective-diverse critic panel on the closed design and fold surviving objections back in — without fan-out, apply the panel's lenses yourself, one pass each; `--critics=<n>` sets how many lenses attack it ([adversarial-critics](../modules/adversarial-critics.md)).

The output is a validated, sliced, closed design — buildable in independent units, every open resolved, residual risks flagged — ready to hand to `decompose` or `develop`, or to publish.
