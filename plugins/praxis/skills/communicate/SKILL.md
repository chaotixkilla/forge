---
name: communicate
description: Produce and route a human-facing artifact of the work — a doc, status update, decision record, onboarding note, or review/handoff message — pitched to a named audience at the right altitude and delivered through the right form and channel. Reach for it when the substance exists and the job is to land it on people; distinct from operate (which owns live-incident status at its own severity-keyed cadence) and from the publish-artifact / communication ports (the doers it delegates delivery to).
metadata:
  flags:
    --audience=<tier>: name the target reader tier (peer|newcomer|exec|external), overriding the tier model-the-audience would infer — a phase input, not a module
    --as=<form>: force the artifact's form (doc|message|walkthrough), overriding the form choose-form-and-channel would pick — a phase input, not a module
    --lang=<code>: produce the artifact in the target language, preserving intent and tone (activates localize-and-translate)
    --notify=<target>: after producing the artifact, announce it to a communication target through the communication capability (activates notify-targets)
    --draft: stop after tighten-and-verify and return the content unsent — no delivery, publish, or notify (activates draft-only)
    --publish: publish the artifact as a durable team-facing document through the artifacts capability and return its canonical location (activates publish-output)
  config_requires:
    - key: tools.knowledge
      if_missing: guide via init:knowledge, else degrade
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies.

communicate owns the judgment — *what* to say, *to whom*, at *what altitude*, in *what form*, and *whether* to send — and delegates the mechanism: it routes messages and notifications to the `communication` port and publishes durable documents to the `publish-artifact` port, so it declares no `config_requires` for either (doer-owns-prerequisites; the ports own `tools.communication` and `tools.artifacts`). It keeps `config_requires: tools.knowledge` alone, because it reads knowledge as direct doc-context — pulling the substance and surrounding conventions it shapes into an artifact — not as a gather step (the settled §2 rule). Its block/degrade posture is behavioral, written into the phases: knowledge unavailable degrades to what the session already holds; a delivery backend unavailable degrades to returning the finished artifact for the user to send or publish by hand.

1. Frame the message: fix intent before writing — what the reader must know, decide, or do after reading, the single takeaway if they read nothing else, and the explicit ask  — see [phases/01-frame-the-message.md](phases/01-frame-the-message.md)
2. Model the audience: profile who receives this on two axes — knowledge-proximity and role/stake — and assign the tier that sets depth, jargon, and framing  — see [phases/02-model-the-audience.md](phases/02-model-the-audience.md)
3. Choose form and channel: pick the shape (doc, message, walkthrough) and delivery path that fit the message's durability, purpose, urgency, and reach  — see [phases/03-choose-form-and-channel.md](phases/03-choose-form-and-channel.md)
4. Draft the content: write it — lead with the takeaway, structure for scanning, size the detail to the decision, and pitch voice and vocabulary to the tier  — see [phases/04-draft-the-content.md](phases/04-draft-the-content.md)
5. Tighten and verify: cut what doesn't serve the reader, confirm the ask and claims land, and strip every internal-process reference so the artifact is a clean export  — see [phases/05-tighten-and-verify.md](phases/05-tighten-and-verify.md)
6. Deliver and route: return, notify, or publish through the resolved targets; confirm it reached the intended readers and capture any follow-up owed  — see [phases/06-deliver-and-route.md](phases/06-deliver-and-route.md)
