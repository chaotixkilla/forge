# Source or declare

Every derived requirement ends one of two ways: it is obtained from a real source, or its absence is stated to the reader. There is no third ending — and the ending a draft reaches for by default is a fourth one that must not exist, where the slot is filled with a plausible sentence nobody sourced. This rule pins where each requirement's answer lives, when to stop looking, and what an honest declaration says. It is applied in [derive-and-source](../phases/04-derive-and-source.md).

## The three dispositions

Every requirement sits on exactly one, and the axis is **where the answer lives**:

| disposition | definition |
|---|---|
| **in session** | this run has already established it — read from a source during the run, or supplied by the caller and confirmed against one |
| **in a reachable source** | not established here, but you can name the file, record, or person that holds it |
| **nowhere** | no one has established it; naming a location for it would itself be a guess |

**Discriminators.**

- *in session vs. in a reachable source* — has this run actually established the answer, or would establishing it require a read not yet performed? Believing a fact is not establishing it. When both fit (established here, and also sitting in the tree), **in session wins** — a settled requirement is not re-sourced.
- *in a reachable source vs. nowhere* — **can you name where to look?** A named file, record, or person → reachable. Naming one would be a guess → nowhere. This is the load-bearing discriminator, because the cheap error runs one way: a run that did not look concludes "nobody knows," and a genuine gap and an unexamined one read identically in the finished artifact. So *nowhere* is a claim with a precondition: it is available only once you can state **what you checked, or why no source would hold it**. "I did not look" resolves to reachable-and-blocked, never to nowhere.

  **How wide the check must be — and no wider.** The search you owe is exactly **the locations already in scope for this artifact's subject**: the tree, records, and knowledge the subject read in [frame-the-message](../phases/01-frame-the-message.md) already covered. Check those and find nothing, and *nowhere* is available. You do **not** owe a wider sweep — and if a plausible holder exists outside that scope, the requirement is **reachable-and-blocked with that holder named**, not nowhere. `(basis: the width inherits the scope boundary this rule already pins below — a wider sweep is an investigation, which belongs to the gather capability and not to this skill. Deriving the bound from the existing boundary rather than pinning a fresh one is deliberate: a new independent threshold here would itself need a tightness, which is how the previous fix at this seam opened a new gap.)`

## When the caller supplies the fact

Two cases, and the discriminator is **could any source contradict this?**

- **A claim about the world** — a system's state, a number, what some code does. A source could contradict it, so it is in-session only once confirmed. When the read contradicts it, **the source wins and the contradiction is surfaced** — correct the artifact and tell the caller what you found, rather than silently overriding them or deferring to them. A caller is often right about intent and wrong about current state, and an artifact repeating a stale belief propagates it with the artifact's authority behind it.
- **A declaration of the caller's own intent or action** — *"we're deploying in ten minutes," "we've decided to adopt this," "I'm handing it to the platform team."* The caller **is** the source. No read could contradict them, because the fact is constituted by their saying it. **In session, and no confirmation is owed.**

Getting this backwards is the failure that makes short coordination artifacts absurd: treat a speaker's own announcement as an unconfirmed claim and every fact in a deploy notice becomes blocked, and the declaration bar then demands the notice declare its own content as missing.

Where a single sentence carries both — *"we're deploying the billing service, which fixes the timeout bug"* — split it: the deploy is self-sourced, the claim about what it fixes is a claim about the world and gets confirmed.

`(basis: the assertive-versus-commissive distinction from speech-act theory — an assertion describes a state of affairs and can be false against it, while a declaration of one's own intent or undertaking constitutes the fact rather than reporting it, so there is no external state for it to be false against. That is exactly the line this discriminator needs, and it is why "could any source contradict this?" is decidable rather than a judgment about how much to trust the caller.)`

**Anchors.** *In session*: what the change under discussion does — read this run, in hand. *Reachable*: a config key's default value — unknown to you, but `the config module` holds it and the read is one hop. *Nowhere*: how long the migration will take against production traffic, where nobody has measured it and no comparable run exists — no file and no person holds it.

`(basis: the set is a partition by construction on the question "where does the answer live?" — an answer has been established in this run, or exists somewhere nameable, or does not exist; there is no fourth location, and the in-session tie-break makes the three mutually exclusive. The name-the-location discriminator is what keeps the partition honest, since the boundary that actually gets misclassified is reachable-read-as-nowhere.)`

## Obtained or blocked — an axis, not a fourth disposition

A requirement in a reachable source can still fail to arrive: the backend is unavailable, the read errors, or obtaining it needs work beyond this skill's mandate. That is **blocked** — it colors the requirement without moving it off *reachable*, because the answer still lives where it lives.

Blocked matters because it changes what the reader is told, and collapsing it into *nowhere* states something false: that the knowledge does not exist, when it does and is one read away.

## When to stop digging

Stop and mark a reachable requirement **blocked** when any holds:

- The read was attempted at the named location and failed or returned nothing.
- The backend holding it is unavailable (communicate's standing degrade posture).
- Obtaining it requires an **investigation rather than a read** — tracing behavior, running the system, standing up an experiment, or a weighted multi-source dig.

That third condition is a boundary, not a budget. communicate reads knowledge as direct doc-context; it does not run investigations, and a run that starts one has left this skill and should say so — name what would settle the requirement so the caller can route it.

`(basis: communicate's own scope, stated in its SKILL.md and usage.md — knowledge is read as direct doc-context, and the weighted cross-lane investigation belongs to the gather capability. The stop bar is that boundary applied per requirement rather than per run, so a single unreachable fact degrades one line of the artifact instead of silently expanding the skill's mandate.)`

## The declaration bar

An unobtained requirement carries **two separate duties**, and collapsing them is what turns a short notice into a list of apologies:

1. **Reported to the caller — always, without exception.** Every requirement that came out blocked or nowhere goes back to whoever asked for the artifact, because they are usually the one person who can supply it. This duty never scales, never tiers, and is never traded away. It is the honesty bar.
2. **Stated in the artifact — only where the reader needs it.** The test: *can the reader take their named action without knowing this is missing?* If yes, it belongs in the report to the caller and not in the reader's copy. If no, it is stated inline in its shortest honest form.

Note what duty 2 turns on — not whether the reader needs the **fact**, but whether they need to know the fact is **absent**. A teammate deciding whether to pause work around a deploy cannot decide it without knowing whether impact is expected, so *that* absence is stated. They can decide it perfectly well without knowing that the release contents were unavailable, so that one goes to the caller alone. Both were derived; only one is the reader's business.

`(basis: pinned against an observed failure — three runs of a nine-word deploy notice produced 55, 73 and 77-word artifacts in which the majority of the text was absences, because a single undifferentiated duty forced every blocked requirement into the reader's copy. Splitting the duties preserves the honesty bar completely, since nothing is dropped: what changes is only which of two audiences receives it. The artifact-side test reuses this skill's existing action frame rather than adding judgment, and asks about the absence rather than the fact because that is the narrower question — a reader needs far fewer absences than facts.)`

Within the reader's copy, three things stay distinct:

- **Nowhere** → *no one has established this.* A gap in the world. Where it is knowable in principle, name what would settle it.
- **Blocked** → *this is established, but this artifact does not carry it* — plus what would settle it. A gap in **this artifact**, not in the subject.
- **Obtained** → no declaration; it is simply content.

**The blocked form, precisely — one shape for every way a read can fail.** Whether the holder was unconfigured, unreachable, or returned nothing, the declaration is the same, and it carries two things:

1. **That the fact exists elsewhere and is not carried here.** Name the holder *only* in terms the reader could act on — a team, a document, a system they already know — and only when such a holder can honestly be named. When none can, the declaration is still complete without it.
2. **What would settle it** — the next step a reader could actually take.

And one thing it must **never** carry: **the cause of the failure.** Not that a backend was unconfigured, not that a read errored, not that a capability was unavailable. A reader cannot act on why a lookup failed; they can act on where the answer lives and what to do next. So *"the retention window is set per-environment and is not recorded here — the platform team owns the current values"* is a declaration; *"the knowledge base was unavailable"* is production history wearing a declaration's clothes.

This is what keeps the bar satisfiable in every case and keeps it from colliding with [clean-export](clean-export.md): a form that required naming a location would be unsatisfiable when there is no nameable holder, and a form that required naming the cause would demand exactly the machinery a delivered artifact must not carry.

`(basis: the split is decided by clean-export's own discriminator, not by ranking the two rules — a sentence is machinery when removing it loses *how the artifact was produced* but no fact the reader needs, and content when it loses a fact the reader acts on. The failure's cause is production history by that test; the holder and the next step are actionable by it. So the two rules agree once the declaration is written at the reader's altitude, and the earlier appearance of a conflict came from stating the run's internal condition instead of the reader's.)`

What a declaration may never become is a smooth sentence that fills the slot without a source. An invented answer is worse than an omission, because omission leaves the reader looking while invention tells them they are done. If you cannot write the fact, write the absence.

`(basis: the house discipline the sibling investigative skills already run — understand's "what stays unknown" holds that a gap named is honest scope while a gap omitted reads as covered, "a different and false claim," and deep-research names its uncertainty and its unestablished sub-questions as first-class output. This rule applies the same bar to an artifact's content slots; the nowhere/blocked split is the addition, because an artifact's reader can act on "it exists, go read it" and cannot act on an undifferentiated gap.)`

## A proxy may accompany a declared absence — never occupy its slot

When the absent figure has a *related* quantity that can be measured, offering it is legitimate and often useful. What is not legitimate is letting it stand **where the absent figure would have gone**: a real measurement sitting in the answer's slot reads as the answer, which is the invented sentence again — this time wearing a genuine number's clothes, which makes it harder to catch, not easier.

So the placement is pinned:

- **The declared absence is the headline.** It occupies the slot the reader came to, and it is what the artifact leads with on that point.
- **A proxy is supporting detail, never the lead**, and it is **labelled as not the thing asked for** — with one clause saying what it does and does not tell the reader. *"Nobody has measured review turnaround. For scale: the review path is ~6,700 words of procedure, which bounds how much a reviewer reads — it says nothing about elapsed time."*
- **No proxy at all is always a valid choice.** Offer one only where it serves the reader's named action; a related number that serves no action is padding with a measurement's authority.

`(basis: the divergence this closes was positional, not evidential — three runs each offered a *correctly measured* proxy for the same absent figure and produced three incomparable headline units, because nothing said the absence rather than the substitute was the lead. Pinning the slot converges them without forbidding adjacent measurement, which is often the most useful thing an artifact can give a reader who cannot have the figure they wanted. The label requirement follows the same test the declaration bar uses: a reader must be able to tell what is established from what is being offered in its place.)`

## The declaration is not a hedge

Declaring an absence is a precise statement, not a softening. *"There is currently no harness that exercises this boundary"* is a declaration; *"testing may vary depending on your setup"* is a hedge wearing a declaration's clothes — it states nothing and cannot be acted on. The test: **does the sentence tell the reader something definite about the state of the world?** If it survives only because it is vague, it is the invented sentence again ([respect-the-readers-time](respect-the-readers-time.md) owns the word-level cut that catches it).
