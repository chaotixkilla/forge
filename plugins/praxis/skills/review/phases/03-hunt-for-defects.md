This is the correctness pass — the reason review exists. With the model built, hunt the change for inputs and states on which it is *wrong*: not "this could read better" (that is [assess-craft](04-assess-craft.md)), but "this produces the wrong result, crashes, breaches, or violates a contract." Run this pass first and at full attention, because the easier craft observations will otherwise crowd out the harder correctness hunt — you will notice the long function before you notice it also loses data.

## On a large change, partition the surface first

If the change is broad — many files across distinct subsystems, not a focused change to a few — partition its surface into cohesive units and hunt each independently (a reviewer per unit in parallel at high/max effort, or one focused pass per unit otherwise), per [cover-a-large-change](../rules/cover-a-large-change.md). A single linear pass over a broad change silently thins its coverage; partitioning is what keeps every subsystem reached. This breadth is orthogonal to the per-symbol depth below — you still follow each candidate out through its blast radius. On a small change, skip this: one pass holds it.

## Sweep the correctness lenses in scope

For each behavior the change introduces or alters, ask "how does this break?" across the correctness lenses. Which lenses, and how deep, is set by `--effort` (the breadth and depth rows in [calibrate-confidence-to-effort](../rules/calibrate-confidence-to-effort.md)) and narrowed by `--lenses` when given:

- **Logic** (`logic`) — the algorithm computes the wrong thing; an inverted condition, a wrong operator, a mishandled case.
- **Edge and boundary** (`boundary`) — empty, null, zero, one, the maximum, the off-by-one; the inputs at the extremes the happy path skips.
- **Error and failure paths** (`error-paths`) — a swallowed exception, an error returned but not handled, cleanup skipped on the failing branch, a partial write left behind.
- **Concurrency** (`concurrency`) — a race on shared state, a lost update, a lock taken in the wrong order, an await point that invalidates an assumption.
- **Security** (`security`, code-review depth) — unsanitized input reaching a sink, a missing authorization check, a leaked secret, an unsafe deserialization. This is the code-review lens, not a full threat model; a change that warrants adversary-scoped analysis is a hand-off to `security-review`, noted as such.
- **Resource safety** (`resource-safety`) — a leaked handle, connection, or lock; an unbounded cache or queue.
- **Data integrity** (`data-integrity`) — a non-atomic multi-step write, a broken invariant across records, a migration that can half-apply.

## Judge across the blast radius, and label confidence honestly

A changed function being locally correct is useless if the change broke a caller that relied on the old contract, so carry each candidate out through its radius ([read-the-diff-in-its-blast-radius](../rules/read-the-diff-in-its-blast-radius.md)) to the depth the effort allows. Before recording a candidate as a defect, confirm it — the failing input exists, the path is reachable, and no guard one frame up already handles it ([confirm-before-claiming](../rules/confirm-before-claiming.md)) — and tag it with the confidence the evidence earns (confirmed / probable / speculative, per [calibrate-confidence-to-effort](../rules/calibrate-confidence-to-effort.md)). Keep only correctness here: if you cannot name an input where the code is wrong, it is a craft finding, not a defect — hold it for the next pass ([separate-correctness-from-taste](../rules/separate-correctness-from-taste.md)). Anchor every candidate to its `file:line` and failing scenario as you record it ([anchor-every-finding-to-evidence](../rules/anchor-every-finding-to-evidence.md)); an unanchored candidate cannot be triaged.

## Recruit an adversary at high effort

At `--effort=high` or `max`, recruit the **adversary critic** to attack the change independently — its lens is "assume this is wrong; construct the input that breaks it" — handing it [calibrate-confidence-to-effort](../rules/calibrate-confidence-to-effort.md) so it grades confidence on that rule's own rungs and anchors rather than a ladder of its own, and [severity-scale](../rules/severity-scale.md) for a *provisional* consequence read that [triage-and-rank](05-triage-and-rank.md) re-grades as the owner of the final severity, and fold its surviving findings into the candidate set. Without fan-out, apply the adversary lens yourself: for each behavior, actively try to construct a failing input before you accept it as correct, rather than reading for confirmation that it works. The pass is not done when you have read every changed line; it is done when the correctness lenses in scope have each been turned on the change.

The output of this phase is a set of *candidate* correctness findings, each anchored and confidence-tagged — not yet severity-ranked and not yet validated against their own refutation. That is [triage-and-rank](05-triage-and-rank.md)'s work.
