Most of a design is routine; a few flows are where it will actually bite mid-build — the migration that can half-apply, the partial failure that leaves state inconsistent, the multi-step sequence with a race in it, the idempotency you assumed and didn't guarantee. This phase pre-solves those on paper, before code makes the cost of getting them wrong concrete. Because effort is finite, it also *rates* the hard flows, so the deepest work goes where the risk is, not where the flow happens to be listed first.

## Find and rate the hard flows — the risk scale

Enumerate the flows that could bite, then rate each on two axes so the list is ordered by risk rather than by discovery order.

`(basis: ratified by the maintainer, 2026-07-05. Severity rungs are condensed from and anchored to the AIAG-VDA FMEA Handbook (2019) severity table; likelihood-to-bite follows FMEA Occurrence + ISO 31000 qualitative likelihood; the numeric rung boundaries are a house standard, since no authority pins occurrence rates for design-time software flows.)`

- **Severity — how hard it bites** (assign by the *worst realistic* consequence if the flow fails):
  - *Critical* — irreversible or safety/legal/data-loss: data corruption, a security breach, regulatory noncompliance, unrecoverable state.
  - *Significant* — a primary user journey degrades or breaks, but it is recoverable and bounded.
  - *Minor* — no discernible effect on the user; cosmetic or a slight, secondary inconvenience.
- **Likelihood-to-bite — how likely it is to go wrong** (assign by a fixed checklist: prevention controls present? path novel/complex? prior incidents on it? test coverage?):
  - *High* — weak/absent controls, a new or complex path, or a history of failing here.
  - *Medium* — partial controls, moderate complexity, some coverage.
  - *Low* — strong controls, a well-trodden path, high coverage, no known prior failure.

**Combining the two axes is a fork — plan does not crown one** (encode the fork, route the choice): *severity-dominant* (any Critical flow is top-priority regardless of likelihood; likelihood only orders within a severity band — `basis: AIAG-VDA Action Priority`) versus *symmetric* (likelihood × impact / RAG grid — `basis: PMI PMBOK 6e`). Cox (2008, *Risk Analysis*) is the caution against naive multiplication — a symmetric grid can mask a low-likelihood/Critical flow behind a high-likelihood/Minor one. Routing: the surrounding team's existing risk practice wins → house rule → maintainer. Whichever is used, a Critical flow is never deprioritized on low likelihood without a documented reason. Recruit the **adversary** critic here to construct the failing input for each hard flow; delegate any hard-algorithm literature to `gather`.

## Sequence the tricky flows

For each flow the risk rating places in the **top priority band** — every *Critical*-severity flow, plus any flow the chosen combination rule ranks highest — sequence it step by step, the non-obvious multi-step path, often as a diagram, so the ordering, the state at each step, and the points where two steps can interleave are explicit rather than assumed. Lower-band flows still get their failure mechanics noted below, but not the full step-by-step treatment; the cutoff is the band, not a fixed count, because how many flows clear it is risk-proportional and varies with the design.

## Specify the failure mechanics

Say mechanically what happens when a step fails: retries and their idempotency, transaction boundaries, what is left behind on a partial write, how the system converges after a fault. Surface the load-bearing assumptions each mechanism rests on ([surface-assumptions](../rules/surface-assumptions.md)) — "the upstream is idempotent", "this write is atomic" — and prefer reversible mechanics over ones that can't be undone ([design-for-reversibility](../rules/design-for-reversibility.md)). Then resolve the spec's edge cases into concrete behavior: the spec said *what* should happen at the boundary; now say *how* it happens mechanically. Under `--deep`, sequence more flows and specify mechanics to a finer grain ([deep-mode](../modules/deep-mode.md)).

The output is the hard flows sequenced, their failure mechanics specified, and each rated and prioritized on the risk scale — the pre-solved core [planning-rollout](05-planning-rollout.md) needs before it can decide how the change ships safely.
