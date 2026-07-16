# Carve into units

The candidate inventory is a pile of work; this phase turns it into *units* — pieces each cut so that it can be completed on its own, owns one coherent outcome, and shares as little as possible with its neighbors. Where you cut is the whole game: cut along a seam the system already has and each unit stays independent and reviewable; cut for a round number or an even count and you sever a tight coupling down the middle, so two "units" cannot move without each other and the independence was a fiction. This phase carves along the real seams, and it carves *differently* depending on whether an upstream plan already drew them.

## First: did a plan already draw the seams?

- **A plan drove ingest (`--from-plan`).** The plan already carved the design into buildable units along its chosen boundaries. **Adopt those boundaries as the unit boundaries** — do not re-carve. decompose's value here is not a second design carve (that is plan's job and re-doing it invites divergence from the approved design); it is rendering those units work-ready and re-sizing them to the team's cadence in phase 3. Carry the plan's units through as-is, each still a single outcome, and move on. The only re-cut you make is the cadence split/merge in phase 3, and it runs *along* these seams, never across them.
- **No plan — a spec or a framed request drove ingest.** There are no design seams yet at the unit grain, so carve them now, using the rest of this phase.

## Cut along the natural seams, not for a count

Cut where the work is *already* least coupled — at the boundaries the system hands you: a module edge, an interface, a data boundary, a point where ownership or reason-to-change already diverges. A cut along such a seam leaves each side able to be built and verified without the other; a cut placed to make the numbers come out even runs straight through a coupling and manufactures a dependency that need not exist ([cut-along-natural-seams](../rules/cut-along-natural-seams.md)). When you must introduce a boundary rather than find one, prefer the **thin vertical slice** — a path through every layer that produces one observable outcome — over a horizontal layer that is inert until later units land ([prefer-vertical-slices](../rules/prefer-vertical-slices.md), which also carries the vertical-vs-horizontal fork for the cases where an architectural enabler genuinely earns its own unit).

## One unit, one outcome

Each unit owns exactly **one coherent outcome** — one thing that becomes true when the unit is done. The operational test is the done-condition: if you cannot state what "done" means for the unit in a single sentence without an "and" that joins two independently-shippable results, it is two units, and you split it here ([one-unit-one-outcome](../rules/one-unit-one-outcome.md)). Conversely, a candidate whose outcome is not observable on its own — it only matters once another candidate lands — is not yet a unit either; note it as a merge candidate for phase 3, where sizing decides which unit absorbs it. Carving sets the *boundaries*; phase 3's sizing decides whether each carved unit is the right *grain*.

The output is the set of candidate units, each cut to a single outcome along a real seam — carried to [size-and-sequence](03-size-and-sequence.md), which right-sizes and orders them.
