# Immutable by default

When you declare a value or a field, the moment this rule governs is whether it should be allowed to change after construction. The reflex is to make everything mutable because the language defaults that way and it's one keyword shorter. The cost is deferred and diffuse: a value handed to two holders becomes a channel between them, and a write by one silently changes what the other reads — the aliasing bug, and its concurrent cousin, the race. Two builders default in opposite directions, so the same data is a frozen fact in one module and a shared mutable cell in another.

## The discriminator

**Default every value to immutable; reach for mutation only when you can name a reason the value must change in place.** The test at declaration:

- **Does this thing have a real changing lifecycle** — an entity whose identity persists while its state genuinely evolves (a connection that opens then closes, an accumulator built in a tight loop) — **or is it a value that simply *is* what it is** (a configuration, a parsed record, a coordinate)? The second is immutable; construct a new value to represent a change rather than mutating the old. Mutation is for the first, where in-place change models something real.
- **Is there a *proven* performance need** — a measured hot path where copying is the bottleneck, not a guessed one? That earns local mutation, kept as contained as possible. "Might be slow" does not; prefer the immutable shape and let the profiler, not the reflex, authorize the exception ([make-it-work-then-make-it-right](../verification/make-it-work-then-make-it-right.md)).
- **Is the value shared or aliased?** Shared mutable state is exactly where aliasing bugs and data races live — a mutable field passed around is a bug waiting for a second writer. If more than one holder can reach it, immutable is not a preference, it's the safety property. Immutability also shrinks how far mutable state reaches ([minimize-state-scope](../functions/minimize-state-scope.md)) and is what lets a function stay pure ([keep-functions-pure](../functions/keep-functions-pure.md)).

(basis: Bloch, *Effective Java* Item 17 — "minimize mutability": immutable objects are simpler, inherently thread-safe, freely shareable, and can't be corrupted by aliasing; and the broad immutability-for-safety principle across functional-programming and concurrency literature — shared mutable state is the root of aliasing and race hazards, so default to values that can't change and confine mutation to where a lifecycle or measured cost demands it.)

## The anchors

- *Good:* a parsed configuration is a frozen record; a component that needs a variant constructs a modified copy, and because the original can't change, handing the same config to ten readers is safe by construction — no reader can perturb another.
- *Bad:* that config is a mutable object shared by ten components; one normalizes a field in place for its own use, and the other nine now read the normalized value they never asked for — a bug that reproduces only when the two run in a particular order.
