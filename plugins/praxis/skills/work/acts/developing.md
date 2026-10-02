# Developing

**Entry condition.** The request is to build new behavior or change existing behavior in the requester's own code: a feature, a change to how something works, what an approved spec or ticket asks for. Fixing a defect goes to the fixing-a-bug act, and keeping code healthy without changing its behavior to maintaining. One step on its own that changes no code — only specifying, only planning — goes to that step's skill directly; a change to code always runs inside an act. (basis: maintainer, 2026-09-30)

**Done when** every unit of the change is built, tested — step 6's verdict PASS — verified — step 7's headline `works`, or step 7 skipped because no flow reaches the unit, or its run-level `no-observable-surface`, which says the same and is recorded as that, never as `works` — and has passed review by [open-the-review-request](../rules/open-the-review-request.md)'s test; each unit's review request, its description written from the task's documentation, has been approved by its reviewers, read through [vcs](../../vcs/SKILL.md) or, where no host carries the request, confirmed by the user; and, when step 4 ran, the units are filed where the team tracks work. A request still waiting on its reviewers, or one that came back with changes requested, isn't done: the wait or the changes are the task's next step, and the task stays open. (basis: derived from the steps' outcomes) (routed to maintainer: the task stays open through review, since feedback that re-enters the same task keeps its record whole.)

## Intent first

When the task takes over someone else's branch, their claims about it ("this part is done") are rationale, checked after your own look ([form-your-own-view-first](../../../craft/evidence/form-your-own-view-first.md)). A changed requirement reopens the spec and its traceability row before another unit is built. (basis: maintainer, 2026-09-30)

## The small-change path

A change with no behavior change and no new interface — a typo, a comment, a rename inside one unit — runs develop on the request itself, as its one unit with the request as its done-condition, then verify where a flow reaches the change. Every other step is skipped by this condition, and the review request opens once develop has landed the change and verify, where it ran, shows it `works`, its description saying no review step ran. The path is done when that request is approved. (basis: maintainer, 2026-09-30) (routed to maintainer: the two conditions, as a typo fix meets them, since a change that alters no behavior and no interface has nothing a spec would add.)

## After approval

Before step 1, [give the task a branch](../rules/give-the-task-a-branch.md).

## Steps

(basis: maintainer, 2026-09-30)

| # | step | inputs | skipped by the act when |
|---|---|---|---|
| 1 | [understand](../../understand/SKILL.md), with the intent as its question, and `--from-code=<the code>` when the intent names code | the intent, and any code it names | the small-change path |
| 2 | [spec](../../spec/SKILL.md), with `--from-issue` when the intent is a tracker item, or `--from-discussion` when it's a conversation | the intent's sources, a ticket file in the repository read as written | the small-change path, or the intent already includes an approved spec: a spec the intent links whose approval is recorded on it, or the spec this task filed and its owner approved. A ticket's acceptance criteria are spec's input, never an approved spec |
| 3 | [plan](../../plan/SKILL.md) `--from-spec=<the spec>` | the spec, and step 1's map | the small-change path |
| 4 | [decompose](../../decompose/SKILL.md) | the plan | the small-change path, or the plan names a single unit within decompose's size bar ([unit-size-scale](../../decompose/rules/unit-size-scale.md)) |
| 5 | [develop](../../develop/SKILL.md) `--from-plan=<the plan>` | the unit, with its done-condition, and step 1's map | never |
| 6 | [test](../../test/SKILL.md) `--changed --from-spec=<the spec>` | the unit's acceptance criteria | the small-change path |
| 7 | [verify](../../verify/SKILL.md) `--from-spec=<the spec>` | the spec's requirements the unit implements | the unit reaches no flow a user or an external caller runs |
| 8 | [review](../../review/SKILL.md) `--changed` | the unit's change, and its rationale | the small-change path |

Steps 5 to 8 run once per unit, in decompose's order. When a unit's review request comes back with changes requested — read through [vcs](../../vcs/SKILL.md)'s *read a review request* when the task resumes — run step 5 on that feedback, then steps 6 to 8 again. (basis: maintainer, 2026-09-30)

When step 5 fails — develop couldn't land the unit — the act stops at that unit, with the blocker as the task's next step. When step 6's verdict is FAIL, step 7's headline is `defective`, or the unit doesn't pass step 8, the unit goes back to step 5 with that step's whole result as its input — its failures, its defective units, or the review's fitness gap and findings at high and above — and steps 6 to 8 run again; after the second failed pass, the act stops at that unit with its last result as the task's next step. A result that settles nothing — step 6 INCONCLUSIVE, step 7 `blocked`, `indeterminate` or `framing-unestablished` — sends nothing back: its gap becomes the unit's next step, and the unit isn't tested or verified until it's settled. The steps after it still run, and the review request opens with the gap stated in its description; the task isn't done until the gap is settled. (routed to maintainer: two passes before stopping, since a second failure on the same change says it needs more than another try.)

When step 3's plan returns an open sign-off ([planning-rollout](../../plan/phases/05-planning-rollout.md)), steps 4 to 8 build on the plan, and close-out puts the sign-off to the maintainer: the task isn't done until it's recorded.

## Filed

Step 1's map and each unit's step 5 to 7 results file as sections of the task's scratchpad. Step 2 files as the spec, step 3 as the plan (with a decision record for each of its one-way doors), step 4's units in the plan, and step 8 as the review record. document keeps the traceability table as these arrive. When the change adds or changes something a person who uses that part without reading its code needs — an operator, an integrator, a caller — the task also files that part's system documentation, from the steps' results, at close-out: a reference page for a format, endpoint, setting or command it adds or changes, an explanation page for a flow, a state or an interaction between parts it changes, and a how-to for an operation someone performs that it adds. A change only to internals no such reader meets files none. (basis: maintainer, 2026-09-30)

## Delivered

- **The units.** File them as work-items per [file-the-units-as-work-items](../rules/file-the-units-as-work-items.md), when step 4 ran.
- **Each unit's review request.** Open it per [open-the-review-request](../rules/open-the-review-request.md) once the unit passes step 8 — on the small-change path, as that path says.
- **The work-item the task traces to.** Update it through [project-mgmt](../../project-mgmt/SKILL.md) to show the change is in review.
