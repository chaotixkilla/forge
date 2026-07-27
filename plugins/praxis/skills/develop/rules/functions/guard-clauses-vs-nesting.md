# Guard clauses vs. nesting

Writing a conditional, the reflex is to nest: the happy path goes inside the `if`, the rest cascades in, and three preconditions deep the real work sits under an arrow of indentation. The judgment this rule governs is *when* to invert a condition and return early instead — pull the special case to the top, handle it, and leave the body flat. Left to taste, one builder flattens everything into a wall of early returns and another nests everything into a pyramid, and the same logic reads two opposite ways.

## The discriminator

The test is **what the branch is doing to the flow** — dispatching a special case out, or choosing between peers that both continue.

- **Invert and return early when the condition is a *precondition, error, or edge case* that is handled-and-gone.** A null input, an empty collection, an unauthorized caller, a not-found lookup — these are the *bouncer at the door*: check it, deal with it, return, and the rest of the function proceeds knowing that case is behind it. Each guard removes a case from everything below, so the main path reads at zero indentation.
- **Keep the nesting when the branches are genuinely parallel** — a real `if`/`else` where both arms are equally-weighted continuations of the same decision, neither one an exception to the other. Forcing an early return here doesn't remove a case; it amputates half of one cohesive choice and scatters it.
- **The tell:** can you name the branch as "the X case we get out of the way first"? Then guard it. If the two arms only make sense read together as "either this or that," they are peers — keep them side by side.

(basis: Fowler, *Refactoring* — "Replace Nested Conditional with Guard Clauses": when one leg of a conditional is a special/exceptional case, handle it first and return, reserving `if`/`else` for cases of equal weight. The precondition-vs-peer distinction is the operative line.)

## The anchors

- *Good:* a function that opened three levels deep — `if user`, then `if user.active`, then `if order.valid`, then the work — flattened to three guard clauses that each reject-and-return up front, leaving the charge logic at the top level, unindented and obvious.
- *Bad:* a single cohesive pricing decision — "if premium tier apply one rate, else the standard rate" — mangled into an early `return premiumRate` so the standard case dangles below with no `else`, hiding that these are two halves of one choice. The reader can no longer see the decision as a unit; the two rates should sit as visible peers.

Guards also keep each function reading at [one-level-of-abstraction-per-function](one-level-of-abstraction-per-function.md), and taming a conditional that has grown many arms is [reduce-branching-complexity](reduce-branching-complexity.md)'s job, not this one's.
