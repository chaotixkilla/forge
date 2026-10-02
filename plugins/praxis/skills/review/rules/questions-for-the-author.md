# Questions for the author

Not everything a review can't settle is a defect, and left alone, that doubt goes one of two wrong ways: either it's dropped, and a choice nobody could justify is approved anyway, or it's dressed up as an unverified finding that asserts a defect no one has shown.

## What earns a question

A question is owed when a **load-bearing choice** has a reason that nothing the review read supplies. Load-bearing means either the change is wrong if the reason doesn't hold, or an approval would ratify the choice (the brief's decisions, [deliver-findings](../phases/06-deliver-findings.md)). The usual sources:

- an approach that departs from the documented idiom of the framework or library it uses;
- a guard, retry or special case with no visible trigger;
- a requirement read one way where it could reasonably be read another;
- a scope cut the intent doesn't mention.

Two things don't earn one. If the code or the evidence already answers it, the review answers it itself: an answer that shows a defect is a finding, and one that clears the choice leaves nothing to report. And curiosity doesn't count: if every possible answer leaves the change the same, there's nothing to ask.

## Question or finding

**A finding asserts a defect the evidence shows; a question asks for a reason the evidence can't supply.** Two tests settle the borderline:

- If the likeliest answer is "that's a bug", it's a finding: report the defect, graded like any other.
- Otherwise it's a question, when the change's correctness turns on which answer is true, or when approving it knowingly needs the answer. A retry with no visible trigger, whose likeliest answer is "the upstream is flaky" but which is wrong if the call isn't idempotent, is a question.

A question carries no severity and no certainty, and never enters the verdict tally.

## The form

Each question is one ask the author can answer in a sentence or two. It's anchored to its `file:line` and carries the evidence that raised it, such as the idiom it departs from (with the source) or the case it leaves unexplained, so the author can answer without reconstructing the review. Ask about the change, never the person: "what makes this retry safe to repeat?", not "why did you do this?".

(basis: maintainer, 2026-09-30)
