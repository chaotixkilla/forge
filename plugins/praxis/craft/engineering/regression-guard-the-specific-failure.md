# Regression-guard the specific failure

A fix without a guard is provisional: it works today, and nothing stops the same failure from returning silently tomorrow, one refactor, one revert or one merge away — and a failure that returns unguarded is worse than the first time, because everyone now believes it was fixed. When a change fixes a concrete failure — a bug, a broken edge case, a regression a dependency bump introduced — capture that exact failure as a check that would have caught it. The reproduction that found the failure is already most of that check.

## What makes a guard *specific*

A guard earns the name only when it pins the actual failure:

- **It fails before the fix and passes after.** Turn the minimal trigger into an automated check that asserts the *correct* behavior on that input, and watch it go red against the unfixed code before you trust its green. A check that was green before the fix guards nothing; one added after the fix and never seen to fail may assert something the failure never violated. Where the unfixed code can't be run, prove the guard can fail another way — a deliberately wrong expectation, or a transient break restored at once ([prove-the-test-can-fail](prove-the-test-can-fail.md)); reasoning the fail state through concretely is the last resort, and a guard shown red only by reasoning is recorded as not proven-red.
- **It pins the mechanism, not the whole feature.** It exercises the specific condition the cause needs — the null that crashed, the boundary that was off by one, the ordering, the version interaction an upgrade exposed — so that reintroducing the fault turns it red. A broad smoke test that happens to cover the area can stay green while the exact failure returns.
- **It lives where the suite will run it.** A guard the project's checks don't execute is documentation, not a guard. Add it to the existing suite in the suite's own style ([match-the-surrounding-code](match-the-surrounding-code.md)).

The discriminator: **does it pin the mechanism, or pass by accident?** Re-check by mentally reintroducing the cause. If the check would still pass, it isn't guarding this failure: it asserts an outcome that holds for reasons unrelated to the fix.

For an intermittent failure the guard is statistical: assert the failure *rate* stays at zero across enough runs, or under the amplified conditions that surfaced it, since a single pass proves nothing about a probabilistic fault.

## The fix isn't done until the original reproduction is dead

Close the loop: re-run the original reproduction against the fixed code and confirm the failure no longer triggers. A fix that makes the new check pass but leaves the original reproduction failing hasn't fixed the reported failure — it has fixed something adjacent.

`(basis: Agans 2002, rule 9; standard regression-testing practice for red-before/green-after; the discriminator and the statistical guard are the maintainer's)`

## The boundary with broader coverage

The change that fixed the failure adds the *one* guard for it; that's within its scope, not handed off. Designing *broader* coverage — filling the suite's gaps, systematically testing the changed surface, deciding what else is under-tested — is test design's job, not the fix's. The discriminator: if the check would have caught *this* failure, it belongs with the fix; if it's coverage the change merely reveals is missing, it's a hygiene note for test design (advice about a pre-existing gap, not work the change itself made necessary). A change that fixes nothing (a pure refactor that preserves behavior) owes no new guard: its guarantee is that the *existing* checks still pass.
