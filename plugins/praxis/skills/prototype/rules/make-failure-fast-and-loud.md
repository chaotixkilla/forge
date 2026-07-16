# Make failure fast and loud

Wire the shortest path to a clear pass/fail signal, and surface errors immediately rather than handling them gracefully. Production code catches, logs, and recovers; a spike does the opposite — it lets the failure you're probing for crash loudly at the first line it reaches, because that crash *is* the signal. Graceful degradation in a spike hides exactly what you built it to see: a swallowed exception on the path you're testing turns a clean *refuted* into a confusing *still-open*.

Two moves: **shortest path to signal** — skip setup, config, and layers the question doesn't turn on; get to the observation in as few steps as the framed unknown allows. **Loud failure** — let it throw, assert hard, print the raw result; don't wrap the thing under test in a try/catch that converts a decisive failure into a quiet fallback. The faster and louder the pass/fail, the cheaper the spike and the more trustworthy the verdict.

Cited from [build-the-spike](../phases/04-build-the-spike.md).
