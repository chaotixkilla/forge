---
name: communicate
description: Produce and route a human-facing artifact of the work — a doc, status update, decision record, onboarding note, or review/handoff message — pitched to a named audience at the right altitude, in the right form, with the channel it's meant for. Reach for it when the substance exists and the job is to land it on people; distinct from the incident act, which owns live-incident status at its own severity-keyed cadence, and from the communication and artifacts ports, which the act delivering the artifact sends it through.
metadata:
  flags:
    --audience=<tier>: name the target reader tier (peer|newcomer|exec|external), overriding the tier model-the-audience would infer — a phase input, not a module
    --as=<form>: force the artifact's form (doc|message|walkthrough), overriding the form choose-form-and-channel would pick — a phase input, not a module
    --lang=<code>: produce the artifact in the target language, preserving intent and tone (activates localize-and-translate)
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies.

communicate owns the judgment — *what* to say, *to whom*, at *what altitude*, in *what form*, and *where* it's meant to go — and sends nothing: the act that runs it delivers the artifact. It reads recorded knowledge through the `knowledge` port, so it declares **no `config_requires` at all** (doer-owns-prerequisites; that port owns `tools.knowledge`). It still reaches knowledge as *direct doc-context* — pulling the substance and surrounding conventions it shapes into an artifact — rather than as a gather step (the settled §2 rule), which is why it calls that port itself instead of routing through `gather`. Its block/degrade posture is behavioral, written into the phases: knowledge unavailable degrades to what the session already holds.

1. Frame the message: fix intent before writing — what the reader must know, decide, or do after reading, the single takeaway if they read nothing else, and the explicit ask  — see [phases/01-frame-the-message.md](phases/01-frame-the-message.md)
2. Model the audience: profile who receives this on two axes — knowledge-proximity and role/stake — and assign the tier that sets depth, jargon, and framing  — see [phases/02-model-the-audience.md](phases/02-model-the-audience.md)
3. Choose form and channel: pick the shape (doc, message, walkthrough) and delivery path that fit the message's durability, purpose, urgency, and reach  — see [phases/03-choose-form-and-channel.md](phases/03-choose-form-and-channel.md)
4. Derive and source what the reader needs: work forward from the reader and their action to the set of things they must have, source each from a real read, and declare the ones nothing can supply — including which requirements are owed a table, a chart, or a diagram  — see [phases/04-derive-and-source.md](phases/04-derive-and-source.md)
5. Draft the content: write it from that set — lead with the takeaway, structure for scanning, size the detail to the decision, and pitch voice and vocabulary to the tier  — see [phases/05-draft-the-content.md](phases/05-draft-the-content.md)
6. Tighten and verify: cut what doesn't serve the reader, confirm the ask and claims land, and strip every internal-process reference so the artifact is a clean export  — see [phases/06-tighten-and-verify.md](phases/06-tighten-and-verify.md)
7. Hand off the artifact: return it in its chosen form, with the destination and audience it's meant for and any follow-up it owes  — see [phases/07-hand-off-the-artifact.md](phases/07-hand-off-the-artifact.md)
