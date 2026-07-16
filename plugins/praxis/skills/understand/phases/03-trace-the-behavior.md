This is where the map is made. With the surfaces located, follow the real execution and data-flow paths end to end — from the entry point the question names, through the paths the answer turns on — and grade each claim by how much you actually established. A trace that reads names instead of behavior, or that states a reasoned guess as a fact, produces a confident map of a system that does not exist. Run this at full attention: the certainty of the whole map is decided here.

## Follow the paths the question turns on
Start at the entry point and follow execution along the paths a claim the framed question must answer depends on — the discriminator is **a path matters when a claim the question must answer depends on what it does** ([stop-when-answered](../rules/stop-when-answered.md)). Trace those end to end; note-but-don't-chase the paths the answer doesn't turn on ([read-at-definition-and-call-sites](../rules/read-at-definition-and-call-sites.md)). Trust what the code does over what its names and comments claim, and verify each path actually runs before resting a claim on it ([follow-execution-not-names](../rules/follow-execution-not-names.md)).

When the system under study is *declarative* rather than executable — a config, a schema, an IaC manifest, a skill — "follow execution" means follow **how the interpreter consumes the artifact** (the loader, validator, or harness that acts on it), not a call stack; the entry point is where the interpreter first reads the artifact ([separate-fact-from-inference](../rules/separate-fact-from-inference.md), "when the system is declarative").

## Trace the data, not only the control
For the values the question turns on, follow the data across its lifecycle — shape at origin, validation and coercion points, mutation, and boundary crossings ([follow-the-data](../rules/follow-the-data.md)) — not just which functions call which. A whole class of behavior (a dropped field, a skipped check, a shape lost at a serialization boundary) is invisible to a control-flow-only read.

## Grade every claim as you establish it
As you record each claim, tag it with the certainty the evidence earns — *observed* / *traced* / *inferred* / *assumed-unverified* ([separate-fact-from-inference](../rules/separate-fact-from-inference.md)) — and anchor it to its locator ([anchor-every-claim](../rules/anchor-every-claim.md)). The grade is assigned from *how* you came to believe the claim: ran it (observed), read the whole path (traced), reasoned from partial evidence (inferred), took a name or doc on faith (assumed-unverified). Grade honestly as you go; a claim you cannot anchor cannot be graded and is not yet a finding.

## The read-only posture — default and hardened
understand is read-only with respect to the system under study: it never edits, commits, or changes it. What it *may run* is bounded by a deterministic trigger, so two cold runs make the same run/don't-run call:

- **Default:** the target rung is *traced* ([stop-when-answered](../rules/stop-when-answered.md)), so **trace by reading first, and run a path (safe observation only) only when the static trace cannot settle a load-bearing claim** — the behavior turns on runtime state reading can't resolve (a dynamic-dispatch target, a config/env-driven branch, an external response), or two static readings are both defensible. When the trace settles the claim, accept *traced* and do not run — running there adds no certainty the map needs. Running an already-settled load-bearing path to reach *observed* is what `--deep` adds ([deep-dive](../modules/deep-dive.md)), not the default.
- **`--read-only`:** running is forbidden entirely; a claim the static trace cannot settle stays at its true (sub-traced) rung, and the top achievable rung is *traced* — state that cap rather than grading a static read as observed.

What counts as safe observation versus a mutation — the line both postures are defined against — is pinned in [read-only-boundary](../modules/read-only-boundary.md); obey it whether or not the flag is set. The certainty rungs are owned by [separate-fact-from-inference](../rules/separate-fact-from-inference.md).

The output of this phase: the traced paths as a set of anchored, certainty-graded claims about what the system does — the raw material [synthesize-the-answer](05-synthesize-the-answer.md) assembles into the map.
