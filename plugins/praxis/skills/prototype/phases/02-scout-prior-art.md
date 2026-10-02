Before building anything, find out what already exists — because the cheapest spike is often not "build a probe" but "reproduce the example someone already wrote and observe it." Prior art gives you three things a from-scratch build doesn't: a reference implementation to reproduce and diverge from ([anchor-to-prior-art](../modules/anchor-to-prior-art.md)), the idiom others converged on (so your probe tests the real approach, not a naive strawman), and — most valuable — the known dead-ends, so you don't spend the spike re-discovering that the obvious approach doesn't work.

## Scout the three sources

Recruit three explorers, each on a different source, and run them directly, not through gather — this is a bounded prior-art scout, not a cross-lane knowledge synthesis:

- **[code](../../../agents/explorers/code.md)** — existing implementations in this codebase or its dependencies: has this been solved here before, is there a pattern to reuse or a prior attempt to learn from?
- **[official-documentation](../../../agents/explorers/official-documentation.md)** — the authoritative contract of any library, API, or tool the unknown touches: what it officially supports, its stated limits, its own examples.
- **[community-practices](../../../agents/explorers/community-practices.md)** — how others solved this in the wild: the blog posts, issues, and Q&A that reveal the pitfalls and the approaches that failed.

**Without fan-out**, run the three scans yourself in sequence — search the codebase and its dependencies, read the official docs of what the unknown touches, then scan community sources for pitfalls — before proceeding. No knowledge-base explorer joins the scout: prototype touches no `tools.knowledge` and stays config-less. `(basis: prototype is deliberately not a gather consumer)`

## Turn what they return into inputs for the probe

Synthesize the three streams into: **what to reproduce or seed from** (a reference the probe can start from rather than build — feeds `--prior-art` and [pick-the-cheapest-probe](03-pick-the-cheapest-probe.md)'s "reuse over fresh" discriminator), and **the dead-ends to skip** (approaches already known to fail, which become recorded dead-ends immediately — [record-dead-ends](../rules/record-dead-ends.md) — rather than probes to re-run). If the scout turns up a reference that *already answers the framed question* under conditions faithful to it, say so and stop: no probe is built, and the run returns the reference's observed result as its finding, with its verdict taken from what the reference showed — a valid, cheap result. `(basis: derived from a verdict resting on observed behavior, whoever observed it)`

The output of this phase: the reference(s) to seed from and the dead-ends to avoid — what [pick-the-cheapest-probe](03-pick-the-cheapest-probe.md) builds on.
