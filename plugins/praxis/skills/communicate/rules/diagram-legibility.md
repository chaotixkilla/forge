# Diagram legibility

A diagram that is correct and unreadable has failed, and it fails invisibly — nothing in a review catches it, because every node in it is true. The two ways it happens are size (everything the author knows, crammed into one picture) and silence (what was left out is not stated, so the picture reads as the whole system). This rule pins the notation, the size bar, and the elision bar. It is applied where a diagram is rendered, in [derive-and-source](../phases/04-derive-and-source.md) and [draft-the-content](../phases/05-draft-the-content.md).

## Notation

Emit diagrams as **mermaid in a fenced block**. It is a house default rather than a law — a team with a drawing backend may reasonably swap it — but it is pinned so that two runs do not produce two notations for the same artifact.

Where the destination cannot render it, do not silently flatten: leave the visible placeholder that names the content and points to its source form, per [degrade-unsupported-content](../../publish-artifact/rules/degrade-unsupported-content.md).

`(basis: praxis emits diagrams as inline text and declares no drawing backend — the constraint understand's diagram module already states, which keeps a diagram from dragging a config prerequisite into a skill that has none. Among text notations, mermaid has the widest render support across the destinations this skill delivers to, and the degrade path for a backend that cannot render it already exists in the artifacts port. The choice is contingent house practice, marked as such, not an invariant of good diagrams.)`

## Size: one level of abstraction per picture

The bar is a test, not a count: **can a reader who does not know the system restate the relation after one pass over the diagram?** If they must study it, it is carrying more than one picture's worth.

When it is, **split by abstraction level rather than shrinking the font** — one diagram showing how the parts relate, another expanding the part that matters, each self-contained and named. A single picture spanning levels is the common failure: it mixes a service boundary with a function call and gives the reader no consistent unit.

`(basis: level-decomposition over cramming is the core discipline of the C4 model, which prescribes distinct diagrams at distinct levels of abstraction rather than one diagram at all of them; the restate-after-one-pass test is the legibility bar that decides when to invoke it, and mirrors the scanning test in [structure-for-scanning](structure-for-scanning.md) — a structure works when its shape is readable before its detail is.)`

**The backstop.** Above **9 nodes**, or **5 participants** in a sequence diagram, a split is mandatory whatever the legibility test says. The test is the primary bar and catches most cases; the number catches the one the test cannot — the run that judges its own hairball legible. It does not run the other way: a six-node diagram that fails the restate-after-one-pass test still splits.

`(basis: ratified by the maintainer, 2026-07-29. No accountable source fixes a diagram node count — C4, the authority here, deliberately prescribes level-decomposition instead — so this is a house calibration, pinned as one rather than derived. It is a ceiling on a self-assessed test, which is why it is a number and not another judgment.)`

## Every edge carries a verb

An unlabeled edge asserts that two things are related without saying how, which is the one thing the reader needed. Label edges with what actually passes or holds — `verify(token)`, `owns`, `on timeout` — not with arrows alone. A diagram whose edges are bare is a list of nodes with decoration between them.

`(basis: labelling the relationship, not just drawing it, is explicit in C4's guidance on relationships and is intrinsic to sequence notation, where the message *is* the label; an unlabelled edge also fails this rule's own restate-after-one-pass test, since a reader cannot restate a relation whose nature was never stated.)`

## Elision is declared, never silent

A diagram shows less than the system; that is what makes it useful. What makes it false is leaving the reduction unstated, because a picture with no stated boundary reads as complete.

State, adjacent to the diagram, **what was left out and why it does not bear on this requirement** — one line. *"Elided: connection pooling and retry, which do not affect the ordering shown."* A reader who knows the omission can trust the rest; a reader who discovers it stops trusting the picture.

`(basis: the same bar [source-or-declare](source-or-declare.md) sets for an absent fact, applied to a picture — an omission that is not stated reads as coverage, which is a false claim rather than a small one. It is the house discipline understand and deep-research already run on their own gaps.)`
