Now the edit — but *how* it lands is not a free choice: the risk tier from [phase 02](02-understand-blast-radius.md) already decided whether this change may go in directly, must be staged behind a guard, or needs a migration path. This phase applies that decision and makes the smallest correct edit that fits the surrounding code. The discipline here is restraint: the tidiest possible rewrite is usually the wrong move in living code, and the boundary between an in-scope improvement and diff-bloating scope creep is a line this phase holds deliberately.

## Let the risk tier choose the action

The tier from phase 02 forces the shape of the change — this is a **rule**, not a judgment ([change-risk-scale](../rules/change-risk-scale.md)):

- **contained** → change it directly. The reach is local and reversible; a direct edit is correct.
- **bounded** → stage it behind a guard (a flag/toggle so the new path is off until proven), *or* — when the full consumer set is enumerable, movable under your control, and fits one atomic reviewable diff — update every consumer in that same diff. The atomic-vs-staged choice is the *mechanism*; either way it's a `bounded` change. Not a flag-day switch on consumers you can't flip back.
- **exposed** → require a migration path: change the contract deliberately with the transition [preserve-the-contract](../rules/preserve-the-contract.md) prescribes (expand–contract, deprecation window, or a same-diff update only when the consumer set is genuinely closed). Never an incidental break.

If the tier demands a guard or migration path the codebase gives you no way to build, that is a reason to stop and report (disposition *blocked-and-reported*), not to downgrade the change to a direct edit it isn't safe for. (A `bounded` change whose consumers need *no* code adaptation — a dependency-version bump graded `bounded`, where the only edit is the manifest/lockfile line — is already atomic: the bump itself *is* the same-diff update and needs no runtime guard, so it does not trip this stop.)

## Make the smallest correct edit

Within the forced action, write the edit to these rules, all cited where they bite:

- **[smallest-reversible-change](../rules/smallest-reversible-change.md)** — the smallest edit that *fully* solves the task, on the most reversible path; measure "small" by reach, not line count.
- **[match-the-surrounding-code](../rules/match-the-surrounding-code.md)** — conform to the local file/module conventions; leave no stylistic seam.
- **[fix-the-cause-not-the-symptom](../rules/fix-the-cause-not-the-symptom.md)** — fix at the origin; a symptom-level guard is only ever a knowingly-labeled, tracked stopgap, per that rule's discriminator.
- **[preserve-the-contract](../rules/preserve-the-contract.md)** — never change a flagged contract surface incidentally.
- **[leave-the-campsite-cleaner](../rules/leave-the-campsite-cleaner.md)** — fold in only improvements that pass its line; surface the rest as follow-ups rather than making them silently. A needed change outside the [phase 01](01-locate-and-reproduce.md) working set is always a follow-up, never a silent extra.
- **[distrust-untyped-input-and-secrets](../rules/distrust-untyped-input-and-secrets.md)** — apply the always-on security hygiene to every boundary the edit touches.

## When the change is a dependency upgrade

A dependency upgrade is a change like any other — graded by [phase 02](02-understand-blast-radius.md) (a patch is usually `contained`, a breaking major is `exposed`) — but it carries its own posture: how tightly to constrain the version and how aggressively to move it. Apply [dependency-upgrade-posture](../rules/dependency-upgrade-posture.md), which encodes the pin-vs-float fork, its routing, and the upgrade cadence.

## Recruit the change critics

Stress the edit before verifying it: recruit the [adversary](../../../agents/critics/adversary.md) critic to attack it ("assume this is wrong; construct the input or state that breaks it") and the [simplicity-hawk](../../../agents/critics/simplicity-hawk.md) critic to challenge whether it's the smallest change that solves the task. Fold their surviving findings back into the edit. **Without fan-out**, apply both lenses yourself in sequence before moving on: try to construct a failing input, and ask what could be cut without losing the fix.

## `--checkpoint-commit`

If `--checkpoint-commit` is set, commit at safe, self-contained milestones as the change is built — a **local commit** (ambient plain git, no configured backend), honoring the project's message convention — so progress is recoverable and the change reads as a reviewable sequence. This selects a finer commit *cadence*; the final attributable commit is still written in [review-and-record](05-review-and-record.md). Never push unless asked.

## `--dry-run`

Under `--dry-run`, **stop here without mutating**: report the plan — the located target and baseline from [phase 01](01-locate-and-reproduce.md), the risk tier and reach from [phase 02](02-understand-blast-radius.md), and the intended edit and the action the tier forces — and do not write. The preview is the deliverable; phases 04–05 do not run.
