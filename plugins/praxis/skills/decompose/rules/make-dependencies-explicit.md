# Make dependencies explicit

A decomposition carries its ordering information in two possible places: in the *position* of units in a list, or in *named links* between them. Position is lossy — it survives only as long as nobody reorders, drops, parallelizes, or pulls a single unit onto a board out of context, and all four of those happen the moment the units leave decompose. A prerequisite that lived only in "it was earlier in the list" is gone, and someone starts a unit whose foundation does not exist yet. This rule requires every cross-unit prerequisite to be a named link on the unit, not an implicit consequence of order. It is cited by [size-and-sequence](../phases/03-size-and-sequence.md), [make-units-actionable](../phases/04-make-units-actionable.md), and [check-coverage-and-handoff](../phases/05-check-coverage-and-handoff.md).

## The discriminator: could the ordering survive a reshuffle?

For each unit, ask what must already exist before it can start, and record each such prerequisite as an explicit link to the unit it depends on — "depends on: <unit>". The test for whether a link is required:

- **If the dependency is real** — the unit genuinely cannot be built or verified until another lands — it gets a named link, full stop. It does not matter that the units happen to be adjacent in the current order; adjacency is not a record.
- **If there is no dependency** — the two units can be built in either order — record *no* link, and do not let list-position imply one. A spurious ordering is as much a defect as a missing one: it serializes work that could run in parallel.
- **The tell:** imagine the units scattered onto a board with the order lost. Every prerequisite that still needs to hold must be readable from the unit itself. If losing the order loses the information, the link was missing.

These explicit links are what [check-coverage-and-handoff](../phases/05-check-coverage-and-handoff.md) checks for completeness and what [emit-tickets](../modules/emit-tickets.md) renders as tracker relations; a dependency never written down cannot be carried into either.

`(basis: house craft rule — an explicit dependency graph over units is the standard precondition for topological sequencing ([order-by-dependency-then-risk](order-by-dependency-then-risk.md)) and survives the reorder/drop/parallelize operations that positional ordering does not. No single external authority; the reason-it-holds is the test above.)`

## Anchors

- *Good:* "unit: send share-notification email — depends on: create-share-record (needs the share id)" — the prerequisite is on the unit, so it holds even if the two are worked by different people out of order.
- *Bad:* two units listed as #3 "create share record" and #4 "send notification" with no link between them — reorder the board and #4 looks ready when it is not; the dependency lived only in the numbers.
