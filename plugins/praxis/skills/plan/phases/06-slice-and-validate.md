This is the closure gate. A design can look complete and still hide a "figure it out later" that detonates mid-build — an open decision from mapping never closed, a seam specified too loosely for two developers to converge, an untested assumption the whole thing rests on. This phase proves the design is *buildable*: sliceable into units each verifiable on its own, with nothing load-bearing left open. A plan that leaves opens is not done, and saying it is done when it isn't is the failure this phase exists to catch.

## Slice into independently buildable units

Break the design into units that can each be built and verified on their own, in an order where each rests only on what came before. The test that the slicing is real: at least one **end-to-end function** can be traced through the units with no gap — a thin path from entry to storage and back that exercises every main component the design introduces. That walking-skeleton trace is what proves the pieces actually connect, not just that they were each named.

## The buildable / closed bar

`(basis: ratified by the maintainer, 2026-07-05. No authority pins a lightweight "design ready" gate — Scrum defines a Definition of Done but no Definition of Ready, and IEEE 1016 defines documentation completeness, not buildability. The positive test is anchored on the walking-skeleton / tracer-bullet lineage (Cockburn, Crystal Clear, 2004; Hunt & Thomas, The Pragmatic Programmer, tracer bullets) and risk-proportional depth (Fairbanks, Just Enough Software Architecture, 2010). The exact threshold wording is the maintainer's house standard.)`

A design is **closed / buildable** when all of these hold — check them explicitly, and a failure is an open, not a nit:

- **Every main component is named**, and one real end-to-end function traces through them with no gap (the walking-skeleton test above).
- **Each seam/contract is specified precisely enough that two independent developers would build the same interface** — the convergence bar from [specify-interfaces](03-specify-interfaces.md).
- **Every open decision surfaced in [mapping-to-system](01-mapping-to-system.md) is now closed** — nothing deferred to "later". (With `--from-spec`, additionally: every spec requirement is addressed by some part of the design — [from-spec](../modules/from-spec.md).)
- **Every moving part earns its place** against a constraint ([justify-every-moving-part](../rules/justify-every-moving-part.md)) — the closure pass is also the last chance to cut what doesn't.
- **The single riskiest assumption has a named validation step** ([surface-assumptions](../rules/surface-assumptions.md)) — the design does not bet the build on an unchecked premise.

Do **not** substitute Scrum's Definition of Done (that is "increment shipped", downstream of this handoff) or a full IEEE-1016 design document (documentation completeness, not buildability) for this bar unless the domain contractually requires the formal artifact.

## Before it goes out, read it as its reader

Put the finished report through [deliver-at-the-readers-register](../../communicate/rules/deliver-at-the-readers-register.md) before delivering it: take from that rule the obligations this phase has not already settled for itself, and apply its honesty floor to the result. A run with no register to write to falls back on the only vocabulary it has loaded — this procedure's own — which is how a report comes out accurate and unreadable. Read the floor from the rule item by item rather than from memory — the passages it protects are exactly the ones that read as padding to anyone not checking whether the claim is true — and let its carve-out for named levels and verdict values hold the graded rungs and status names this skill defines and reports on.

**And a visual where prose would carry it worse.** Where what this report describes alters a *structure* — a shape, a flow, a set of relationships — show it rather than describing it, per `output.diagrams` (`when-structural` by default — [report-style-settings](../../init/rules/report-style-settings.md)) and the judgment in [when-a-visual-is-owed](../../communicate/rules/when-a-visual-is-owed.md), which decides whether one is genuinely owed here. A visual is earned by what the subject *is*, never by how long the prose ran: it stands in for the paragraph that would have described the shape, and it is decoration the moment it sits beside that paragraph instead.

## Flag residual risk, stress-test, and hand off

Flag the known unknowns that remain and what needs a spike or throwaway prototype *before* committing to build — the design can be closed on paper and still name a risk that a small experiment should retire first. Run the final perspective-diverse critic panel on the closed design and fold surviving objections back in; `--critics=<n>` sets how many lenses attack it ([adversarial-critics](../modules/adversarial-critics.md)). When invoked with `--publish`, hand the finished design to [publish-handoff](../modules/publish-handoff.md) as a clean, team-facing document — the design and its decisions, stripped of all praxis machinery.

The output is a validated, sliced, closed design — buildable in independent units, every open resolved, residual risks flagged — ready to hand to `decompose` or `develop`, or to publish.
