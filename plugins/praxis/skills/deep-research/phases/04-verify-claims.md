## Select the claims to verify

Select the set by the materiality discriminator and the `--verify` level, both pinned in [verification-level](../rules/verification-level.md).

## Test each selected claim

For each claim in the set, run the three tests its level demands:

1. **Corroborate across independent origins** ([triangulate-before-trusting](../../../craft/evidence/triangulate-before-trusting.md)) — find sources that do not trace to a common origin, and count origins, not posts; echoes of one source are not corroboration.
2. **Chase to the primary source** ([prefer-primary-sources](../../../craft/evidence/prefer-primary-sources.md)) — follow the citation chain to the origin; a claim whose chain dead-ends in a circular echo is unverified, however widely repeated.
3. **Hunt the disconfirming** ([guard-against-confirmation](../../../craft/evidence/guard-against-confirmation.md)) — run the search that would *refute* the claim, not just confirm it; a claim only ever confirmed is not yet verified.

Check currency as you go ([watch-recency-and-drift](../../../craft/evidence/watch-recency-and-drift.md)): a claim predating the subject's last breaking change is presumed stale until re-confirmed, and a newer weak source contradicting an older strong one triggers re-examination — resolved by method and corroboration, not by date.

## Recruit the critics at strict

At `--verify=strict`, recruit the critics to attack the answer independently — [adversary](../../../agents/critics/adversary.md) (construct the case that the answer is wrong), [assumption-hunter](../../../agents/critics/assumption-hunter.md) (surface the premises the answer rests on but never checked), [completeness-auditor](../../../agents/critics/completeness-auditor.md) (name the sub-question, source type, or counter-case not yet covered), each handed the [claim-confidence-scale](../rules/claim-confidence-scale.md) so it grades on that rule's own rungs and anchors rather than a ladder of its own — and fold their surviving challenges back into the claim set. Without fan-out available, apply each lens yourself in turn, following that critic's own method ([agents/critics/](../../../agents/critics/)): for every load-bearing claim, construct its refutation, name its unchecked premises, and ask what is missing, before letting the answer stand.

## Grade each verified claim

Assign every claim its confidence on the [claim-confidence-scale](../rules/claim-confidence-scale.md) (established / corroborated / contested / unverified), from how many independent origins of what strength corroborated it and whether a credible contradiction stands — kept distinct from the source strength that fed it ([separate-fact-from-inference](../../../craft/evidence/separate-fact-from-inference.md)).

The output is the verified claim set — each claim confidence-graded, its corroboration and primary chain recorded, disconfirming evidence noted — ready for synthesis.
