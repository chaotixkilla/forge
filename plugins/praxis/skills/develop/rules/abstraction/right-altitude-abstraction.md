# Right-altitude abstraction

The moment this rule governs is the one where you've decided some indirection is warranted — an interface, a base class, a config-driven strategy, a generic helper — and now choose its *shape*. Indirection is not free: every layer is one more hop a reader traverses and one more thing the next maintainer must understand before they can change anything. Too high, it's ceremony that hides nothing; at the right altitude, it hides real complexity behind a small face. The judgment is *which shape* pays for itself, and two builders left to taste reach for very different rungs. This rule pins the discriminator.

## The discriminator

This rule takes the *timing* call as already made — whether to abstract at all *yet* is [avoid-premature-abstraction](avoid-premature-abstraction.md)'s, and *how much duplication* triggers extracting is the fork in [dry-vs-incidental-duplication](../reuse/dry-vs-incidental-duplication.md). Given the abstraction is warranted, it pins the **altitude**: the simplest shape that holds the requirement.

- **Would removing the indirection lose anything a present requirement needs?** If the layer could be inlined with no loss to any real caller, it's too high — dead weight. If inlining it would force a real duplication or break a seam a present requirement needs, it's earning its keep. (A layer justified only by a *hypothetical future* caller isn't mis-altitude, it's premature — [avoid-premature-abstraction](avoid-premature-abstraction.md).)
- **Prefer the simplest shape that holds the requirement.** A function beats a class beats a hierarchy beats a framework, when each holds the requirement. Reach up the ladder only when the rung below genuinely can't carry the load.
- **The depth test.** A right-altitude indirection is a *deep* one — a small interface over real hidden complexity; a shallow pass-through that adds a hop without hiding anything is at the wrong altitude however real its caller ([shallow-interface-deep-module](shallow-interface-deep-module.md)). Depth, not layer-count, is the measure.

## The anchors

- *Right altitude:* two call sites genuinely need the same behavior parameterized one way, so a single function with one parameter replaces them — nothing simpler holds the two, and inlining it back would re-create the duplication.
- *Too high (reject):* the same real two-caller need built as an abstract base class + two subclasses + a factory — the requirement is genuine (not premature), but the *shape* sits three rungs above what holds it; collapse it to the parameterized function. (Contrast a layer with *no* second caller at all — that is premature, a timing fault, not a mis-altitude one: [avoid-premature-abstraction](avoid-premature-abstraction.md).)
