# Shipping

**Entry condition.** The request is to take finished work into its integration target and, where an environment deploys from it, out to that environment. The work is built and verified, and where the team requires review, the review is approved. Only merging, or only rolling out a change that's already merged, goes to the [land](../../land/SKILL.md) or [roll-out](../../roll-out/SKILL.md) skill directly. (basis: maintainer, 2026-09-30)

**Done when** the change is merged into its target, rolled out to the environment the request or the task names with a health verdict (or recorded as not rolled out, with why, when none is named), and the outcome has been reported to the change's owners. A run that rests at awaiting-review or stopped-on-failure isn't done: what its outcome names becomes the task's next step. (basis: derived from the steps' outcomes)

## A hotfix keeps its floor

Hand roll-out the landing type land assigned. When the task came to shipping from responding to an incident, the landing type is hotfix whatever land read off the diff, since the incident is why the change exists. (basis: derived from make-rollout-reversible's hotfix floor)

## Steps

(basis: maintainer, 2026-09-30)

| # | step | inputs | skipped by the act when |
|---|---|---|---|
| 1 | [land](../../land/SKILL.md) | the change (its branch or its review request), and `--into=<branch>` when the request or the task names a target | never |
| 2 | [roll-out](../../roll-out/SKILL.md) `--target=<env>` | the branch step 1 merged into, step 1's landing type, and the environment the request or the task names | step 1's outcome isn't merged, or neither the request nor the task names an environment |

When step 1 doesn't merge, step 2 is skipped by its condition and the act stops, with step 1's outcome as the task's next step. A needs-rollback verdict doesn't roll back on its own: roll-out keeps its default failure policy unless the request names one, and the report tells the owners what the verdict calls for. (routed to maintainer: no automatic rollback in the act; a request that wants one says `--on-fail=rollback`.)

## Filed

Both steps' results file as the task's ship notes: what merged where, the gate status, the rollout and its exposure, and the health verdict with the signals behind it. (basis: derived from the document types' membership tests)

## Delivered

Close-out reports the outcome to the change's owners through [communication](../../communication/SKILL.md), routed and shaped by [report-to-where-it-matters](../rules/report-to-where-it-matters.md): what landed and where, the gate status, the rollout and its health verdict, and what the owners should do when it isn't healthy. (basis: maintainer, 2026-07-11)
