# The failure-classification taxonomy

[run-and-observe](../phases/05-run-and-observe.md) produces red results, and a red is not a verdict until it is classified — because a flake reported as a genuine failure sends someone chasing a bug that isn't there, and a genuine failure dismissed as a flake ships the bug. Naming the three classes is not the closure; the discriminators that sort them are. This rule pins those discriminators and the order to apply them, cheapest and most-mechanical first.

**One term, pinned once, because it is load-bearing for two of the three classes:** *the unchanged revision* means **the current revision under test, held unmodified across reruns** — you re-run the very code you are verifying, changing nothing, to see whether the result is stable. It does **not** mean the pre-change baseline; whether a red reproduces on the *pre-change* code is a different question (it separates a change-caused break from a pre-existing one, used below and in [prove-the-test-can-fail](prove-the-test-can-fail.md)), not the determinism test.

The three classes, in test order:

## 1. environment noise — the run's setup failed, not the code

The red came from the *environment*, not the code under test. Two near-mechanical discriminators sort it first, because they are the cheapest and most reliable:

- **phase** — the failure occurred *before or around the assertion*: during collection/import, fixture setup or teardown, or the job aborted with an infra signature (out-of-memory / SIGKILL, "cannot connect to …", a connection timeout, a failed checkout, a lost runner). A test whose body never executed its assertions did not test the code — many runners report this as an *error* distinct from an assertion *failure*.
- **not caused by the change** — phase alone is not enough, because a change can itself break collection or import (the change won't compile, an import it added is missing, a signature it altered breaks a caller's module load — the classic "un-updated caller" break). A setup/collection/import red is **environment noise only if it is not caused by the code under test**: it carries an infra signature (the list above), *or* it reproduces on the *pre-change* revision (so it predates the change). A setup/collection/import red that appears *only* with the change, and carries no infra signature, is a **genuine failure** — the change broke the build/import — not environment noise.
- **scope / correlation** — many *unrelated* tests went red at the same time with the same error → a shared-infrastructure cause, not N independent code failures; and it fails identically on a known-good revision.
- *Anchor:* forty unrelated tests red with "exit 137" on one runner — environment. *Counter-anchor:* the suite fails to compile because a changed function signature left three callers un-updated — a genuine failure surfacing at collection, **not** environment, because it is caused by the change and carries no infra signature.

## 2. flake — the test is nondeterministic

`(basis: the genuine-vs-flake discriminator — re-run the same test on the unchanged revision — is settled across the authorities: Qingzhou Luo et al., "An Empirical Analysis of Flaky Tests" (FSE 2014); John Micco / Google Testing Blog; Martin Fowler, "Eradicating Non-Determinism in Tests". The common flake root causes — async/timing, concurrency, test-order dependency — are Luo's top three, ~78%.)`

Re-run the *same* test on the *unchanged* revision and config: it produces both passes and failures. Common root causes: async-wait / timing, concurrency, test-order dependency, network, nondeterministic data. Treat a flake as a defect *in the test* ([control-nondeterminism](control-nondeterminism.md)), not noise to retry past.

- **The critical guard** — a pass on rerun does **not** clear the production code. Luo found 86% of flaky-test fixes that touched code-under-test were fixing a real *nondeterministic production bug*. So a single green rerun downgrades the result to **"suspected nondeterministic bug, needs root-cause,"** never to "flake, ignore." `(basis: Luo et al. FSE 2014, RQ4 — 86% of code-touching flaky fixes fixed a real nondeterministic bug; Fowler — treating intermittent failures as ignorable makes the test "useless" and masks regressions.)`
- *Anchor:* a test that passes 7 of 10 runs on the unchanged commit with an async-timing stack — flake candidate; root-cause it, don't retry to green.

## 3. genuine failure — the production code is wrong

Reproduces *deterministically* on the unchanged revision: fails every run, same assertion, stack pointing at production code. This is the only class that can set the verdict to **FAIL** — but classification only establishes that a red is *genuine*; whether it sets FAIL is decided in [report-the-verdict](../phases/06-report-the-verdict.md), which fires FAIL only for an **in-claim** genuine failure (its scope test — which uses the pre-change test below) and surfaces an out-of-claim genuine failure separately.

- *Anchor:* an assertion failure that fires on every run with the same expected-vs-actual — genuine.

## The confusable-pair discriminators

- **environment vs genuine** — *did the test body execute its assertions, and is the red caused by the change?* A setup/collection/infra red is environment **only** if it carries an infra signature or reproduces on the pre-change revision; a setup/collection red that appears only with the change (a build/import the change broke) is genuine, and an assertion in the executed body is genuine-or-flake. (phase + caused-by-the-change)
- **genuine vs flake** — *does it reproduce deterministically on the unchanged revision?* Every run the same = genuine; mixed pass/fail = flake — but apply the critical guard: "passed on rerun" is not a clean bill of health for the production code. (determinism + the guard)
- **environment vs flake** — *scope.* A simultaneous wall of unrelated reds = environment; scattered single-test intermittency = flake. (correlation)

The rerun count used to expose nondeterminism is **open-by-design**: the right number varies with the test's flake-proneness and the run's budget (a low-frequency flake needs many reruns; CI budget bounds them), so pinning a fixed N would be false precision. What *is* pinned is the invariant — never let one green rerun auto-resolve a red to "flake."

`(basis: the three-class split is the skill's role ("separate genuine failures from flakes and environment noise") — note the authorities (Luo/Micco/Fowler) treat environment as a *cause* of flakiness rather than a separate verdict, so the environment class rests on corroborated community practice (the phase/scope discriminators — the runner's own error-vs-failure reporting, CI infra signatures), while genuine-vs-flake rests on the authoritative determinism discriminator above.)`
