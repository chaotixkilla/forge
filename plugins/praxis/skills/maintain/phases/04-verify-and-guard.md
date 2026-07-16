A maintenance change is not done when it's written — it's done when it's shown to do what it intended and to have broken nothing reachable. Because maintenance usually has no upstream spec, "correct" is defined against the *baseline reproduced in [phase 01](01-locate-and-reproduce.md)* and the existing checks, not against an external contract. This phase proves the change, captures the specific failure it fixed so the failure can't return silently, and produces an honest verdict — including the verdict that says "couldn't confirm."

## Prove the change against the baseline

Show the intended delta and no unintended one (**judgment**, anchored to the phase-01 baseline):

- **A fix** → the reproduced failure is now gone (the demonstration that failed before now passes) *and* the surrounding behavior is unchanged.
- **A refactor** → the captured current behavior is bit-for-bit preserved: the baseline outputs/tests still hold.
- **An upgrade** → the previously-green checks are green again, and any behavior change the upgrade introduced is intended and accounted for.

## Run the project's checks

Run the project's existing checks over the working set, and confirm the broader picture where continuous integration is available — delegate the run/build confirmation to the [ci](../../ci/SKILL.md) skill. Without that capability, run the checks locally as the fallback and note that the confirmation is local-only. Scope the run to the working set and its reverse-dependents (what the change can reach), not an arbitrary subset — a change verified only on the file it touched is unverified on the callers it broke.

## Guard the specific failure

If the change fixed a concrete failure, capture it as a regression guard — a check that fails before the fix and passes after ([regression-guard-the-specific-failure](../rules/regression-guard-the-specific-failure.md)). A pure refactor that fixed nothing owes no new guard; its guarantee is that the existing checks still pass. **maintain adds the one guard for the failure it fixed and no more** — broader coverage design is delegated to the [test](../../test/SKILL.md) skill, and a coverage gap the change merely reveals is surfaced as a routine hygiene note (advice for test; it does *not* make the run partial — [review-and-record](05-review-and-record.md)), not filled here. Apply the always-on security hygiene as part of verification too ([distrust-untyped-input-and-secrets](../rules/distrust-untyped-input-and-secrets.md)): confirm the change left no tainted-data path or exposed secret at the boundaries it touched.

## `--security`: the gating pass

When `--security` is set, run the escalated security/compliance pass here and gate completion on it — see [security-pass](../modules/security-pass.md). Its verdict feeds the phase verdict below: a blocking security finding makes this phase's verdict **not-verified**, and an audit that couldn't run makes it **inconclusive**.

## The verdict — a three-value partition

This phase resolves to exactly one verdict, and the set is exhaustive and mutually exclusive — walk it deliberately, because the third value is the one a two-value check drops:

- **verified** — the intended delta is shown against the baseline, the checks in scope pass, the regression guard (if any) is in place, and (under `--security`) the security bar is cleared. Proceeds to [review-and-record](05-review-and-record.md) as a landing change.
- **not-verified** — a check fails, the baseline delta is wrong, or a `--security` finding blocks. The change does not land as-is; loop back to [make-the-change](03-make-the-change.md) to correct it, or stop and report if it can't be corrected in scope.
- **inconclusive** — the checks could not be run at all (no runnable suite, and the baseline can't be captured because the code can't be exercised at all — per [phase 01](01-locate-and-reproduce.md)), or a delegated capability the verdict depends on was unavailable *with no local substitute* (ci down **and** no runnable local check, `--security` audit unrunnable). This is **not** a pass: report it distinctly so "we couldn't confirm" never reads as "verified," and carry it to [review-and-record](05-review-and-record.md) as a change that needs the missing confirmation before it's trusted.

The partition holds across the matrix: a run with no tests but a baseline captured by exercising the code can still reach *verified* on the baseline delta (with the coverage gap surfaced); a run whose code can't be exercised at all — no tests *and* no way to capture a baseline — lands in *inconclusive*, never silently in *verified*; a `--security` run whose audit is blocked-or-unrun lands in *not-verified* or *inconclusive* respectively, never *verified*.

## Degraded and edge cases

- **No existing tests** → verify against the reproduced baseline captured by exercising the code ([phase 01](01-locate-and-reproduce.md)), plus — *for a fix* — the new regression guard; a pure refactor verifies against the baseline alone and owes no guard. The verdict can still be *verified* on that basis, with the absent coverage surfaced as a routine hygiene note for [test](../../test/SKILL.md) — advice about a *pre-existing* gap, not the change-made-necessary work that would make a run *partial* ([review-and-record](05-review-and-record.md)).
- **CI unavailable** → run locally, verdict notes local-only confirmation (a *verified* with a stated caveat, not an *inconclusive*, when the local run is genuine and complete).
- **Checks fail** → *not-verified*; back to phase 03.
