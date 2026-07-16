# Clean up on the failing path

Code that acquires something — a file handle, a connection, a lock, a transaction, an allocated buffer — has to release it, and the happy path always does. The judgment this rule governs is the branches nobody looks at: what happens to that resource when a step *after* the acquire throws or returns early. Left to reflex, cleanup is written once, at the end of the success path, and every early exit leaks past it — the handle stays open, the lock stays held, the transaction stays half-applied. The bug hides on the error path, which is exactly the path least likely to be exercised, so it ships. Two builders diverge: one hangs cleanup off scope, one hand-writes it per branch and misses one. This rule pins the discriminator so two builders converge on releasing on every path.

## The discriminator

The property this turns on is **whether each acquire has a release bound to release automatically on every exit — success, early return, and thrown**, rather than repeated by hand on each branch.

- **For every acquire, find its guaranteed release.** Pair each resource with cleanup the language runs unconditionally when scope unwinds — the scope-bound construct (`defer`, `with`, RAII/destructors, `try`/`finally`, try-with-resources), not a manual close at each of the three places control can leave. Hand-rolled per-branch cleanup is the pattern that leaks: the branch added last forgets it.
- **Make partial work atomic or undone.** A sequence that mutates shared state across steps must, on failure midway, either commit nothing (transaction, staged-then-swap) or explicitly roll back what it already did — never leave the half-written state a later reader will trust.
- **The test:** *if the step after this acquire throws, does the resource still get released and the partial write still get undone?* Trace the throw, not just the return. If the answer needs you to remember to catch it manually, bind it to scope instead — the failing path you didn't write is the one that leaks.

Where the failure is then surfaced or propagated is a separate decision ([handle-errors-at-the-boundary](handle-errors-at-the-boundary.md)); cleanup runs regardless of who ultimately handles the error.

(basis: Stroustrup's RAII — resource acquisition is initialization, tying a resource's lifetime to a scope so release is guaranteed by unwinding, including on exceptions; Bloch, *Effective Java* — prefer try-with-resources to try/finally, because hand-written finally cleanup is error-prone and silently omitted. The structured-cleanup principle: bind release to scope, don't repeat it per branch.)

## The anchors

- *Good:* a function opens a connection inside a scope-bound guard, does three fallible steps, and returns early on the second's failure — the guard releases the connection on the way out, and a transaction wrapping the writes rolls back the first step's mutation automatically.
- *Bad:* the same function closes the connection only in the last line of the success path and commits step by step, so the early return leaks the connection and leaves the first write applied — a leak and a half-update that only appear when step two fails, which no test drove.
