# roll-out — usage

Take a change that is already merged into its integration target and roll it out to a named environment: check that the environment deploys from that branch, choose a rollout strategy sized to the change's risk, promote it, confirm it arrived, and judge whether its health holds there.

## When to use
- A change is merged and you want it in an environment in a way you can undo fast if it misbehaves.
- You want the rollout's pace set by how hard the change is to take back, not by habit: small increments, staged exposure, or behind a switch.
- You want an honest health verdict from the post-ship signals, on the shared results scale ([results-and-certainty](../../craft/evidence/results-and-certainty.md)): holds, fails, unsettled when there isn't enough signal to tell, or not checked when no signal could be read.

## Not for / use instead
- Merging the change into its integration target → **land**.
- Carrying a change from finished to merged to rolled out, with the outcome reported to the change's owners → the shipping act in **work**.
- Restoring a service that is already failing → the incident act in **work**, whose mitigation may roll a change back.
- Driving the running application to check behavior → **verify**.

## Examples
`--target=staging` — roll out to staging, at the pace the change's risk tier sets.
`--target=production --watch` — roll out to production and stay attached until the rollout and the post-ship signals settle.
`--target=production --on-fail=rollback` — reverse the deployment if the rollout fails or the health verdict fails.
`--target=production --dry-run` — report the strategy and the promotion that would run, without promoting.

## Gotchas
- **roll-out needs no configuration of its own.** Promotion goes through `ci`, which owns `tools.ci`, and the health read through `telemetry`, which owns `tools.telemetry`. With no `tools.ci`, nothing is promoted and the result says why; with no `tools.telemetry`, the rollout stands but the health verdict is not checked.
- **No environment, no rollout.** Without `--target`, roll-out promotes nothing: there is no default deploy environment.
- **An environment ships only from the branch it deploys from.** `--target=production` on a change merged into `develop` doesn't promote when production deploys from `main`; the result says the rollout waits for the change to reach that branch.
- **One pass, not a ramp driver.** A staged or behind-a-switch rollout rests at the stage this run reaches and reports what remains; it doesn't block to drive the ramp to full exposure.
- **Unsettled is an answer.** Too little signal to judge is reported as unsettled, never rounded up to holds.
