# Keep functions pure

As you write a function, computation and effect tend to fuse: the routine that calculates a result also reads the clock, writes a row, logs, or mutates a shared structure along the way. The judgment this rule governs is whether to keep the two tangled or split them — pure computation that returns a value from its inputs, separated from the effects (I/O, mutation, time, randomness) that touch the world. Left to taste, one builder writes a function that computes-and-writes in one breath and another separates them, and the first version is the one nobody can test without standing up the world.

## The discriminator

The test is **whether the effect *is* the function's job, or is riding along inside a computation.**

- **Push effects to the edges; keep a pure core.** A function that derives a result purely from its arguments — no reads of mutable outside state, no writes, same inputs always same output — is testable, cacheable, and reasoned-about in isolation. Keep as much of the logic in that form as you can, and let a thin outer layer do the reading and writing that feeds it and stores its result.
- **Split when a function *both* computes and effects.** If a routine calculates something non-trivial *and* persists/emits/mutates as a side errand, separate them: a pure function that returns the decision, and a caller that enacts it. The tell is a function you cannot unit-test without a fake clock, a stubbed store, or a captured global — the effect is entangled with logic that had no need of it.
- **Don't split when the effect is the point.** A function whose whole job is *write this record* or *emit this event* is cohesively an effect — leave it. Forcing a "pure" shell around a one-line side effect adds a layer that hides nothing. The discriminator is entanglement, not effect-presence.

(basis: the functional-core / imperative-shell design (Gary Bernhardt) — a pure core of decision logic wrapped in a thin effectful shell; Hunt & Thomas, *The Pragmatic Programmer* — decoupling for testability. The pure-function testability argument is the shared thread: a value-returning function is trivially testable; an effectful one drags the world into every test.)

## The anchors

- *Good:* `computeInvoice(order) -> Invoice` is pure and unit-tested with plain data; a separate `saveInvoice(invoice)` does the write. The pricing logic — the part with bugs worth catching — is exercised without a database in sight. Its state stays local while it computes ([minimize-state-scope](minimize-state-scope.md)).
- *Bad:* `computeInvoice(order)` that internally fetches the tax rate over the network, stamps `Date.now()`, writes the row, and returns the total — untestable without mocking three systems, and the pricing math is impossible to check in isolation. Failures at its boundary also have nowhere clean to be caught ([handle-errors-at-the-boundary](../errors/handle-errors-at-the-boundary.md)).
