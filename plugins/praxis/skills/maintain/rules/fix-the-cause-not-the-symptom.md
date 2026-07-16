# Fix the cause, not the symptom

A maintenance change that silences a symptom while the cause lives on is a change that has to be made again — and the second time it's harder, because now there's a guard obscuring where the real defect is. Trace the behavior you're changing to its actual origin and fix it there. The instinct to patch the nearest surface — wrap the crashing call in a try, clamp the bad value where it's read — is strong because it's fast and it works *for the case in front of you*; it fails every other case the cause still reaches. This rule holds the line between a fix and a patch, and it does not forbid patches — it forbids *unlabeled* ones.

## Locate the cause before you touch anything

The cause is the earliest point where the code first does the wrong thing — not the point where the wrong thing becomes visible. A null that crashes three frames down originates where it was allowed to be null, not where it was dereferenced. Trace back along the data and control flow to the first frame that violated an invariant, and confirm it by asking: *if I fix it here, does every downstream symptom disappear?* If fixing your candidate site leaves other paths still broken, you're at a symptom, not the cause.

## The discriminator: when a stopgap is acceptable

A knowingly-labeled stopgap — a symptom-level guard you place *deliberately*, as a holding action — is legitimate in maintenance work; pretending otherwise produces heroic cause-fixes nobody asked for. A stopgap is acceptable when **all** of these hold:

- **It's labeled and tracked.** The code says it's a stopgap (a comment naming what the real cause is) and a follow-up is recorded ([review-and-record](../phases/05-review-and-record.md) surfaces it), so it can't masquerade as the fix.
- **It doesn't deepen the debt.** The guard adds no new coupling to the symptom and doesn't make the eventual cause-fix harder — it holds the line, it doesn't build on the wrong foundation.
- **The cause is genuinely out of reach now.** The cause sits outside the change's [scope](change-risk-scale.md) or its blast-radius tier, or fixing it now is materially riskier than the stopgap (e.g. the cause is in an `exposed`-tier contract that needs a migration path this change can't carry).

The **cause-fix is required** — a stopgap is *not* acceptable — when any of these hold, regardless of convenience:

- The symptom **recurs across sites**: the same guard is being (or would be) copy-pasted to several call sites, which is the signature of a systemic cause that a per-site patch will never contain.
- The stopgap would **mask data corruption or a security defect** — here a guard that hides the symptom is actively dangerous, because it removes the signal that the corruption/breach is happening.
- The cause is **inside the change's scope already** — you're touching the causing code anyway, so "out of reach" doesn't apply and patching around it is pure avoidance.

`(basis: derived from the fix-at-the-cause craft (root-cause over symptom is the shared position of debugging and refactoring literature); the acceptability discriminator is the maintainer's ratified house line for when a labeled stopgap is defensible — ratified 2026-07-11 together with the cleanup-vs-focus line in leave-the-campsite-cleaner, since "may I hold with a stopgap" and "may I improve beyond the fix" are the same scope-discipline call from two directions.)`

## When you must patch, patch honestly

If the discriminator says a stopgap is acceptable, make it *visibly* a stopgap: name the real cause in a comment, keep the guard minimal, and record the follow-up. A patch that announces itself is a maintenance decision; a patch dressed as a fix is a trap for the next maintainer, who will build on it believing the cause is gone. Relate this to [smallest-reversible-change](smallest-reversible-change.md): the honest stopgap is often the *more* reversible move, and that's a point in its favor — as long as it's labeled.
