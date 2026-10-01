# Fixing a bug

**Entry condition.** The request is to find and remove the cause of a defect that has already shown itself — a failure, a wrong result, a crash, a regression. Only diagnosing it goes to the [debug](../../debug/SKILL.md) skill directly, and restoring a live production service first to the incident act. (basis: maintainer, 2026-09-30)

**Done when** the cause is confirmed, the fix sits at it with a guard that fails without the fix and passes with it, the original reproduction no longer triggers, the fix is verified where a flow reaches the defect — step 4's headline `works`, or step 4 skipped because no flow reaches it — the change has passed review by [open-the-review-request](../rules/open-the-review-request.md)'s test, and its review request has been approved, read through vcs or, where no host carries it, confirmed by the user; a request still waiting on its reviewers is the task's next step. A diagnosis that isn't confirmed isn't done: the evidence that would confirm it becomes the task's next step. (basis: derived from the steps' outcomes)

## Fix only a confirmed cause

Step 2 runs only at a cause step 1 confirmed: a mechanism you can toggle the failure on and off with ([root-cause-confidence](../../debug/rules/root-cause-confidence.md)). A probable cause is fixed only in a task that is responding to an incident, and the fix is recorded as provisional until the cause is confirmed. A suspected cause is never fixed: the act stops, with the evidence that would confirm it as the next step. Fixing an unconfirmed cause is how a new bug ships while the original survives. (basis: maintainer, 2026-07-10)

## When the fix needs design

When step 1's recommended fix needs design work — a new abstraction, an interface or contract change that ripples across call sites, a cross-cutting refactor — the act stops after step 1 and the task continues as developing, with the diagnosis as the spec's input. (basis: maintainer, 2026-07-10)

## After approval

Before step 1, give the task a branch: when the work starts on the integration line, cut one from its head, named for the task's key, and run every step on it; work already on a branch of its own stays there, and on resume, a task whose branch exists checks it out instead of cutting another. Nothing the act builds reaches the integration line except through a review request. (basis: derived from open-the-review-request's no-direct-merge)

## Steps

(basis: maintainer, 2026-09-30)

| # | step | inputs | skipped by the act when |
|---|---|---|---|
| 1 | [debug](../../debug/SKILL.md), with `--from-incident`, `--from-telemetry` or `--from-logs` when the request carries one | the symptom, and its reproduction or seed | the request carries a cause already confirmed with evidence |
| 2 | [develop](../../develop/SKILL.md) | step 1's mechanism and its recommended fix: the altitude, and the change | the cause isn't confirmed, or the fix needs design (above) |
| 3 | [test](../../test/SKILL.md) `--changed` | the guard step 1 names, which must fail without the fix and pass with it, and the original reproduction, re-run | never |
| 4 | [verify](../../verify/SKILL.md) | the flows the defect reaches | the defect reaches no flow a user or an external caller runs |
| 5 | [review](../../review/SKILL.md) `--changed` | the fix, and step 1's diagnosis | never |

When step 2 fails — develop couldn't land the fix — the act stops, with the blocker as the task's next step. When step 3's verdict is FAIL, step 4's headline is `defective`, or the fix doesn't pass step 5, the fix goes back to step 2 with that step's whole result as its input, and steps 3 to 5 run again; after the second failed pass, the act stops with its last result as the task's next step. A result that settles nothing — step 3 INCONCLUSIVE, step 4 `blocked`, `indeterminate` or `framing-unestablished` — sends nothing back: its gap becomes the task's next step. (routed to maintainer: two passes before stopping.)

## Filed

Step 1's diagnosis — the mechanism, its confidence, the blast radius and the reproduction — and steps 2 to 4's results file as sections of the task's scratchpad, and step 5's result as the review record. (basis: derived from the document types' membership tests)

## Delivered

- **The review request.** Open it per [open-the-review-request](../rules/open-the-review-request.md).
- **The work-item the bug traces to.** Update it through [project-mgmt](../../project-mgmt/SKILL.md) to show the fix is in review.

In a task that is responding to an incident, the change ships next as a hotfix, through the shipping act.
