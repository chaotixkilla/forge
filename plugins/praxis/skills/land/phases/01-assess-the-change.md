A landing that starts before it knows *what* it is landing merges blind: it gates the wrong base and merges into a branch the change was never headed for.

## Survey the change against the integration target

Establish the ground facts before judging anything:

- **Diff scope** — what files, components, and surfaces the change touches. Recruit the **code explorer** to locate the touched symbols and their callers/callees (the blast radius), and the **repository explorer** for recent history near the changed lines (a prior attempt, a revert, a linked discussion). Without fan-out, do these reads inline. This is the raw material for the landing type. Recruit only as [fan-out-only-when-it-pays](../../gather/rules/fan-out-only-when-it-pays.md) allows.
- **The integration target** — the branch this work lands *into*, resolved from **durable records only**, never an ancestry guess. Precedence, first match wins — and the same first-match order governs the sub-sources within a tier when both exist and disagree: (1) an explicit `--into=<branch>`; (2) else the target **recorded** for this branch, taking the stronger merge-intent signal first — an open review request's base branch (read through [vcs](../../vcs/SKILL.md)'s *read a review request* for this branch), which is the *explicit* statement of where this change is headed, else a configured parent/integration ref the tooling keeps; (3) else the repository's default branch (the trunk) — the remote's default head, or the local default branch when there's no remote, never assumed to be `main`. Do **not** infer the fork parent from commit ancestry, or from a bare upstream that resolves to the branch's own remote counterpart (`origin/<self>`) — nothing durably records "the branch I forked from," so guessing it diverges run to run. `(basis: derived from a re-verify cold walk that split main-vs-develop on an unrecorded base)`
  This resolved target is what every later phase reconciles against, gates the merge into, and lands into. Which environment, if any, deploys from it is not land's question.
- **Branch state and divergence** — which branch the work is on, and how far it has diverged from the **resolved target's** live head. Divergence sizes the reconcile work in [prepare-the-increment](02-prepare-the-increment.md) and flags semantic-conflict risk ([integrate-against-current-target](../rules/integrate-against-current-target.md)).
- **The team's flow** — detect the repo's merge strategy and branch model here, by the detection discriminators and precedence in [match-the-team-flow](../rules/match-the-team-flow.md), so every later phase follows the team's ritual rather than a generic one. Also read the recent commit-message convention — but as a **conflict check against the house baseline**, not a ritual to adopt: whether recent commits *consistently* fail to parse as Conventional Commits (a template, a tag scheme, or a plain free-form style). That read only matters when no format preference is already set; when one is, the baseline-or-preference resolves without a question. A detected conflict is resolved in [prepare-the-increment](02-prepare-the-increment.md) by surfacing it and asking the user (then persisting the answer), never by following it silently ([commits-tell-the-why](../../../craft/engineering/commits-tell-the-why.md)).

## Classify the landing type — it forks the procedure

Assign exactly one by walking the tests **in order** (the order is what makes them mutually exclusive):

1. **hotfix** — *is production currently broken or degraded, and does this change restore it?* Yes → hotfix. An active-incident fix, where the cost of the bug is being paid right now.
2. **feature** — else, *does the change add or alter behavior a user can observe?* Yes → feature. New or changed user-facing behavior, not driven by an active incident.
3. **chore** — else → chore. No user-observable behavior change and no active incident: a refactor, a dependency bump, tooling, docs, tests.

**Partition proof.** The ordered test is exhaustive and mutually exclusive: every change either restores an active breakage (hotfix), or — failing that — changes observable behavior (feature), or — failing that — does neither (chore); the ordering resolves the overlaps (a fix that also changes behavior but has no active incident is a *feature*, because hotfix requires live breakage; a refactor bundled with a behavior change is a *feature* by test 2, and the bundling is flagged as a coherence problem per [one-coherent-change-per-unit](../rules/one-coherent-change-per-unit.md)).

**What each type changes downstream:**

| Type | Gate ([run-the-gate](03-run-the-gate.md)) | Landing ([merge](04-merge.md)) |
|---|---|---|
| **hotfix** | still green-before-land — the stop is never skipped — but the gate may be scoped to the affected checks for speed | fast-tracked per the routed policy below |
| **feature** | full gate | normal team flow |
| **chore** | full gate | normal team flow |

The landing type is part of land's result.

`(basis: derived from two axes read off the change: active-incident urgency and user-observability)` `(routed to maintainer: a hotfix may bypass the full-review path but never the green-before-land stop, and a feature or chore takes the full flow; review fast-track and hotfix gate scope are a house call)`

## Close the phase — state the assessment

Emit the assessment the rest of the run consumes: the integration target (with the record that resolved it), the team's flow, the diff scope and blast radius, the branch/divergence state, and the landing type (with the test that placed it). Under `--dry-run`, this assessment is part of the previewed plan. A later phase that finds the assessment missing a fact routes back here rather than guessing it.
