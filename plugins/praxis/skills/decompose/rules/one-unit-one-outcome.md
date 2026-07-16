# One unit, one outcome

The most common way a decomposition goes soft is a unit that quietly does two things — "add logout and refresh the session token," "build the importer and the export report." It reads as one line on a board, but it is two results that ship, verify, and can fail independently, and bundling them means neither can be reviewed, tracked, or reverted on its own. This rule pins the test that separates one unit from two, so two people decomposing the same work draw the boundary in the same place. It is cited by [ingest-the-source](../phases/01-ingest-the-source.md), [carve-into-units](../phases/02-carve-into-units.md), and [make-units-actionable](../phases/04-make-units-actionable.md).

## The discriminator: the single-sentence done-condition

State, in one sentence, what becomes true when the unit is done. Then test that sentence:

- **If you can state it without an "and" that joins two independently-shippable results, it is one unit.** "The `/logout` endpoint clears the session cookie and returns 204" is one outcome — the two clauses describe one coherent result, not two shippable ones.
- **If the sentence needs an "and" joining two results that could each ship and be verified on their own, it is two units — split it.** "Users can log out **and** administrators can see the audit log" is two outcomes wearing one card; each has its own done-condition and its own reason to be worked.
- **The tell** is not the word "and" (a single outcome often has internal clauses) — it is whether the two halves could be *delivered and verified separately*. If cutting the sentence in two leaves each half a shippable, checkable result, they were two units.

`(basis: the single-outcome test operationalizes INVEST's *Independent* and *Testable* (Bill Wake, 2003) — an independent unit is one whose value and verification do not depend on a second unit shipping, and a testable unit is one you can write a pass/fail check for, which a two-outcome unit resists. Craft consensus traceable to INVEST, not a standards mandate.)`

## The inverse: a fragment that is not yet a unit

The test cuts both ways. A candidate whose done-condition is not observable on its own — it only becomes meaningful once another unit lands — is not a unit either; it is a fragment to merge into the unit whose outcome it completes ([unit-size-scale](unit-size-scale.md)'s too-small verdict). One unit, one outcome means exactly one: not two bundled, and not half of one stranded.

## Anchors

- *One unit:* "the password-reset email is sent with a single-use token link" — one outcome, one done-condition, verifiable alone.
- *Two units (split):* "reset password by email and by SMS" — two delivery paths, each independently shippable and verifiable ([prefer-vertical-slices](prefer-vertical-slices.md); this is SPIDR's Path split).
- *A fragment (merge):* "add the `reset_token` column" — no observable outcome until the reset flow reads it; merge into the reset unit.
