A refactor has no upstream spec: "correct" means the behavior captured in the *baseline from [phase 01](01-locate-and-baseline.md)* still holds, along with the existing checks.

## Prove the behavior is unchanged

Show there is no delta at all (**judgment**, anchored to the phase-01 baseline): the captured current behavior is bit-for-bit preserved — output that is nondeterministic by design (a timestamp, an unordered collection) is compared normalized, the volatile field masked or the collection sorted, and named in the report — so the baseline outputs and tests still hold. `(basis: derived from no delta meaning no behavioral delta)` A refactor fixed nothing, so it owes no new regression guard; its guarantee is that the existing checks still pass.

## Run the project's checks

Run the project's existing checks locally over the working set. Continuous integration confirms only a ref that carries the change, and this phase has none — the change isn't pushed — so the verdict is local, and hosted confirmation is left to whoever pushes it, through [ci](../../ci/SKILL.md). `(basis: derived from a hosted check seeing only what is pushed)` Scope the run to the working set and its reverse-dependents (what the change can reach), not an arbitrary subset — a change verified only on the file it touched is unverified on the callers it broke.

A coverage gap the refactor merely reveals is surfaced as a routine hygiene note in [commit-and-hand-off](05-commit-and-hand-off.md), not filled here. Apply the always-on security hygiene as part of verification too ([distrust-untyped-input-and-secrets](../../../craft/engineering/distrust-untyped-input-and-secrets.md)): confirm the restructuring left no tainted-data path or exposed secret at the boundaries it touched.

## The verdict — a three-value partition

This phase resolves to exactly one verdict, and the set is exhaustive and mutually exclusive — walk it deliberately, because the third value is the one a two-value check drops:

- **verified** — the baseline still holds and every in-scope check ran and passes. Proceeds to [commit-and-hand-off](05-commit-and-hand-off.md).
- **not-verified** — a check fails, or the baseline shows a delta. The change does not stand as-is; loop back to [make-the-change](03-make-the-change.md) to correct it, or stop and report if it can't be corrected in scope.
- **inconclusive** — some or all in-scope checks couldn't run (no runnable suite and no baseline — per [phase 01](01-locate-and-baseline.md) — or a check needing an unavailable service), with nothing failing among those that ran and no baseline delta. Where a run fits both — a check couldn't run *and* something failed or is unaccounted — it is **not-verified**: a known defect outranks a missing confirmation. `(basis: derived)` Inconclusive is **not** a pass: report it distinctly so "we couldn't confirm" never reads as "verified", and carry it to [commit-and-hand-off](05-commit-and-hand-off.md) as a change that needs the missing confirmation before it's trusted.

The partition holds across the matrix: a run with no tests but a baseline captured by exercising the code can still reach *verified* on the baseline (with the coverage gap surfaced); a run whose code can't be exercised at all — no tests *and* no way to capture a baseline — lands in *inconclusive*, never silently in *verified*.

## Degraded and edge cases

- **No existing tests** → verify against the baseline captured by exercising the code ([phase 01](01-locate-and-baseline.md)). The verdict can still be *verified* on that basis, with the absent coverage surfaced as a routine hygiene note — advice about a *pre-existing* gap, not work the change made necessary.
- **CI unavailable** → no change: the verdict is local either way.
- **Checks fail** → *not-verified*; back to phase 03.
