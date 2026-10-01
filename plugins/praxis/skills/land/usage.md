# land — usage

Take a finished change and get it into its integration target: stage coherent commits, reconcile with the target's live head, pass the pre-merge gate, and merge. The target defaults to the trunk but can be an epic or `develop` branch (`--into`). land merges and stops; rolling the merged change out to an environment is **roll-out**'s.

## When to use
- A change is finished and, where the team requires it, its review request is approved, and you want it committed, reconciled, gated and merged in one honest pass.
- You want the landing to follow how this team works — its branch model and merge style — instead of a generic ritual.
- You want the gate enforced honestly: the change reconciled against the *current* target before it's checked, and a red or skipped check treated as a stop.

## Not for / use instead
- Building the change → **develop**. land lands finished work; it doesn't build.
- Judging whether the change is correct → **review**. land requires a green gate; it doesn't review the code.
- Opening the review request for a change → the developing or fixing-a-bug act in **work**, which writes the description from the task's documentation. land merges a request once it's approved; it doesn't open one.
- Shipping the merged change to an environment → **roll-out**.
- Carrying a change from finished to merged to rolled out, with the outcome reported to its owners → the shipping act in **work**.

## Examples
`land` — assess, stage coherent commits, reconcile with the target, run the gate, and merge.
`--into=epic-checkout` — land into the `epic-checkout` branch instead of the trunk; the reconcile and gate run against that branch.
`--commit` — stop after recording coherent local commits: nothing is pushed, gated or merged.
`--message="fix: guard against empty batch"` — use this text as the commit message verbatim.
`--gate` — force the full gate and block on anything short of green, even where the flow would narrow it.
`--on-fail=rollback` — if the landing fails after the merge, revert the merge instead of stopping and reporting.
`--dry-run` — report the commits, reconcile, gate and merge that would happen, without doing any of them.

## Gotchas
- **land needs no configuration of its own.** Hosted version control goes through `vcs`, which owns `tools.vcs`, and the hosted pipeline through `ci`, which owns `tools.ci`. With no `tools.ci`, the gate falls back to the local build and checks and the result says the hosted pipeline wasn't consulted; with no `tools.vcs` and a remote, land stops at local commits, because it can't read whether the target needs a review.
- **It lands finished work; it doesn't decide the work is good.** Run **review** first. land enforces that the gate is green, not that the diff is right.
- **A target that needs review is never merged around.** Where the target requires an approved review request and the change has none, land stops at *awaiting-review*. It never opens the request itself and never pushes past the protection.
- **Merge style and branch model follow the team; the commit-message format defaults to the house baseline.** Where recent history *consistently* uses another message convention, land asks which to use and remembers the answer, rather than silently adopting the history's shape.
- **Green is a hard stop.** A failing or skipped required check blocks the merge. `--on-fail` changes what happens after a failure, never whether a red gate blocks.
- **In a project set up for praxis, it commits only inside an act.** Invoked on its own there, its commits are blocked until an act starts; the shipping act in **work** runs it.
