# Record the rejected alternatives

The most durable part of a design is the record of what it *didn't* do and why. Six months out, the chosen approach is visible in the code, but the reasoning that beat the alternatives lives only in the head of whoever is now gone — so a maintainer re-litigates a settled question, or "simplifies" away a choice that silently prevented a bug. The rejection rationale is the guardrail. This rule pins what every recorded decision must carry and where it lives.

## The content contract (pinned)

Every design decision worth recording carries these elements; the assignment test is **present and specific** vs **absent or vague**:

- **Context and the forces in tension** — the constraints, technical and organizational, that pull the decision in different directions.
- **The decision, stated actively** — "We will …", in full sentences, not a hedge.
- **The alternatives seriously considered, each with why it was rejected** — tied to the specific axis or MUST-constraint it lost on (from [choosing-approach](../phases/02-choosing-approach.md)'s scoring). *This is the load-bearing element*: a record with a decision but no weighed-and-rejected options fails the test — it documents a conclusion, not a choice.
- **Consequences, positive and negative** — what the decision buys and what it costs; a record listing only upsides is incomplete.
- **A status** — proposed / accepted / superseded — so a later reversal is visible rather than silent.

`(basis: ISO/IEC/IEEE 42010:2022 requires an architecture description record its rationale including "architectural alternatives not chosen"; Nygard 2011, MADR 4.0, Fowler's ADR bliki, Zimmermann's Y-statement, and Tyree & Akerman 2005 (IEEE Software) all converge on this element set — the richer templates add nothing that contradicts it.)` *Anchor (top):* an entry naming ≥2 considered options with concrete pros/cons and a decision tied to named drivers. *Anchor (bottom):* a bare "we chose X" with no alternatives and no negative consequences.

## Where the record lives (house default)

`(basis: ratified by the maintainer, 2026-07-05. No external authority mandates a file layout — ISO 42010 requires the rationale content but is format-agnostic. House default: inline rationale inside the plan's design document, because plan already emits one team-facing design doc and a separate numbered ADR tree would drift out of sync with it and duplicate the export. Routing: an existing repo convention (a `doc/adr/` tree, or established rationale sections) wins first → this house default → maintainer.)`

Escalate a decision to a **standalone MADR-minimal numbered file** only when it is architecturally significant *and* needs immutable, individually-addressable history that must outlive edits to the design doc — the case where the ADR camp's superseded-not-edited discipline earns its ceremony. The cost inline pays is that rationale is mutable and can be overwritten as the doc evolves; keep the rejection reasons intact through edits, since erasing them is exactly the failure this rule exists to prevent.

Cited by [choosing-approach](../phases/02-choosing-approach.md). Related: [design-for-reversibility](design-for-reversibility.md) (a one-way decision most needs its rationale), [surface-assumptions](surface-assumptions.md) (an assumption is a decision's hidden premise).
