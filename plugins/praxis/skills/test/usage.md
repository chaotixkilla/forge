# test — usage

Establish whether a change does what it should: design meaningful test coverage for it, run the project's own suite, observe the real behavior, and return a verdict — pass/fail against a framed claim, plus the coverage gaps and residual risk left unverified.

## When to use
- A change is written (or being written) and you want to *know* it behaves correctly — not eyeball the diff, but design the cases that would catch it being wrong and watch them run.
- You have a spec or acceptance criteria and want each criterion turned into a concrete pass/fail check (`--from-spec`).
- An existing suite is green but you don't trust it: you suspect the tests assert too little, mock too much, or never actually exercise the risky path — you want coverage that *discriminates*, judged against a defined adequacy bar.
- A test is flaky or a failure is ambiguous and you need genuine failures separated from flakes and environment noise before anyone acts on the result.

## Not for / use instead
- Building the change itself (writing the production code, wiring it up) → **develop** (test verifies a change; it does not implement one).
- Making a failing test pass by changing production code, or root-causing a specific known failure → **develop** for the change, **debug** for the diagnosis. test authors and runs tests and *reports* the verdict; it deliberately does not modify production code to turn a red test green.
- Driving the real running application end-to-end to observe it behaving (click the flow, hit the endpoint, read the live output) → **verify** (test runs the automated suite; verify exercises the running app).
- Critically reading a finished diff for latent defects and craft → **review** (review reads statically and does not execute; test designs and runs executable checks).
- A dedicated threat audit → **security-review**.

## Examples
`--changed` — scope the run to what the working-tree diff touched (changed files plus their reverse-dependents) instead of the whole surface; the fast inner-loop window.
`--from-spec=specs/export.md` — take the claim under test from a spec file: map each acceptance criterion to a concrete pass/fail check, and flag any criterion the current suite contradicts.
`--until=green` — loop the verification until it passes (or `--until=first-failure` to stop at the first red, or `--until=20` to repeat a flake-prone case a set number of times to expose nondeterminism).
`--sandbox` — run in a disposable, network/filesystem-isolated local environment with seeded fixtures, so the result is reproducible and can't touch real state.
`--from-spec=specs/export.md --changed` — verify only the changed surface, against the spec's criteria.

## Gotchas
- **test does not fix.** Its *deliverable* is the test suite and the verdict, never a production-code change. A failing test is *reported* with a reproduction; turning it green is develop's or debug's job. This keeps the boundary with develop/debug clean. (The ban is on *delivering* a production change — a transient, self-reverting probe to watch a new test go red, per prove-the-test-can-fail, leaves a net-zero diff and is verification, not a delivered change.)
- **Green is not the verdict; the framed claim is.** A suite passing tells you nothing until you've said what "passing" had to mean for *this* change. test frames the claim first, then reads the run against it — a green suite that never exercised the risky path is a coverage gap, reported as such, not a pass.
- **Coverage is judged for meaning, not for a number.** "Enough" coverage is assessed against a defined adequacy bar (does each behavior that can break have a case that would catch it), not a line-percentage target. Where the project already has a coverage convention, test follows it; it does not impose a number.
- **A test never seen red proves nothing.** A new or changed test is confirmed to *fail against the broken behavior* before it is trusted green — a test that has only ever passed may be asserting nothing.
- **test discovers the project's own runner; it names no tool.** It reads how this codebase already runs and structures tests and uses that, rather than assuming a framework. If there is no runnable suite and no way to author one (no language runtime, no test surface), that is a stated stop, not a silent pass.
- **`--changed` assumes a version-controlled working tree.** With no diff to derive (not a repo, or nothing changed), it falls back to the framed surface and says so.
</content>
