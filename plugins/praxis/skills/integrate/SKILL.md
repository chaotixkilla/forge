---
name: integrate
description: Get finished work safely into the trunk and out to production — stage coherent commits, reconcile with the latest trunk and resolve conflicts, pass the pre-merge gate, land via direct merge or a review request, then roll out to a target environment and confirm the change is healthy where it landed. Reach for it once a change is written and reviewed and you need it landed and shipped — not while building it (develop), judging it (review), or responding to a production incident (operate).
metadata:
  flags:
    --pr: land via a review request instead of a direct merge — assemble the description, link the originating work, route to reviewers (activates open-for-review)
    --commit: stop after recording coherent local commits; do not push, open, or merge anything (activates commit-only)
    --message=<text>: use the caller-supplied text as the commit/PR message verbatim instead of synthesizing one (a phase input read by prepare-the-increment and land-it)
    --watch: stay attached after landing/shipping — poll the run and post-ship signals until they settle, then report (activates watch-the-pipeline)
    --into=<branch>: land into a specific integration target (e.g. an epic or `develop` branch) instead of the derived one; the target defaults to the branch this work is based on, else the trunk (a phase input read by assess-the-change)
    --target=<env>: direct the ship phase at a named environment, resolving its promotion path and gating (activates promote-to-environment)
    --gate: force the pre-merge gate to run and block on it even when the default flow would skip or soft-pass it (activates require-explicit-gate)
    --on-fail=<abort|continue|ask|rollback>: policy for a failed gate or rollout, overriding the default stop-and-report (activates failure-policy)
    --dry-run: plan and report the full landing/ship path — commits, reconcile, gate, merge, rollout — without performing any mutation
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies. integrate owns no backend of its own: it delegates every *hosted* version-control operation — push a ref, open or merge a PR, set a status — to the `vcs` skill (local staging and the local commit are ambient plain git, done directly), every pipeline operation to the `ci` skill, and its post-ship read / channel report / work-item link to the `telemetry`, `communication`, and `project-mgmt` skills — so it declares no `config_requires`.

`--on-fail=<policy>` sets what happens when the gate or a rollout fails, across the gate and ship phases both: see [modules/failure-policy.md](modules/failure-policy.md).

1. Assess the change: survey what is actually changing vs. the integration target — diff scope, branch state, divergence from the resolved target (an epic branch, `develop`, or the trunk), and the landing type that forks the rest of the run  — see [phases/01-assess-the-change.md](phases/01-assess-the-change.md)
2. Prepare the increment: shape the local work into landable units — stage coherent commits, reconcile with the latest target, and resolve conflicts before anything leaves the machine  — see [phases/02-prepare-the-increment.md](phases/02-prepare-the-increment.md)
3. Run the gate: put the change through the pre-merge checks and require they pass before proceeding  — see [phases/03-run-the-gate.md](phases/03-run-the-gate.md)
4. Land it: integrate into the shared line via the vcs capability — open the change for review or merge it, attaching the context reviewers need  — see [phases/04-land-it.md](phases/04-land-it.md)
5. Ship to target: promote the merged change to the requested environment, choosing a rollout strategy sized to the change's risk, and confirm it reached the target  — see [phases/05-ship-to-target.md](phases/05-ship-to-target.md)
6. Confirm and report: watch post-ship signals via the telemetry capability, judge whether the change is healthy where it landed, and report the outcome to the right channel and people  — see [phases/06-confirm-and-report.md](phases/06-confirm-and-report.md)
