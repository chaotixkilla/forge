# Build in verified slices

This is where the change is written. The discipline is one word: *slices*. Build one independently-runnable unit at a time and prove it green on the loop from phase 2 before starting the next, rather than writing the whole change and running it once at the end. Slicing is what keeps a failure attributable — when a slice goes red, the cause is in the handful of lines you just wrote, not somewhere in a thousand-line diff — and it is what lets `--until` and `--checkpoint-commit` mark real progress. The craft-library is applied *here*, in the moment of writing each slice, not bolted on after.

## Take the slices in order

Build in the order phase 1 carried forward. When you set the order yourself (a spec-driven or direct build, where a plan didn't fix it), order by **hard dependency first, then risk** — a slice that others need comes before them; among independent slices, pull the riskiest or most uncertain earlier so it fails while the change is small. The first slice should reach a running, green state as thin as possible (even a walking skeleton wired end-to-end): a green baseline you extend beats a large first slice that can't run.

## Write each slice applying the craft-library

The rules under `rules/` are the in-the-moment judgments woven into writing — an open, seeded library of 44 across 10 families. What follows is a **routing table, not a checklist**: each entry leads with the situation that puts it in play, so you can decide from this page alone which two or three a slice needs, and open only those. Most slices trigger a handful. A slice that triggers none needs none — that is a valid outcome, not a skipped step.

**Before you write it**
- A helper for this may already exist → [reuse-before-writing](../rules/reuse/reuse-before-writing.md) (the first search happened in orient)
- A dependency almost does what you need and the last piece doesn't fit → [exhaust-the-documented-path](../rules/reuse/exhaust-the-documented-path.md)
- New code that more than one caller will want → [put-shared-code-at-the-right-home](../rules/reuse/put-shared-code-at-the-right-home.md)
- You're tempted to make it general "for later" → [avoid-premature-abstraction](../rules/abstraction/avoid-premature-abstraction.md)
- The slice needs a shape to hold its data → [choosing-the-right-data-structure](../rules/data-and-types/choosing-the-right-data-structure.md)

**As the function takes shape**
- Nesting is past two levels, or an early return would flatten it → [guard-clauses-vs-nesting](../rules/functions/guard-clauses-vs-nesting.md)
- It's doing two things, or you're about to write a "// now do X" comment mid-body → [when-to-extract-a-function](../rules/functions/when-to-extract-a-function.md), [keep-functions-cohesive](../rules/functions/keep-functions-cohesive.md)
- High-level orchestration and low-level detail sit side by side in one body → [one-level-of-abstraction-per-function](../rules/functions/one-level-of-abstraction-per-function.md)
- Branches are multiplying, or you keep extending a switch → [reduce-branching-complexity](../rules/functions/reduce-branching-complexity.md)
- It reaches outside itself — ambient state, a mutable field, a global → [keep-functions-pure](../rules/functions/keep-functions-pure.md), [minimize-state-scope](../rules/functions/minimize-state-scope.md)

**When you name something**
- Any new name → [name-for-the-reader](../rules/naming/name-for-the-reader.md)
- A value whose unit or nullability a wrong guess would act on → [naming-variables](../rules/naming/naming-variables.md)
- A function, or a boolean-returning predicate → [naming-functions](../rules/naming/naming-functions.md)
- The surrounding code already has a word for this thing → [one-name-per-concept](../rules/naming/one-name-per-concept.md)
- The obvious name would overstate or misdescribe what it does → [avoid-misleading-names](../rules/naming/avoid-misleading-names.md)

**When you add an abstraction or a type**
- A new interface, base class, or layer → [right-altitude-abstraction](../rules/abstraction/right-altitude-abstraction.md), [shallow-interface-deep-module](../rules/abstraction/shallow-interface-deep-module.md)
- You're reaching for inheritance → [prefer-composition-over-inheritance](../rules/abstraction/prefer-composition-over-inheritance.md)
- The type could make the invalid state unrepresentable → [model-with-the-type-system](../rules/data-and-types/model-with-the-type-system.md)
- A value can be absent, empty, or not-yet-loaded → [null-and-empty-handling](../rules/data-and-types/null-and-empty-handling.md)
- Untrusted or loosely-typed input crosses into the slice → [parse-dont-validate](../rules/data-and-types/parse-dont-validate.md)
- State two callers could mutate → [immutable-by-default](../rules/data-and-types/immutable-by-default.md)

**When the slice can fail**
- A call crosses a boundary — a service, a store, the filesystem, user input → [handle-errors-at-the-boundary](../rules/errors/handle-errors-at-the-boundary.md), [choose-an-error-strategy](../rules/errors/choose-an-error-strategy.md)
- You're relying on an invariant you believe cannot break → [fail-loud-in-dev](../rules/errors/fail-loud-in-dev.md)
- The failure could be made impossible instead of handled → [define-errors-out-of-existence](../rules/errors/define-errors-out-of-existence.md)

**Before you call the slice green**
- The diff grew past what the task needed → [keep-the-diff-focused](../rules/change-hygiene/keep-the-diff-focused.md)
- You improved something while passing through → [boy-scout-rule-bounded](../rules/change-hygiene/boy-scout-rule-bounded.md), [separate-refactor-from-behavior-change](../rules/change-hygiene/separate-refactor-from-behavior-change.md)
- You felt the pull to explain a line → [comment-the-why-not-the-what](../rules/comments/comment-the-why-not-the-what.md), [keep-comments-truthful](../rules/comments/keep-comments-truthful.md)
- The slice adds or changes something a caller outside this module uses → [document-the-public-contract](../rules/comments/document-the-public-contract.md)
- It does something an operator would need to see from outside → [logging-what-matters](../rules/verification/logging-what-matters.md)
- Landing it switched on is risky → [feature-flagging-risky-changes](../rules/risk/feature-flagging-risky-changes.md)
- You're polishing before it works → [make-it-work-then-make-it-right](../rules/verification/make-it-work-then-make-it-right.md)
- The same shape now appears a third time → [dry-vs-incidental-duplication](../rules/reuse/dry-vs-incidental-duplication.md)

Reach for a rule when its situation appears; the point is that the judgment is made *deliberately and consistently*, not from private taste.

## Prove each slice green before the next

A slice is not done when it compiles or when you believe it works — it is done when it is a **verified slice** per [verified-slice](../rules/verified-slice.md): its behavior was exercised on the loop and the loop passed, *and* nothing in the baseline-green set regressed. "Green" (and the baseline it's measured against) is defined there; hold to it. A slice you cannot get green is a **red slice**, and the hand-off test is *where the fault lives*, not how long you've tried: if the cause is in the lines this slice changed, fix it and re-verify; if it isn't localizable to this slice's own diff, stop and hand off to `debug` rather than thrashing (`--until=red` makes this an explicit stop). Never build the next slice on an unverified one; the whole point of slicing is lost the moment failures can accumulate across two.

## Recruit the simplicity-hawk, checkpoint, and stop conditions

A slice can also surface a decision that is not yours to close alone — a substitute for behavior a dependency was meant to provide, or a footprint outgrowing the task. Apply the third branch of the decide-or-route test ([orient-in-the-code](01-orient-in-the-code.md)) as it arises, rather than banking it for the final report: its whole value is being asked before the next slice builds on the answer.

- **Challenge for accidental complexity.** On a non-trivial slice — one that introduces an abstraction, adds branching, or touches more than a localized one-spot edit — recruit the **simplicity-hawk critic** to attack what isn't pulling its weight — premature abstraction, speculative generality, a structure a simpler one would beat. Without fan-out, apply the lens yourself: before accepting a slice, ask what in it could be deleted or flattened. Fold surviving objections back in before the slice is called green.
- **Checkpoint at slice boundaries.** With `--checkpoint-commit`, record a commit at each verified-slice boundary — see [checkpoint-commit](../modules/checkpoint-commit.md) (which also carries the commit-granularity fork). A verified slice is exactly the right commit boundary: recoverable progress, and history that reads as the build.
- **Honor `--until`.** After each verified slice, check the `--until` stop condition (see [until-checkpoint](../modules/until-checkpoint.md)); when it is met, stop here and report state rather than continuing to phase 4.

The output of this phase is a set of verified slices composing the change's behavior. Making that behavior *reachable in the running system* — wiring it to callers, config, and boundaries — is [integrate-and-wire-up](04-integrate-and-wire-up.md)'s work.
