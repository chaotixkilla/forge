A message written before its point is fixed wanders: it recounts what happened instead of saying what it means, buries the ask under context, and leaves the reader to reconstruct the intent the writer never stated. This phase fixes *what the artifact is for* before a word of it is drafted — the facts every later phase depends on: what the reader must take away, what they are trying to do, what they must do in response, and what kind of artifact this is. Skip it and the draft optimizes for the writer's memory of events, not the reader's need.

## Fix the intent: know, do, respond

State, in one sentence each, the answer to four questions — this is the artifact's job, and the draft is judged against it:

- **What must the reader *know* after reading?** The fact or state they didn't have before.
- **What is the reader trying to *do*?** Their **action in the world** — the task in their own work that this artifact has to make possible: ship the dependent change, size the risk before committing, keep a release on track, decide whether to adopt the thing. This is the artifact's reason for existing, and it is **always present**.
- **What must the reader do *in response*?** The **ask** — approve, merge, escalate, reply by Friday, or explicitly nothing.
- **What is the single takeaway** — the one sentence that, if the reader read nothing else, still lets them act correctly?

**The action and the ask are different facts, and conflating them breaks the phases downstream.** The discriminator: *would the reader still be doing this if the artifact had never been sent?* If yes, it is their **action** — it belongs to their work and the artifact merely serves it. If it exists only because the artifact arrived, it is the **ask**. So "keeping the release on schedule" is an action; "confirm you've read this" is an ask.

The consequence worth stating plainly: **an artifact whose ask is explicitly nothing still has an action.** A status update nobody must reply to is read by someone tracking a release; a decision record nobody must approve is read by someone about to build on the decision. An informational artifact is not an artifact with no purpose — the ask is empty and the action is not, and reading "nothing is owed" as "nothing is being enabled" is what turns a legitimate informational artifact into one that cannot be sized or sourced at all.

**When the framing names no action, derive it from the artifact type — and say that you did.** A run cannot suspend itself to ask, so leaving this blank guarantees each run invents its own, and the requirement sets derived downstream then diverge on which facts are load-bearing. Take the default for the type fixed below, and **carry it back to the caller as a declared assumption** so they can correct it:

| type | default action |
|---|---|
| status update | decide whether this changes what they are currently doing |
| decision record | build on the decision, or re-litigate it |
| doc | perform the task the doc is about |
| onboarding note | get oriented enough to start |
| review/handoff | take over the named work |

Declaring the default is what keeps this inside the closing checkpoint's bar rather than around it: that checkpoint forbids an action *silently defaulted*, and a default the caller can see and override is not silent. What still routes to the user is an unknown **reader** — that one cannot be derived from anything the artifact holds, because who receives it is context only the caller has.

`(basis: each default is the reader's minimum action for that type — the thing a reader of that artifact does with it even when nothing is asked of them, derived from the type definitions below rather than added as new judgment. The status-update default is pinned against an observed failure: three runs of a deploy notice spread 6/6/2 on their requirement sets and split on whether "does this touch my work" was content, a stated absence, or absent — the default makes that fact required by construction, since a reader deciding whether the deploy changes what they are doing cannot decide it without knowing whether it touches them.)`

`(basis: this phase's own closing precondition already presupposes the action — it holds that "an artifact aimed at no one, enabling no decision, cannot be sized" — and [right-size-the-detail](../rules/right-size-the-detail.md) states outright that its test needs "the target reader and the single decision or action the artifact must enable" and that this phase "fixes both." Both already depend on the action; naming it as an explicit output makes an existing assumption reachable rather than adding a requirement. The would-they-be-doing-it-anyway discriminator is the same counterfactual cut this phase already uses to separate takeaway from setup, applied to a different pair.)`

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

## Establish what the artifact is about — read it, don't reconstruct it

The takeaway is a claim about something real — a decision, a change, a state — and you cannot state it from recollection. Locate the thing itself: recruit the **repository** and **code** explorers for what changed and why in the tree, and the **knowledge-base** explorer for the settled context the artifact rests on (a direct doc-context read — reading, not investigating — which is why it goes to the [knowledge](../../knowledge/SKILL.md) port rather than through `gather`); or, without fan-out, perform those reads inline before continuing. If knowledge is unavailable, degrade to what the session already holds and note where the framing rests on unconfirmed recollection.

This read establishes the artifact's *subject*, which is all this phase needs. What its *reader* needs is a different set, derived and sourced later against the reader and form this phase has not yet fixed — see [derive-and-source](04-derive-and-source.md). Do not try to gather everything here; a sweep run before the audience and form are known returns atmosphere.

## The precondition this phase owes downstream

[right-size-the-detail](../rules/right-size-the-detail.md) can only decide altitude once the **target reader** and the **single decision or action** are fixed; this phase is where they are fixed. If either is genuinely ambiguous — the work has no identified audience yet, or no one can say what the artifact is meant to make happen — that is not a gap to fill with an average guess. Stop and surface it: name what is unresolved and route it to the user, because an artifact aimed at no one, enabling no decision, cannot be sized. *(Deliberately open: who the reader is and what they must do is context the author holds and the skill cannot enumerate — but it must be* stated*, not defaulted; an unstated audience is the open-by-omission this checkpoint prevents.)*

Done-state: the takeaway, the reader's action in the world, the ask (or its explicit absence), the artifact type, the learning-mode flag, and the subject are all fixed and written down — enough that the next phase profiles a reader against a known message, not a vague one.
