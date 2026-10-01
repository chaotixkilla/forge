# develop — usage

Implement a change to a finished, integrated standard: orient in the existing code, stand up the tightest per-slice verify loop, build the change in verified slices while applying the engineering craft, wire it into the running system, check your own diff against the task, and land the working tree to a clean, committable local state — ready to hand off to review and land.

## When to use
- You have a plan or a spec (or a clear, decomposed task) and it is time to write the code — not to design it, decide requirements, or break it into units.
- You want the change built *coherently with the existing system*: matching local conventions, reusing what already exists, kept to a focused diff, with errors handled deliberately at the right boundary.
- You want each slice proven green as you go — behavior observed to actually run, not merely compiling — rather than a big-bang change checked only at the end.
- You want to bias the whole build toward a concern (`--lens=performance`, `--lens=accessibility`, `--lens=security`) so it shapes choices throughout, not just at review time.
- You want the branch left clean and hand-off ready: full local check green, no debris, tree committable — without opening a PR or shipping.

## Not for / use instead
- **Designing the approach, choosing interfaces, or planning rollout** → **plan** (develop consumes a plan; it does not produce one). Turning a fuzzy request into requirements → **spec**.
- **Breaking a design into independently shippable units** → **decompose** (develop builds the units; it does not carve them).
- **Comprehensive test coverage — designing the cases that discriminate, edges, failure paths** → **test**. develop stands up the *tightest verify loop per slice* to prove its own work green; it does not author the change's full test suite. A slice that needs real coverage hands the coverage design to **test**.
- **A second pair of eyes on a finished change** → **review**. develop's phase-5 self-review is the author's *pre-hand-off* check of the change against its task, plus a future maintainer's read; it doesn't judge the change's correctness or craft the way review does. review is the independent reviewer that reads the change cold.
- **Getting the finished work reviewed, into the trunk and out the door** → the developing act in **work** opens the review request; **land** merges and **roll-out** ships, or the shipping act in **work** runs both. develop lands to a clean *local* state only.
- **Root-causing a defect that already bit** → **debug**. When a slice goes red and the cause is not obvious from the change in hand, develop hands off to debug rather than thrashing on the fix.

## Examples
`--from-plan=docs/plans/checkout.md` — consume the plan's buildable units and ordering as the build backbone (the preferred entry: a plan pre-decides slices and interfaces).
`--from-spec=docs/specs/checkout.md` — drive from a spec instead: derive the implementation order yourself and flag each design decision the spec left open as you reach it.
`--until=slice:2` — build through the second buildable unit, prove it green, then stop and report state instead of landing.
`--until=phase:3` — run orient → feedback-loop → build-in-slices, then stop; for staged, review-as-you-go work.
`--until=green` — stop at the first fully-green state (first passing full local check); `--until=red` — stop at the first failing slice, for hand-off to debug.
`--lens=performance` — bias every phase toward performance: locate hot paths in orient, add a benchmark to the loop, avoid the N+1 as you write, keep the lens's check part of "green."
`--checkpoint-commit` — record a local commit at each verified-slice boundary so progress is recoverable and history reads as the build's slices.

## Gotchas
- **develop needs no configuration of its own.** Building, running the local check, bringing the tree to a clean committable state, and **committing** are all ambient local git — no backend required, so it declares no `config_requires`.
- **develop lands locally; it never pushes, opens a PR, or ships.** A develop run ends with a clean, committable branch, not a PR URL.
- **"Done" is a defined bar, not a feeling.** develop lands only when the change meets the [definition of done](rules/definition-of-done.md) — complete, integrated/reachable, verified-green, coherent, landed-clean. A run that stops short of it reports as *checkpointed* (a deliberate `--until`) or *blocked* (a red slice), never as done.
- **The tightest loop first.** develop's leverage is the per-slice feedback loop (phase 2) — standing it up *before* building, so every slice is proven in seconds. Skipping it to "just write the code" is the anti-pattern the skill exists to prevent.
- **The engineering craft is applied, not recited.** praxis's engineering standards are the in-the-moment judgments woven into building, shared with plan, refactor and review; a phase cites the ones it uses. They are an open library, extended over time — not a closed checklist.
- **In a project set up for praxis, it changes code only inside an act.** Invoked on its own there, its edits are blocked until an act starts; the work skill routes the change to the act that runs it.
