# refactor — usage

Restructure existing code without changing what it does: locate the code and capture how it behaves now, grade the change by its reach and reversibility, make the smallest reversible edit, prove the behavior unchanged, and commit an attributable diff.

## When to use
- Code needs restructuring — an extraction, a rename, a split, removing duplication or dead code — and nothing it does for its callers may change.
- A feature switch has held one value for its whole exposure and its read and dead branch can go.
- You want the change sized to its blast radius: direct where nothing outside observes it, behind a guard or a migration path where something does.

## Not for / use instead
- Changing behavior, building something new, or changing a contract on purpose → **develop**.
- Moving a dependency to a new version → **upgrade**.
- Finding why something broke and fixing it → **debug**, or the fixing-a-bug act in **work**.
- Carrying a maintenance change through review, records and delivery → the maintaining act in **work**, which runs refactor as its change step.

## Examples
`refactor` — locate, baseline, grade, change, prove it unchanged, and commit.
`--scope='src/billing/**'` — keep every read, edit and check inside the billing tree; anything needed outside is a follow-up.
`--module=billing` — resolve the billing subsystem's boundary and owners, and return the owners with the change.
`--require-clean` — refuse to start on a dirty tree, so the diff is only this change.
`--dry-run` — report the target, baseline, risk tier and intended edit without changing anything.

## Gotchas
- **Behavior is the contract.** Proving it unchanged rests on the baseline captured before the edit. Code that can't be exercised at all gives no baseline, and the verdict is inconclusive, never verified.
- **Unknown reach grades high.** When the consumers can't be enumerated, the change grades `exposed` and needs a migration path, or it's blocked and reported.
- **It commits locally and stops.** refactor never pushes, opens a review request or records anything outside the repository.
- **In a project set up for praxis, it changes code only inside an act.** Invoked on its own there, its edits are blocked until an act starts; the work skill routes the change to the act that runs it.
