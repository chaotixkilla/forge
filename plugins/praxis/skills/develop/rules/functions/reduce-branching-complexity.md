# Reduce branching complexity

A conditional grows one case at a time: a new `else if` here, a nested flag there, and eventually a function is mostly branching. The judgment this rule governs is whether that branching is *earning* its complexity or is accidental structure that a different shape would erase. Left to taste, one builder keeps extending the `switch` because it "works" and another rewrites it into a lookup, and the same logic ends up either an ever-growing ladder or a table — with no shared reason for which.

## The discriminator

Branching earns its complexity when **each branch is genuinely distinct logic**; it is accidental when the branches share a shape and only differ in data.

- **Same shape repeated per case → data-drive it.** If every arm of a `switch` does the structurally identical thing with a different constant, handler, or field, the cases are *data*, not logic — replace the ladder with a dispatch table or map keyed on the discriminant, so adding a case is adding a row, not a branch. If the arms differ by the *type* they operate on, that is the shape polymorphism replaces ([prefer-composition-over-inheritance](../abstraction/prefer-composition-over-inheritance.md) for how to carry the variants).
- **Redundant or double-negated conditions → collapse them.** `if (!(a && !b))` and a check re-tested in a nested `if` are accidental complexity; simplify the boolean and hoist the shared condition out. A precondition buried in nesting is usually a guard clause trying to get out ([guard-clauses-vs-nesting](guard-clauses-vs-nesting.md)).
- **Genuinely distinct logic per case → leave the branch.** When each arm is real, different behavior with nothing structural in common, an explicit conditional is the honest shape; do not contort it into a table that hides the differences. The test: would data-driving it force you to smuggle per-case behavior into the "data"? Then it isn't data.

(basis: McConnell, *Code Complete* — taming conditional complexity with table-driven methods, replacing sprawling logic with a lookup when cases share structure; Fowler, *Refactoring* — "Replace Conditional with Polymorphism" when the branches vary by type. The shared-shape-vs-distinct-logic split is the operative test.)

## The anchors

- *Good:* a `switch` on message-type with ten arms, each just picking a handler, collapsed to a map from type to handler — adding an eleventh type is one entry, and the dispatch reads at a glance.
- *Bad:* a five-arm `switch` where each arm runs materially different validation, workflow, and side effects, force-fitted into a "config table" of nested lambdas — the distinct logic is now hidden inside data, harder to read than the honest branches it replaced.
