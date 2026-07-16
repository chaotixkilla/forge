# Match existing spec conventions

A spec that imports a foreign template reads as an outsider's document and gets reformatted or ignored. If the team writes requirements as user stories and the spec arrives as a numbered SHALL-list, if they prioritize with MoSCoW and the spec ranks 1–5, if their specs are coarse-grained and this one enumerates every field — the mismatch is friction at best and, at worst, the spec is quietly rewritten to fit, losing whatever rigor it had. This rule keeps the spec's vocabulary, requirement format, and granularity aligned with the surrounding work, and — because spec has several places where more than one format is defensible — it carries the **routing rule** that decides each of those forks the same way every time.

## The discriminator: is there a convention to mirror?

For each formatting choice (how requirements are phrased, how they're bucketed, how acceptance criteria are written, how priority is expressed), walk one routing chain and stop at the first hit:

1. **Mirror the repo.** If the surrounding repo already has specs/RFCs/requirement docs, match their vocabulary, format, and granularity. An existing convention in the codebase wins — consistency with what the team already reads beats any external ideal.
2. **Else the house rule.** Absent a repo artifact to mirror, use the established house default (below). These are conventions, not arbitrary picks — each is both the praxis house standard and a recognized industry framework.
3. **Else route to the maintainer.** Absent even a house default, propose a sourced candidate and route it to the maintainer — non-gating: the spec proceeds on the proposal, flagged, rather than stalling.

The routing is non-gating at every step: the point is to pick *a* convention and note where it came from, never to block the spec on a formatting question.

## The house defaults (step 2), and their forks

Three choices are genuine forks — more than one format is defensible — so each is pinned to a house default with its live alternatives recorded, resolved by the chain above:

- **Requirement taxonomy** — house default: **functional / non-functional / data / interface-contract** (with functional stated as user stories). Fork: vs. a pure user-story/Gherkin backlog, vs. ADR-style decision records. `(basis: house convention — the existing spec skill's phase-03 buckets, propagated across sibling skills (decompose, test); aligns with ISO/IEC/IEEE 29148's requirement categories. Routed to maintainer only if a repo convention contradicts it.)`
- **Priority framework** — house default: **MoSCoW**. Fork: vs. numeric 1–5, vs. Kano. `(basis: house convention — the praxis spec design's phase-05; MoSCoW is the DSDM standard. The scale rungs/anchors are defined and maintainer-ratified (2026-07-04) in [sequencing-and-sizing](../phases/05-sequencing-and-sizing.md).)`
- **Acceptance-criteria format** — house default: **Given/When/Then**, with example tables for combinatorial rules and bounded assertions for quality attributes ([prefer-examples-over-prose](prefer-examples-over-prose.md) carries the per-case fork). Fork: vs. example-tables-first, vs. flat assertion lists. `(basis: house convention — the existing spec skill's phase-04; GWT is standard BDD practice.)`

## Method

Before choosing a format in [requirement-structuring](../phases/03-requirement-structuring.md), [making-it-concrete](../phases/04-making-it-concrete.md), or [sequencing-and-sizing](../phases/05-sequencing-and-sizing.md), run the chain: check for a repo convention to mirror (a [gather](../../gather/SKILL.md) read can surface one); absent that, take the house default and note it; absent that, propose and route. Record which rung of the chain each choice landed on, so a reader can see whether a format was mirrored, defaulted, or proposed — and so the maintainer knows exactly what is theirs to ratify.
