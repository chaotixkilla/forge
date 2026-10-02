## Let the risk tier choose the action

The tier from [phase 02](02-map-the-blast-radius.md) forces the shape of the change — this is a **rule**, not a judgment ([change-risk-scale](../../../craft/engineering/change-risk-scale.md)):

- **contained** → change it directly.
- **bounded** → stage it behind a guard (a flag/toggle so the new path is off until proven; a guard installed here owes its removal, [retire-the-switches](../../../craft/engineering/retire-the-switches.md)), *or* — when the full consumer set is enumerable, movable under your control, and fits one atomic reviewable diff — update every consumer in that same diff. The atomic-vs-staged choice is the *mechanism*; either way it's a `bounded` change. Not a flag-day switch on consumers you can't flip back.
- **exposed** → require a migration path: change the contract deliberately with the transition [preserve-the-contract](../../../craft/engineering/preserve-the-contract.md) prescribes (expand–contract, deprecation window, or a same-diff update only when the consumer set is genuinely closed). Never an incidental break.

If the tier demands a guard or migration path the codebase gives you no way to build, that is a reason to stop and report (disposition *blocked-and-reported*), not to downgrade the change to a direct edit it isn't safe for.

## Make the smallest correct edit

Make the edit as a sequence of named moves from [refactoring-catalogue](../../../craft/engineering/refactoring-catalogue.md) — each move's condition checked, the checks green before and after it — never as one edit checked at the end; a move that turns the checks red is handled by that standard's fork. Within the forced action, write each move to these rules, all cited where they bite:

- **[smallest-reversible-change](../../../craft/engineering/smallest-reversible-change.md)** — the smallest edit that *fully* solves the task, on the most reversible path; measure "small" by reach, not line count.
- **[match-the-surrounding-code](../../../craft/engineering/match-the-surrounding-code.md)** — conform to the local file/module conventions; leave no stylistic seam.
- **[preserve-the-contract](../../../craft/engineering/preserve-the-contract.md)** — never change a flagged contract surface incidentally.
- **[leave-the-campsite-cleaner](../../../craft/engineering/leave-the-campsite-cleaner.md)** — fold in only improvements that pass its line; surface the rest as follow-ups rather than making them silently. A needed change outside the [phase 01](01-locate-and-baseline.md) working set is always a follow-up, never a silent extra.
- **[distrust-untyped-input-and-secrets](../../../craft/engineering/distrust-untyped-input-and-secrets.md)** — apply the always-on security hygiene to every boundary the edit touches.
- **[separate-refactor-from-behavior-change](../../../craft/engineering/separate-refactor-from-behavior-change.md)** — the restructuring changes no behavior; a behavior change it turns out to need is its own change, never folded in.

The shape the restructuring moves the code toward is the one the engineering standards describe, so judge the target against the ones the refactor's purpose names: functions ([keep-functions-cohesive](../../../craft/engineering/keep-functions-cohesive.md), [when-to-extract-a-function](../../../craft/engineering/when-to-extract-a-function.md), [one-level-of-abstraction-per-function](../../../craft/engineering/one-level-of-abstraction-per-function.md), [reduce-branching-complexity](../../../craft/engineering/reduce-branching-complexity.md), [keep-functions-pure](../../../craft/engineering/keep-functions-pure.md), [minimize-state-scope](../../../craft/engineering/minimize-state-scope.md)), names ([name-for-the-reader](../../../craft/engineering/name-for-the-reader.md), [naming-functions](../../../craft/engineering/naming-functions.md), [naming-variables](../../../craft/engineering/naming-variables.md), [one-name-per-concept](../../../craft/engineering/one-name-per-concept.md)), data ([choosing-the-right-data-structure](../../../craft/engineering/choosing-the-right-data-structure.md), [immutable-by-default](../../../craft/engineering/immutable-by-default.md), [model-with-the-type-system](../../../craft/engineering/model-with-the-type-system.md)), abstractions and boundaries ([right-altitude-abstraction](../../../craft/engineering/right-altitude-abstraction.md), [shallow-interface-deep-module](../../../craft/engineering/shallow-interface-deep-module.md), [prefer-composition-over-inheritance](../../../craft/engineering/prefer-composition-over-inheritance.md), [seam-along-change-boundaries](../../../craft/engineering/seam-along-change-boundaries.md)), and where code lives and how often it repeats ([put-shared-code-at-the-right-home](../../../craft/engineering/put-shared-code-at-the-right-home.md), [dry-vs-incidental-duplication](../../../craft/engineering/dry-vs-incidental-duplication.md)).

## Recruit the change critics

Stress the edit before verifying it: recruit the [adversary](../../../agents/critics/adversary.md) critic to attack it ("assume this is wrong; construct the input or state that breaks it") and the [simplicity-hawk](../../../agents/critics/simplicity-hawk.md) critic to challenge whether it's the smallest change that solves the task. Fold their surviving findings back into the edit. **Without fan-out**, apply both lenses yourself in sequence before moving on: try to construct a failing input, and ask what could be cut without losing the restructuring.

## `--checkpoint-commit`

With `--checkpoint-commit`, commit locally after each green move: see [modules/checkpoint-commit.md](../modules/checkpoint-commit.md).

## `--dry-run`

Under `--dry-run`, **stop here without mutating**: report the plan — the located target and baseline from [phase 01](01-locate-and-baseline.md), the risk tier and reach from [phase 02](02-map-the-blast-radius.md), and the intended edit and the action the tier forces — and do not write. The preview is the deliverable; phases 04–05 do not run.
