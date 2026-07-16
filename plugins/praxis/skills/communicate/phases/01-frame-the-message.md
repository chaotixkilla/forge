A message written before its point is fixed wanders: it recounts what happened instead of saying what it means, buries the ask under context, and leaves the reader to reconstruct the intent the writer never stated. This phase fixes *what the artifact is for* before a word of it is drafted — the three facts every later phase depends on: what the reader must take away, what they must do, and what kind of artifact this is. Skip it and the draft optimizes for the writer's memory of events, not the reader's need.

## Fix the intent: know, decide, or do

State, in one sentence each, the answer to three questions — this is the artifact's job, and the draft is judged against it:

- **What must the reader *know* after reading?** The fact or state they didn't have before.
- **What must the reader *decide* or *do*?** The action the artifact exists to enable — approve, merge, adopt, escalate, or simply "nothing, this is for the record."
- **What is the single takeaway** — the one sentence that, if the reader read nothing else, still lets them act correctly?

Finding the takeaway is the judgment this phase turns on, and it is not "the first thing that happened" — it is the *conclusion*, the thing everything else is evidence for. The discriminator between takeaway and setup: setup is what the reader needs to *believe* the takeaway; the takeaway is what they *act on*. If a sentence can be cut and the reader still knows what to do, it was setup; if cutting it leaves them unable to act, it was the takeaway. Apply [lead-with-the-takeaway](../rules/lead-with-the-takeaway.md) to separate the two — that rule carries the full method and its anchors.

## Make the ask explicit — or state there is none

An implied ask gets no response: the reader who isn't sure whether they're being informed or asked will default to informed and move on. Name precisely what you want from the reader and by when, or state plainly that nothing is owed. The bar for an explicit ask, and how to phrase a deadline that isn't a fix-ETA, is [make-the-ask-explicit](../rules/make-the-ask-explicit.md). This is fixed *here*, not discovered in the draft, because the ask shapes the form and channel chosen next — a message that needs an answer by Friday routes differently from a record nobody must act on.

One recurrent case needs a pinned default so two writers don't diverge: **a decision communicated to someone with authority to approve it.** Is it an informational record ("here is what we decided") or a ratification request ("we propose this — confirm")? Decide from the framing, and **default to informational**: a decision *record* records a decision already made; it becomes a ratification request only when the framing explicitly seeks sign-off, approval, or confirmation. So "communicate the decision we made, to the maintainer" defaults to no-action-owed; "get the maintainer to sign off on X" is an explicit ask with an owner and a when. When the framing is silent, take the informational default and say so in the artifact ("for the record, no action needed") rather than inventing an approval deadline. `(basis: the default follows the artifact type — a decision record's job is to record, per [preserve-the-why](../rules/preserve-the-why.md); an ask is added only when the framing states one, mirroring make-the-ask-explicit's "or explicitly nothing.")`

## Name the artifact type — and detect the learning mode

The type is the reader's expectation of shape, and it sets defaults the later phases consume. Classify into one of:

- **status update** — where the work stands now, for people tracking it;
- **decision record** — a decision, its reasoning, and the alternatives rejected, for people who will live with it or re-litigate it — this type owes the *why*, per [preserve-the-why](../rules/preserve-the-why.md);
- **doc** — a durable, self-contained reference or explanation people will return to;
- **onboarding note** — orienting material for someone joining the work;
- **review/handoff message** — findings or a state handed to a specific next owner.

Then detect one cross-cutting bit: is the reader in a **learning mode** — being onboarded or mentored, acquiring the skill rather than applying it? Learning mode is not a type and not an audience tier; it is an overlay that layers worked-example scaffolding on top of whatever tier and type this is (a peer being onboarded to a new area is a peer *in learning mode*), governed by [meet-the-learner-where-they-are](../rules/meet-the-learner-where-they-are.md). Record it here so the draft phase knows to reach for that rule; it is detected from the intent (does the reader need to *do the task once* or *be able to do it thereafter*?), not from the audience tier. `(basis: Diátaxis — acquisition-vs-application is a situation the reader is in, orthogonal to who they are; ratified house decision, 2026-07-13, learning is a mode overlay, not a fifth audience tier.)`

## Tell adjacent types apart

The five aren't one ladder, so two moves keep a borderline artifact from landing on a different type run to run (the same walk-the-boundaries method the [audience-tiers](../rules/audience-tiers.md) discriminators use). First, a boundary test for each of the two pairs that most blur:

- **status update vs review/handoff** — is it *broadcast to whoever tracks the work* (no named recipient, nothing handed over → status update) or *handed to a specific next owner who must act on it* (→ review/handoff)? The line is whether ownership transfers to a named reader.
- **decision record vs doc** — is it anchored to *one decision and the alternatives rejected*, frozen at the moment it was made (→ decision record), or a *standing explanation of a subject* that stays current as the subject evolves (→ doc)? The line is decision-anchored-and-frozen versus subject-anchored-and-living.

Second, when more than one type still fits — a handoff that also records a decision, a doc that also freezes one — do **not** rank the types and drop the loser. **Name the artifact by the reader's primary action** (the *do* fixed at the top of this phase: act on it now → review/handoff; live with or re-litigate a decision → decision record; return to it as reference → doc; get oriented → onboarding note; track progress → status update), then **carry every obligation each fitting type triggers**: a handoff that records a decision stays a handoff *and* keeps the decision's *why*; a doc that freezes one keeps the *why* too. Types are not exclusive picks — obligations are cumulative, and the only real error is *dropping* one (a decision's *why*, a handoff's named ask), which is unrecoverable, never merely carrying an extra section a reader can skip. `(basis: the walk-the-boundaries method mirrors [audience-tiers](../rules/audience-tiers.md); typing by the reader's primary action reuses this phase's own know/decide/do frame, and treating obligations as cumulative rather than one exclusive pick is what closes the non-status pairs a partial-order tie-break cannot rank.)`

## Gather the substance — read it, don't reconstruct it

The artifact reports something real — a decision, a change, a state — and the facts must come from the work, not the writer's recollection. Where the substance isn't fully in hand, recruit the explorers to read it: the **repository** and **code** explorers for what changed and why in the tree, the **knowledge-base** explorer for the settled context and prior decisions the artifact rests on (this is the direct doc-context read that keeps `tools.knowledge` on this skill — reading, not investigating). Without fan-out, do these reads inline before drafting — locate the decision, the change, or the state yourself; the reads are not optional, only the delegation is. If knowledge is unavailable, degrade to what the session already holds and note that the artifact rests on unconfirmed recollection where it does.

## The precondition this phase owes downstream

[right-size-the-detail](../rules/right-size-the-detail.md) can only decide altitude once the **target reader** and the **single decision or action** are fixed; this phase is where they are fixed. If either is genuinely ambiguous — the work has no identified audience yet, or no one can say what the artifact is meant to make happen — that is not a gap to fill with an average guess. Stop and surface it: name what is unresolved and route it to the user, because an artifact aimed at no one, enabling no decision, cannot be sized. *(Deliberately open: who the reader is and what they must do is context the author holds and the skill cannot enumerate — but it must be* stated*, not defaulted; an unstated audience is the open-by-omission this checkpoint prevents.)*

Done-state: the takeaway, the ask (or its explicit absence), the artifact type, the learning-mode flag, and the substance are all fixed and written down — enough that the next phase profiles a reader against a known message, not a vague one.
