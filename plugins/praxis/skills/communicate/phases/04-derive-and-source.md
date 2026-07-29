The takeaway, the reader, the tier, and the form are fixed. The reflex now is to start drafting — and drafting from whatever the session happens to hold is where the artifact quietly fails. [right-size-the-detail](../rules/right-size-the-detail.md) and [respect-the-readers-time](../rules/respect-the-readers-time.md) are both *filters*: they sort and tighten candidate material that already exists. A required element nobody gathered never becomes a candidate, so no filter ever notices it missing — and the slot gets filled with a confident, unsourced sentence. That is the failure this phase prevents, and it is worse than an omission: an invented sentence tells the reader they are covered when they are not.

So this phase runs *before* the draft and produces its input: the set of things the reader must have, each one obtained from a real source or explicitly declared unobtained.

It runs after the form is chosen because two of its judgments depend on the form: how much of its own working it records, and whether a requirement is worth a diagram — which cannot be asked before you know the artifact can carry one.

## Derive what the reader needs

Work forward from the reader and the **action in the world** fixed in [frame-the-message](01-frame-the-message.md) — their task, not the ask this artifact makes of them: what must be true in that reader's head before they can take that action? Each answer is one requirement. An artifact whose ask is explicitly nothing still has an action, so this walk always has an input. Derive the set — and judge it complete — by the walk-the-action method and the stopping test in [derive-the-requirement-set](../rules/derive-the-requirement-set.md); a set assembled by recalling what you happen to know, rather than by walking the action, is the failure that rule exists to prevent.

This is derivation, not a template lookup. There is no per-genre section list here on purpose: the artifact type fixed in framing sets *expectations of shape*, but what this particular reader needs to act follows from the action, and two readers of the same artifact type routinely need different things.

**Checkpoint — do not draft until the set exists.** A draft begun before the requirement set is derived reorganizes what is already in context and calls the result complete; the omission is then invisible to every later phase, because the draft reads finished. Hold here until the set exists.

## Scale the recording to the form — never the deciding

Every requirement is derived, triaged, and sourced whatever the artifact is; that is this phase's job and it does not flex. What flexes is how much of the working gets **written down**, and it keys to one primitive already resolved in [choose-form-and-channel](03-choose-form-and-channel.md): **does anything here outlive the exchange?**

- **Durable** — the artifact is a document, or a walkthrough that owes a written summary afterward → **write the set out**, each entry carrying its disposition and its source or declaration. The record is part of what makes the artifact re-checkable later.
- **Ephemeral** — the artifact is a conversational message, or a walkthrough that leaves no written record → **hold the set**; do not tabulate it. Write down only the entries that come out **blocked** or **nowhere**, since those are the only ones that change what the artifact says.

Keying on durability rather than on the form's name is deliberate: the three forms do not partition this cleanly on their own, because a walkthrough falls on either side depending on whether a summary is owed. Durability decides it in every case.

Two things this guard explicitly does not touch. The **derivation** never shortens — a small action simply yields few requirements, which is the scaling working correctly rather than a corner cut. And the **declaration bar** never scales: a blocked or nowhere requirement is stated in the artifact whatever its form ([source-or-declare](../rules/source-or-declare.md)).

`(basis: the form was resolved on durability and purpose signals, and durability is precisely what predicts whether anyone re-reads the working — a conversational message is, by that phase's own anchor, true now and worthless next week, so a written provenance record for it outlives the thing it documents. The split is also empirical: a house dogfood run produced nine separate written process artifacts for a nine-word message, and the ceremony, not the derivation, was what the run reported as disproportionate.)`

## Triage each requirement, then source it

Place every requirement on exactly one of the three dispositions defined in [source-or-declare](../rules/source-or-declare.md) — that rule holds the definitions, the discriminators that separate adjacent dispositions, and the tie-break when more than one appears to fit. The dispositions turn on *where the answer lives*, and the rule's central discipline is that "I could not name where to look" is not the same finding as "no one has established this."

Then act on the disposition:

- **In session** — use it.
- **In a reachable source** — perform a *targeted* read for that requirement at that location. Recruit the **repository** and **code** explorers for what the tree holds and the **knowledge-base** explorer for settled context and prior decisions; or, without fan-out, perform those reads inline yourself before proceeding. A targeted read is aimed at one named requirement; a general sweep of the area is what this phase replaces, and it returns atmosphere rather than the missing fact.
- **Nowhere** — declare it, per the declaration bar in [source-or-declare](../rules/source-or-declare.md). Declaring is not a failure of the run; it is the run's most valuable output when it is true.

Sourcing runs until every requirement is either obtained or settled on a disposition. When to stop pursuing a read and mark it blocked instead is the stop bar in that same rule — it is a boundary, not a budget.

## Decide which requirements are visual, and source those too

A requirement whose content is a relation, an ordering, or a structure is discharged badly by prose: the reader has to rebuild the graph in their own head, and most will not. Test each requirement for visual shape, and route it to a table, a chart, a diagram of a named kind, or prose, using [when-a-visual-is-owed](../rules/when-a-visual-is-owed.md) — the shape test, the table/chart/diagram fork, the kind selection, and the fallback a chart takes when no charting capability is present all live there, and a run that picks a form without them picks by habit.

Where the rule selects a diagram, the kind determines **which read** its content must come from; that rule's per-kind sourcing table names it. A diagram is not exempt from the dispositions in [source-or-declare](../rules/source-or-declare.md): an unreadable relation is a blocked requirement, declared rather than sketched from memory. Render to the bars in [diagram-legibility](../rules/diagram-legibility.md).

## When the run cannot complete the sweep

- **No requirements derive.** If walking the action yields nothing the reader lacks, the artifact has no job. Do not draft one — return to [frame-the-message](01-frame-the-message.md); this is the same unresolved reader-and-action that phase's closing checkpoint routes to the user.
- **A knowledge or repository read is unavailable.** The requirement stays in its disposition but is *unobtained*: carry it forward as blocked and declare it in the form [source-or-declare](../rules/source-or-declare.md) pins for that case. Degrading is communicate's standing posture; silently dropping the requirement is not.
- **Every requirement is in session already.** A legitimate outcome for a small artifact about work just completed — record that the sweep ran and found nothing to source, so a reader of the run can tell a complete sweep from a skipped one.

Done-state: a complete requirement set — every entry derived, triaged onto a disposition, and either sourced or marked for declaration, with its visual form assigned where the shape test fired — recorded to the depth the form calls for. This set, not the session's contents, is what the draft is built from.
