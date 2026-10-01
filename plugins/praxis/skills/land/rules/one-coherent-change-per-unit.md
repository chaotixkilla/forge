# One coherent change per unit

A commit or PR that bundles two unrelated concerns is a unit you can neither cleanly review, cleanly revert, nor cleanly bisect. When the bugfix and the refactor ride in one commit and the bugfix later proves wrong, reverting drags the refactor out with it; when a history-bisection lands on that commit it points at a +800/−300 blob instead of the one line that broke. `(basis: practitioner bisect accounts from the squash-vs-per-commit debate; DORA; derived from review's separate-correctness-from-taste discipline)`

## The discriminator — is this one concern?

A unit (a commit, or a PR) is coherent when it passes all three tests; if it fails one, split it:

- **Revert-independence** — could this unit be reverted on its own without dragging out an unrelated change, and without leaving a half-change behind? If undoing it forces you to also undo something unrelated, two concerns are fused.
- **One-pass review** — can a reviewer hold the whole unit's intent in one pass and judge it against one question? A unit that makes the reviewer context-switch between "is this refactor safe?" and "is this new behavior correct?" is two units.
- **No refactor-plus-behavior mixing** — does the unit change behavior *and* restructure code in the same breath? Separate them: a pure refactor (no behavior change) lands as its own unit so that a behavior regression is never hidden inside a diff the reviewer read as "just moving code."

The tell across all three: **the diff should have one reason to exist.** If the honest description needs an "and" joining two outcomes ("fix the guard *and* rename the module"), it is two units.

## Splitting is not always land's call

Where the working tree already bundles concerns, land splits it into coherent commits during [prepare-the-increment](../phases/02-prepare-the-increment.md) when the split is mechanical (unrelated files, separable hunks). Where the concerns are genuinely entangled in the same lines — a split would require rewriting the change — that is a signal the *work* was not done as coherent units, and land surfaces it rather than silently landing a tangled unit or fabricating a split that misrepresents what happened. Landing finished work does not include re-authoring it.
