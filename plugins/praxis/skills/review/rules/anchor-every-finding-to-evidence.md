# Anchor every finding to evidence

A finding the author cannot act on is noise, however real the underlying problem. "This feels fragile" gives them nowhere to go; "line 42 dereferences `user.profile` which is null whenever the account is unverified — see the caller at line 88" gives them the exact edit and the exact reason. This rule requires every finding to carry its evidence: a concrete location and a concrete failing scenario. It is what turns a review from an opinion into a diagnosis, and it is cited from every phase that produces or keeps a finding — [hunt-for-defects](../phases/03-hunt-for-defects.md), [assess-craft](../phases/04-assess-craft.md), [triage-and-rank](../phases/05-triage-and-rank.md), and [deliver-findings](../phases/06-deliver-findings.md).

## The two anchors every finding owes

- **A location** — `file:line` (a span for a multi-line issue), pointing at the exact site, not the general area. If the cause and the symptom are in different places, name both: the line that is wrong and the line that reveals it.
- **A scenario** — the concrete condition under which it matters. For a correctness defect, the input or state that triggers the wrong behavior and the path that reaches it (the three reads in [confirm-before-claiming](confirm-before-claiming.md)). For a craft finding, the concrete cost: the future edit that duplication will force to two places, the specific reader the name will mislead.

A finding missing either anchor is not ready to report — it goes back for another read, not into the list with a hedge.

## The discriminator: evidence vs. a vague concern

The test that separates a real finding from a worry: **could the author verify or refute it from the anchor alone, without asking you what you meant?** If the location and scenario let them reproduce the problem in their head or their editor, it is anchored. If they would have to reconstruct which line and which case you had in mind, it is a concern, not a finding — and a concern dressed as a finding wastes the author's time and dilutes the ones that matter.

This anchoring is also what makes triage possible: severity ([severity-scale](severity-scale.md)) is assigned from the *consequence in the scenario*, and confidence ([calibrate-confidence-to-effort](calibrate-confidence-to-effort.md)) from *how much of the scenario you actually traced*. An unanchored finding cannot be graded on either axis, which is another way of seeing that it isn't finished.
