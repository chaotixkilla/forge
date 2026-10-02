Pre-solve on paper the few flows where the design will bite mid-build: the migration that can half-apply, the partial failure that leaves state inconsistent, the multi-step sequence with a race in it, the idempotency assumed and never guaranteed.

## Find and rate the hard flows — the risk scale

Enumerate the flows that could bite, then rate each on [the risk scale](../rules/risk-scale.md) — severity, likelihood-to-bite on its four-answer checklist, and the scale's routed rule for combining the two — so the deepest work goes where the risk is. If no flow could bite, say so and keep the phase short.

For each hard flow, recruit the **adversary** critic to construct the input that makes it fail (without fan-out, construct it yourself, as its own pass). Where a flow turns on a hard algorithm, invoke [gather](../../gather/SKILL.md) on its `authoritative-literature` lane with the flow and the property it must hold, and carry back the known approach and its failure modes.

## Sequence the tricky flows

For each flow the risk rating places in the **top priority band** — every *Critical*-severity flow, plus any flow the chosen combination rule ranks highest — sequence it step by step, the non-obvious multi-step path, often as a diagram, so the ordering, the state at each step, and the points where two steps can interleave are explicit rather than assumed. Lower-band flows still get their failure mechanics noted below, but not the full step-by-step treatment; the cutoff is the band, not a fixed count, because how many flows clear it is risk-proportional and varies with the design.

## Specify the failure mechanics

Say mechanically what happens when a step fails: retries and their idempotency, transaction boundaries, what is left behind on a partial write, how the system converges after a fault. Surface the load-bearing assumptions each mechanism rests on ([surface-assumptions](../rules/surface-assumptions.md)) — "the upstream is idempotent", "this write is atomic" — and prefer reversible mechanics over ones that can't be undone ([design-for-reversibility](../../../craft/engineering/design-for-reversibility.md)). Then resolve the spec's edge cases into concrete behavior: the spec said *what* should happen at the boundary; now say *how* it happens mechanically. Under `--deep`, sequence more flows and specify mechanics to a finer grain ([deep-mode](../modules/deep-mode.md)).

The output is the hard flows sequenced, their failure mechanics specified, and each rated and prioritized on the risk scale — the pre-solved core [planning-rollout](05-planning-rollout.md) needs before it can decide how the change ships safely.
