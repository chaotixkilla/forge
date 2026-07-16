# deep-dive (`--deep`)

Activated by `--deep`, referenced from the SKILL.md body (it widens the whole run, not one phase).

`--deep` escalates the investigation from an efficient single pass to an exhaustive one. It raises three dials, all measured against the stopping test in [stop-when-answered](../rules/stop-when-answered.md) — it does not remove the test, it raises the target the test measures against:

1. **Target certainty rung** — raise the target to *observed*: run the load-bearing paths to witness them, where [read-only-boundary](read-only-boundary.md) allows, rather than accepting the *traced* reading the default settles for once a static trace is conclusive. The default runs only to settle a claim reading cannot; `--deep` runs the load-bearing paths even when reading already settled them ([03-trace-the-behavior](../phases/03-trace-the-behavior.md), [separate-fact-from-inference](../rules/separate-fact-from-inference.md)).
2. **Blast radius** — follow the secondary paths and edge cases the default notes-but-skips: the paths a claim doesn't directly turn on but could under an input the question didn't name, the boundary inputs, the error branches. Widen from "the paths the answer turns on" to "the paths that could change the answer."
3. **Corroboration** — delegate to gather in its own deep mode (`gather --deep`: wider lane set, more lead-chasing rounds) so the history and ground-truth checks in [corroborate-against-reality](../phases/04-corroborate-against-reality.md) are canvassed rather than sampled.

`--deep` trades latency for a map that is both more certain (higher rungs) and wider (more paths); it changes how hard understand digs, never what a claim or the map *means*.
