# Smallest reversible change

In living code, the change you can cleanly back out beats the tidier one you can't. Maintenance runs against code that is already in use, already depended on, already working for someone — so the cost of a change isn't just writing it, it's the risk it carries and the difficulty of undoing it if that risk lands. This rule biases every edit toward the smallest version that *fully* solves the task and the most reversible path to it, because a small reversible change is one you can ship with confidence and retract without drama.

## Smallest that *fully* solves — not smallest that appears to

"Smallest" is bounded by completeness: the edit must actually resolve the task, not just the visible part of it. A change that fixes the reported case but leaves the [cause](fix-the-cause-not-the-symptom.md) intact isn't the smallest solution — it's an incomplete one that will be reopened. The test: prefer the edit with the smallest [blast-radius tier](change-risk-scale.md) that still fully solves the task. Reach up a tier only when the smaller edit leaves the task genuinely unsolved, and say why.

## Reversible over tidy — the tie-breaker

When two edits both fully solve the task, prefer the one that is easier to back out:

- A change that can be undone by a single clean revert beats one whose revert would strand data, migrations, or dependent edits.
- A change staged behind a guard (per [change-risk-scale](change-risk-scale.md)'s middle tier) is more reversible than a flag-day switch — the guard *is* the undo.
- A change that preserves the old path until the new one is proven beats one that deletes the old path in the same motion.

Tidiness is a real good, but it loses to reversibility when they conflict: a more elegant refactor you can't cleanly retract carries risk the maintenance task didn't ask for. When tidiness and reversibility *don't* conflict, take both — this rule is not an argument for sloppy code, only for not trading away the ability to back out.

## The bound on smallness

Smallest-reversible does not mean smallest-*keystrokes*: a one-character change that silently alters a [contract](preserve-the-contract.md) is neither small (its blast radius is large) nor safe. Measure "small" by reach and reversibility, not by line count — the two are what this rule and [change-risk-scale](change-risk-scale.md) both turn on.
