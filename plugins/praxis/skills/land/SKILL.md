---
name: land
description: Get a finished change into the shared line safely — shape it into coherent commits, reconcile it with the current target and resolve conflicts, pass the pre-merge gate, and merge it, stopping where the target needs an approved review the change doesn't have. Returns the landing outcome; reporting it is the caller's job.
metadata:
  flags:
    --commit: stop after recording coherent local commits; nothing is pushed, gated or merged (activates commit-only)
    --message=<text>: use the caller-supplied text as the commit message verbatim instead of synthesizing one (a phase input read by prepare-the-increment and merge)
    --into=<branch>: land into a specific integration target (an epic or `develop` branch) instead of the derived one; without it, assess-the-change resolves the target from durable records, else the trunk (a phase input read by assess-the-change)
    --gate: force the pre-merge gate to run in full and block on anything short of green, even where the flow would narrow or soft-pass it (activates require-explicit-gate)
    --on-fail=<abort|continue|ask|rollback>: policy for a failed gate or a failed landing, overriding the default stop-and-report (activates failure-policy)
    --dry-run: plan and report the commits, reconcile, gate and merge without performing any of them
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies. land owns no backend of its own: it delegates every hosted version-control operation (push a ref, read the target's landing constraint, merge) to the [vcs](../vcs/SKILL.md) skill and the hosted pipeline to the [ci](../ci/SKILL.md) skill, each the doer that owns its own prerequisite. Local staging, committing and reconciling are ambient.

`--on-fail=<policy>` sets what happens when the gate or the landing fails: see [modules/failure-policy.md](modules/failure-policy.md).

1. Assess the change: survey what is changing against the integration target — diff scope, branch state, divergence from the resolved target, the team's flow — and classify the landing type that forks the rest of the run  — see [phases/01-assess-the-change.md](phases/01-assess-the-change.md)
2. Prepare the increment: shape the local work into coherent commits, reconcile with the target's live head, and resolve conflicts before anything leaves the machine  — see [phases/02-prepare-the-increment.md](phases/02-prepare-the-increment.md)
3. Run the gate: put the reconciled change through the pre-merge checks and require that they pass  — see [phases/03-run-the-gate.md](phases/03-run-the-gate.md)
4. Merge: integrate the green change into the target by the team's flow, through an approved review request where the target requires one, and return the run's outcome  — see [phases/04-merge.md](phases/04-merge.md)
