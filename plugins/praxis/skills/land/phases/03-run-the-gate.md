The gate runs against the reconciled base from [prepare-the-increment](02-prepare-the-increment.md), and nothing lands until it passes.

## Run the checks on the reconciled base

- **Read the landing constraint first.** Read the target's landing constraint through [vcs](../../vcs/SKILL.md)'s *read a landing constraint* before running anything: it names the checks this gate requires ([green-before-land](../rules/green-before-land.md)), and [merge](04-merge.md) reuses it. If it can't be read, every check is required, and merge degrades as it states.
- **Local checks are ambient; the hosted pipeline is delegated.** Run the build, tests, and lint the repo defines (ambient — any skill runs these locally). For the hosted pipeline, the reconciled change must be on the remote first: push the branch through [vcs](../../vcs/SKILL.md)'s *push a branch* — the push the merge needs anyway — then run [ci](../../ci/SKILL.md)'s *run the checks* for that ref, and await the run its reference names for the aggregate pass/fail verdict. A purely local target has no hosted pipeline; the local checks are the gate. `(basis: derived from a hosted check seeing only what is pushed)` If the push fails, never run ci against a ref it didn't update: **unavailable** → the hosted pipeline is not consulted and the local checks are the gate, as in the degrade below; **retryable** → retry once, then as unavailable; **refused** for a needed reconcile → the target moved, so re-reconcile and push again; **not-found**, **permanent**, or any other refusal → the gate is not green and the run stops on failure, naming the push.
- **Scope a hotfix's gate, never below the required checks.** For a **hotfix** ([assess-the-change](01-assess-the-change.md)'s landing type), run the required checks plus those the change affects, skipping the rest for speed — unless `--gate` forces the gate in full. Every other landing type runs the full gate.
- **Gate the merged result, not the branch.** The checks must run on the post-reconcile tree ([integrate-against-current-target](../rules/integrate-against-current-target.md)); if the target moved since the reconcile, re-reconcile and re-run before proceeding.

## Require green — the hard stop

The change proceeds only when every required check — required by the test in [green-before-land](../rules/green-before-land.md) — has concluded a **pass**: a failure, a still-running check, a skipped/disabled required check, a soft-pass, or a hand-overridden red each **blocks**. This is not tunable by the caller. On a failure, fetch the failing run's logs (via the [ci](../../ci/SKILL.md) capability's *fetch a run's logs*) so the report names *what* failed, not just that it did.

## The two gate-related flags — how they compose

The two act at distinct points and do not overlap. `(basis: derived from where each flag acts in the run)`

- **`--gate`** ([require-explicit-gate](../modules/require-explicit-gate.md)) acts **here, pre-merge**: it forces the gate to run in full and hard-block even where the flow would narrow or soft-pass it (e.g. a scoped hotfix gate). It changes *whether the gate may be lenient*, never what a pass is.
- **`--on-fail`** ([failure-policy](../modules/failure-policy.md)) is the **policy at a failure**, spanning this gate and the landing in [merge](04-merge.md): abort / ask / rollback / continue. But `continue` can **never** carry a failed *required* gate past the green-before-land stop — it applies only to advisory, non-required checks.

## Degrade when the pipeline backend is absent

The hosted pipeline goes through the [ci](../../ci/SKILL.md) capability (which owns `tools.ci` — doer-owns-prerequisites; land declares none). If it reports the backend unavailable, **degrade**: run the local build/tests/lint as the gate and report plainly that the *hosted* pipeline was not consulted, so the caller knows the gate was narrower than a fully-configured run (the `ci` skill owns guiding the user through `init:ci`). Do not treat an unavailable pipeline as a pass: an absent gate is not a green one. The ci port's other answers map too: no run found for the ref → trigger one; a retryable failure → retry once, and if it recurs the gate is not green; a run still unsettled when the await ends → not green, reported as unsettled; a permanent failure (the request invalid as asked) → not green, the run stops on failure naming the request. `(basis: per-capability degrade; mirrors review's vcs degrade)`

## Close the phase

The gate is passed only when the acceptance test in [green-before-land](../rules/green-before-land.md) is met on the reconciled base. Under `--dry-run`, report the checks that *would* run and the ref they'd run against, without triggering them. On a pass, hand to [merge](04-merge.md); on a block, apply the `--on-fail` policy (default: stop and report what failed, with the log evidence).
