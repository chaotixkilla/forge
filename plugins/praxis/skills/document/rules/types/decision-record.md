# Decision record

One decision set out whole, holding plan's content contract ([record-rejected-alternatives](../../../plan/rules/record-rejected-alternatives.md)) and led by the decision and its state. (basis: maintainer, 2026-10-02) A part of the contract the result doesn't hold, the alternatives an author weighed, say, is stated as not recorded, never reconstructed ([preserve-the-why](../../../../craft/writing/preserve-the-why.md)). (basis: Nygard 2011, through plan's contract)

## Reader and question

A maintainer later, about to build on the decision or undo it: "Why is it this way, what did we give up for it, and when should it be reopened?"

## Page

`on the spec page at task scale, own page at an epic`

## Membership

A decision earns its own record when it's a one-way door by the test in [design-for-reversibility](../../../../craft/engineering/design-for-reversibility.md), or when its `architectural` is `yes` ([decision-register](decision-register.md)). (basis: benchmark, 2026-11-13, a maintainer found the why of two-way choices that shape the system only in register rows) For a review, that means those among the decisions the review names; the rest stay in the review record. A decision the requirement itself dictates, the ticket specified the format, is the requirement's, not a design decision: it earns no record, and the spec carries it. (routed to maintainer: one-way doors and the choices that shape the system, so the record set stays the few a maintainer builds on; agreement, maintainer, 2026-11-13) In a review the decision is the author's, not the reviewer's: the record names who made it and links the change, and the decision stays `proposed` until an agreement covers it, since approving or landing a change settles no item ([items-and-agreements](../items-and-agreements.md)). (basis: maintainer, 2026-10-07; agreement, maintainer, 2026-11-11)

Its subject is one decision, so a record is one `DEC`: a decision that supersedes it gets a record of its own, and both stay. A record is named by its decision's id and a two-to-five-word slug of the decision, `DEC-4-require-tenant-claim`, and keeps that name when filed again. (basis: maintainer, 2026-11-11, records numbered by their item's id) At task scale each record is a subsection of the spec's decisions section, titled by its record name, with its own sections as headings below that. It is filed again when its decision's state changes.

## Items

Shows one `DEC` (home: [decision-register](decision-register.md)), whether or not the task owes the register.

## Sections

1. **What did we decide?** Always. The decision card. A superseded decision opens with the decision that superseded it; a superseding one names what it replaced. (basis: PEP 1, reciprocal Replaces and Superseded-By)
2. **Why did this need deciding?** Always. The decision's body, then the requirements and needs it `serves`.
3. **What did we weigh?** Always. Its options, each with its pros and cons, the chosen one marked.
4. **What does it buy, and what does it cost?** Always. Its gains, then its costs.
5. **How do we check the work follows it?** Always. Its confirmation, linking the test when it is one. (basis: MADR 4.0)
6. **When should it be reopened?** Always. Its revisit-when.

## Checks

*Computed:* none beyond those its decision's home declares.

*Judgment:* (basis: Zimmermann's decision anti-patterns, Nygard 2011, MADR 4.0)
- A context that argues for the choice instead of stating the problem.
- Fewer than two real options, or a straw-man option set up to lose.
- Only gains listed, or costs nobody would mind.
- A decision that doesn't solve the problem its context states.
- A decision that is neither one-way nor `architectural` `yes` given a record of its own.
- A weighted score presented as more precise than the judgment behind it.
- A confirmation that nothing could fail.

## Views

- **Decision card:** `cards` of `DEC` with `id is <its DEC>` and `state in` every state (`open`, `lean`, `proposed`, `deferred`, `agreed`, `superseded`, `withdrawn`, `recorded`), so a superseded or withdrawn decision still shows: chosen, state, tier, reversibility, reach, architectural, confidence, what it `answers`, `supersedes` and `superseded-by`, and the covering agreement's decider, consulted, informed, date and link.

## Minimum form

Each section keeps its heading with one line saying what isn't recorded, such as "Options weighed: not recorded."
