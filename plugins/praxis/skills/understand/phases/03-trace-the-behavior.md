## Follow the paths the question turns on
Start at the entry point and follow execution along the paths a claim the framed question must answer depends on — the discriminator is **a path matters when a claim the question must answer depends on what it does** ([stop-when-answered](../rules/stop-when-answered.md)). Trace those end to end; note-but-don't-chase the paths the answer doesn't turn on ([read-at-definition-and-call-sites](../rules/read-at-definition-and-call-sites.md)). Trust what the code does over what its names and comments claim, and verify each path actually runs before resting a claim on it ([follow-execution-not-names](../../../craft/evidence/follow-execution-not-names.md)).

When the system under study is *declarative* rather than executable — a config, a schema, an IaC manifest, a skill — "follow execution" means follow **how the interpreter consumes the artifact** (the loader, validator, or harness that acts on it), not a call stack; the entry point is where the interpreter first reads the artifact ([certainty-scale](../rules/certainty-scale.md), "when the system is declarative").

## Trace the data, not only the control
For the values the question turns on, follow the data across its lifecycle — shape at origin, validation and coercion points, mutation, and boundary crossings ([follow-the-data](../../../craft/engineering/follow-the-data.md)) — not just which functions call which.

## Grade every claim as you establish it
As you record each claim, tag it with the certainty the evidence earns — *observed* / *traced* / *inferred* / *unverified*, by the discriminators in [results-and-certainty](../../../craft/evidence/results-and-certainty.md) and understand's placement test in [certainty-scale](../rules/certainty-scale.md) — and anchor it to its locator ([anchor-every-claim](../../../craft/evidence/anchor-every-claim.md)). Grade honestly as you go; a claim you cannot anchor cannot be graded and is not yet a finding.

## The read-only posture — default and hardened
understand is read-only with respect to the system under study: it never edits, commits, or changes it. What it *may run* is bounded by a deterministic trigger, so two cold runs make the same run/don't-run call:

- **Default:** the target rung is *traced* ([stop-when-answered](../rules/stop-when-answered.md)), so **trace by reading first, and run a path (safe observation only) only when the static trace cannot settle a load-bearing claim** — the behavior turns on runtime state reading can't resolve (a dynamic-dispatch target, a config/env-driven branch, an external response), or two static readings are both defensible. When the trace settles the claim, accept *traced* and do not run — running there adds no certainty the map needs. Running an already-settled load-bearing path to reach *observed* is what `--deep` adds ([deep-dive](../modules/deep-dive.md)), not the default.
- **`--read-only`:** running is forbidden entirely; a claim the static trace cannot settle stays at its true (sub-traced) rung, and the top achievable rung is *traced*.

What counts as safe observation versus a mutation is pinned in [mutation-vs-observation](../rules/mutation-vs-observation.md); obey it on every run, and under `--read-only` also [read-only-boundary](../modules/read-only-boundary.md)'s zero-execution rule.

The output of this phase: the traced paths as a set of anchored, certainty-graded claims about what the system does — the raw material [synthesize-the-answer](05-synthesize-the-answer.md) assembles into the map.
