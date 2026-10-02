# The verification level

`--verify` sets how hard claims are tested before they are trusted — and, just as load-bearingly, *which* claims get tested at all. It is a dial with a default (like review's `--rigor`), not an on/off module. Cited from [verify-claims](../phases/04-verify-claims.md) (which applies it) and [compose-output](../phases/06-compose-output.md) (which reports the level used).

## Which claims get verified — the materiality discriminator

Verification is spent on the claims that carry the answer, not on every incidental fact. Two nested classes, decided by a counterfactual test:

- A claim is **material** when a *sub-answer* changes if the claim is false. Test: "if this were wrong, would any sub-question's answer change?" — yes → material.
- A claim is **load-bearing** when the *main answer* to the original question changes if it is false — the subset of material claims the top-line conclusion rests on.

Everything else is incidental: it is not verified, and grades on the evidence gathering already holds, by the standard ([results-and-certainty](../../../craft/evidence/results-and-certainty.md)), **single-source** only when nothing beyond the source it arrived from was gathered. When the main answer is itself a documented **absence** ("no source establishes X"), the absence *is* the load-bearing claim: verify it by the counter-search — actively hunt the evidence that would fill the gap ([guard-against-confirmation](../../../craft/evidence/guard-against-confirmation.md)) — and treat finding none as confirming the absence, not a failed search. (basis: the standard load-bearing-premise test; ICD 203)

## The three levels

`(basis: derived from the three levels' definitions: off skips, light corroborates the load-bearing, strict adversarially checks every material claim)`

- **off** — no verification. Return the gathered sweep, each claim graded on the evidence gathering holds, on support or, where the standard puts it there, on certainty ([support-scale](support-scale.md)), and the report labelled an unchecked scan. For orientation, never for a decision that rests on the answer being right.
- **light** *(the default)* `(basis: maintainer, 2026-07-13)` — verify the **load-bearing** claims: corroborate each across independent origins ([triangulate-before-trusting](../../../craft/evidence/triangulate-before-trusting.md)), chase each to its primary source ([prefer-primary-sources](../../../craft/evidence/prefer-primary-sources.md)), and run a counter-search against the main answer ([guard-against-confirmation](../../../craft/evidence/guard-against-confirmation.md)). Material-but-not-load-bearing claims are corroborated when one more search or fetch would do it, within any budget set; one that search doesn't corroborate grades as its evidence stands, as incidental claims do.
- **strict** — verify **every material** claim to the light standard, and additionally recruit the critics ([verify-claims](../phases/04-verify-claims.md) recruits [adversary](../../../agents/critics/adversary.md), [assumption-hunter](../../../agents/critics/assumption-hunter.md), [completeness-auditor](../../../agents/critics/completeness-auditor.md)) to attack the answer, its hidden premises, and its coverage. For a high-stakes answer where being wrong is costly.

## Composition with the spend caps

`--verify` is orthogonal to `--deep` (which widens *gathering*, not verification). Against `--budget`/`--timebox` it is not orthogonal: those caps are hard, so verification **degrades to fit and says so** — verify as many load-bearing claims as the remaining budget/time covers, in importance order, and report the effective level reached, never silently overspending and never refusing the run ([budget-discipline](../modules/budget-discipline.md), [timeboxing](../modules/timeboxing.md)). A claim that materiality selected for verification but a cap left unchecked grades as its gathered evidence stands, like an incidental claim, and the level's sentence names it as unchecked.

## How the report states the level

The report says what the level did, never the flag's name or value:

- **off** — *"An unchecked scan: no claim was tested; each is graded on what the search turned up."*
- **light** — *"The claims the answer rests on were checked against independent and primary sources, and against a search for evidence to the contrary."*
- **strict** — *"Every claim a sub-answer rests on was checked against independent and primary sources and a search for evidence to the contrary, and the answer was argued against."*
- **cut short by a cap** — the level's sentence, with how far it got and what stopped it: *"The claims the answer rests on were checked, 3 of 5 before the budget ran out."*

(basis: maintainer, 2026-10-02)
