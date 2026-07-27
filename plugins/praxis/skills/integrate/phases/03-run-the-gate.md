The gate is the last check before the change becomes everyone's problem. It runs the pre-merge checks — build, tests, lint, and the hosted CI pipeline — against the reconciled base from [prepare-the-increment](02-prepare-the-increment.md), and requires they pass before anything lands. Its whole value is that a failure *stops* the change; a gate that runs but doesn't block is theater. This phase pins what runs, what "pass" means, and how the three gate-related flags compose.

## Run the checks on the reconciled base

- **Local checks are ambient; the hosted pipeline is delegated.** Run the build, tests, and lint the repo defines (ambient — any skill runs these locally). For the hosted pipeline, delegate to the [ci](../../ci/SKILL.md) capability's *run the checks* operation for the reconciled ref — trigger it, or read the run already triggered by the push, and take its aggregate pass/fail verdict.
- **Gate the merged result, not the branch.** The checks must run on the post-reconcile tree ([integrate-against-current-target](../rules/integrate-against-current-target.md)); if the target moved since the reconcile, re-reconcile and re-run before proceeding — a verdict against a stale base does not vet what will merge.

## Require green — the hard stop

The change proceeds only when every required check has concluded a **pass**, per [green-before-land](../rules/green-before-land.md): a failure, a still-running check, a skipped/disabled required check, a soft-pass, or a hand-overridden red each **blocks**. This is not tunable by the caller — it is the stop the gate exists to enforce. On a failure, fetch the failing run's logs (via the [ci](../../ci/SKILL.md) capability's *fetch a run's logs*) so the report names *what* failed, not just that it did.

## The three gate-related flags — how they compose

`(basis: this resolves the seed's open question on the --gate / --watch / --on-fail relationship — they touch the run lifecycle at three distinct points and do not overlap.)`

- **`--gate`** ([require-explicit-gate](../modules/require-explicit-gate.md)) acts **here, pre-merge**: it forces the gate to run in full and hard-block even where the flow would narrow or soft-pass it (e.g. a scoped hotfix gate). It changes *whether the gate may be lenient*, never what a pass is.
- **`--on-fail`** ([failure-policy](../modules/failure-policy.md)) is the **policy at a failure**, spanning this gate and the [ship-to-target](05-ship-to-target.md) rollout: abort / ask / rollback / continue. But `continue` can **never** carry a failed *required* gate past the green-before-land stop — it applies only to advisory, non-required checks.
- **`--watch`** ([watch-the-pipeline](../modules/watch-the-pipeline.md)) acts **post-land**, in [confirm-and-report](06-confirm-and-report.md): staying attached until the run and post-ship signals settle. It does not change the pre-merge gate.

## Degrade when the pipeline backend is absent

The hosted pipeline goes through the [ci](../../ci/SKILL.md) capability (which owns `tools.ci` — doer-owns-prerequisites; integrate declares none). If it reports the backend unavailable, **degrade**: run the local build/tests/lint as the gate and report plainly that the *hosted* pipeline was not consulted, so the caller knows the gate was narrower than a fully-configured run (the `ci` skill owns guiding the user through `init:ci`). Do not treat an unavailable pipeline as a pass — an absent gate is not a green one. `(basis: integrate's per-capability degrade — a missing pipeline narrows the gate to local checks, it never fabricates a pass; doer-owns-prerequisites, mirrors review's vcs degrade.)`

## Close the phase

The gate is passed only when the acceptance test in [green-before-land](../rules/green-before-land.md) is met on the reconciled base. Under `--dry-run`, report the checks that *would* run and the ref they'd run against, without triggering them. On a pass, hand to [land-it](04-land-it.md); on a block, apply the `--on-fail` policy (default: stop and report what failed, with the log evidence).
