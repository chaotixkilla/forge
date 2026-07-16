# Testable or it's not a requirement

This is the skill's thesis. A statement you cannot check is not a requirement — it is intent, a wish, a direction of travel. "The system should be fast," "sharing should be easy," "handle errors gracefully" all sound like requirements and commit no one to anything: nobody can build to them and nobody can prove them met, so at acceptance they resolve to whatever the reader wants them to mean. The single most valuable move spec makes is pushing each such statement until it becomes something a build can be held to and a test can pass or fail. This rule pins what "testable" means, precisely enough that two cold specifiers draw the line between a requirement and a wish in the same place — and it is the completion condition [strict-gate](../modules/strict-gate.md) enforces.

## The bar: verifiable, unambiguous, singular

A statement is a requirement when it clears three quality characteristics, taken from the requirements-engineering standard rather than from a sense of what reads well:

- **Verifiable** — "structured and worded such that its realization can be verified to the approving authority's satisfaction"; verifiability is enhanced when the requirement is measurable.
- **Unambiguous** — it can be interpreted in exactly one way.
- **Singular** — it states a single capability, characteristic, constraint, or quality factor, with no conjunctions bundling two requirements into one line.

`(basis: ISO/IEC/IEEE 29148:2018 §5.2.5 requirement quality characteristics — the standard defines nine (necessary, appropriate, unambiguous, complete, singular, feasible, verifiable, correct, conforming); verifiable + unambiguous + singular are the three this skill's testability bar turns on. Verifiability, unambiguity, and singularity are the standard's, not a model default.)`

## The discriminator: name the verification method

The one test that separates a requirement from a wish: **can you name a verification method that returns pass or fail on the finished system?** The standard's four methods are *inspection* (read the artifact), *analysis* (reason/model it), *demonstration* (show it running), and *test* (execute against defined inputs). If you can name one that yields an unambiguous pass/fail, the statement is verifiable — a requirement. If you cannot — if checking it would require asking the author what they meant — it is still intent, and it goes back to be pushed until it is checkable.

- "Search returns results in under 200 ms at p95 under 10k concurrent users" → test/analysis, pass/fail → requirement.
- "Search should be fast" → no method returns pass/fail (fast to whom, measured how?) → intent, not done.

## The vague-language tell

Certain word classes are near-certain signs a statement has not cleared the bar — the standard names them as language to avoid because they produce requirements "difficult or even impossible to verify":

- **Subjective language** — *user-friendly, easy to use, intuitive, seamless, robust.*
- **Superlatives and comparatives** — *best, fastest, better than the old one, high-quality.*
- **Ambiguous adverbs/adjectives** — *fast, significant, minimal, quickly, roughly, sufficient.*
- **Open-ended / loophole terms** — *as appropriate, if possible, etc., including but not limited to, where feasible.*

Each is a placeholder for a measurable condition the author knew and the sentence didn't state. Replace it: not "fast" but a latency number at a percentile and a load; not "robust" but the named failure it must survive and the behavior it must show. `(basis: ISO/IEC/IEEE 29148 §5.2.7 requirement language criteria.)` This is the quantify step in [pin-down-ambiguity](../phases/02-pin-down-ambiguity.md), applied as a completeness check here.

## Quantifying — the number is the specifier's, the *having* of a number is the standard's

The standard requires measurability but sets **no numeric thresholds** — it does not say what "fast enough" is, because the right number is contingent on the system, the users, and the budget. So the bar splits cleanly: *that* a vague quality must become a measurable condition is non-negotiable and sourced; *which* number that condition carries is a house or project call. `(basis: 29148 ties verifiability to measurable "conditions" but prescribes no numeric bar — the threshold is deliberately the specifier's.)` Where the number is a genuine house standard (a standing perf budget, an a11y baseline), pull it rather than invent one — that is a [gather](../../gather/SKILL.md) read, run in [pin-down-ambiguity](../phases/02-pin-down-ambiguity.md); *deliberately open where no standing number exists:* propose one and flag it as an assumption to confirm ([make-the-unsaid-explicit](make-the-unsaid-explicit.md)), never silently pick.

## The singular trap

A statement joined by "and" usually hides two requirements, and a compound requirement is untestable as one line because its halves pass or fail independently: "the export must be fast **and** support CSV and JSON" bundles a performance requirement with two format requirements. Split on the conjunction until each line states one capability with its own acceptance criterion. A line you cannot give a single pass/fail to is not singular yet.

## Where this rule runs

It is a **baseline, always on**: every requirement is held to it as it is made concrete in [making-it-concrete](../phases/04-making-it-concrete.md), and a requirement that fails is surfaced as a warning delivered with the spec. [strict-gate](../modules/strict-gate.md) (`--strict`) escalates that warning to a hard block — the run does not finish while any requirement is below the bar. The check is the same either way; only the consequence changes.
