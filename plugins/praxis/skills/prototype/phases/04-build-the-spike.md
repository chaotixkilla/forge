Now build the probe chosen in [pick-the-cheapest-probe](03-pick-the-cheapest-probe.md) — at spike speed, which is a different discipline from writing software. The goal is a clear observation of the framed unknown, not a working feature, so every instinct honed on production code (handle the errors, name things well, factor out the duplication, cover the edge cases) is a cost here, not a virtue. Build the shortest thing that produces the signal, and build it to be deleted.

## Build only the path to the signal

- **Stub everything that isn't the unknown** ([isolate-what-you-test](../rules/isolate-what-you-test.md)) — hardcode inputs, fake dependencies, skip config and setup the question doesn't turn on. The one thing you never stub is the framed unknown itself.
- **Fail fast and loud** ([make-failure-fast-and-loud](../rules/make-failure-fast-and-loud.md)) — wire the shortest path to an unambiguous pass/fail; let the thing under test throw rather than catching and recovering, because the crash is the signal.
- **Borrow over craft** ([favor-disposability](../rules/favor-disposability.md)) — reproduce the reference [scout-prior-art](02-scout-prior-art.md) found rather than writing from scratch, and don't invest in structure or naming you'd want in production; this code is about to be thrown away.

## Module activations

- **`--sandbox`** — build and run the spike inside an isolated throwaway environment so it can't touch real state and is trivial to discard wholesale: see [sandbox-isolation](../modules/sandbox-isolation.md). (Its teardown is in [capture-and-discard](06-capture-and-discard.md).)
- **`--prior-art=REF`** — start by reproducing the named reference to a known-good baseline, then diverge toward the framed unknown so the divergence isolates exactly what's in doubt: see [anchor-to-prior-art](../modules/anchor-to-prior-art.md).
- Effort here is bounded by **`--timebox`** — see [timeboxed-spike](../modules/timeboxed-spike.md); if the clock expires mid-build, stop and carry whatever ran into [evaluate-against-the-question](05-evaluate-against-the-question.md) as a still-open result, rather than pushing on.

The output of this phase: a runnable probe that exercises the framed unknown and produces an observable pass/fail — ready to run and read in [evaluate-against-the-question](05-evaluate-against-the-question.md).
