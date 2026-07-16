# Document the public contract

When you add a function, type, or module that others will call, the judgment this rule governs is what to write above it — and how much. The signature carries the names and types; it does not carry the units, the invariants, the failure modes, or the side effects a caller needs to use it *correctly*. Left to taste, one builder documents nothing public and lets callers reverse-engineer the contract by reading the body; another ceremonially docstrings every private helper with `// returns the result`, drowning the surface that matters in boilerplate. This rule pins the discriminator so two builders converge on what to document and how deep.

## The discriminator

Document what **crosses the boundary** — the contract of a public function, type, or module — at the depth a caller needs to use it correctly *without reading the body*. The test is a single question: **can a caller use this correctly from the doc and signature alone?**

- **Document the public surface, not the internals.** What is reachable by another module or another author needs a contract stated. A private helper whose only caller sits three lines below it does not — its meaning is visible at its one call site, and a docstring there is ceremony. The bar for writing a doc is *distance and reach*, not a blanket "document everything."
- **State what the signature can't.** The things a caller needs and cannot see from names and types: **inputs** (accepted ranges, what counts as valid), **outputs** (units, what's returned when there's nothing to return — [null-and-empty-handling](../data-and-types/null-and-empty-handling.md)), **invariants** it assumes and preserves, **failure modes** (what it raises/returns on bad input, and whose job validation is), and **side effects** (what it mutates, writes, or calls). A caller who can't predict these from the doc will misuse the function.
- **Describe the abstraction, not the implementation.** The doc says *what the function promises and requires* — not *how* it computes it. Documenting the algorithm couples the contract to the body, so the doc breaks every time the implementation is refactored without the promise changing. Keep it to the *why* and the *what-it-guarantees*, never the mechanics ([comment-the-why-not-the-what](comment-the-why-not-the-what.md)).

(basis: Ousterhout, *A Philosophy of Software Design* — interface comments describe the *abstraction* a caller needs, deliberately omitting implementation detail so the module stays deep; the docstring/javadoc convention of documenting the contract — parameters, return, raises, effects — not the body. Document the contract, not the implementation.)

## The anchors

- *Good:* a public `chargeCard(order)` whose doc states: amount is taken from `order.total` in **minor units**, returns a settled-transaction id, **raises** `PaymentDeclined` on a hard decline and retries transient failures internally, and **writes** an audit row as a side effect. A caller wires it correctly having never opened the body.
- *Bad:* the same function with `// charges the card` — restating the name, hiding the units, the exception, and the audit write, so every caller either reads the implementation or gets one of them wrong. Equally bad: a three-line docstring on a private one-line helper whose call site already tells the whole story.
