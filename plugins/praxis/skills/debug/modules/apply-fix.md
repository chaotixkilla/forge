# apply-fix (`--fix`)

Activated by `--fix`, referenced from [report-or-resolve](../phases/06-report-or-resolve.md).

The base debug run stops at a confirmed diagnosis and hands it off; the author applies the fix. This module extends the run past diagnosis: make the change at the confirmed cause, guard it, and confirm the bug is dead. Deletion test: remove it and debug still delivers its diagnosis; applying the fix is optional behavior a flag turns on — which is why it is a module.

## Gate on confidence before touching code

A fix is only as trustworthy as the cause it targets. Apply a fix by default **only at a confirmed-mechanism cause** — one you can toggle the failure on and off with (per [the root-cause-confidence scale](../rules/root-cause-confidence.md)). A **probable** cause may be fixed only under the incident / production-pressure routing of [report-or-resolve](../phases/06-report-or-resolve.md)'s mitigation fork, and the fix is recorded as provisional pending confirmation. A **suspected** cause is never fixed — it routes back into the investigation loop. Committing a fix to an unconfirmed cause is how `--fix` ships a new bug while the original survives.

## Apply the smallest correct change, or hand off

The change must be the smallest *correct* one — smallest in scope and blast radius, not merely fewest lines — placed at the layer that owns the violated invariant ([fix-at-the-right-altitude](../rules/fix-at-the-right-altitude.md)), never a symptom patch at the convenient call site ([distinguish-cause-from-symptom](../rules/distinguish-cause-from-symptom.md)).

The discriminator between applying and handing off:

- **Apply** when the correct fix is a **localized change at the fault's owning layer plus its guarding test** — bounded to the mechanism, introducing no new design decision.
- **Hand off** to plan/develop when the correct fix requires a **decision the author owns**: a new abstraction, an interface or contract change that ripples across call sites, or a cross-cutting refactor — anything large enough to warrant its own plan or review. Deliver the diagnosis plus the recommended fix altitude; do not absorb feature-sized work into a debug run.

`(basis: ratified by the maintainer, 2026-07-10. The apply-vs-hand-off cutoff = a localized change at the fault's owning layer (+ its guarding test) is applied; a change requiring a design decision the author owns (new abstraction, interface/contract change across call sites, cross-cutting refactor) is handed off. Editing the tree at a confirmed cause is consequential, so the boundary between "localized" and "design-sized" is the maintainer's ratified house standard — derived from review's apply-fixes cutoff (confirmed, least-invasive edits only) and the smallest-scope-not-fewest-lines principle (Hayes, WPShout 2018).)`

## Guard it, and confirm the original reproduction is dead

Every applied fix carries a regression test that **fails before and passes after** and that pins the mechanism, not an incidental outcome ([guard-against-regression](../rules/guard-against-regression.md)). Then re-run the original reproduction against the fixed code and confirm the failure no longer triggers — a fix that greens the new test but leaves the original repro failing has fixed something adjacent, not the reported bug.

## Report what was applied and what was left

Distinguish, in the run's record, the change that was applied (with its guarding test) from any part handed off for design work, so the outcome is auditable and nothing is silently "fixed." The boundary is deliberate: debug edits and re-checks the fix at its site and against the original reproduction; it does not confirm broad end-to-end health across the app — that hands off to a separate verify/test pass.
