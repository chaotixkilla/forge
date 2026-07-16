# Leave the campsite cleaner

The boy-scout rule — *leave the code a little better than you found it* — is good maintenance instinct and a real trap. Followed without a bound, it turns a one-line dependency bump into a forty-file reformat, and the actual change drowns in the cleanup: the reviewer can't find it, the revert can't isolate it, and a regression can't be bisected to it. This rule keeps the instinct and bounds it: improve, but keep the improvement *inside the diff's reach* and *separable* from the change, so the change stays about the one thing it set out to do.

## The line: in-scope improvement vs. unrelated refactor

An improvement earns its place in this diff only when **all** of these hold; fail any one and it's a follow-up, not a fold-in:

- **It's in code the change already touches** for its primary purpose — you're editing this function/file anyway. Cleanup that reaches into untouched code is a separate errand.
- **It's behavior-preserving or independently safe** — a rename, a dead-code removal (subject to [decode-intent-from-history](decode-intent-from-history.md)), an extracted helper — so it can't be the thing that broke something.
- **It doesn't raise the diff's risk tier.** If folding it in pushes the change up a [change-risk-scale](change-risk-scale.md) tier (e.g. a "tidy" that now touches a contract), it's no longer incidental — it's a second change wearing the first one's clothes.

When an improvement is worth doing but fails the test, don't silently drop it and don't silently do it — **surface it as a follow-up** in [review-and-record](../phases/05-review-and-record.md), so it's captured rather than lost. That is the discipline that lets you honor the instinct without bloating the diff: the campsite still gets cleaner, just not all in one commit.

`(basis: ratified by the maintainer, 2026-07-11 — the house line is touched-code ∧ behavior-preserving/independently-safe ∧ same-risk-tier; anything failing it is a surfaced follow-up. It's the direct counterpart to smallest-reversible-change (which biases toward the minimal edit); the line where they meet is a house scope-discipline call with no single external authority, ratified together with the stopgap discriminator in fix-the-cause-not-the-symptom.)`

## The fork it sits on

This rule and [smallest-reversible-change](smallest-reversible-change.md) pull in opposite directions on purpose — one biases toward improving, the other toward the minimal edit — and the line above is where they're reconciled. When in genuine doubt on a specific improvement, the tie-breaker is the diff's *legibility to a reviewer*: if folding it in makes the change harder to read as one coherent thing, it's a follow-up. Keeping cleanup separable is not timidity; it's what makes the change reviewable ([review](../../review/SKILL.md) judges it) and reversible.
