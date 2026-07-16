# Make the ask explicit

The most common way an artifact fails is not being wrong — it is being ignored, because the reader could not tell they were being asked for something. A reader who isn't sure whether a message informs or requests defaults to "informs" and moves on; the response the writer expected never comes, and each blames the other. This rule makes the ask a stated element, not an inference the reader must draw. It is fixed in [frame-the-message](../phases/01-frame-the-message.md), written where the reader will act on it in [draft-the-content](../phases/04-draft-the-content.md), and checked for ambiguity in [tighten-and-verify](../phases/05-tighten-and-verify.md).

## The bar: who does what, by when — or explicitly nothing

An ask is explicit only when a reader can answer all three without inference:

- **Who** — is this ask directed at *me*, or at someone else on the thread? A broadcast "someone should look at this" is owned by no one and done by no one; name the owner.
- **What** — the specific action, concretely enough to do it: "approve the migration plan," "reply with your service's peak QPS," not "thoughts?" or "let me know."
- **By when** — a time the response is needed, so the reader can prioritize it against everything else asking for their attention.

And the inverse is equally explicit: when nothing is owed, **say so** — "for your awareness, no action needed" — so the reader can file it and move on rather than wondering what they're supposed to do.

## The discriminator: implied vs explicit

The test: could a reader who skims the artifact once state what they must do and when? If the ask lives only in the *implication* of a paragraph ("the deadline is tight and we're blocked on the schema") rather than a stated request ("**@dana: sign off on the schema by Thu, or we slip the release**"), it is implied — a finding, not a nuance. An ask buried at the end, after the reader has decided how much attention to give, is functionally implied too; put it where the takeaway is.

## Ask for the next thing, not the whole thing

Where the artifact is a status or a request that will iterate, commit to the *next* concrete step and its time, not a distant end-state you can't guarantee — "I'll have the design up for review by Wednesday," not "this'll be done soon." A near, keepable ask gets acted on; a vague far one gets deferred. `(basis: the next-update-time-not-fix-ETA discipline, corroborated across incident-comms practice — Atlassian, Rootly — and applied here to asks generally: promise the next step, which you control, not the finish, which you may not.)`
