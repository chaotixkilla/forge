# Green before land

A gate is only worth running if a failure *stops* the change. Treat a failing, skipped, or soft-passed required check as a hard stop, not a warning to note and land past — and never silence a check to get a change through. The failure this prevents is the confident bad merge: a change lands, the mainline goes red for everyone, and the next developer builds on top of the breakage. This rule pins what "green" means so two cold runs treat the same gate state identically, and it is the one gate concern that does **not** defer to team convention.

## The acceptance test — what counts as green

The change may land only when **every required check has concluded a pass**. Each of these is *not* green, and each blocks:

- **A failed check** — any required check whose verdict is failure/error. Blocks. Never land on red.
- **A still-running check** — not yet a pass; wait for it to settle, do not land on an in-flight gate assuming it will pass.
- **A skipped or disabled required check** — a check that should have run and didn't (skipped in config, disabled to get through). Treated as non-green: a gate you turned off is not a gate you passed.
- **A soft-passed check** — a required check reported as advisory/allowed-to-fail so the flow proceeds. If it is required, a non-pass blocks; `--gate` ([require-explicit-gate](../modules/require-explicit-gate.md)) forces exactly this.
- **A hand-overridden red** — a failure dismissed by force-merge or an override without fixing the cause. Blocks; the override is the silencing this rule forbids.

`(basis: "keep the mainline green; do not build or integrate on a broken build; a broken build is the team's top priority" is a settled hard discipline, stated imperatively and without dissent across the CI authorities — Martin Fowler, "Continuous Integration" ("Continuous Integration can only work if the mainline is kept in a healthy state"; martinfowler.com/articles/continuousIntegration.html); DORA's Continuous Integration capability (names "not fixing broken builds right away" a critical pitfall; dora.dev); and Software Engineering at Google, Ch.23 ("a cultural norm that strongly discourages committing any new work on top of known failing tests"; abseil.io swe-book). This is why green-before-land is pinned as a hard stop, not encoded as a fork.)`

`(basis: house rule — treating a SKIPPED or DISABLED required check as non-green is a house extension. The authorities above address failing/broken builds explicitly; none I found states a verbatim rule that a skipped/disabled test counts as red (Google's norm against building on "known failing tests" is adjacent, not identical). Adopted here because a check silenced to pass answers a different question than a check that passed — surfaced, not smuggled, so the maintainer can loosen it.)`

## Failure is a stop, and the fast fix is revert

When the gate is red, the change does not land — full stop. Beyond stopping, the authorities agree the fastest safe recovery for an *already-landed* breakage is to **revert the offending change**, not to forward-fix under pressure (Fowler, DORA, and SWE-at-Google all name revert as the preferred fast path). For integrate's pre-merge gate, the analog is: fix the change until the gate is green before landing it; do not land it broken intending to fix forward.

## This rule outranks the failure policy

`--on-fail` ([failure-policy](../modules/failure-policy.md)) chooses what happens *at* a failure (hold, ask, roll back), but it can never turn a red required gate into a landing: `--on-fail=continue` is refused on a required-gate failure, because green-before-land is not a policy the caller tunes — it is the stop the gate exists to enforce. `continue` applies only to advisory, non-required checks.
