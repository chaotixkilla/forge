# Diagram legibility

A diagram that is correct and unreadable has failed, and it fails invisibly — nothing in a review catches it, because every node in it is true.

## Notation

Emit diagrams in **mermaid**: in a published document as a diagram block whose source is mermaid; anywhere else as a fenced mermaid block. A diagram stays text, so it brings no config prerequisite with it. It is a house default rather than a law — a team with a drawing backend may swap it, and a swapped notation travels as code, never as the diagram block — but it is pinned so that two runs do not produce two notations for the same artifact.

A diagram carries a one-line caption above it, stating the relation it shows, and its elision line below it ([elision](#elision-is-declared-never-silent)). `(basis: derived — a reader meets the relation before the picture, as a chart's caption carries its claim)` Outside a published document, where the destination cannot draw it, do not silently flatten: keep the source visible as code under that caption, saying it is a diagram's source.

`(basis: house practice; mermaid for the widest render support among text notations; maintainer, 2026-10-01: mermaid accepted on record as the pinned house notation; maintainer, 2026-10-07: every shipped documentation backend draws mermaid natively, checked on one and per their documentation for the rest, as each adapter's content support surface records)`

## Size: one level of abstraction per picture

The bar is a test, not a count: **can a reader who does not know the system restate the relation after one pass over the diagram?** If they must study it, it is carrying more than one picture's worth.

When it is, **split by abstraction level rather than shrinking the font** — one diagram showing how the parts relate, another expanding the part that matters, each self-contained and named. A single picture spanning levels is the common failure: it mixes a service boundary with a function call and gives the reader no consistent unit.

`(basis: the C4 model; the restate test is a house bar mirroring structure-for-scanning's scanning test)`

**The backstop.** Above **9 nodes**, or **5 participants** in a sequence diagram, a split is mandatory whatever the legibility test says. The test is the primary bar and catches most cases; the number catches the one the test cannot — the run that judges its own hairball legible. It does not run the other way: a six-node diagram that fails the restate-after-one-pass test still splits.

`(basis: maintainer, 2026-07-29)`

## Every edge carries a verb

An unlabeled edge asserts that two things are related without saying how, which is the one thing the reader needed. Label edges with what actually passes or holds — `verify(token)`, `owns`, `on timeout` — not with arrows alone.

`(basis: C4's guidance on relationships)`

## Elision is declared, never silent

A diagram shows less than the system; that is what makes it useful. What makes it false is leaving the reduction unstated, because a picture with no stated boundary reads as complete.

State, adjacent to the diagram, **what was left out and why it does not bear on this requirement** — one line. *"Elided: connection pooling and retry, which do not affect the ordering shown."*

`(basis: derived from source-or-declare's declaration bar)`
