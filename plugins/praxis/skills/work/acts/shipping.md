# Shipping

**Entry condition.** The request is to take finished work into its integration target and, where an environment deploys from it, out to that environment. The work is built and verified, and where the team requires review, the review is approved. Only merging, or only rolling out a change that's already merged, goes to the [land](../../land/SKILL.md) or [roll-out](../../roll-out/SKILL.md) skill directly. (basis: maintainer, 2026-09-30)

**Done when** the change is merged into its target, rolled out to the environment the request or the task names with a health verdict (or recorded as not rolled out, with why, when none is named), and the outcome has been reported to the change's owners. A health verdict of `not checked` ([results-and-certainty](../../../craft/evidence/results-and-certainty.md)) carries its reason and is reported as health unread, never as a healthy ship. A run that rests at awaiting-review or stopped-on-failure isn't done: what its outcome names becomes the task's next step. (basis: derived from the steps' outcomes)

## A hotfix keeps its floor

Hand roll-out the landing type land assigned. When the task came to shipping from responding to an incident, the landing type is hotfix whatever land read off the diff, since the incident is why the change exists. (basis: derived from make-rollout-reversible's hotfix floor)

## Steps

(basis: maintainer, 2026-09-30)

| # | step | inputs | skipped by the act when |
|---|---|---|---|
| 1 | [land](../../land/SKILL.md) | the change (its branch or its review request), `--into=<branch>` when the request or the task names a target, and, when the task that built the change has a record, `--message=<text>`: the merge or squash commit's message, written to [commits-tell-the-why](../../../craft/engineering/commits-tell-the-why.md) from that record's current state and its rounds' decisions (basis: maintainer, 2026-10-07) | never |
| 2 | [roll-out](../../roll-out/SKILL.md) `--target=<env>` | the branch step 1 merged into, step 1's landing type, the environment the request or the task names, and the service's dashboards or alerts the task or the project's runbook names, for its health verdict | step 1's outcome isn't merged, or neither the request nor the task names an environment |

When step 1 doesn't merge, step 2 is skipped by its condition and the act stops, with step 1's outcome as the task's next step. A health verdict of `fails` doesn't roll back on its own: roll-out keeps its default failure policy unless the request names one, and the report tells the owners what the verdict calls for. (routed to maintainer: no automatic rollback in the act, since reversing production is an outward action the request should choose; a request that wants one says `--on-fail=rollback`.)

## Shipping a task's change

When the change was built by a task of an act that authors a change, shipping runs as that task's ship round ([open-the-task](../phases/02-open-the-task.md)), and its review requests not yet merged ship base-most first. Each goes through step 1 with a `--message` written from what that request carries. Once one merges, the next has its base changed to the target through [vcs](../../vcs/SKILL.md) before its own step 1. Step 2 runs once the last has merged, and also after any request the latest plan's rollout rolls out on its own, each time covering every request merged since the last roll-out, with the first of their landing types in land's order, hotfix, then feature, then chore; each roll-out is handed to document with the requests it covered. A request that doesn't merge stops the act there. When the ship round closes with the change merged, its close-out filing gives the task record the shipped status its [type](../../document/rules/types/task-record.md) sets, and hands each decision record the change carries back with its status set to accepted, updated in place. (basis: maintainer, 2026-10-07)

## Filed

Both steps' results file as the round's ship notes: what merged where, the gate status, the rollout and its exposure, and the health verdict with the signals behind it. (basis: derived from the document types' membership tests)

## Delivered

Close-out reports the outcome to the change's owners through [communication](../../communication/SKILL.md), routed and shaped by [report-to-where-it-matters](../rules/report-to-where-it-matters.md): what landed and where, the gate status, the rollout and its health verdict, and what the owners should do when it doesn't hold. (basis: maintainer, 2026-07-11) A ship round that runs close-out more than once reports at each what was reached since the last report, its channel's part naming each request it covers with what that request reached, `ship report · 405 merged · 406 awaiting review`, so each is a channel of its own. (basis: maintainer, 2026-10-07)
