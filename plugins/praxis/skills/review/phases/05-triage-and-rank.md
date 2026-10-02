The hunt and craft passes produce *candidates* — some real, some false positives, some too uncertain or too trivial to be worth the author's attention. Turn that pile into the ordered list the author acts on.

## Validate each candidate — try to refute it

Take each candidate and attempt to *break the finding*, not just re-read it. Re-confirm the correctness candidates against [confirm-before-claiming](../rules/confirm-before-claiming.md): does the failing input really exist, is the path really reached, is there really no guard upstream? A candidate in a [known noise class](../rules/known-noise-classes.md) whose exception doesn't hold is dropped too. A candidate that cannot survive its own re-confirmation is dropped.

At `--rigor=high` or `max`, recruit the **adversary critic** with the inverted lens — "assume this finding is a false positive; argue why the code is actually correct" — and keep only the candidates that survive the refutation. Without fan-out, argue the opposing case for each finding yourself before letting it stand: state the strongest reason the code might be right, and drop the finding if that reason holds.

Re-test each candidate question from [build-the-mental-model](02-build-the-mental-model.md) against [questions-for-the-author](../rules/questions-for-the-author.md). One that proves a bug joins the correctness candidates here, validated and graded like them; the questions that stand skip the grading and floors below.

## Grade both axes, then apply the floors

For each survivor, assign the two independent grades:

- **Severity** — how bad the consequence, per the scale in [severity-scale](../rules/severity-scale.md) (critical / high / medium / low / info), assigned from the consequence in the finding's scenario.
- **Certainty** — how sure it is real, on the certainty scale of [results-and-certainty](../../../craft/evidence/results-and-certainty.md) (observed / traced / inferred / unverified), placed per [calibrate-certainty-to-rigor](../rules/calibrate-certainty-to-rigor.md): for a correctness finding, from how much of the cause→effect chain you actually read; for a craft finding, from how sure you are its premise holds (the cited helper exists and applies, the blocks truly duplicate) — the craft placement in the same rule.

Then drop what is below the bar: anything under the **certainty floor** the rigor level sets (low reports traced and above; high and max admit unverified, labelled), and anything under **`--severity-min`** when the caller set one. The floors are reporting filters applied after grading, not hunting limits — you graded everything, you deliver only what clears both.

## Separate scope findings, then rank

Pull out the scope-creep observations noted back in [scope-the-review](01-scope-the-review.md) and hold them as their own findings, not folded into the correctness or craft verdict ([respect-author-intent](../rules/respect-author-intent.md)). Scope findings are **not graded** on either axis — no severity, no certainty, no floor applies ([severity-scale](../rules/severity-scale.md)); they are ungraded boundary notes delivered in their own section, so the grading and floors above are for the correctness and craft candidates only. (If a bundled change is itself wrong, its wrongness is a correctness candidate graded like any other — distinct from the scope note.) Then order the survivors so the author reads them in the order they should act ([weight-by-impact-not-count](../rules/weight-by-impact-not-count.md)): **severity descending, certainty as the tie-break, blast radius as the final tie-break.** Merge duplicates — three symptoms of one root cause are one finding with three locations, never three findings; and if you partitioned a large change ([cover-a-large-change](../rules/cover-a-large-change.md)), pool the units' candidates here and dedupe across their seams, since one seam defect surfaces from both units. Resist inflating a finding's severity to justify keeping it. If nothing survives, that is the result: a clean change returns no findings.

**Coverage checkpoint — before declaring the verdict.** Confirm every in-scope file was actually reviewed: walk the in-scope set from [scope-the-review](01-scope-the-review.md) against what the passes (or the parallel units) covered, and account for each file — *reviewed*, or *set aside with its stated reason*. A file that is neither is a coverage hole; review it before delivering, and never let a report be silent about a file no pass opened ([cover-a-large-change](../rules/cover-a-large-change.md)). Carry the coverage into the scope line so the author sees the whole set was covered.

The output is a validated, graded, floored, ranked list — the correctness and craft findings kept distinct, with the scope findings and the questions for the author beside them — ready for [deliver-findings](06-deliver-findings.md) to render.
