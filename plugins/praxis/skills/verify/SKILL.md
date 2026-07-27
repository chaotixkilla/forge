---
name: verify
description: Establish that a change actually works by driving the real running application end-to-end and observing its behavior — stand the app up, exercise each framed flow through the entry point a user actually uses, separate a genuine behavioral defect from environment noise, and return a per-flow verdict with reproductions. Reach for it when the suite is green and the question is whether the thing works; distinct from test (authors and runs the automated suite, never drives the app), from debug (root-causes a failure already known), and from operate (owns live production, not a pre-landing check).
metadata:
  flags:
    --from-spec=<path>: derive the flows to exercise from a spec's requirements, and report per requirement rather than per flow — a phase input, not a module
    --flows=<list>: exercise only these named flows instead of the set framed from the change; names are the project's own (checkout, password-reset), so the domain is open by design
    --ux: add an experiential pass — walk each flow as a first-time user and record every point of confusion, not just whether it functioned (activates ux-walkthrough)
    --as-user=<persona>[,<persona>...]: experience each flow as each named persona, including users of assistive technology, and report what that user encounters — one drive and one graded unit per persona (activates as-user)
    --sandbox: stand the app up in a disposable, isolated environment so the run cannot touch real state (activates isolated-sandbox)
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

verify owns no backend and needs none: standing up and driving a local application is **ambient** — the same way [develop](../develop/SKILL.md) reads the working tree — so it declares no `config_requires` and touches no external capability. Routing a verdict to people is [communicate](../communicate/SKILL.md)'s job, not a flag here. `--ux` adds an experiential pass: see [modules/ux-walkthrough.md](modules/ux-walkthrough.md). `--as-user` re-runs the flows in each named user's shoes: see [modules/as-user.md](modules/as-user.md). `--sandbox` isolates the running instance: see [modules/isolated-sandbox.md](modules/isolated-sandbox.md).

The distinction that defines this skill: a green suite proves the code passes the checks someone wrote for it; verify proves the *application does the thing*. Those come apart constantly — a flow that every unit test covers and that nobody can complete, a feature wired to no reachable entry point, a build that works and a page that never renders. So verify's evidence is always an observation of a running system, never a reading of the code, and it drives that system the way a user reaches it rather than through a harness ([reach-the-real-entry-point](rules/reach-the-real-entry-point.md)).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies, and phase 5 is gated on the verdict scale.

1. Frame the observation: name the claim about running behavior under check and the concrete flows that would settle it — derived from the change, or from a spec under `--from-spec`, or given by `--flows`  — see [phases/01-frame-the-observation.md](phases/01-frame-the-observation.md)
2. Stand the app up: get a real instance running and reachable, establish how a user reaches each flow, and record the environment the observation is scoped to  — see [phases/02-stand-the-app-up.md](phases/02-stand-the-app-up.md)
3. Exercise the flows: drive each framed flow end-to-end through the real entry point, recording what was actually observed at each step rather than what should have happened  — see [phases/03-exercise-the-flows.md](phases/03-exercise-the-flows.md)
4. Separate defect from environment: for every flow that did not behave as claimed, establish whether the fault is in the change or in the setup around it, and confirm a genuine defect reproduces  — see [phases/04-separate-defect-from-environment.md](phases/04-separate-defect-from-environment.md)
5. Report the verdict: assign each flow a verdict from the four defined levels, attach a reproduction for every defect, and hand off rather than fix  — see [phases/05-report-the-verdict.md](phases/05-report-the-verdict.md)
