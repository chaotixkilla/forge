The same substance can be a durable document, a channel message, or a live walkthrough — and the wrong shape defeats it: a decision buried in a chat message evaporates, a one-line coordination fact bloated into a document nobody reads, a genuine disagreement flattened into a memo when it needed a conversation. This phase picks the form and the delivery path from the message's properties, not the writer's habit. It is a real decision with a defined method, because "put it wherever" is exactly the standard-point two writers resolve differently.

## The four signals — assign each with its test

Read the message on four signals; each has a decidable test:

- **S1 Durability** — will anyone outside this exchange, including a future joiner, need to reconstruct the *what* and especially the *why* later? Or: does it settle a structural choice, a decision, or something important/fundamental? Any yes → durability HIGH.
- **S2 Purpose** — is the goal **conveyance** (transmit settled facts or context; the reader absorbs at their own pace) or **convergence** (build shared understanding, resolve a disagreement, negotiate meaning, ideate)? This is the sync-vs-async discriminator.
- **S3 Urgency** — must the reader act now, before they'd next check asynchronously? (For a *production* incident, this is not communicate's call — see the boundary below.)
- **S4 Reach** — who needs this, now or later: a specific small set, or a broad/unknown/future audience?

`(basis: S1 durability from ADR structural-significance (Nygard) + 37signals "important, critical, or fundamental"; S2 from Media Synchronicity Theory (Dennis, Fuller & Valacich 2008) — conveyance favors low-synchronicity/async, convergence favors high-synchronicity/sync; S4 from public-by-default handbook practice (GitLab). These are empirical/handbook sources, so the method is RECOMMENDED, not mandatory.)`

## Map the signals to a form and a channel

**Form** (from S1 + S2):
- **Durable document** when S1 is HIGH — a decision record, a design doc, anything structural or important. "Writing solidifies; chat dissolves."
- **Conversational message** when S1 is LOW and S2 is conveyance and the stakes are ephemeral — coordination, a quick status, a settled fact.
- **Live walkthrough (synchronous)** when S2 is convergence — resolving ambiguity or disagreement, ideating, or building trust with new people — or when async has already failed to converge. A meeting is the last resort, not the first reach; and when S1 is also HIGH, still capture a durable written summary *afterward*, or the decision dissolves with the call.

**Channel** (from S4, matching medium richness to how much must be *worked out* live):
- **Broadcast + durable** (a published doc, a public thread) — permanent and broad-or-future audience.
- **Broadcast + ephemeral** (a channel post) — announce or coordinate to a known group, low durability.
- **Direct** (a DM, a small thread, a 1:1) — a specific small audience, or sensitive content.
- The more must be resolved live (high equivocality), the richer the channel; pure settled facts take the leanest channel that carries them. `(basis: Media Richness Theory (Daft & Lengel) supplies the richness-to-equivocality match; MST refines it — richer is better only for convergence, and for conveyance leaner/async is actively better. Encoded per MST, keeping MRT's richness ladder as the ambiguity-matching intuition — the fork is resolved toward the current theory, not averaged.)`
- **Reach tie-breaker — a named present reader that is also durable.** When S4 says "specific small set" (one named reader now) but S1 is HIGH (future joiners will need to reconstruct it), the future reach dominates the present addressee: choose **broadcast + durable** even though one reader is named today — the artifact outlives the one recipient. A decision record you happen to hand to one approver is still a durable record, not a DM. `(basis: durability outranks a singular present addressee — a decision that will be re-litigated is written for whoever reads it later, not only the person it is sent to now; ADR/durability practice.)`

**Urgency (S3) sets delivery immediacy, not form.** S3 is the one signal that maps to *how fast and how directly* the message reaches the reader, never to its shape: when S3 is HIGH — the reader must act before they'd next check asynchronously — push toward the most immediate channel that reaches the actor *now* (a direct or interruptive path over a passive broadcast), and pair a near, keepable deadline in the ask per [make-the-ask-explicit](../rules/make-the-ask-explicit.md). The **form** stays what S1/S2 derived: an urgent durable decision is still a document, delivered by an interruptive nudge with a link, not flattened into a chat message because it's urgent. `(basis: the incident-comms principle that urgency/impact overrides delivery timing but not the record — urgency raises immediacy, durability sets form; the two are orthogonal, so urgency is wired to the channel's directness, not to S1/S2's form choice.)`

## The default, and `--as=`

When no signal fires decisively, the default is **async, written, and broadcast-visible** — sync and private are justified exceptions, never the baseline. `(basis: async-default handbook practice — GitLab, 37signals; RECOMMENDED.)` `--as=<form>` overrides the derived form (`--as=doc` forces a durable document even for something the signals would have made a message); it names the form the phase always resolves, so it is a phase input, not a module. When the override contradicts the signals (forcing a message for something plainly durable), honor it and note the tension — the caller may know a constraint the signals don't.

## The boundary: live-incident status is operate's

If the urgency is a *production incident* — a degraded service, a firing alert, the acknowledge → mitigate → resolve arc — this is **operate**'s territory, and operate owns the severity-keyed cadence matrix and the resolution declaration. communicate does not carry an incident cadence and must not invent one; hand incident status to operate. communicate's S3 urgency covers the ordinary urgent message (a time-boxed decision, a heads-up before a deploy), not incident response. `(basis: operate owns live-incident comms — see operate's right-sized-status-updates; boundary kept to avoid two skills with conflicting cadences.)`

## The residue is open-by-design — with a stopping test that bounds it

The exact thresholds — *how* important is "important enough to document," *how* ambiguous is "ambiguous enough to meet," *how* broad is "broad enough to broadcast" — are set by no authority, and the handbook sources draw the lines in different places. They are **open by design**: the right cutoff depends on the team's norms, which this skill cannot enumerate. But the openness is *bounded*, not a blank — two writers converge when they calibrate against worked examples. The stopping test: **classify against anchors, not against the abstract signal.** For each borderline call, ask which of these the message most resembles — and stop when a clear anchor matches:

- *Clearly document* (top of durability): a decision the team will re-litigate in six months — an architecture choice, a policy, a rejected alternative worth remembering.
- *Clearly message* (bottom of durability): "deploying in 10, heads up" — true now, worthless next week.
- *Clearly meet* (convergence): two engineers who have disagreed twice in the thread and are not converging — escalate to a call, then write the outcome down.

The escalation trigger is explicit: **after roughly two async round-trips without convergence, move to a synchronous form** rather than a third. `(basis: the thresholds are open-by-design because no source pins them and they are genuinely team-contingent; the anchors + the two-round escalation trigger are the house stopping test that bounds the openness so two writers converge — this is open-by-design WITH a reason and a bound, not open-by-omission.)`

Done-state: the form and the channel are chosen (with the signals that decided them named), the incident boundary is respected, and any `--as=` override and its tension are recorded — the draft phase knows what shape it is writing and where it will go.
