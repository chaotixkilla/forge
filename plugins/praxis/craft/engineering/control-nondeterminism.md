# Control nondeterminism

Pin every source of nondeterminism a case touches — the clock, random seeds, iteration and collection ordering, concurrency and scheduling, and any external timing — so the case's result depends only on the behavior under test. A case that can pass or fail on the *unchanged* code is not a weaker test; it is a broken instrument, and a suite full of them trains everyone to retry past red until it turns green, which is how a real regression ships unnoticed.

The stance this standard takes: **a flaky test is a defect in the test, not background noise.** It is fixed where the test is set up, by removing the nondeterminism, not managed at run time by re-running. A red that turns out to be a flake is a defect to root-cause, and its critical guard applies: a green rerun does not clear the code, because the nondeterminism may sit in the production code, not only in the test. `(basis: Fowler, "Eradicating Non-Determinism in Tests"; Luo et al., FSE 2014)`
