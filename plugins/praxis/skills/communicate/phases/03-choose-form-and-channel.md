The same substance can be a durable document, a channel message, or a live walkthrough — and the wrong shape defeats it: a decision buried in a chat message evaporates, a one-line coordination fact bloated into a document nobody reads, a genuine disagreement flattened into a memo when it needed a conversation. Pick the form and the delivery path from the message's properties, not the writer's habit.

## The four signals — assign each with its test

Read the message on four signals; each has a decidable test:

- **S1 Durability** — will anyone outside this exchange, including a future joiner, need to reconstruct the *what* and especially the *why* later? Or: does it settle a structural choice, a decision, or something important/fundamental? Any yes → durability HIGH.
- **S2 Purpose** — is the goal **conveyance** (transmit settled facts or context; the reader absorbs at their own pace) or **convergence** (build shared understanding, resolve a disagreement, negotiate meaning, ideate)? This is the sync-vs-async discriminator.
- **S3 Urgency** — must the reader act now, before they'd next check asynchronously? (For a *production* incident, this is not communicate's call — see the boundary below.)
- **S4 Reach** — who needs this, now or later: a specific small set, or a broad/unknown/future audience?

`(basis: Nygard's ADR structural significance and 37signals for S1; Dennis, Fuller and Valacich 2008 for S2; GitLab's public-by-default handbook for S4; recommended, not mandatory)`

## Map the signals to a form and a channel

**Form** (from S1 + S2):
- **Durable document** when S1 is HIGH — a decision record, a design doc, anything structural or important.
- **Conversational message** when S1 is LOW and S2 is conveyance and the stakes are ephemeral — coordination, a quick status, a settled fact.
- **Live walkthrough (synchronous)** when S2 is convergence — resolving ambiguity or disagreement, ideating, or building trust with new people — or when async has already failed to converge. A meeting is the last resort, not the first reach; and when S1 is also HIGH, still capture a durable written summary *afterward*, or the decision dissolves with the call.

**Channel** (from S4, matching medium richness to how much must be *worked out* live):
- **Broadcast + durable** (a published doc, a public thread) — permanent and broad-or-future audience.
- **Broadcast + ephemeral** (a channel post) — announce or coordinate to a known group, low durability.
- **Direct** (a DM, a small thread, a 1:1) — a specific small audience, or sensitive content.
- The more must be resolved live (high equivocality), the richer the channel; pure settled facts take the leanest channel that carries them. `(basis: Daft and Lengel's media richness, as refined by media synchronicity theory)`
- **Reach tie-breaker — a named present reader that is also durable.** When S4 says "specific small set" (one named reader now) but S1 is HIGH (future joiners will need to reconstruct it), the future reach dominates the present addressee: choose **broadcast + durable** even though one reader is named today — the artifact outlives the one recipient. A decision record you happen to hand to one approver is still a durable record, not a DM. `(basis: ADR practice)`

**Urgency (S3) sets delivery immediacy, not form.** When S3 is HIGH, push toward the most immediate channel that reaches the actor *now* (a direct or interruptive path over a passive broadcast), and pair a near, keepable deadline in the ask per [make-the-ask-explicit](../../../craft/writing/make-the-ask-explicit.md). The **form** stays what S1/S2 derived: an urgent durable decision is still a document, delivered by an interruptive nudge with a link, not flattened into a chat message because it's urgent. `(basis: incident-communication practice)`

## The default, and `--as=`

When no signal fires decisively, the default is **async, written, and broadcast-visible** — sync and private are justified exceptions, never the baseline. `(basis: GitLab and 37signals handbooks; recommended)` `--as=<form>` overrides the derived form (`--as=doc` forces a durable document even for something the signals would have made a message). When the override contradicts the signals (forcing a message for something plainly durable), honor it and note the tension — the caller may know a constraint the signals don't.

## The boundary: live-incident status is the incident act's

If the urgency is a *production incident* — a degraded service, a firing alert, the acknowledge → mitigate → resolve arc — the incident act in **work** owns the severity-keyed cadence and the resolution declaration, and posts the status updates itself. communicate does not carry an incident cadence and must not invent one, which would conflict with the act's. It does write the incident's retrospective once the service is stable ([incident-retrospective](../rules/incident-retrospective.md)). communicate's S3 urgency covers the ordinary urgent message (a time-boxed decision, a heads-up before a deploy), not incident response. `(basis: derived from the incident act's status cadence)`

## The residue is open-by-design — with a stopping test that bounds it

The exact thresholds — *how* important is "important enough to document," *how* ambiguous is "ambiguous enough to meet," *how* broad is "broad enough to broadcast" — are set by no authority, and the handbook sources draw the lines in different places. They are **open by design**: the right cutoff depends on the team's norms, which this skill cannot enumerate. But the openness is *bounded*, not a blank — two writers converge when they calibrate against worked examples. The stopping test: **classify against anchors, not against the abstract signal.** For each borderline call, ask which of these the message most resembles — and stop when a clear anchor matches:

- *Clearly document* (top of durability): a decision the team will re-litigate in six months — an architecture choice, a policy, a rejected alternative worth remembering.
- *Clearly message* (bottom of durability): "deploying in 10, heads up" — true now, worthless next week.
- *Clearly meet* (convergence): two engineers who have disagreed twice in the thread and are not converging — escalate to a call, then write the outcome down.

The escalation trigger is explicit: **after roughly two async round-trips without convergence, move to a synchronous form** rather than a third. `(basis: house stopping test)`

Done-state: the form and the channel are chosen (with the signals that decided them named), the incident boundary is respected, and any `--as=` override and its tension are recorded.
