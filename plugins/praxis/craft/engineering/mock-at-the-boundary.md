# Mock at the boundary

Setting up a test decides what is real and what is a double at each seam, and getting it wrong in either direction makes the run lie. Over-mock and the tests exercise the mocks — green while the integrated code is broken (false confidence). Under-mock and they exercise the network — slow and flaky, testing a third party's reliability rather than your change.

## The position this standard takes: classicist / minimal-mocking

Minimal mocking is the default: a test's two worst outcomes, a false alarm on a behavior-preserving refactor and false confidence (green while behavior broke), are both the documented over-mocking failure modes. `(basis: Fowler, "Mocks Aren't Stubs"; Khorikov, "Unit Testing Principles, Practices, and Patterns"; Beck and DHH ("mock almost nothing"))`

Keep the unit under test **and its in-process collaborators real**; assert observable outcomes and state, never internal call order. Substitute a double only at a true external seam. The sharp discriminator (Khorikov's managed/unmanaged split):

- **internal collaborator** — your own in-process code → real, never mocked.
- **managed out-of-process dependency** — reachable only through your app, unobservable from outside (e.g. your own database) → real (a real or containerized instance), not mocked; it is an implementation detail.
- **unmanaged out-of-process dependency** — observable externally and nondeterministic (a third-party API, a message bus, SMTP, the clock, the filesystem) → *this* is the boundary to mock.

And "don't mock what you don't own": wrap an un-owned third-party library in an owned adapter, double the adapter, and cover the adapter itself with one real integration test.

## Which seams count as "real" — open-by-design within the position

Exactly which dependencies are unmanaged/external for a given change is per-context and deliberately not enumerable here — a datastore is a managed dependency in one architecture and a shared external service in another. Deliberately open: pinning a fixed seam list would be false precision. What *is* pinned is the discriminator above (internal vs managed vs unmanaged; owned vs not-owned), which decides each case — the openness is which side a specific dependency falls on, not the test that decides it.

## The fork — classicist vs mockist

Authorities genuinely conflict on mocking a unit's *own in-process collaborators*: the mockist / London school (Freeman and Pryce's GOOS) mocks them and verifies interactions (mocks as a design tool); the classicist / Detroit school (Fowler, Khorikov) keeps them real and verifies outcomes (regression safety, resistance to refactoring). This standard defaults classicist for the reason above. The mockist case — mocks as a design-discovery tool — has force only where a test is written before the design it drives; even there the default stays classicist, because a test's lasting job is regression safety, which over-mocking undermines. `(basis: derived from the default's own reason)` Routing is non-gating: a suite already written London-style → match its convention ([match-the-surrounding-code](match-the-surrounding-code.md)) rather than fighting it; else the house default → the maintainer. How much internal-collaborator mocking to tolerate before flagging it stays per-context judgment.

`(basis: maintainer, 2026-07-10)`
