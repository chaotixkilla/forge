## Let the risk tier choose the action

The tier from [grade-the-upgrade](02-grade-the-upgrade.md) forces the shape of the change — a **rule**, not a judgment ([change-risk-scale](../../../craft/engineering/change-risk-scale.md)):

- **contained** → bump it directly.
- **bounded** → a bump whose consumers need *no* code adaptation, where the only edit is the manifest and lockfile line, is already atomic: the bump itself *is* the same-diff update and needs no runtime guard. One whose call sites must adapt updates every call site in that same diff when they're all enumerable and under your control, or stages the new path behind a guard otherwise (a guard installed here owes its removal, [retire-the-switches](../../../craft/engineering/retire-the-switches.md)).
- **exposed** → require a migration path: take the breaking change deliberately, with the transition [preserve-the-contract](../../../craft/engineering/preserve-the-contract.md) prescribes. A bump that moves a separately-deploying co-importer with no in-scope way to migrate it is blocked and reported, not forced.

If the tier demands a guard or migration path the codebase gives you no way to build, stop and report (outcome *blocked-and-reported*) rather than downgrading the change to a direct bump it isn't safe for.

## Bump to the project's posture

Apply [dependency-upgrade-posture](../rules/dependency-upgrade-posture.md): commit the lockfile, keep the manifest's pin-or-float form as the project keeps it, and take the increment its cadence allows — a major manually and in sequence, one major at a time, never a blind jump across several.

## Fix what breaks, at its cause

Follow the migration steps phase 01 read, and adapt each call site the new version breaks:

- **[fix-the-cause-not-the-symptom](../../../craft/evidence/fix-the-cause-not-the-symptom.md)** — adapt the call site to the new API properly; a shim that hides the break is only ever a knowingly-labeled, tracked stopgap.
- **[exhaust-the-documented-path](../../../craft/engineering/exhaust-the-documented-path.md)** — when the new version no longer fits how the code uses it, exhaust its documented path — the migration guide, the API's intended use — before building around it.
- **[smallest-reversible-change](../../../craft/engineering/smallest-reversible-change.md)** — the smallest adaptation that fully solves the break, measured by reach, not line count.
- **[match-the-surrounding-code](../../../craft/engineering/match-the-surrounding-code.md)** — conform to the local conventions; leave no stylistic seam.
- **[preserve-the-contract](../../../craft/engineering/preserve-the-contract.md)** — never change a flagged contract surface incidentally.
- **[leave-the-campsite-cleaner](../../../craft/engineering/leave-the-campsite-cleaner.md)** — fold in only improvements that pass its line; surface the rest as follow-ups.
- **[distrust-untyped-input-and-secrets](../../../craft/engineering/distrust-untyped-input-and-secrets.md)** — new code from the dependency crosses your trust boundary; apply the always-on security hygiene at every boundary the bump reaches.

## Recruit the change critics

Stress the change before verifying it: recruit the [adversary](../../../agents/critics/adversary.md) critic to attack it ("assume this is wrong; construct the input or state that breaks it") and the [simplicity-hawk](../../../agents/critics/simplicity-hawk.md) critic to challenge whether each adaptation is the smallest that solves its break. Fold their surviving findings back in. **Without fan-out**, apply both lenses yourself in sequence before moving on.

## `--checkpoint-commit`

With `--checkpoint-commit`, commit locally at each green step: see [modules/checkpoint-commit.md](../modules/checkpoint-commit.md).

## `--dry-run`

Under `--dry-run`, **stop here without mutating**: report the plan — the versions, consumers, upgrade path and baseline from [phase 01](01-read-the-upgrade-path.md), the risk tier and reach from [phase 02](02-grade-the-upgrade.md), and the intended bump and adaptations — and write nothing.
