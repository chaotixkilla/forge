# Prefer the smaller suggestion

When a review finds a problem, it also proposes a fix — and the reviewer's instinct is to propose the fix they would write, which is often a redesign. That instinct is a trap: the author owns the change, has context the reviewer lacks, and did not ask to have their approach replaced. A finding that says "restructure this module" when "add one guard clause" would resolve the actual defect turns a fixable review into an argument. This rule biases every suggestion toward the least-invasive change that genuinely resolves the finding.

## The bar: smallest fix that resolves *this* finding

For each finding, propose the change with the smallest blast radius that removes the defect or the craft cost you named — not the change that would make the code ideal. A null-deref is resolved by handling the null, not by introducing an Option type across the module. Duplication is resolved by pointing at the existing helper, not by designing a new abstraction layer. The test: **does the suggestion do more than the finding requires?** If it fixes the named problem *and also* reshapes things the finding didn't mention, it has overreached — cut it back to what the finding needs.

## Why smaller is not just politeness

A minimal suggestion is easier to evaluate (the author can see it resolves the issue), easier to accept (it doesn't force unrelated decisions), and safer (a small change has a small chance of introducing a new bug — the [apply-fixes](../modules/apply-fixes.md) path especially depends on this, since it edits the tree). A sprawling suggestion, even a good one, invites the author to reject the whole thing rather than untangle the part that matters. The finding is the deliverable; the suggestion serves it.

## When the smaller fix is genuinely wrong

Occasionally the small fix is a patch over a defect whose real cause is structural — the guard clause silences the symptom while the broken invariant lives on. Do not propose a band-aid you know is one. But the response is not to prescribe the redesign; it is to **report the finding at the right altitude** — name the structural cause, its consequence, and that a local patch would only mask it — and let the author decide how to address it. Naming the real problem is within review's mandate; designing the author's solution is not. If the change genuinely needs a redesign, that is a finding about scope, delivered as such ([respect-author-intent](respect-author-intent.md)), not a suggestion you impose.
