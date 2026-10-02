A rollout that starts before it knows where the change can go, and how hard it would be to take back, ships blind: it promotes into an environment that doesn't deploy from that branch, or ships a risky change all at once.

## Roll out only to a named environment that deploys from the change's branch

Two conditions must both hold, or nothing is promoted and the run goes straight to [confirm-healthy](03-confirm-healthy.md) with the reason, never inventing an environment:

- **A target environment is named.** With no `--target`, nothing rolls out: the config model carries no default deploy environment, and promoting an unnamed one is the unsafe surprise. `(basis: maintainer, 2026-07-11)`
- **That environment deploys *from* the branch the change merged into.** Resolve, per (branch, env), whether `<env>` is configured to deploy from that branch — read the environment→source-branch mapping from the repository's own deploy configuration (an ambient read of its pipeline or deploy files). `(basis: derived — no port declares the mapping; it lives in the repo)` Route by these outcomes, in order, first match wins:
  - **`<env>` deploys from the branch** → go on to the risk tier below. (Trunk→production; a long-lived `develop` integration branch→staging.)
  - **`<env>` resolves to a *known* deploy branch that is *not* this one** (e.g. `--target=production` for a change merged into `develop`, where production deploys from `main`) → don't promote; the result says the change rolls out to `<env>` once it reaches `<env>`'s deploy branch. The `--target` is surfaced, never silently dropped.
  - **`<env>` can't be resolved to a deploy source** — the mapping is unreadable (no deploy configuration maps environments to sources), or `<env>` is absent from a readable mapping (an unknown, unconfigured or mistyped env) → **degrade**: nothing is promoted, and the result says `<env>` couldn't be resolved to a deploy source. Never promote, and never name a deploy branch that doesn't exist. `(basis: maintainer, 2026-07-11; the per-(branch, env) form derived from re-verify cold walks)`

The branch the change merged into comes from the caller; without one, take the branch whose first-parent history holds the change's merge commit — the line it was merged into, not a line it was later promoted to. `(basis: derived from first-parent history recording where a merge happened)`

## Assign the change-risk tier

Read off the diff how hard the change is to take back if it's wrong, and assign the tier that [make-rollout-reversible](../rules/make-rollout-reversible.md) maps to a rollout strategy. A **hotfix** — production is broken or degraded now, and this change restores it — raises the floor and never lowers it ([make-rollout-reversible](../rules/make-rollout-reversible.md)). The caller passes the landing type when it has one; without it, apply that one test to the change.

## Close the phase

Emit what the rest of the run consumes: the environment and the deploy branch it was resolved against (or why nothing rolls out), the risk tier with the reversibility fact that set it, and whether the hotfix floor applies. Under `--dry-run`, this assessment is part of the previewed plan.
