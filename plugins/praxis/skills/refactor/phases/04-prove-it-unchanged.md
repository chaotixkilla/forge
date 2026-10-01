A refactor has no upstream spec: "correct" means the behavior captured in the *baseline from [phase 01](01-locate-and-baseline.md)* still holds, along with the existing checks.

## Prove the behavior is unchanged

Show there is no delta at all (**judgment**, anchored to the phase-01 baseline): the captured current behavior is bit-for-bit preserved, so the baseline outputs and tests still hold. A refactor fixed nothing, so it owes no new regression guard; its guarantee is that the existing checks still pass.

## Run the project's checks

Run the project's existing checks over the working set, and confirm the broader picture where continuous integration is available — delegate the run/build confirmation to the [ci](../../ci/SKILL.md) skill. Without that capability, run the checks locally as the fallback and note that the confirmation is local-only. Scope the run to the working set and its reverse-dependents (what the change can reach), not an arbitrary subset — a change verified only on the file it touched is unverified on the callers it broke.

A coverage gap the refactor merely reveals is surfaced as a routine hygiene note in [commit-and-hand-off](05-commit-and-hand-off.md), not filled here. Apply the always-on security hygiene as part of verification too ([distrust-untyped-input-and-secrets](../../../craft/engineering/distrust-untyped-input-and-secrets.md)): confirm the restructuring left no tainted-data path or exposed secret at the boundaries it touched.

## The verdict — a three-value partition

This phase resolves to exactly one verdict, and the set is exhaustive and mutually exclusive — walk it deliberately, because the third value is the one a two-value check drops:

- **verified** — the baseline still holds and the checks in scope pass. Proceeds to [commit-and-hand-off](05-commit-and-hand-off.md).
- **not-verified** — a check fails, or the baseline shows a delta. The change does not stand as-is; loop back to [make-the-change](03-make-the-change.md) to correct it, or stop and report if it can't be corrected in scope.
- **inconclusive** — the checks could not be run at all (no runnable suite, and the baseline can't be captured because the code can't be exercised at all — per [phase 01](01-locate-and-baseline.md)), or a delegated capability the verdict depends on was unavailable *with no local substitute* (ci down **and** no runnable local check). This is **not** a pass: report it distinctly so "we couldn't confirm" never reads as "verified", and carry it to [commit-and-hand-off](05-commit-and-hand-off.md) as a change that needs the missing confirmation before it's trusted.

The partition holds across the matrix: a run with no tests but a baseline captured by exercising the code can still reach *verified* on the baseline (with the coverage gap surfaced); a run whose code can't be exercised at all — no tests *and* no way to capture a baseline — lands in *inconclusive*, never silently in *verified*.

## Degraded and edge cases

- **No existing tests** → verify against the baseline captured by exercising the code ([phase 01](01-locate-and-baseline.md)). The verdict can still be *verified* on that basis, with the absent coverage surfaced as a routine hygiene note — advice about a *pre-existing* gap, not work the change made necessary.
- **CI unavailable** → run locally; the verdict notes local-only confirmation (a *verified* with a stated caveat, not an *inconclusive*, when the local run is genuine and complete).
- **Checks fail** → *not-verified*; back to phase 03.
