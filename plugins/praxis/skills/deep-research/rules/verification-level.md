# The verification level

`--verify` sets how hard claims are tested before they are trusted — and, just as load-bearingly, *which* claims get tested at all. It is a dial with a default (like review's `--effort`), not an on/off module. If the levels and the "which claims" test are undefined, two cold runs on the same evidence verify different sets and reach different confidence, so this rule pins both. Cited from [verify-claims](../phases/04-verify-claims.md) (which applies it) and [compose-output](../phases/06-compose-output.md) (which reports the level used).

## Which claims get verified — the materiality discriminator

Verification is spent on the claims that carry the answer, not on every incidental fact. Two nested classes, decided by a counterfactual test:

- A claim is **material** when a *sub-answer* changes if the claim is false. Test: "if this were wrong, would any sub-question's answer change?" — yes → material.
- A claim is **load-bearing** when the *main answer* to the original question changes if it is false — the subset of material claims the top-line conclusion rests on.

Everything else is incidental: it carries the strength of its single source, flagged, and is not verified. When the main answer is itself a documented **absence** ("no source establishes X"), the absence *is* the load-bearing claim: verify it by the counter-search — actively hunt the evidence that would fill the gap ([guard-against-confirmation](guard-against-confirmation.md)) — and treat finding none as confirming the absence, not a failed search. (basis: the "load-bearing premise" test — verify what the conclusion depends on — is the standard analytic discipline, and ICD 203 draws the same line between judgment-critical evidence and background. The counterfactual phrasing is what makes it cold-convergent: two runs asking "would the answer change if this were false?" select the same set.)

## The three levels

`(basis: the level definitions derive from the seed's own gloss — off skips, light corroborates the load-bearing, strict adversarially checks every material claim — operationalized against this skill's own verbs: corroborate across independent origins ([triangulate-before-trusting](triangulate-before-trusting.md)), chase to the primary ([prefer-primary-sources](prefer-primary-sources.md)), and hunt disconfirming evidence ([guard-against-confirmation](guard-against-confirmation.md)).)`

- **off** — no verification. Return the gathered sweep with every claim capped at **unverified** ([claim-confidence-scale](claim-confidence-scale.md)) and the report labelled an unverified scan. For orientation, never for a decision that rests on the answer being right.
- **light** *(proposed default)* — verify the **load-bearing** claims: corroborate each across independent origins, chase each to its primary source, and run a counter-search against the main answer. Material-but-not-load-bearing claims are corroborated where cheap; incidental claims carry their source's strength, flagged.
- **strict** — verify **every material** claim to the light standard, and additionally recruit the critics ([verify-claims](../phases/04-verify-claims.md) recruits [adversary](../../../agents/critics/adversary.md), [assumption-hunter](../../../agents/critics/assumption-hunter.md), [completeness-auditor](../../../agents/critics/completeness-auditor.md)) to attack the answer, its hidden premises, and its coverage. For a high-stakes answer where being wrong is costly.

`(basis: ratified by the maintainer, 2026-07-13. The default level is **light**. Reasoning: off defeats the skill's purpose (adversarial verification is its identity), strict is expensive and best reserved for high-stakes runs, and light delivers trustworthy load-bearing claims at a proportionate cost — the level a caller who names none most likely wants. Ratified as the house default.)`

## Composition with the spend caps

`--verify` is orthogonal to `--deep` (which widens *gathering*, not verification). Against `--budget`/`--timebox` it is not orthogonal: those caps are hard, so verification **degrades to fit and says so** — verify as many load-bearing claims as the remaining budget/time covers, in importance order, and report the effective level (`verified at light, budget-bound — 3 of 5 load-bearing claims checked`), never silently overspending and never refusing the run ([budget-discipline](../modules/budget-discipline.md), [timeboxing](../modules/timeboxing.md)). A claim that materiality selected for verification but a cap left unchecked is delivered **unverified**, not silently trusted.
