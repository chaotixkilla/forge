# Justify every moving part

Every component, service, layer and abstraction a design introduces is a cost paid for as long as it lives: one more thing to understand, test, deploy and keep coherent. Each addition feels locally justified when it's drawn, so complexity accretes one reasonable-looking box at a time until the design is heavier than the problem.

## The bar: earns its place

A new moving part earns its place only if it traces to a **MUST-level constraint** — a requirement the design must meet, not one it would merely like to — that **no already-present part covers**. State the constraint next to the part. A part justified only by a *presumptive future* need — "we might want to swap this later", "this makes it extensible" — has not earned its place; cut it, and design so it can be added when a real need arrives. This restrains presumptive features and structure, not effort that keeps the design easy to change: a well-placed seam isn't a violation. `(basis: maintainer, 2026-07-05; after Fowler's YAGNI)`

## When the moving part is an abstraction

The commonest unjustified moving part is a premature abstraction, and three standards decide it: whether to abstract at all yet — the floor of two real, present callers — is [avoid-premature-abstraction](avoid-premature-abstraction.md)'s; whether two lookalike pieces are one piece of knowledge, and how much repetition triggers extracting, is [dry-vs-incidental-duplication](dry-vs-incidental-duplication.md)'s; and the shape an earned abstraction takes, and the signal that it has gone wrong, is [right-altitude-abstraction](right-altitude-abstraction.md)'s.

## What this standard is not

It is not a mandate to minimize part *count* at the cost of the problem's essential complexity — a hard problem that genuinely needs the machinery keeps it; cutting essential complexity breaks the design. The test is always "what constraint is lost if this goes?", not "is this the fewest boxes?".

Related: [seam-along-change-boundaries](seam-along-change-boundaries.md) (where a justified boundary goes), [design-for-reversibility](design-for-reversibility.md) (a cheap-to-undo part is a cheaper bet).
