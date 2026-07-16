Gathering tells you what the sources *say*; verification tells you which of it you can *trust*. This is the pass that separates deep-research from a search summary: the load-bearing claims are attacked, corroborated, and chased to their origin before they are allowed into the answer. What gets tested, and how hard, is set by the verification level; skipping this pass is a choice (`--verify=off`), never a default.

## Select the claims to verify

Not every claim earns verification — spend it on the ones that carry the answer. Apply the materiality discriminator in [verification-level](../rules/verification-level.md): a claim is **load-bearing** if the *main answer* changes when it is false, **material** if a *sub-answer* does. `--verify` sets the set: `light` (the default) verifies the load-bearing claims; `strict` verifies every material claim; `off` verifies none and caps every claim at unverified. A claim materiality selected but a `--budget`/`--timebox` cap left unchecked is delivered unverified, not silently trusted.

## Test each selected claim

For each claim in the set, run the three tests its level demands:

1. **Corroborate across independent origins** ([triangulate-before-trusting](../rules/triangulate-before-trusting.md)) — find sources that do not trace to a common origin, and count origins, not posts; echoes of one source are not corroboration.
2. **Chase to the primary source** ([prefer-primary-sources](../rules/prefer-primary-sources.md)) — follow the citation chain to the origin; a claim whose chain dead-ends in a circular echo is unverified, however widely repeated.
3. **Hunt the disconfirming** ([guard-against-confirmation](../rules/guard-against-confirmation.md)) — run the search that would *refute* the claim, not just confirm it; a claim only ever confirmed is not yet verified.

Check currency as you go ([watch-recency-and-drift](../rules/watch-recency-and-drift.md)): a claim predating the subject's last breaking change is presumed stale until re-confirmed, and a newer weak source contradicting an older strong one triggers re-examination — resolved by method and corroboration, not by date.

## Recruit the critics at strict

At `--verify=strict`, recruit the critics to attack the answer independently — [adversary](../../../agents/critics/adversary.md) (construct the case that the answer is wrong), [assumption-hunter](../../../agents/critics/assumption-hunter.md) (surface the premises the answer rests on but never checked), [completeness-auditor](../../../agents/critics/completeness-auditor.md) (name the sub-question, source type, or counter-case not yet covered) — and fold their surviving challenges back into the claim set. Without fan-out available, apply each lens yourself in turn, following that critic's own method ([agents/critics/](../../../agents/critics/)): for every load-bearing claim, construct its refutation, name its unchecked premises, and ask what is missing, before letting the answer stand.

## Grade each verified claim

Assign every claim its confidence on the [claim-confidence-scale](../rules/claim-confidence-scale.md) (established / corroborated / contested / unverified), from how many independent origins of what strength corroborated it and whether a credible contradiction stands — kept distinct from the source strength that fed it ([separate-claim-from-inference](../rules/separate-claim-from-inference.md)).

The output is the verified claim set — each claim confidence-graded, its corroboration and primary chain recorded, disconfirming evidence noted — ready for synthesis.
