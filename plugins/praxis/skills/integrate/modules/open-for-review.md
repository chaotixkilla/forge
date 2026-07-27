# open-for-review (`--pr`)

Activated by `--pr`, referenced from [land-it](../phases/04-land-it.md).

The base landing merges the reconciled, green change directly into the shared line. This module changes *how the change lands*: instead of a direct merge, open it as a review request and stop there, so a human approves before it merges. Deletion test: remove this module and integrate still lands by direct merge; opening a review request is an alternate landing sink a flag selects, which is why it is a module and not part of the land phase.

## The delta — open a change for review instead of merging

- **Open the change for review through the vcs capability.** Push the branch (if not already pushed) and open a review request against the integration line, through the [vcs](../../vcs/SKILL.md) capability's operations; the dispatch resolves to whichever provider is configured. The direct merge does **not** happen — landing terminates at *opened-for-review*, and the merge becomes a human's call on the request.
- **Assemble the description.** Compose the request's title and body to carry the why and the shape of the change, not a restatement of the diff ([commits-tell-the-why](../rules/commits-tell-the-why.md)); if `--message=` was supplied, use it verbatim as described in [prepare-the-increment](../phases/02-prepare-the-increment.md). Scope the request to one coherent concern ([one-coherent-change-per-unit](../rules/one-coherent-change-per-unit.md)) — a request bundling unrelated changes is split, not opened as one.
- **Link the originating work.** If the change traces to a tracked work-item, link it through the [project-mgmt](../../project-mgmt/SKILL.md) capability's *fetch a work-item* operation (to resolve the item's reference) so the request points back to the work it closes.
- **Route to reviewers.** Derive reviewers from the team/ownership data in config — the owners of the area the diff touches ([report-to-where-it-matters](../rules/report-to-where-it-matters.md) resolves ownership the same way) — and request their review. Where ownership is unresolvable, open the request without an assignee rather than blocking, and say so.

## Composition and mutual exclusion

- **`--commit` is mutually exclusive with `--pr`** — one stops before pushing, the other pushes and opens a request. Refuse the combination up front ([commit-only](commit-only.md)), rather than silently honoring one.
- **`--target`/`--watch`** still apply *after* the request merges, not now: opening a review request is a landing terminus for *this* run. If the caller wants ship-on-merge, that is a follow-up run once the request is approved and merged — say so rather than promoting an unmerged change.

## Prerequisite and degrade

`--pr` is a landing path that *requires* the vcs capability — there is no local fallback for "open a review request," so this is the one integrate path where a missing vcs backend **blocks** the requested landing rather than narrowing it. Invoke the [vcs](../../vcs/SKILL.md) capability (which owns `tools.vcs` — doer-owns-prerequisites; integrate declares none); if it reports the backend unavailable, report plainly that the review request could not be opened (the `vcs` skill owns guiding the user through `init:vcs`) and do **not** silently fall back to a direct merge, which would land unreviewed work the caller explicitly wanted reviewed. `(basis: mirrors review's --pr degrade — a path whose whole purpose is the backend has nothing to fall back to; the doer-owns-prerequisites shed is the ratified port pattern.)`

The originating-work **link** degrades independently: if the [project-mgmt](../../project-mgmt/SKILL.md) capability is unavailable (`tools.project_mgmt` unconfigured), open the request **without** the link and note it, rather than blocking the landing on a missing tracker. `(basis: the link is additive context, not the landing itself — decompose's --ticket degrade-not-block posture applied to an additive link, ratified 2026-07-10.)`
