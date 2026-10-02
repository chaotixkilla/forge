Read the draft as the reader will. Its author knows what they meant, so they read the intent into gaps the reader can't, and they carry the process in their head, so the machinery that helped produce the draft feels invisible to them and glaring to the reader. This phase is a gate: the artifact does not proceed to delivery until each check below passes.

## Cut to the reader's need

Two rules run the cut, at two altitudes:

- **Detail** — walk the draft against the stopping test in [right-size-the-detail](../../../craft/writing/right-size-the-detail.md), for the reader and action already fixed. When it holds, stop — over-cutting past the need is as much a defect as padding.
- **Words** — cut hedging, throat-clearing, and redundancy at the sentence level per [respect-the-readers-time](../../../craft/writing/respect-the-readers-time.md). This is the word-economy pass on the details that survived the altitude cut.

## Confirm the artifact lands its job

Check what a reader needs the artifact to do, against what [frame-the-message](01-frame-the-message.md) fixed:

- **The ask is unambiguous** — a reader can tell whether they must act, what to do, and by when, per [make-the-ask-explicit](../../../craft/writing/make-the-ask-explicit.md); an implied ask is a finding, not a style nit.
- **Claims and links resolve** — every link, reference, and name points at something that exists. A dangling link or an unverifiable claim ships misinformation.
- **Every requirement is sourced or declared** — walk the artifact against the requirement set from [derive-and-source](04-derive-and-source.md). Each obtained requirement's claim must trace to what was actually read rather than to recollection, and each unobtained one must appear as its declaration, in the form [source-or-declare](../../../craft/writing/source-or-declare.md) pins for it — a stated absence, not a smooth sentence occupying the slot. This is the last place a filled-in gap can be caught, and it is the hardest, because an invented sentence is indistinguishable from a sourced one by reading alone: check it against the set, not against how it sounds.
- **The register and tier fit** — the voice matches what [calibrate-tone-to-context](../../../craft/writing/calibrate-tone-to-context.md) resolved, and the depth/jargon/framing match the assigned tier in [audience-tiers](../../../craft/writing/audience-tiers.md). An artifact pitched a tier off — mechanism at an exec, undefined house jargon at an external reader — is a finding.

## Run the clean-export check

This is a content check, not a formatting pass. Read the whole artifact for **internal-process references** and strip every one, by the strip list and the machinery-vs-content discriminator in [clean-export](../../../craft/writing/clean-export.md). This check is mandatory for *every* delivery path — returned, notified, or published — because the artifact is a human-facing export the moment it leaves the skill. `(basis: ratified house decision, "artifacts are team-facing documents")` A document bound for an audience space also stands alone: it links nothing in the artifacts home, in a knowledge source whose note doesn't say the whole company can read it, or in the version-control, CI or telemetry backends, since its readers may have no access — state what the reader needs from such a page instead of linking it, and in doubt don't link. (routed to maintainer: the tracker and chat counted as open to the whole company, since in most companies they are, and assuming so errs toward the safer redaction.)

## Recruit the adversarial readers

Two critics read the draft as the person on the other end, each with a lens the author can't apply to their own work:

- The **user-advocate** stands in the reader's place and hunts the confusing dead end, the leaked internal, the missing affordance, the wrong-problem-solved — where the artifact costs the reader because it was written for the author's convenience.
- The **completeness-auditor** assumes something required is missing and hunts the gap — the unstated ask, the dropped why a decision record owed, the next step never named, the question the reader will obviously ask and the artifact never answers.

Recruit both; without fan-out, apply each lens yourself in a deliberately reader's-eye pass before proceeding — the lenses are not optional, only the delegation is. Their method is in [user-advocate](../../../agents/critics/user-advocate.md) and [completeness-auditor](../../../agents/critics/completeness-auditor.md).

**Disposition their findings** — communicate declares no severity scale, so grade in plain terms against one bar: a finding is **blocking** when it breaks the reader's ability to act on the artifact — a leaked internal, a dangling or wrong claim, a missing ask/why/next-step the type owes, a tier mismatch that misinforms — and must be fixed before delivery; it is **advisory** when the artifact still lands its job and the finding would only polish it, surfaced to the user but not gating. When a finding's blocking-ness is genuinely unclear, treat it as blocking and fix it — an under-served reader is the failure this skill exists to prevent. `(basis: derived from the two critics' clean-verdict definitions)`

Done-state: the draft is cut to the reader's need, its ask and register verified, every claim traced to its source and every unobtained requirement declared, every internal-process reference stripped, and every blocking critic finding closed.
