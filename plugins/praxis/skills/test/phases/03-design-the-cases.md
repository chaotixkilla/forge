This is where coverage is designed for *meaning*. The set of cases you could write is unbounded; the job is to select the ones that actually discriminate, order them by risk, prune the rest, and then judge whether the set is adequate. A phase that skips the judging produces a pile of cases; a phase that does it produces coverage you can defend.

## Enumerate the candidate cases

For each behavior in the framed claim — the behaviors the change introduces or alters and the reverse-dependents it affects (from [map-the-surface](02-map-the-surface.md)), plus, under `--from-spec`, the spec's criteria — enumerate the cases that would catch it breaking: the happy path, the boundaries and edges that bite ([cover-the-edges-that-bite](../rules/cover-the-edges-that-bite.md) — empty, null, zero, one, max, off-by-one), the error and failure paths, and the counter-examples that must **not** pass (the inputs a correct implementation rejects). Do not narrow enumeration to the spec's criteria under `--from-spec`: the change's own behaviors are always in scope. Assert observable behavior, not internal structure ([test-behavior-not-implementation](../rules/test-behavior-not-implementation.md)); shape each so one failure points at one cause ([one-reason-to-fail](../rules/one-reason-to-fail.md)).

## Keep only the discriminating cases

A case earns its place iff it can fail for a reason no already-kept case fails for. The discriminator: it exercises an uncovered equivalence partition or boundary, **or** it would catch a plausible wrong implementation that every kept case passes ([prove-the-test-can-fail](../rules/prove-the-test-can-fail.md)). A second case in the same partition, or one that only re-fails on a defect another kept case already catches, is redundant — drop it. `(basis: a test earns its place by detecting something the suite does not — equivalence partitioning and boundary-value analysis (Myers, "The Art of Software Testing"; ISTQB) and the mutation-adequacy notion of killing a mutant no other test kills (Just et al. 2014); the two framings reinforce.)`

## Prioritize by risk

Rank the kept cases by [risk-priority](../rules/risk-priority.md) (likelihood × blast-radius, High / Medium / Low) and spend the case budget top-down: every High-risk behavior must be covered, Medium as budget allows, Low only when cheap. Ranking by risk is what makes a bounded budget buy the most verification, and it is what [coverage-adequacy](../rules/coverage-adequacy.md) reads when it asks whether "the highest-risk behaviors" are covered.

## Judge coverage adequacy

Assess the designed set against [coverage-adequacy](../rules/coverage-adequacy.md): is every High- and Medium-risk behavior covered by a discriminating case (**adequate**, with any uncovered Low-risk behavior merely noted), is a Medium-risk behavior left as a named gap (**partial**), or is a High-risk behavior unverified or the cases non-discriminating (**inadequate**)? A *partial* set is acceptable to proceed on only if each gap is carried forward as named residual risk to [report-the-verdict](06-report-the-verdict.md). Do **not** measure adequacy by a line-coverage percentage — that measures whether code ran, not whether a case would catch the change being wrong.

## Output

The designed, risk-ordered, adequacy-judged case set — with any residual-risk gaps named — handed to [set-up-the-harness](04-set-up-the-harness.md).
