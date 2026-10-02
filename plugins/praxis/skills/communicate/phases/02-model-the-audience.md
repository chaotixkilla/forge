Resolve the one call that governs depth, jargon, framing, and confidentiality downstream: which audience tier this artifact is for. Every writer defaults to their own vantage — their mental model, their vocabulary, what is obvious to them — and a tier read from it calibrates every later phase for the wrong person: a peer-dense note leaks internal context to an outsider, an exec summary strands the implementer who needed the mechanism.

## Assign the tier — the method

The audience tier is a graded scale, and it is assigned by a two-axis method, not by a job title. Both the tiers and the method are pinned in [audience-tiers](../../../craft/writing/audience-tiers.md); this phase *runs* it:

1. Place the reader on **Axis A — knowledge proximity to *this* subject**: has-our-context / in-domain-but-new / outside-the-org. This axis drives depth and jargon.
2. Place them on **Axis B — role and stake**: implements-the-work / decides-on-the-work / sits-outside. This axis drives framing and what to lead with.
3. Map to one of the four tiers — **peer, newcomer, exec, external** — using the per-tier assignment test in the rule, **or to a split** (a depth-tier + a framing-tier) when the two axes land on different tiers. A high-proximity decision-maker (peer on Axis A, exec on Axis B) is the archetype: the rule's *when-the-axes-split* section records it as a pair ("peer-depth / exec-framing") and says which layer each axis governs — do not collapse it to one tier. Record the tier (or the pair) with its two-axis justification.

Carry the learning-mode flag from [frame-the-message](01-frame-the-message.md) through: a reader in learning mode gets the tier's prescription *plus* the acquisition scaffolding of [meet-the-learner-where-they-are](../../../craft/writing/meet-the-learner-where-they-are.md).

## Honor `--audience=` as an override, not a suggestion

`--audience=<tier>` names the tier explicitly; when present, it *overrides* the inferred tier rather than seeding it — the caller knows their reader better than the inference does. Still run the two-axis read, because it surfaces a mismatch worth flagging: if the caller says `exec` but the artifact plainly serves an implementer (it is all mechanism, no decision), note the tension for the user rather than silently pitching mechanism at a decision-maker.

## Multiple audiences: split or serve the widest

An artifact sometimes faces more than one reader — a decision record read by peers *and* an exec, a release note for customers *and* internal support. Resolve it, don't average it (an artifact pitched at the mean of exec and peer serves neither):

- If the readers' depth needs don't genuinely differ, don't split: pitch to the widest, least-context reader, as below.
- If the readers need genuinely different depth **and** the form allows it, **split** — a layered artifact whose top serves the exec (the bottom-line) and whose body serves the peer (the mechanism), each section self-sufficient for its reader per the stop-anywhere test in [right-size-the-detail](../../../craft/writing/right-size-the-detail.md).
- If the form is single-shot (one message, one channel post), **serve the widest, least-context reader** the artifact will actually reach, and pitch to that tier — because the artifact leaks to the lowest-context reader whether or not you wrote for them. When one of the readers is **external**, the external prescription (no internal context, confidentiality-checked) governs the whole artifact; you cannot un-leak an internal name to an outsider by having also addressed a peer.

## Read the destination's own voice

Register is matched, not invented, so this phase also reads *where the artifact is going* — the engineering home by default, an audience space when the request names a non-engineering reader ([choose-form-and-channel](03-choose-form-and-channel.md) fixes which) — for existing artifacts of the same type, so the draft can match their voice: documents in the repository through the **repository** and **code** explorers' reads of the tree, and documents in the home or any space configured as a knowledge source through the [knowledge](../../knowledge/SKILL.md) port's search. Without fan-out, do those reads yourself. What you find feeds [calibrate-tone-to-context](../../../craft/writing/calibrate-tone-to-context.md), whose routing fork prefers the surrounding convention over any house default. If the destination is new and has no prior art to match, note that — the draft will fall back to the house register.

Done-state: the tier is assigned (with its two-axis justification), any multi-audience split-or-serve call is made, the learning-mode overlay is carried through, and the destination's voice (or its absence) is recorded.
