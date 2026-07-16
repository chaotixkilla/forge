# Cut along natural seams

When you must place a boundary between units, there is always a temptation to cut for a tidy count — five units instead of "one big one and two small ones." But a cut placed for the count runs straight through whatever coupling happens to sit there, and the two pieces it makes cannot move without each other: you have manufactured a dependency the design never had, and called it a unit boundary. This rule pins *where* to cut — at the seams the system already has — so the units come out genuinely independent rather than independent-looking. It is cited by [carve-into-units](../phases/02-carve-into-units.md).

## The discriminator: cut where coupling is already lowest

Cut at the boundaries the work hands you, where two sides already change for different reasons and share the least: a module edge, a published interface, a data boundary, a point where ownership or the reason-to-change diverges. The test is the same reason-to-change test that separates real from incidental coupling: **would a realistic change to one side of the cut force a change to the other?**

- **If the two sides change for different reasons** — a realistic change to one leaves the other untouched — the seam is real; cut there, and each unit stays independently buildable and reviewable.
- **If a realistic change to one side forces the other to change too** — they share a reason to change — the cut runs through a coupling; do not put a unit boundary there, or you get two units that must always be worked together.
- **The count is an output, not an input.** Let the number of units fall out of where the real seams are. If the seams give you three units, three is right; forcing a fourth by cutting a coupled pair in half is how independence becomes fictional.

`(basis: the low-coupling / high-cohesion boundary is the coupling-and-cohesion principle of structured design (Constantine & Yourdon) and information-hiding (Parnas — modules encapsulate what changes together); within praxis it is the unit-level application of plan's seam-along-change-boundaries rule, which places design seams where change and ownership diverge. The reason-to-change discriminator is the operative test, mirroring develop's dry-vs-incidental-duplication.)`

## When a plan already drew the seams

Under `--from-plan`, the plan has already carved the design along its chosen boundaries; those are natural seams by construction and you **adopt them** rather than re-cutting ([carve-into-units](../phases/02-carve-into-units.md)). This rule then governs only the cadence-driven re-cuts in [size-and-sequence](../phases/03-size-and-sequence.md) — a split runs *along* the plan's seams, refining grain, never across them into a fresh design boundary.

## Anchors

- *Good (natural seam):* split a checkout feature at the payment-gateway interface — the cart logic and the gateway integration change for different reasons and already talk through one contract; each is a unit.
- *Bad (cut through a coupling):* split "parse the file and validate its records" into "parse" and "validate" when the validator needs the parser's in-memory shape and every format change touches both — two units that can never be worked apart; keep them one.
