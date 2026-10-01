An upgrade is correct when the checks that were green before the bump are green again and every behavior change it brought is one the publisher announced and you meant to take — measured against the baseline from [phase 01](01-read-the-upgrade-path.md).

## Prove the upgrade against the baseline

Show the intended delta and no unintended one (**judgment**, anchored to the phase-01 baseline):

- the previously-green checks are green again;
- each behavior change the upgrade introduced is accounted for: the changelog announced it, and the call sites take it on purpose;
- each break the upgrade caused and phase 03 fixed carries a guard that fails without the fix and passes with it ([regression-guard-the-specific-failure](../../../craft/engineering/regression-guard-the-specific-failure.md)).

## Run the project's checks

Run the project's existing checks over the working set, and confirm the broader picture where continuous integration is available — delegate the run/build confirmation to the [ci](../../ci/SKILL.md) skill. Without that capability, run the checks locally as the fallback and note that the confirmation is local-only. Scope the run to the working set and its reverse-dependents, not an arbitrary subset.

Apply the always-on security hygiene here too ([distrust-untyped-input-and-secrets](../../../craft/engineering/distrust-untyped-input-and-secrets.md)): an upgrade is a taint event, so confirm no tainted-data path or exposed secret opened at the boundaries the bump reached.

## The verdict — a three-value partition

This phase resolves to exactly one verdict:

- **verified** — the baseline checks are green again, every behavior change is accounted for, and each fixed break is guarded. Proceeds to [commit-and-hand-off](05-commit-and-hand-off.md).
- **not-verified** — a check fails, or a behavior change appeared that no changelog accounts for. Loop back to [bump-and-fix](03-bump-and-fix.md) to correct it, or escalate the tier and stop and report if it can't be corrected in scope.
- **inconclusive** — the checks couldn't run at all (no runnable suite and no way to exercise the call sites), or a delegated capability the verdict depends on was unavailable *with no local substitute*. This is **not** a pass: report it distinctly, and carry it to [commit-and-hand-off](05-commit-and-hand-off.md) as a change that needs the missing confirmation before it's trusted.

## Degraded and edge cases

- **CI unavailable** → run locally; the verdict notes local-only confirmation (a *verified* with a stated caveat, when the local run is genuine and complete).
- **No changelog for part of the span** → the green checks carry the discharge alone; say which span had none, and grade the delta on [change-risk-scale](../../../craft/engineering/change-risk-scale.md) accordingly.
- **Checks fail** → *not-verified*; back to phase 03.
