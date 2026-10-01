A hypothesis that survived testing is the *best current explanation*, not yet a confirmed root cause. Prove the mechanism end to end and grade how much of the proof you actually have; when confirmation fails, you do not lower the bar — you drop back into the loop for the evidence that would meet it.

## Prove the mechanism with the controlled toggle

The decisive test of causality is the controlled experiment: **make the failure appear and disappear on demand by changing only the claimed cause.** With the cause present, the reproduction fails; remove or correct exactly that one thing and nothing else ([change-one-thing-at-a-time](../../../craft/evidence/change-one-thing-at-a-time.md)), and the failure goes; re-introduce it, and the failure returns.

Then **name every link in the chain** from that cause to the observed symptom — why the cause produces the next state, which produces the next, down to the failure you framed in [reproduce-and-frame](01-reproduce-and-frame.md). A gap in the chain is a place the "cause" might actually be a coincidental correlate.

## Distinguish the true cause from a trigger or a symptom

Two failure modes masquerade as root cause; reject both:

- **The downstream symptom** — you have localized to where the bad state was *used*, not where it was *created*. Trace once more to the first divergence ([follow-the-first-divergence](../rules/follow-the-first-divergence.md)); if an earlier point already holds the wrong state, you are not at the cause yet.
- **The coincidental trigger** — the claimed cause co-occurs with the failure but does not mechanically produce it (the classic "it broke when X deployed," where X merely exposed a latent bug). Keep asking why one level deeper until the explanation bottoms out in a mechanism, not another effect ([fix-the-cause-not-the-symptom](../../../craft/evidence/fix-the-cause-not-the-symptom.md)).

## Grade the confidence, then try to break the grade

Assign the confidence rung from what you actually demonstrated — the controlled toggle plus a complete chain, one observed link, or only an inferred chain — per [the root-cause-confidence scale](../rules/root-cause-confidence.md) (confirmed-mechanism / probable / suspected). The rung is not decoration: [report-the-diagnosis](06-report-the-diagnosis.md)'s fix-gate reads off it.

Before the grade stands, attack it. Recruit the [adversary critic](../../../agents/critics/adversary.md) to refute the mechanism — construct the input or state where the claimed cause is present but the failure does *not* follow, or the failure occurs *without* the cause — and the [assumption-hunter critic](../../../agents/critics/assumption-hunter.md) to name the unstated premise the mechanism rests on and the reachable world that falsifies it. Both grade on the root-cause-confidence scale above. Without fan-out, run both lenses yourself: state the strongest case that this is *not* the cause, and keep the grade only if that case fails. Drop the grade a level if the toggle or a link cannot withstand the challenge.

The output is the confirmed cause, its confidence rung, and the cause→symptom chain — the diagnosis [report-the-diagnosis](06-report-the-diagnosis.md) writes up or acts on. If nothing reached at least a defensible **probable** with an observed link, that is the honest result: return to the loop, or report the failure as not-yet-root-caused with the best current hypothesis and the evidence that would confirm it.
