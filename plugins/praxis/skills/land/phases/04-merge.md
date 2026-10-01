The gate is green ([run-the-gate](03-run-the-gate.md)) and the increment reconciled ([prepare-the-increment](02-prepare-the-increment.md)); now the change merges into the **integration target** resolved in [assess-the-change](01-assess-the-change.md) (an epic/`develop` branch, or the trunk).

## Hosted actions go through the vcs capability

Merging touches the host platform, so delegate every hosted action — push a ref, read the target's landing constraint and the change's review request, merge — to the [vcs](../../vcs/SKILL.md) capability; the dispatch resolves to whichever provider is configured, and land names the capability, never the provider. (Routine local git — the commits and reconcile — was ambient in [prepare-the-increment](02-prepare-the-increment.md); this phase is the platform-mediated part.) land declares no vcs prerequisite — the `vcs` skill owns `tools.vcs` (doer-owns-prerequisites).

## Choose the landing path

The path follows the team's flow and what the **target** permits ([match-the-team-flow](../rules/match-the-team-flow.md)), with the merge strategy (merge-commit / squash / rebase) taken from the detected convention, not a house default. **Resolve what the target permits up front, don't discover it by failing:** read the target's landing constraint — does it require an approved review request (branch protection / required review) or allow a direct merge? — through the vcs capability before attempting to merge, rather than attempting a direct merge and reacting to a rejection (a rejected merge attempt can leave a side effect). This constraint is a team-flow fact, read for the *resolved target*: an epic branch may be unprotected where the trunk is protected, or the reverse.

Then decide by two facts: the target's constraint, and the repo's **collaboration posture**. More than one contributor in recent history, a configured team roster of more than one, an existing review-request practice, or branch protection each signal *collaboration*; a single contributor with none of these signals *solo*.

- **The target requires review, or the repo is a collaboration repo → merge only through an approved review request.** Read the change's review request through the vcs capability. Approved → merge it, by the team's strategy. Missing, open without approval, or with changes requested → don't merge: the run rests at *awaiting-review*, naming what's missing. land never opens a review request, since delivering the change for review belongs to whoever wrote it, and never merges around a required review. A shared line is never direct-merged by default, whether or not protection enforces it. `(basis: maintainer, 2026-07-11)`
- **A solo repo whose target requires no review → merge directly.** The caller ran land to land the change, so the merge is the intent. (routed to maintainer: a solo landing merges without asking, now that opening a review request belongs to the act that wrote the change.)

**When the landing constraint can't be read (`tools.vcs` unavailable), degrade to the safe side, never the risky one.** Do **not** assume a direct merge is safe: the target may be protected, and a blind push would bypass its required review. If the target is **purely local** (no remote configured), a direct merge is ambient local git and proceeds normally, since there is no shared or protected line to endanger. If a **remote exists** but the constraint can't be read, degrade to `--commit` semantics, which stay fully recoverable: record the coherent local commits, stop at *committed-only*, and report that the change was committed locally but not landed because the landing constraint could not be determined (the `vcs` skill owns guiding through `init:vcs`). `(basis: dogfood run against an unconfigured repo; per-capability degrade)`

`--commit` ([commit-only](../modules/commit-only.md)) never reaches this phase: it ended the run at *committed-only* in [prepare-the-increment](02-prepare-the-increment.md).

## Never land on red

Re-affirm the gate at the moment of merging: merge only on green ([green-before-land](../rules/green-before-land.md)). If the target moved since the gate ran, the gate is stale — re-reconcile and re-gate before merging ([integrate-against-current-target](../rules/integrate-against-current-target.md)). The merge carries the why-and-shape message ([commits-tell-the-why](../../../craft/engineering/commits-tell-the-why.md)), scoped to one coherent concern ([one-coherent-change-per-unit](../rules/one-coherent-change-per-unit.md)).

## The run's terminal outcomes — the partition

Every executing, run-to-completion land run resolves to **exactly one** terminal outcome, read off the change's **resting state** — not off which failure the run hit. `--on-fail` ([failure-policy](../modules/failure-policy.md)) decides the resting state; it adds no outcomes.

**Two non-member carve-outs** (states that are not a completed run):
- **`--dry-run`** → not a member: a preview mutates nothing, so it reaches no resting state. It reports its *would-be* outcome, computed by evaluating the members below as if `--dry-run` were unset and reading the target's constraint and the review request read-only, never by attempting a mutation. `(basis: derived from the --dry-run flag's definition)`
- **`--on-fail=ask`, paused** → not a member *yet*: an `ask` at a failure waits for a human decision, and the run resolves to whichever member the decision reaches — **retry** re-enters the flow, **stop** rests where `abort` would, **roll back** rests at the state after the reversal, **continue** (advisory failures only) proceeds. Where the run can't ask, `ask` acts as `abort` ([failure-policy](../modules/failure-policy.md)). `(basis: derived from ask's definition in failure-policy)`

**The four members:**
- **committed-only** — the change is committed **locally only**, not pushed or merged (`--commit`, or the unreadable-constraint degrade above).
- **awaiting-review** — the path requires an approved review request the change doesn't have, so it isn't merged. The outcome names what's missing: no request, a request not yet approved, or changes requested.
- **stopped-on-failure** — the change is **not merged into its target**: a failed required gate, an unresolvable conflict, or a backend unavailable for the merge halted it, **or** a landing failure's `rollback` reverted the merge.
- **merged** — the change **is merged into its target**.

**Determination (top-down, first match wins):** `--dry-run` → carve-out · an `--on-fail=ask` pause → carve-out until resolved · the run stopped at local commits → committed-only · the path requires an approved review the change lacks → awaiting-review · not merged into the target → stopped-on-failure · merged into the target → merged.

**Partition proof:** past the carve-outs, each member is read off one fact, checked in order — *did the run stop at local commits*, then *does the landing path require an approved review the change lacks*, then *is the change in the target line*. The order makes the members exclusive, and the last fact is binary, so they are exhaustive. Each `--on-fail` action lands the run in one member by reversing, or not, the failing stage's own effect: `abort` reverses nothing; `rollback` reverts a merge that a post-merge failure followed (→ stopped-on-failure) and is a no-op before any merge; `continue` proceeds; `ask` is the carved-out pause.

## Close the phase

Under `--dry-run`, report the landing path, the resolved target, the merge strategy and the message that *would* be used, without merging. Return the outcome with what a caller needs to act on it: the resolved target and the record that resolved it, the landing type, the merged commit (for *merged*), what's missing (for *awaiting-review*), what failed with its log evidence (for *stopped-on-failure*), and the **gate status as a named field** — `green`, `failed`, or `degraded: hosted pipeline not consulted` — so a run that never checked the hosted pipeline can't return a clean result with the omission hidden.
