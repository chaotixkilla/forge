# Carry just enough context

A work-ready unit sits between two failure modes. Too little context and the executor who picks it up cannot act without reading the whole design back — the unit is a title, not a task. Too much and the unit copies the entire plan into itself, which goes stale the moment the plan changes and buries the one constraint that matters under the ninety-nine that do not. This rule pins the middle: restate the *why* and the constraints this unit must respect, and link back to the source for everything else. It is cited by [make-units-actionable](../phases/04-make-units-actionable.md).

## The discriminator: what must this unit respect, and why?

The context a unit carries answers exactly two questions, and links out for the rest:

- **Include, inline:** the *decision this unit serves* (why it exists), and the *constraints it must not break* — the invariant, the interface it must match, the edge the design already ruled on. These are the things an executor would otherwise get wrong precisely because they are not visible from the code the unit touches.
- **Link, don't copy:** the full design, the rationale for decisions this unit does *not* touch, the other units' internals. A pointer to the source ([the plan/spec the run ingested](../phases/01-ingest-the-source.md)) keeps one authoritative copy; duplicating it creates a second copy that drifts.
- **The test for "just enough":** could the executor start and know when they are done from the unit alone, and does every line of context earn its place by being something they must *respect* (not merely something that is *true*)? Context that is true but not load-bearing for this unit is noise — send it to the link.

`(basis: house craft rule; the link-don't-duplicate half is the single-authoritative-source principle applied to unit context (a duplicated design is a second source that goes stale — the same reasoning as DRY's "one authoritative representation," Hunt & Thomas). No external authority pins the "just enough" line; the respect-vs-true test above is the discriminator.)`

## Anchors

- *Good:* "unit: enforce the 5MB upload cap. Why: the design caps uploads to protect the sync queue (see plan §4). Must match: return 413 with the existing `ErrorBody` shape. Full rationale and the queue design: <link>." — carries the constraint and the why, links the rest.
- *Bad (too little):* "unit: add the upload cap" — no number, no error shape, no why; the executor guesses the limit and invents an error format.
- *Bad (too much):* the unit re-pastes the entire sync-queue design section — the 413 requirement is lost in three paragraphs about queue internals the unit never touches, and the paste is stale the next time the queue design changes.
