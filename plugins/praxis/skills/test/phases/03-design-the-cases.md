The set of cases you could write is unbounded: select the ones that actually discriminate, order them by risk, prune the rest, and then judge whether the set is adequate.

## Enumerate the candidate cases

For each behavior in the framed claim — the behaviors the change introduces or alters and the reverse-dependents it affects (from [map-the-surface](02-map-the-surface.md)), plus, under `--from-spec`, the spec's criteria — enumerate the cases that would catch it breaking: the happy path, the boundaries and edges that bite ([cover-the-edges-that-bite](../../../craft/engineering/cover-the-edges-that-bite.md) — empty, null, zero, one, max, off-by-one), the error and failure paths, and the counter-examples that must **not** pass (the inputs a correct implementation rejects). Do not narrow enumeration to the spec's criteria under `--from-spec`: the change's own behaviors are always in scope. Assert observable behavior, not internal structure ([test-behavior-not-implementation](../../../craft/engineering/test-behavior-not-implementation.md)); shape each so one failure points at one cause ([one-reason-to-fail](../../../craft/engineering/one-reason-to-fail.md)).

**Where a design stated its assumptions, they are case sources too.** A design that came through `plan` carries its load-bearing assumptions written as *falsifiable* statements, each paired with what would break if it were false ([surface-assumptions](../../plan/rules/surface-assumptions.md)). Read them as cases and take both halves: the assumption's **falsification** is the input to construct, and the stated breakage is that case's **expected** behavior — which is what makes it a test rather than a worry. Only the single riskiest assumption gets a validation step before a design commits, so the rest arrive here stated and unexercised; they are the cheapest real cases available, because someone already did the work of naming what would go wrong. Where no design or no stated assumption is in hand, this source is simply empty — say so rather than inventing premises the design never claimed.

`(basis: maintainer, 2026-09-02)`

## Keep only the discriminating cases

A case earns its place iff it can fail for a reason no already-kept case fails for. The discriminator: it exercises an uncovered equivalence partition or boundary, **or** it would catch a plausible wrong implementation that every kept case passes ([prove-the-test-can-fail](../../../craft/engineering/prove-the-test-can-fail.md)). A second case in the same partition, or one that only re-fails on a defect another kept case already catches, is redundant — drop it. `(basis: Myers, "The Art of Software Testing"; ISTQB; Just et al. 2014)`

## Prioritize by risk

Rank the kept cases by [risk-priority](../rules/risk-priority.md) (likelihood × blast-radius, High / Medium / Low) and spend the case budget top-down by its budget rule. That ranking is what [coverage-adequacy](../rules/coverage-adequacy.md) reads when it asks whether "the highest-risk behaviors" are covered.

## Judge coverage adequacy

Grade the designed set against [coverage-adequacy](../rules/coverage-adequacy.md), whose three grades and their tests decide it. A *partial* set is acceptable to proceed on only if each gap is carried forward as named residual risk to [report-the-verdict](06-report-the-verdict.md).

## Output

The designed, risk-ordered, adequacy-judged case set — with any residual-risk gaps named — handed to [set-up-the-harness](04-set-up-the-harness.md).
