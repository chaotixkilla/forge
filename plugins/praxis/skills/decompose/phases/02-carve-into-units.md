# Carve into units

Turn the candidate inventory into *units*: each completable on its own, owning one coherent outcome, and sharing as little as possible with its neighbors.

## First: did a plan already draw the seams?

- **A plan drove ingest (`--from-plan`).** The plan already carved the design into buildable units along its chosen boundaries. **Adopt those boundaries as the unit boundaries** — do not re-carve: that is plan's job, and re-doing it invites divergence from the approved design. Carry the plan's units through as-is, each still a single outcome. The only re-cut you make is the cadence split/merge in phase 3, and it runs *along* these seams, never across them.
- **No plan — a spec or a framed request drove ingest.** There are no design seams yet at the unit grain, so carve them now, using the rest of this phase.

## Cut along the natural seams, not for a count

Cut where the work is *already* least coupled — at the boundaries the system hands you: a module edge, an interface, a data boundary, a point where ownership or reason-to-change already diverges — never to make the count come out even ([cut-along-natural-seams](../rules/cut-along-natural-seams.md)). When you must introduce a boundary rather than find one, prefer the **thin vertical slice** — a path through every layer that produces one observable outcome — over a horizontal layer that is inert until later units land ([prefer-vertical-slices](../rules/prefer-vertical-slices.md), which also carries the vertical-vs-horizontal fork for the cases where an architectural enabler genuinely earns its own unit).

## One unit, one outcome

Each unit owns exactly **one coherent outcome**. The operational test is the done-condition: if you cannot state what "done" means for the unit in a single sentence without an "and" that joins two independently-shippable results, it is two units, and you split it here ([one-unit-one-outcome](../rules/one-unit-one-outcome.md)). Conversely, a candidate whose outcome is not observable on its own — it only matters once another candidate lands — is not yet a unit either; note it as a merge candidate for phase 3, where sizing decides which unit absorbs it.

The output is the set of candidate units, each cut to a single outcome along a real seam — carried to [size-and-sequence](03-size-and-sequence.md), which right-sizes and orders them.
