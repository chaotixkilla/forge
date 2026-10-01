---
name: roll-out
description: Take a merged change from the shared line out to an environment — check the environment deploys from that line, size a reversible rollout strategy to the change's risk, promote it through the pipeline, confirm it arrived, and judge from its post-ship signals whether it's healthy there. Returns the rollout outcome and the health verdict; reporting them is the caller's job.
metadata:
  flags:
    --target=<env>: the environment to roll out to; without one nothing rolls out, since no default deploy environment exists (a phase input read by assess-the-rollout)
    --watch: stay attached through the rollout and the post-ship signal window until they settle, then return the settled verdict (activates watch-the-pipeline)
    --on-fail=<abort|continue|ask|rollback>: policy for a failed rollout or a needs-rollback verdict, overriding the default stop-and-report (activates failure-policy)
    --dry-run: report the environment, the strategy and the promotion that would run, without promoting
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies. roll-out owns no backend of its own: it promotes and awaits runs through the [ci](../ci/SKILL.md) skill and reads post-ship signals through the [telemetry](../telemetry/SKILL.md) skill, each the doer that owns its own prerequisite.

`--on-fail=<policy>` sets what happens when the rollout fails or its health verdict is needs-rollback: see [modules/failure-policy.md](modules/failure-policy.md).

1. Assess the rollout: confirm the named environment deploys from the branch the change merged into, and assign the change's risk tier, raised for a hotfix  — see [phases/01-assess-the-rollout.md](phases/01-assess-the-rollout.md)
2. Promote: roll the change out at the pace its risk tier sets, through any environment gating, and confirm it reached the scope this run promotes to  — see [phases/02-promote.md](phases/02-promote.md)
3. Confirm it's healthy: read the post-ship signals against their baseline, reach the health verdict, and return the run's outcome  — see [phases/03-confirm-healthy.md](phases/03-confirm-healthy.md)
