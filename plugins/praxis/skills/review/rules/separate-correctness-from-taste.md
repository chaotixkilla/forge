# Separate correctness from taste

The most useful thing a review does for an author is tell a *bug* apart from a *preference*. Blur them and every finding reads as equally optional — the author fixes the naming nit and ships the null-deref — or equally mandatory, and the author resents being told to rename a variable as if it were a crash. Keeping the two classes distinct is what makes the verdict actionable: must-fix defects in one pile, optional cleanups in another, each judged by its own bar. This rule pins the line between them so two reviewers sort the same finding the same way.

## The discriminator

A finding is a **correctness defect** if you can name an input or state on which the change produces a **wrong result, a crash, a security breach, or a violated contract**. It is a **craft finding** if the behavior is correct for every input and only the *form* is worse — reuse, simplicity, efficiency, clarity, or consistency.

The test is one question: **can I name an input where the code is *wrong*?**

- **Yes** → correctness. It belongs to [hunt-for-defects](../phases/03-hunt-for-defects.md) and is severity-graded by consequence.
- **No** → craft. It belongs to [assess-craft](../phases/04-assess-craft.md) and is graded — on *severity* — by the cost a maintainer pays, not by any failing input. It still carries a *confidence* like every finding, but craft confidence measures how sure you are the finding's **premise** holds (the cited existing helper really exists and applies; the two blocks really duplicate; the simpler form really preserves behavior) — the craft-confidence ladder in [calibrate-confidence-to-effort](calibrate-confidence-to-effort.md), not the correctness cause→effect chain.

If you cannot name the wrong input but strongly suspect one exists, that is not a craft finding — it is a *speculative* correctness finding ([calibrate-confidence-to-effort](calibrate-confidence-to-effort.md)); keep it in the correctness pile at low confidence rather than demoting it to taste.

(basis: this two-pile split is the review role's own framing — "correctness, craft, and risk" as distinct outputs — and matches the harness code-review skill, which separates "correctness bugs" from "reuse/simplification/efficiency cleanups.")

## Why the passes are separate, not just the labels

The split is structural, not cosmetic: [hunt-for-defects](../phases/03-hunt-for-defects.md) and [assess-craft](../phases/04-assess-craft.md) are two passes precisely because the mindset differs. Hunting correctness means asking "how does this break?"; assessing craft means asking "how does this read and evolve?" Running them as one pass lets the easier craft observations crowd out the harder correctness hunt — you notice the long function before you notice it also loses data. Do correctness first, at full attention, then switch modes for craft.

## The boundary case: a craft problem that is also a latent bug

Some findings sit on the seam — duplication that will drift out of sync, a missing guard that is currently unreachable but one refactor away from firing. Resolve it by the same test applied to the *plausible near future*: if a realistic evolution of this code turns the craft problem into a wrong result, it is a **medium-severity correctness risk** (a footgun), reported in the correctness pile with the evolution named. If the code would only ever be *uglier*, it stays craft. Do not let "it might become a bug someday" inflate every style nit into a defect — the near-future evolution has to be concrete and plausible, not imaginable.
