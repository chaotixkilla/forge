# The unit-size scale

Every unit decompose keeps carries a size verdict, and that verdict is what decides the grain of the whole breakdown: whether a unit is split, kept, or folded into another. If the scale is undefined, each person decomposing invents their own sense of "too big" — one carves a design into six units, another into twenty, and the same design yields two incompatible plans of work. A sized output with no defined scale is not a lighter-weight decomposition; it is one whose most load-bearing judgment is left to chance. This rule pins the scale. It is applied in [size-and-sequence](../phases/03-size-and-sequence.md), which assigns each unit its verdict; [emit-tickets](../modules/emit-tickets.md) consults it too — to establish that a right-sized unit set needs *no* size label on the emitted item (the scale governs the carve, not the output). The scale earns its own file on its **depth** — a defined vocabulary, per-verdict assignment tests, adjacent-verdict discriminators, and top/bottom anchors — not on how many callers cite it.

## What "size" is measured against — the review/integration cadence

Size answers one question: **does this unit fit what the team reviews and integrates as one coherent change?** The measuring stick is deliberately *relative to the team's review/integration cadence* — how large a change the team can review, verify, and merge as a single step — not an absolute count of hours, points, or t-shirt letters. This is a different, *finer* cadence than the delivery/iteration cadence `spec` sizes its value slices to: a single shippable spec slice, or a single buildable plan unit, can legitimately resolve into several review-sized units here. Sizing to the team's own rhythm is what keeps units "small enough to review and verify quickly, large enough to avoid bookkeeping churn."

`(basis: ratified by the maintainer, 2026-07-10 — the cadence-relative form is the house rule, with no absolute number by design. No authority pins "size to the team's review/integration cadence": INVEST (Wake, 2003) gives an *absolute* band ("a few person-days to a few person-weeks"), a different measuring stick, and #NoEstimates is community discourse, not authority. The cadence-relative choice is anchored to Reinertsen (Principles of Product Development Flow, 2009 — smaller batches cut cycle time and risk) and Accelerate (Forsgren/Humble/Kim, 2018 — batches completable in ≤ ~1 week correlate with higher delivery performance), and deliberately carries no fixed number because the skill's design intends size as a method, not an invented scale. The ratified cut: a unit is too-big when it cannot be reviewed/integrated as one coherent change in the team's cadence, or bundles more than one one-sentence done-condition; absent a stated cadence, when it bundles more than one independently-verifiable done-condition.)`

Absent a known team cadence at run time, do not stall or invent a number: size by the qualitative bar alone — one coherent outcome, one checkable done-condition, buildable-and-verifiable as a unit — and flag the missing cadence as an assumption to confirm. The cadence bound only sharpens the split call at the margin; the single-outcome and independent-verifiability tests carry the verdict without it.

## The three verdicts

`(basis: the three-verdict structure — right-sized / too-big→split / too-small→merge — mirrors the maintainer-ratified sizing scale in spec's sequencing-and-sizing (2026-07-04), itself grounded in INVEST (Bill Wake, 2003): the vertical-slice, single-outcome, and independent-verifiability discriminators are INVEST's Valuable/Independent/Testable. Ratified for decompose by the maintainer, 2026-07-10. The absolute cut behind "too-big" carries the routed-to-maintainer marker above.)`

Assign by walking each unit against the properties until a verdict fits:

- **right-sized** — one coherent outcome; buildable and verifiable as a single change; fits one review/integration cycle.
  - *Anchor:* "add a `/logout` endpoint that clears the session cookie and returns 204" — one outcome, reviewable and mergeable on its own, verifiable alone.
- **too-big → split** — fails any one of: cannot be reviewed/integrated as one coherent change in one cycle, **or** bundles more than one independently-shippable outcome, **or** its done-conditions cannot all be verified together. Split along the *value* seam into thin vertical sub-units ([prefer-vertical-slices](prefer-vertical-slices.md)), never into horizontal layers.
  - *Anchor (top of scale):* "implement authentication" — login, logout, session management, password reset, and token refresh bundled; many review-sized changes across many merges. Split.
- **too-small → merge** — delivers no independently-observable outcome (a pure sub-task of another unit) **or** cannot be verified until another unit is built first. Merge into the unit whose outcome it completes.
  - *Anchor (bottom of scale):* "add the `last_login` timestamp column" — no reviewable outcome alone; meaningful only once the login flow writes it. Merge into the login unit.

## The adjacent-verdict discriminators

The boundary tests are what stop a unit sliding between two verdicts:

- **right-sized vs too-big** — can it be reviewed *and* verified as one coherent change within one cycle, delivering one outcome? All three hold → right-sized; fails any → too-big. (the cadence + single-outcome line)
- **right-sized vs too-small** — does it deliver an outcome observable *on its own*, verifiable without another unit built first? Yes → right-sized; no (a pure sub-task) → too-small. (the independent-verifiability line)

When a unit seems both too-big and coherent, the split test wins: if you cannot state its done-condition in one sentence without an "and" joining two shippable results, it is too-big however coherent it feels ([one-unit-one-outcome](one-unit-one-outcome.md)). A unit you cannot size at all because it is genuinely uncertain is not force-verdicted — it becomes a timeboxed spike ([size-the-unknowns-as-spikes](size-the-unknowns-as-spikes.md)).
