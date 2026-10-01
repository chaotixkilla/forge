# Source or declare

Every *requirement* — a fact the artifact's reader needs in order to act — ends one of two ways: it is obtained from a real source, or its absence is declared. The ending a draft reaches for by default, where the slot is filled with a plausible sentence nobody sourced, must not exist.

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

  **How wide the check must be — and no wider.** The search you owe is exactly **the locations already in scope for this artifact's subject**: the tree, records, and knowledge the artifact's subject was read from. Check those and find nothing, and *nowhere* is available. You do **not** owe a wider sweep — and if a plausible holder exists outside that scope, the requirement is **reachable-and-blocked with that holder named**, not nowhere. `(basis: derived from the stop bar's investigation boundary below)`

## When the caller supplies the fact

Two cases, and the discriminator is **could any source contradict this?**

- **A claim about the world** — a system's state, a number, what some code does. A source could contradict it, so it is in-session only once confirmed. When the read contradicts it, **the source wins and the contradiction is surfaced** — correct the artifact and tell the caller what you found, rather than silently overriding them or deferring to them. A caller is often right about intent and wrong about current state, and an artifact repeating a stale belief propagates it with the artifact's authority behind it.
- **A declaration of the caller's own intent or action** — *"we're deploying in ten minutes," "we've decided to adopt this," "I'm handing it to the platform team."* The caller **is** the source. No read could contradict them, because the fact is constituted by their saying it. **In session, and no confirmation is owed.**

Getting this backwards is the failure that makes short coordination artifacts absurd: treat a speaker's own announcement as an unconfirmed claim and every fact in a deploy notice becomes blocked, and the declaration bar then demands the notice declare its own content as missing.

Where a single sentence carries both — *"we're deploying the billing service, which fixes the timeout bug"* — split it: the deploy is self-sourced, the claim about what it fixes is a claim about the world and gets confirmed.

`(basis: speech-act theory's assertive/commissive distinction)`

**Anchors.** *In session*: what the change under discussion does — read this run, in hand. *Reachable*: a config key's default value — unknown to you, but `the config module` holds it and the read is one hop. *Nowhere*: how long the migration will take against production traffic, where nobody has measured it and no comparable run exists — no file and no person holds it.

`(basis: derived, a partition on "where does the answer live?")`

## Obtained or blocked — an axis, not a fourth disposition

A requirement in a reachable source can still fail to arrive: the backend is unavailable, the read errors, or obtaining it needs work beyond what writing does. That is **blocked** — it colors the requirement without moving it off *reachable*, because the answer still lives where it lives.

Blocked matters because it changes what the reader is told, and collapsing it into *nowhere* states something false: that the knowledge does not exist, when it does and is one read away.

## When to stop digging

Stop and mark a reachable requirement **blocked** when any holds:

- The read was attempted at the named location and failed or returned nothing.
- The backend holding it is unavailable.
- Obtaining it requires an **investigation rather than a read** — tracing behavior, running the system, standing up an experiment, or a weighted multi-source dig.

That third condition is a boundary, not a budget. Writing reads what it needs as direct context; it does not run investigations, and a writer that starts one has stopped writing and should say so — name what would settle the requirement so the caller can route it to an investigation.

`(basis: derived from writing's scope: it reads, it doesn't investigate)`

## The declaration bar

An unobtained requirement carries **two separate duties**, and collapsing them is what turns a short notice into a list of apologies:

1. **Reported to the caller — always, without exception.** Every requirement that came out blocked or nowhere goes back to whoever asked for the artifact, because they are usually the one person who can supply it. This duty never scales, never tiers, and is never traded away. It is the honesty bar.
2. **Stated in the artifact — only where the reader needs it.** The test: *can the reader take their named action without knowing this is missing?* If yes, it belongs in the report to the caller and not in the reader's copy. If no, it is stated inline in its shortest honest form.

Note what duty 2 turns on — not whether the reader needs the **fact**, but whether they need to know the fact is **absent**. A teammate deciding whether to pause work around a deploy cannot decide it without knowing whether impact is expected, so *that* absence is stated. They can decide it perfectly well without knowing that the release contents were unavailable, so that one goes to the caller alone. Both were derived; only one is the reader's business.

`(basis: observed in three house dogfood runs of a nine-word deploy notice)`

Within the reader's copy, three things stay distinct:

- **Nowhere** → *no one has established this.* A gap in the world. Where it is knowable in principle, name what would settle it.
- **Blocked** → *this is established, but this artifact does not carry it* — plus what would settle it. A gap in **this artifact**, not in the subject.
- **Obtained** → no declaration; it is simply content.

**The blocked form, precisely — one shape for every way a read can fail.** Whether the holder was unconfigured, unreachable, or returned nothing, the declaration is the same, and it carries two things:

1. **That the fact exists elsewhere and is not carried here.** Name the holder *only* in terms the reader could act on — a team, a document, a system they already know — and only when such a holder can honestly be named. When none can, the declaration is still complete without it.
2. **What would settle it** — the next step a reader could actually take.

And one thing it must **never** carry: **the cause of the failure.** Not that a backend was unconfigured, not that a read errored, not that a capability was unavailable. A reader cannot act on why a lookup failed; they can act on where the answer lives and what to do next. So *"the retention window is set per-environment and is not recorded here — the platform team owns the current values"* is a declaration; *"the knowledge base was unavailable"* is production history wearing a declaration's clothes.

This is what keeps the bar satisfiable in every case and keeps it from colliding with [clean-export](clean-export.md): a form that required naming a location would be unsatisfiable when there is no nameable holder, and a form that required naming the cause would demand exactly the machinery a delivered artifact must not carry.

`(basis: derived from clean-export's machinery-vs-content discriminator)`

What a declaration may never become is a smooth sentence that fills the slot without a source. An invented answer is worse than an omission, because omission leaves the reader looking while invention tells them they are done.

`(basis: derived from the evidence standards' discipline for what wasn't established: it is declared, never filled)`

## A proxy may accompany a declared absence — never occupy its slot

When the absent figure has a *related* quantity that can be measured, offering it is legitimate and often useful. What is not legitimate is letting it stand **where the absent figure would have gone**: a real measurement sitting in the answer's slot reads as the answer, which is the invented sentence again — this time wearing a genuine number's clothes, which makes it harder to catch, not easier.

So the placement is pinned:

- **The declared absence is the headline.** It occupies the slot the reader came to, and it is what the artifact leads with on that point.
- **A proxy is supporting detail, never the lead**, and it is **labelled as not the thing asked for** — with one clause saying what it does and does not tell the reader. *"Nobody has measured review turnaround. For scale: the review path is ~6,700 words of procedure, which bounds how much a reviewer reads — it says nothing about elapsed time."*
- **No proxy at all is always a valid choice.** Offer one only where it serves the reader's named action; a related number that serves no action is padding with a measurement's authority.

`(basis: observed in three house dogfood runs that each led with a different proxy)`

## The declaration is not a hedge

Declaring an absence is a precise statement, not a softening. *"There is currently no harness that exercises this boundary"* is a declaration; *"testing may vary depending on your setup"* is a hedge wearing a declaration's clothes — it states nothing and cannot be acted on. The test: **does the sentence tell the reader something definite about the state of the world?** If it survives only because it is vague, it is the invented sentence again ([respect-the-readers-time](respect-the-readers-time.md) owns the word-level cut that catches it).
