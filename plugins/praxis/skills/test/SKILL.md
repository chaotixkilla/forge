---
name: test
description: Establish whether a change does what it should by designing meaningful test coverage and observing real behavior — frame the claim under test, map the existing suite, design the cases that actually discriminate (prioritized by risk), run the project's own suite, separate genuine failures from flakes and environment noise, and report a verdict with coverage gaps and residual risk. Authors and runs tests and reports the verdict; its deliverable never includes a production-code change (fixing a failure is develop/debug) and it does not drive the running app to observe it (that is verify).
metadata:
  flags:
    --changed: scope the run to what the working-tree diff touched (changed files plus their reverse-dependents) rather than the whole surface — a phase input to framing/mapping, not a separate mode
    --from-spec=<path>: treat a spec file as the source of the claim under test — map each acceptance criterion to a concrete pass/fail check — instead of deriving the claim from the change; a phase input to framing
    --until=<condition>: loop the verification until a stop condition is met (first failure, green, or a repeat count) instead of a single pass — activates the run-until-signal module
    --sandbox: run in a disposable, network/filesystem-isolated local environment with seeded fixtures, so the run is reproducible and side-effect-free — activates the isolated-sandbox module
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

test owns no backend of its own: it is config-less. Running the project's suite and observing its behavior is in-environment execution (it discovers and runs the project's own test command, it declares no runner backend), `--changed` derives from the local working-tree diff, and `--sandbox` is resolved locally (a disposable scratch environment). So it declares no `config_requires`. It is a leaf: it returns the verdict to its caller and invokes no downstream skill.

`--until=<condition>` reshapes [run-and-observe](phases/05-run-and-observe.md) — loop rather than a single pass: see [modules/run-until-signal.md](modules/run-until-signal.md). `--sandbox` reshapes the execution environment established in [set-up-the-harness](phases/04-set-up-the-harness.md): see [modules/isolated-sandbox.md](modules/isolated-sandbox.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies.

1. Frame what to verify: pin the claim under test — what behavior must hold, at what test level, and what "passing" concretely means for this change — derived from the spec or the change, not guessed  — see [phases/01-frame-what-to-verify.md](phases/01-frame-what-to-verify.md)
2. Map the surface: locate the code paths, seams, and existing test conventions the change touches; find where tests live and how this codebase already exercises similar surfaces  — see [phases/02-map-the-surface.md](phases/02-map-the-surface.md)
3. Design the cases: enumerate the cases that actually discriminate — happy path, boundaries, failure modes, counter-examples that must NOT pass — prioritized by risk and pruned of redundancy, against a defined coverage-adequacy bar  — see [phases/03-design-the-cases.md](phases/03-design-the-cases.md)
4. Set up the harness: establish fixtures, doubles, and the execution environment so cases run deterministically and in isolation; decide what is real vs. stubbed at each boundary  — see [phases/04-set-up-the-harness.md](phases/04-set-up-the-harness.md)
5. Run and observe: execute the suite, watch real behavior, and separate genuine failures from flakes and environment noise before drawing conclusions  — see [phases/05-run-and-observe.md](phases/05-run-and-observe.md)
6. Report the verdict: state pass/fail against the framed claim, attach reproductions for failures, and surface coverage gaps and residual risk left unverified  — see [phases/06-report-the-verdict.md](phases/06-report-the-verdict.md)
</content>
</invoke>
