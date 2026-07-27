The previous phase hunted loads that are too eager. This one hunts the opposite defect, and it is the more damaging of the two: a citation into a file the step **cannot be done correctly without**, phrased as an optional aside, so the executor never opens it and fills the standard from its priors instead. Nothing fails, nothing stalls, and the bar the plugin took care to pin never reaches the run.

The property being checked is the rule-citation register, defined in full by `skip-resistance` in [audit-contract](../../audit-contract/SKILL.md) — that rule owns the two registers and the conformant phrasing, and this phase applies it. Do not re-derive the definition; read it there.

## Find the citations that must be load-bearing

You are not checking every citation — most are correctly optional. You are looking for the ones where the cited file holds something the step's output must **conform** to. Locate them from the cited side, which is far more reliable than reading every phase:

1. **List the files that define a conforming vocabulary.** In this kit they are recognisable: a graded scale with named levels, a defined taxonomy or term set, a pinned numeric threshold, a named set the output must draw from. Their filenames often say so (`*-scale`, `*-tiers`, `*-classification`, `*-taxonomy`, `*-priority`, `*-adequacy`, `*-level`), but confirm by opening each — a file named like a scale that merely discusses one does not qualify, and a file named nothing like one may define a closed term set.
2. **For each, find every citation into it.** Grep the skill for the filename.
3. **Read the citing sentence.** Does it name what the step needs *from* the file, or does it merely point?

## The test, and what conformance looks like

The test is the counterfactual: **could a cold executor complete this step, and produce output of the right shape, without opening the cited file?** If yes, and the file defines the shape, the citation is under-powered.

- **Conformant** — the sentence names the thing that only the file supplies, so acting without it is visibly impossible: *"assign one of the five levels defined in …"*, *"classify with a term from the taxonomy in …"*, *"apply the threshold pinned in …"*. An executor that never opened the file cannot name five levels it has not read.
- **Non-conformant** — a step that grades, ranks, selects, filters, or classifies, whose discriminator lives only in the cited file, and whose citation is a bare trailing parenthetical: *"grade the finding (see …)"*. This reads as a courtesy reference, and it is treated as one.

One exemption, and it is common: where the citing file **states the discriminator inline as well**, the citation is depth-on-demand by construction — the executor can act correctly from the phase alone, and the rule adds calibration. Not a finding. Check for this before filing, because it is the difference between a real defect and a demand that the author repeat themselves.

## Then check the other direction: are the optional reads marked optional?

The register check has a failure mode if run alone — an author who wants to pass it marks every citation load-bearing, and the skill becomes a mandatory read of its whole library. That is the eager-loading defect the previous phase just measured, arrived at by fixing this one. So sample the citations you did *not* flag and confirm the genuinely conditional ones say when they apply. A rule that is in play for some runs and not others, cited with no condition, is the routing defect from [index-vs-roster](../rules/index-vs-roster.md) at single-link scale.

Where the two checks disagree about the same citation — this phase wants it mandatory, the fan-out read wants it conditional — resolve toward **mandatory**, and record the disagreement rather than hiding it. The asymmetry is deliberate: a load-bearing citation phrased as optional loses the standard *silently*, while an optional citation phrased as mandatory costs tokens *visibly*, and a visible cost gets fixed. Say in the report that the site is contested and why, so the maintainer can settle it rather than inheriting whichever way this run happened to fall.

## What this phase hands forward

Per finding: the cited file and what it defines, the citing sentence quoted as it stands, the conforming phrasing that would fix it, and — where relevant — that the same site is contested against the fan-out read. Plus the count of load-bearing citations checked and found conformant, so the report can distinguish a skill whose registers were verified from one where nobody looked.
