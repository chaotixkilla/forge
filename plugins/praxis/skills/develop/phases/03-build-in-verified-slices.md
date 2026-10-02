# Build in verified slices

Build one independently-runnable unit at a time and prove it green on the loop from phase 2 before starting the next, rather than writing the whole change and running it once at the end. Slicing is what keeps a failure attributable — when a slice goes red, the cause is in the handful of lines you just wrote, not somewhere in a thousand-line diff — and it is what lets `--until` and `--checkpoint-commit` mark real progress.

## Take the slices in order

Build in the order phase 1 carried forward. When you set the order yourself (a spec-driven or direct build, where a plan didn't fix it), order by **hard dependency first, then risk** — a slice that others need comes before them; among independent slices, pull the riskiest or most uncertain earlier so it fails while the change is small. The first slice should reach a running, green state as thin as possible (even a walking skeleton wired end-to-end).

## Write each slice applying the engineering craft

The engineering standards are the in-the-moment judgments woven into writing — an open library. What follows is a **routing table, not a checklist**: each entry leads with the situation that puts it in play, so you can decide from this page alone which two or three a slice needs, and open only those. A slice that triggers none needs none — that is a valid outcome, not a skipped step.

**Before you write it**
- A helper for this may already exist → [reuse-before-writing](../../../craft/engineering/reuse-before-writing.md) (the first search happened in orient)
- A dependency almost does what you need and the last piece doesn't fit → [exhaust-the-documented-path](../../../craft/engineering/exhaust-the-documented-path.md)
- New code that more than one caller will want → [put-shared-code-at-the-right-home](../../../craft/engineering/put-shared-code-at-the-right-home.md)
- You're tempted to make it general "for later" → [avoid-premature-abstraction](../../../craft/engineering/avoid-premature-abstraction.md)
- The slice needs a shape to hold its data → [choosing-the-right-data-structure](../../../craft/engineering/choosing-the-right-data-structure.md)

**As the function takes shape**
- Nesting is past two levels, or an early return would flatten it → [guard-clauses-vs-nesting](../../../craft/engineering/guard-clauses-vs-nesting.md)
- It's doing two things, or you're about to write a "// now do X" comment mid-body → [when-to-extract-a-function](../../../craft/engineering/when-to-extract-a-function.md), [keep-functions-cohesive](../../../craft/engineering/keep-functions-cohesive.md)
- High-level orchestration and low-level detail sit side by side in one body → [one-level-of-abstraction-per-function](../../../craft/engineering/one-level-of-abstraction-per-function.md)
- Branches are multiplying, or you keep extending a switch → [reduce-branching-complexity](../../../craft/engineering/reduce-branching-complexity.md)
- It reaches outside itself — ambient state, a mutable field, a global → [keep-functions-pure](../../../craft/engineering/keep-functions-pure.md), [minimize-state-scope](../../../craft/engineering/minimize-state-scope.md)

**When you name something**
- Any new name → [name-for-the-reader](../../../craft/engineering/name-for-the-reader.md)
- A value whose unit or nullability a wrong guess would act on → [naming-variables](../../../craft/engineering/naming-variables.md)
- A function, or a boolean-returning predicate → [naming-functions](../../../craft/engineering/naming-functions.md)
- The surrounding code already has a word for this thing → [one-name-per-concept](../../../craft/engineering/one-name-per-concept.md)
- The obvious name would overstate or misdescribe what it does → [avoid-misleading-names](../../../craft/engineering/avoid-misleading-names.md)

**When you add an abstraction or a type**
- A new interface, base class, or layer → [right-altitude-abstraction](../../../craft/engineering/right-altitude-abstraction.md), [shallow-interface-deep-module](../../../craft/engineering/shallow-interface-deep-module.md)
- You're reaching for inheritance → [prefer-composition-over-inheritance](../../../craft/engineering/prefer-composition-over-inheritance.md)
- The type could make the invalid state unrepresentable → [model-with-the-type-system](../../../craft/engineering/model-with-the-type-system.md)
- A value can be absent, empty, or not-yet-loaded → [null-and-empty-handling](../../../craft/engineering/null-and-empty-handling.md)
- Untrusted or loosely-typed input crosses into the slice → [parse-dont-validate](../../../craft/engineering/parse-dont-validate.md)
- State two callers could mutate → [immutable-by-default](../../../craft/engineering/immutable-by-default.md)

**When the slice can fail**
- A call crosses a boundary — a service, a store, the filesystem, user input → [handle-errors-at-the-boundary](../../../craft/engineering/handle-errors-at-the-boundary.md), [choose-an-error-strategy](../../../craft/engineering/choose-an-error-strategy.md)
- You're relying on an invariant you believe cannot break → [fail-loud-in-dev](../../../craft/engineering/fail-loud-in-dev.md)
- The failure could be made impossible instead of handled → [define-errors-out-of-existence](../../../craft/engineering/define-errors-out-of-existence.md)

**Before you call the slice green**
- The diff grew past what the task needed → [keep-the-diff-focused](../../../craft/engineering/keep-the-diff-focused.md)
- You improved something while passing through → [leave-the-campsite-cleaner](../../../craft/engineering/leave-the-campsite-cleaner.md), [separate-refactor-from-behavior-change](../../../craft/engineering/separate-refactor-from-behavior-change.md)
- You felt the pull to explain a line → [comment-the-why-not-the-what](../../../craft/engineering/comment-the-why-not-the-what.md), [keep-comments-truthful](../../../craft/engineering/keep-comments-truthful.md)
- The slice adds or changes something a caller outside this module uses → [document-the-public-contract](../../../craft/engineering/document-the-public-contract.md)
- It does something an operator would need to see from outside → [logging-what-matters](../../../craft/engineering/logging-what-matters.md)
- Landing it switched on is risky → [feature-flagging-risky-changes](../../../craft/engineering/feature-flagging-risky-changes.md)
- You're polishing before it works → [make-it-work-then-make-it-right](../rules/verification/make-it-work-then-make-it-right.md)
- The same shape now appears a third time → [dry-vs-incidental-duplication](../../../craft/engineering/dry-vs-incidental-duplication.md)

## Prove each slice green before the next

A slice is not done when it compiles or when you believe it works — it is done when it is a **verified slice** per [verified-slice](../rules/verified-slice.md), which defines "green", the baseline it is measured against, and when a **red slice** you cannot get green is yours to fix or `debug`'s. Never build the next slice on an unverified one.

## Recruit the simplicity-hawk, checkpoint, and stop conditions

A slice can also surface a decision that is not yours to close alone — a substitute for behavior a dependency was meant to provide, or a footprint outgrowing the task. Apply the third branch of [decide-or-route](../rules/decide-or-route.md) as it arises, rather than banking it for the final report: its whole value is being asked before the next slice builds on the answer.

- **Challenge for accidental complexity.** On a non-trivial slice — one that introduces an abstraction, adds branching, or touches more than a localized one-spot edit — recruit the **simplicity-hawk critic** to attack what isn't pulling its weight — premature abstraction, speculative generality, a structure a simpler one would beat. Without fan-out, apply the lens yourself: before accepting a slice, ask what in it could be deleted or flattened. Fold surviving objections back in before the slice is called green.
- **Checkpoint at slice boundaries.** With `--checkpoint-commit`, record a commit at each verified-slice boundary — see [checkpoint-commit](../modules/checkpoint-commit.md) (which also carries the commit-granularity fork).
- **Honor `--until`.** After each verified slice, check the `--until` stop condition (see [until-checkpoint](../modules/until-checkpoint.md)); when it is met, stop here and report state rather than continuing to phase 4.

The output of this phase is a set of verified slices composing the change's behavior. Making that behavior *reachable in the running system* — wiring it to callers, config, and boundaries — is [integrate-and-wire-up](04-integrate-and-wire-up.md)'s work.
