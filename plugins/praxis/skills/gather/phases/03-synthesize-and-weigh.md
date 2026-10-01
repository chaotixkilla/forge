**This phase always runs** — it does not matter whether collection fanned out across explorers or one agent gathered inline. The tiering, conflict-resolution, and corroboration below are gather's *actual work*; reading the collectors' raw findings and reasoning over them directly — instead of running this pass — is *skipping* gather, not shortcutting it.

## Tier and weigh

Read the key files the code and repository explorers name before weighing their findings: a summary is weighed against the file it summarizes, not instead of it.
1. Tier every finding — authoritative / anecdotal / project-internal ground truth — and weigh conflicts by the composition rules in [sourcing-model](../rules/sourcing-model.md).
2. Keep what a source *states* distinct from what you *conclude* from it — [separate-fact-from-inference](../../../craft/evidence/separate-fact-from-inference.md).

## Corroborate and resolve
3. Where independent lanes or origins converge, corroborate — count origins not posts, trace echoes, and grade down when independence can't be established: [triangulate-before-trusting](../../../craft/evidence/triangulate-before-trusting.md). Date each finding against the subject's change cadence, not the calendar: one predating the subject's last breaking version is presumed stale until re-confirmed ([watch-recency-and-drift](../../../craft/evidence/watch-recency-and-drift.md)).
4. Where they conflict, run the conflict test and surface the disagreement rather than collapsing it — [surface-disagreement](../../../craft/evidence/surface-disagreement.md). A project-reality-vs-domain-norm divergence (code/repo disagreeing with a spec or the docs) is itself a finding, never averaged away.

## Mark what you cannot resolve
5. The one call you never make: whether an authoritative source *transfers* to this project. Report how far each source reaches and flag the gap; leave the transfer decision to the caller — open by design (see [sourcing-model](../rules/sourcing-model.md)): the caller holds the project context you lack.

The output of this phase: findings organized by tier, conflicts and divergences surfaced with their positions, corroboration graded, and every transfer question flagged — the weighed picture, ready to hand back.
