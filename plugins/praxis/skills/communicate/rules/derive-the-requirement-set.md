# Derive the requirement set

An artifact is complete relative to a reader and an action, not relative to what its author happened to know — but the author's knowledge is what a draft reaches for by default, and the gap between the two is invisible from inside the draft. This rule produces the set of things the reader must have, by construction rather than by recall, so that completeness becomes checkable instead of felt. It is applied in [derive-and-source](../phases/04-derive-and-source.md).

## The seam with the sizing rules

This rule **enumerates**; the sizing rules then act on what it hands them — [right-size-the-detail](right-size-the-detail.md) and [respect-the-readers-time](respect-the-readers-time.md) own the seam between themselves. One direction of travel, no shared bar. The reason derivation must run first: a filter can only sort what it is handed, so a requirement never derived is never tiered and never missed.

**An absence that reaches the artifact is tierable — but never to zero.** [source-or-declare](source-or-declare.md) decides *which* absences reach the reader's copy at all; the ones that do enter the sizing rules like any other entry and may be deferred or compressed to a clause. What they may not be is **dropped**, because dropping an absence the reader was judged to need restores exactly the silent gap the declaration exists to prevent. Where sizing would cut one entirely, it stays inline in its shortest honest form. `(basis: the two rules divide cleanly once the audience question is settled first — that rule sorts absences by audience, this one sizes the reader's share. Sizing cannot be the thing that removes an absence from the reader's copy, because sizing has no way to tell a gap the reader needs from one they do not; that is the action-keyed test, and it runs earlier.)`

## Walk the action, don't recall the topic

Take the single decision or action fixed in [frame-the-message](../phases/01-frame-the-message.md) and walk it as the reader will perform it, step by step. At each step ask: **what must this reader already know, or have in front of them, to take this step correctly?** Each answer is one requirement.

Walking the *action* rather than surveying the *topic* is the whole method. A topic survey returns what is interesting about the subject and is unbounded; an action walk returns what is load-bearing for one reader doing one thing, and terminates. The difference shows up most where the reader must not do something — a step they could plausibly take and shouldn't is a requirement (*the constraint that rules it out*), and a topic survey never surfaces it because nothing about the subject is missing.

Two requirement classes fall out of the walk that recall reliably misses, so sweep for them explicitly:

- **Preconditions** — what must be true before the reader starts, including what happens if it isn't.
- **Failure and boundary conditions** — what the reader sees when the step does not go as described, and where the described behavior stops applying. A reader who only has the happy path will follow it into the case it does not cover.

`(basis: derived from [right-size-the-detail](right-size-the-detail.md)'s need-to-know test, run forward as enumeration rather than backward as a filter — that rule already establishes the reader-and-action pair as the thing altitude is relative to, and asks of an existing detail "what does its absence cost the named reader pursuing the named action?"; asking the same question of the action's steps rather than of a candidate list yields the set the filter presupposes. The precondition and failure-condition sweeps are the recall-blind classes that forward derivation exposes and backward filtering cannot.)`

## The discriminator: required, not relevant

The set bloats if every true and interesting fact enters it. The test that separates a requirement from a relevant fact: **remove it, and can the reader still complete the step correctly?** If yes, it is not a requirement — it may still earn a place as context, but it enters [right-size-the-detail](right-size-the-detail.md) as an ordinary candidate rather than as something the artifact owes.

Note the word *correctly*. A reader who can complete the step but would do it wrong, or would not know they had done it wrong, is missing a requirement.

`(basis: the same need-to-know test cited above, applied as an inclusion filter on the derived set rather than as a tier sort — "removing it changes what the reader can decide or do" is [right-size-the-detail](right-size-the-detail.md)'s own Tier-1 definition, and reusing it here is what keeps the two rules on one bar instead of two competing ones. The *correctly* qualifier is the addition forward derivation needs: a backward filter only ever sees details someone already wrote down, so it never encounters the silent-wrong-completion case.)`

## The stopping test

The set is complete when all hold:

1. Every step of the walked action has at least one requirement covering what the reader needs to take it, or is explicitly noted as needing nothing.
2. The precondition and failure-condition sweeps have both been run.
3. One further pass over the walked action surfaces no requirement not already in the set.
4. Every entry passes the required-not-relevant discriminator.

When 1–4 hold, stop. Two writers walking the same action for the same reader converge on **the same load-bearing entries** — the facts whose absence changes what the reader can do. They routinely differ on **granularity**: whether a compound precondition is one requirement or two, and how finely the failure sweep splits. That residue is deliberate and bounded, because a split entry and a merged one carry the same content into the draft — the artifact converges even where the set's row count does not.

What must **not** differ is *which facts are present*. A set missing a load-bearing entry has failed clause 1; it has not merely chosen a coarser grain.

`(basis: observed — house dogfood runs walking the same action converged on the facts and differed on entry granularity, so the claim is pinned at the level the evidence supports. A stronger claim of row-level identity was falsified by those runs, and the reader-and-action pair fixed in [frame-the-message](../phases/01-frame-the-message.md) is what bounds the remaining spread.)`

## When the walk yields nothing

An action walk that surfaces no requirement means the reader can already act — there is nothing the artifact adds. That is a real and reportable outcome, not an empty set to paper over: say so rather than drafting an artifact with no job. In practice it usually means the reader or the action was never genuinely fixed, which routes back to [frame-the-message](../phases/01-frame-the-message.md)'s closing checkpoint.
