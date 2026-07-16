# Regression-guard the specific failure

A fix without a guard is provisional: it works today, and nothing stops the same failure from returning silently tomorrow when someone edits nearby. When a maintenance change fixes a concrete failure — a bug, a broken edge case, a regression a dependency bump introduced — capture that exact failure as a check that would have caught it. The guard is what converts "fixed" into "stays fixed."

## What makes a guard *specific*

A guard earns the name only when it pins the actual failure, provable by the fail-then-pass test:

- **It fails before the fix and passes after.** If it passes against the unfixed code, it isn't guarding this failure — it's testing something adjacent. Confirm the fail state first (run it against the pre-fix behavior, or reason it through concretely), then confirm the fix flips it.
- **It pins the failing case, not the whole feature.** The guard exercises the specific input, state, or path that broke — the null that crashed, the boundary that was off by one, the version interaction the upgrade exposed — so a future regression trips it precisely. A broad smoke test that happens to cover the area is not a specific guard; it can stay green while the exact failure returns.
- **It lives where the suite will run it.** A guard the project's checks don't execute is documentation, not a guard. Add it to the existing suite in the suite's own style ([match-the-surrounding-code](match-the-surrounding-code.md)).

## The boundary with broader coverage

maintain adds the *one* guard for the failure it fixed — that is within its scope and it does not hand that off. Designing *broader* coverage — filling the suite's gaps, systematically testing the changed surface, deciding what else is under-tested — is the [test](../../test/SKILL.md) skill's deliverable, and maintain delegates it there rather than expanding into a testing pass. The discriminator: if the check would have caught *this* failure, it's maintain's guard; if it's coverage the change merely reveals is missing, it's a routine hygiene note for test (advice about a pre-existing gap, not the change-made-necessary work that would make a run *partial*). A maintenance change that fixes nothing (a pure refactor that preserves behavior) owes no new guard — its guarantee is that the *existing* checks still pass ([verify-and-guard](../phases/04-verify-and-guard.md)).
