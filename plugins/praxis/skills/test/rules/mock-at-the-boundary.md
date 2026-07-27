# Mock at the boundary

[set-up-the-harness](../phases/04-set-up-the-harness.md) decides what is real and what is a double at each seam, and getting it wrong in either direction makes the run lie. Over-mock and the tests exercise the mocks — green while the integrated code is broken (false confidence). Under-mock and they exercise the network — slow and flaky, testing a third party's reliability rather than your change. This rule pins where the line sits, and it states the position it takes rather than pretending the choice is neutral.

## The position this rule takes: classicist / minimal-mocking

`(basis: classicist / Detroit / minimal-mocking is the position appropriate to *change verification*. Martin Fowler, "Mocks Aren't Stubs" (stays classicist — the mockist cost is coupling tests to implementation); Vladimir Khorikov, "Unit Testing Principles, Practices, and Patterns" (the four pillars, especially resistance-to-refactoring); Beck / DHH, "mock almost nothing." The reasoning is this skill's job specifically: a change-verifier's two worst outcomes are a false alarm on a behavior-preserving refactor and false confidence (green while behavior broke), and both are the documented over-mocking failure modes — so minimizing internal mocking directly serves verification. The mockist school's headline basis — mocks as a design-discovery tool (Freeman & Pryce, "Growing Object-Oriented Software, Guided by Tests") — is out of scope here: the change is already designed.)`

Keep the unit under test **and its in-process collaborators real**; assert observable outcomes and state, never internal call order. Substitute a double only at a true external seam. The sharp discriminator (Khorikov's managed/unmanaged split):

- **internal collaborator** — your own in-process code → real, never mocked.
- **managed out-of-process dependency** — reachable only through your app, unobservable from outside (e.g. your own database) → real (a real or containerized instance), not mocked; it is an implementation detail.
- **unmanaged out-of-process dependency** — observable externally and nondeterministic (a third-party API, a message bus, SMTP, the clock, the filesystem) → *this* is the boundary to mock.

And "don't mock what you don't own": wrap an un-owned third-party library in an owned adapter, double the adapter, and cover the adapter itself with one real integration test.

## Which seams count as "real" — open-by-design within the position

Exactly which dependencies are unmanaged/external for a given change is per-context and deliberately not enumerable here — a datastore is a managed dependency in one architecture and a shared external service in another. Deliberately open: pinning a fixed seam list would be false precision. What *is* pinned is the discriminator above (internal vs managed vs unmanaged; owned vs not-owned), which decides each case — the openness is which side a specific dependency falls on, not the test that decides it.

## The fork — classicist vs mockist

Authorities genuinely conflict on mocking a unit's *own in-process collaborators*: the mockist / London school (GOOS) mocks them and verifies interactions (mocks as a design tool); the classicist / Detroit school (Fowler, Khorikov) keeps them real and verifies outcomes (regression safety, resistance to refactoring). This rule defaults classicist for the change-verification reason above. Routing is non-gating: a suite already written London-style → match its convention ([match-the-suites-conventions](match-the-suites-conventions.md)) rather than fighting it; else the house default → the maintainer.

`(basis: ratified by the maintainer, 2026-07-10. Classicist / minimal-mocking is the house default for change verification — keep the unit and its in-process collaborators real, mock only unmanaged external seams; route to the project's existing mocking style first, else this default. No external authority pins the default for this skill (the authorities and lived practice lean classicist for verification — Fowler; Khorikov's refactor-resistance pillar — while GOOS argues the mockist case as a design tool), so the classicist default is the maintainer's ratified call. How much internal-collaborator mocking to tolerate before flagging stays per-context executor judgment.)`
