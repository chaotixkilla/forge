Collection produced a pile of lane-tagged findings; this phase turns the pile into one weighted picture. This is where gather earns its name — the cross-lane composition the explorers deliberately don't do, done once, here.

**This phase always runs** — it does not matter whether collection fanned out across explorers or one agent gathered inline. The tiering, conflict-resolution, and corroboration below are gather's *actual work*; reading the collectors' raw findings and reasoning over them directly — instead of running this pass — is *skipping* gather, not shortcutting it. There is no path from collection to the return that bypasses this step.

## Tier and weigh
1. Tier every finding by the sourcing model — authoritative / anecdotal / project-internal ground truth — and weigh conflicts by it: authority over anecdote, per-claim accountability, code/repo over knowledge-base on what-is-true-now. The full model, tiers and composition rules, is [sourcing-model](../rules/sourcing-model.md); apply it, don't re-derive it.
2. Keep what a source *states* distinct from what you *conclude* from it — [separate-provenance-from-conclusion](../rules/separate-provenance-from-conclusion.md). The picture must never let a conclusion inherit the authority of the finding it was drawn from.

## Corroborate and resolve
3. Where independent lanes or origins converge, corroborate — count origins not posts, trace echoes, and grade down when independence can't be established: [corroborate-across-independent-origins](../rules/corroborate-across-independent-origins.md).
4. Where they conflict, run the conflict test and surface the disagreement rather than collapsing it — [surface-conflicts-not-consensus](../rules/surface-conflicts-not-consensus.md). A project-reality-vs-domain-norm divergence (code/repo disagreeing with a spec or the docs) is itself a finding, never averaged away.

## Mark what you cannot resolve
5. The one call you never make: whether an authoritative source *transfers* to this project. Report how far each source reaches and flag the gap; leave the transfer decision to the caller — open by design (see [sourcing-model](../rules/sourcing-model.md)): the caller holds the project context you lack.

The output of this phase: findings organized by tier, conflicts and divergences surfaced with their positions, corroboration graded, and every transfer question flagged — the weighed picture, ready to hand back.
