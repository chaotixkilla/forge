Fix *what the artifact is for* before a word of it is drafted. A message written before its point is fixed wanders: it recounts what happened instead of saying what it means, buries the ask under context, and leaves the reader to reconstruct the intent the writer never stated.

## Fix the intent: know, do, respond

State, in one sentence each, the answer to four questions — this is the artifact's job, and the draft is judged against it:

- **What must the reader *know* after reading?** The fact or state they didn't have before.
- **What is the reader trying to *do*?** Their **action in the world** — the task in their own work that this artifact has to make possible: ship the dependent change, size the risk before committing, keep a release on track, decide whether to adopt the thing. This is the artifact's reason for existing, and it is **always present**.
- **What must the reader do *in response*?** The **ask** — approve, merge, escalate, reply by Friday, or explicitly nothing.
- **What is the single takeaway** — the one sentence that, if the reader read nothing else, still lets them act correctly?

**The action and the ask are different facts, and conflating them breaks the phases downstream.** The discriminator: *would the reader still be doing this if the artifact had never been sent?* If yes, it is their **action** — it belongs to their work and the artifact merely serves it. If it exists only because the artifact arrived, it is the **ask**. So "keeping the release on schedule" is an action; "confirm you've read this" is an ask.

**An artifact whose ask is explicitly nothing still has an action.** A status update nobody must reply to is read by someone tracking a release; a decision record nobody must approve is read by someone about to build on the decision. Reading "nothing is owed" as "nothing is being enabled" leaves an informational artifact that cannot be sized or sourced at all.

**When the framing names no action, derive it from the artifact type — and say that you did.** A run cannot suspend itself to ask, so leaving this blank guarantees each run invents its own, and the requirement sets derived downstream then diverge on which facts are load-bearing. Take the default for the type fixed below — the reader's minimum action, what they do with that type even when nothing is asked of them — and **carry it back to the caller as a declared assumption** so they can correct it:

| type | default action |
|---|---|
| status update | decide whether this changes what they are currently doing |
| decision record | build on the decision, or re-litigate it |
| doc | perform the task the doc is about |
| onboarding note | get oriented enough to start |
| review/handoff | take over the named work |

Declaring the default keeps this inside the closing checkpoint's bar: that checkpoint forbids an action *silently defaulted*, and a default the caller can see and override is not silent. An unknown **reader** still routes to the user: it cannot be derived from anything the artifact holds, because who receives it is context only the caller has.

`(basis: derived from the type definitions below; the status-update row from three dogfood runs of a deploy notice that split on "does this touch my work")`

`(basis: for the action as an explicit output, derived from right-size-the-detail's precondition and this phase's closing checkpoint)`

Finding the takeaway is the judgment this phase turns on: it is the *conclusion*, the thing everything else is evidence for, not "the first thing that happened." Separate it from setup with [lead-with-the-takeaway](../../../craft/writing/lead-with-the-takeaway.md), which carries the method and its anchors.

## Make the ask explicit — or state there is none

Name precisely what you want from the reader and by when, or state plainly that nothing is owed, to the bar in [make-the-ask-explicit](../../../craft/writing/make-the-ask-explicit.md), which also covers phrasing a deadline that isn't a fix-ETA. Fix it *here*, not in the draft, because the ask shapes the form and channel chosen next: a message that needs an answer by Friday routes differently from a record nobody must act on.

One recurrent case has a pinned default: **a decision communicated to someone with authority to approve it.** Is it an informational record ("here is what we decided") or a ratification request ("we propose this — confirm")? Decide from the framing, and **default to informational**: a decision *record* records a decision already made; it becomes a ratification request only when the framing explicitly seeks sign-off, approval, or confirmation. So "communicate the decision we made, to the maintainer" defaults to no-action-owed; "get the maintainer to sign off on X" is an explicit ask with an owner and a when. When the framing is silent, take the informational default and say so in the artifact ("for the record, no action needed") rather than inventing an approval deadline. `(basis: derived from the decision-record type and make-the-ask-explicit)`

## Name the artifact type — and detect the learning mode

The type is the reader's expectation of shape, and it sets defaults the later phases consume. Classify into one of:

- **status update** — where the work stands now, for people tracking it;
- **decision record** — a decision, its reasoning, and the alternatives rejected, for people who will live with it or re-litigate it — this type owes the *why*, per [preserve-the-why](../../../craft/writing/preserve-the-why.md);
- **doc** — a durable, self-contained reference or explanation people will return to;
- **onboarding note** — orienting material for someone joining the work;
- **review/handoff message** — findings or a state handed to a specific next owner.

Then detect one cross-cutting bit: is the reader in a **learning mode** — being onboarded or mentored, acquiring the skill rather than applying it? Learning mode is not a type and not an audience tier; it is an overlay that layers worked-example scaffolding on top of whatever tier and type this is (a peer being onboarded to a new area is a peer *in learning mode*), governed by [meet-the-learner-where-they-are](../../../craft/writing/meet-the-learner-where-they-are.md). Record it here so the draft phase knows to reach for that rule; it is detected from the intent (does the reader need to *do the task once* or *be able to do it thereafter*?), not from the audience tier. `(basis: maintainer, 2026-07-13; after Diátaxis)`

## Tell adjacent types apart

The five aren't one ladder, so two moves keep a borderline artifact from landing on a different type run to run (the same walk-the-boundaries method the [audience-tiers](../../../craft/writing/audience-tiers.md) discriminators use). First, a boundary test for each of the two pairs that most blur:

- **status update vs review/handoff** — is it *broadcast to whoever tracks the work* (no named recipient, nothing handed over → status update) or *handed to a specific next owner who must act on it* (→ review/handoff)? The line is whether ownership transfers to a named reader.
- **decision record vs doc** — is it anchored to *one decision and the alternatives rejected*, frozen at the moment it was made (→ decision record), or a *standing explanation of a subject* that stays current as the subject evolves (→ doc)? The line is decision-anchored-and-frozen versus subject-anchored-and-living.

Second, when more than one type still fits — a handoff that also records a decision, a doc that also freezes one — do **not** rank the types and drop the loser. **Name the artifact by the reader's primary action** (the *do* fixed at the top of this phase: act on it now → review/handoff; live with or re-litigate a decision → decision record; return to it as reference → doc; get oriented → onboarding note; track progress → status update), then **carry every obligation each fitting type triggers**: a handoff that records a decision stays a handoff *and* keeps the decision's *why*; a doc that freezes one keeps the *why* too. Dropping an obligation (a decision's *why*, a handoff's named ask) is unrecoverable; carrying an extra section a reader can skip is not an error. `(basis: derived from audience-tiers' boundary method and this phase's know/decide/do frame)`

## Establish what the artifact is about — read it, don't reconstruct it

The takeaway is a claim about something real — a decision, a change, a state — and you cannot state it from recollection. Locate the thing itself: recruit the **repository** and **code** explorers for what changed and why in the tree, and the **knowledge-base** explorer for the settled context the artifact rests on (a direct doc-context read — reading, not investigating — which is why it goes to the [knowledge](../../knowledge/SKILL.md) port rather than through `gather`); or, without fan-out, perform those reads inline before continuing. If knowledge is unavailable, degrade to what the session already holds and note where the framing rests on unconfirmed recollection. Recruit only as [fan-out-only-when-it-pays](../../gather/rules/fan-out-only-when-it-pays.md) allows.

This read establishes the artifact's *subject*, which is all this phase needs. What its *reader* needs is a different set, derived and sourced later against the reader and form this phase has not yet fixed — see [derive-and-source](04-derive-and-source.md). Do not try to gather everything here; a sweep run before the audience and form are known returns atmosphere.

## The precondition this phase owes downstream

[right-size-the-detail](../../../craft/writing/right-size-the-detail.md) can only decide altitude once the **target reader** and the **single decision or action** are fixed; this phase is where they are fixed. If either is genuinely ambiguous — the work has no identified audience yet, or no one can say what the artifact is meant to make happen — that is not a gap to fill with an average guess. Stop and surface it: name what is unresolved and route it to the user, because an artifact aimed at no one, enabling no decision, cannot be sized. *(Deliberately open: who the reader is and what they must do is context the author holds and the skill cannot enumerate — but it must be* stated*, not defaulted.)*

Done-state: the takeaway, the reader's action in the world, the ask (or its explicit absence), the artifact type, the learning-mode flag, and the subject are all fixed and written down.
