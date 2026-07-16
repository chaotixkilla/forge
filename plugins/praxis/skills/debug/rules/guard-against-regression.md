# Guard against regression

A fix with no test behind it is one refactor, one revert, one merge away from silently coming back — and a bug that returns unguarded is worse than the first time, because everyone now believes it was fixed. The reproduction you built to find the bug is already the test that keeps it dead; not encoding it throws away the most valuable artifact of the whole session. This rule turns the reproduction into a permanent guard.

## Encode the reproduction as a red-before / green-after test

Turn the minimal trigger from [reproduce-before-fixing](reproduce-before-fixing.md) into an automated test that asserts the *correct* behavior on that input. Then confirm the sequence that proves it actually guards the bug: the test **fails before** the fix (run it against the unfixed code and watch it go red — a test that was green before the fix guards nothing) and **passes after**. A test only added after the fix, never seen to fail, may be asserting something the bug never violated.

## The discriminator: does the test pin the mechanism, or pass by accident?

A regression test earns its place only if it would catch *this bug's mechanism* again — not merely pass today. The test:

- **Guards the mechanism:** it exercises the specific condition the cause needs (the boundary value, the ordering, the state) so that reintroducing the fault turns it red. This is the one you want.
- **Passes by accident:** it asserts an outcome that holds for reasons unrelated to the fix, so the fault could return without tripping it. Re-check by mentally reintroducing the cause — if the test would still pass, it isn't guarding the bug.

For an intermittent failure, the guard is statistical: assert the failure *rate* stays at zero across enough runs (or under the amplified conditions that surfaced it), since a single pass proves nothing about a probabilistic bug.

## The bug isn't fixed until the original reproduction is dead

Close the loop: re-run the original reproduction against the fixed code and confirm the failure no longer triggers. A fix that makes the new test pass but leaves the original repro failing has not fixed the reported bug — it has fixed something adjacent.

`(basis: Agans' Rule 9, "If You Didn't Fix It, It Ain't Fixed" — Debugging: The 9 Indispensable Rules (2002): verify the fix actually removed the failure; the bug was never a fluke. The red-before/green-after sequence is standard regression-testing practice; the "guards the mechanism vs. passes by accident" discriminator and the statistical-guard case are the maintainer's house articulation for what makes the guard real.)`
