# Open the review request

An act that changed code delivers the change for review; it doesn't merge it. A change merged without a reviewer's look is the review the team never got, and a review request whose description restates the diff gives the reviewer nothing the diff didn't. This rule is how the developing, fixing-a-bug and maintaining acts deliver.

## Open it

- **Through the vcs capability.** Push the branch if it isn't pushed yet, and open a review request against the change's integration line through the [vcs](../../vcs/SKILL.md) port, which resolves to whichever provider is configured. Nothing merges: the merge is a human's call on the request, and shipping is a later act.
- **One coherent concern per request.** A request that bundles unrelated changes is split, not opened as one.

## When a change has passed review

A change passes its review step when review's fitness verdict is *satisfies* and no finding at high or above stands — the floor review's own gate blocks on. A change that doesn't pass goes back to its build step with the review's result as input — its fitness gap and its findings at high and above — and the steps after it run again; the act file says when the loop stops. A finding below high doesn't hold the request: it goes into the description, for the reviewer. (routed to maintainer: high as the floor, matching review's gate default.)

## Write the description from the task's documentation

The description belongs to the request and is addressed to people who never open praxis, so it carries the work and none of the machinery that produced it ([clean-export](../../../craft/writing/clean-export.md)). Write it from the task's documentation, not from the diff: what the change does and why, the decisions it makes with the reasons that decided them ([preserve-the-why](../../../craft/writing/preserve-the-why.md)), how it was verified, and what a reviewer should check. Link the task's documentation for the rest, where the reviewer can open it — a page backend's page, or, on the local backend, the task's pages, committed on the change's branch in their own commit just before the request opens — and never paste it whole. (basis: maintainer, 2026-09-30)

## Link the originating work, and route it to reviewers

- **The work-item.** When the change traces to a tracked work-item, resolve its reference through the [project-mgmt](../../project-mgmt/SKILL.md) port and link it, so the request points back to the work it closes.
- **The reviewers.** Request review from the owners of the area the diff touches, resolved from the team roster's ownership the way [report-to-where-it-matters](report-to-where-it-matters.md) resolves it. Where ownership can't be resolved, open the request without an assignee and say so, rather than blocking.

## Degrade

A review request has no local substitute. When the vcs port reports its backend unavailable, say plainly that the request couldn't be opened, leave the change committed on its branch, and make opening it the task's next step; the description is finished content, so it's kept with the task's documentation and returned for hand delivery ([deliver-through-the-ports](deliver-through-the-ports.md), degraded-return). Never fall back to a direct merge, which would land unreviewed work the act exists to put in front of a reviewer. Without the project-mgmt port, open the request unlinked and say so. (basis: the ratified doer-owns-prerequisites port pattern; degrade-not-block for the work-item link, ratified 2026-07-10)
