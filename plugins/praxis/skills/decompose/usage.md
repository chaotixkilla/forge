# decompose — usage

Turn an approved design or plan into an ordered set of independently shippable work units — sized to how your team reviews and integrates, sequenced by dependency and risk, each actionable on its own — then return them for review or render them as one ordered checklist. Filing them as tracked work-items is the caller's delivery.

## When to use
- A design or plan is approved and you need the work-ready tasks: the ordered, independently-buildable units, each with a clear done-condition, explicit dependencies, and just-enough context for whoever picks it up.
- You want the units sized to *your* team's rhythm — small enough to review and integrate cleanly, large enough to avoid bookkeeping churn — rather than to an arbitrary hours/points scale.
- You want the breakdown in a form the work can be tracked from: returned for review, ready to file as one work-item per unit, or rendered as a single ordered checklist.
- You want a coverage guarantee — that every part of the source is owned by exactly one unit, with nothing dropped and nothing double-owned, and genuinely uncertain work carved out as a timeboxed spike.

## Not for / use instead
- Carving the *design* into buildable units and proving it is buildable (walking-skeleton, closed seams, resolved opens) → **plan** (its slice-and-validate closes the design and hands off here). decompose renders those units into work-ready tasks and re-sizes them to your review cadence; it does not re-derive the design or re-open its seams.
- Carving *requirements* into prioritized, independently-shippable value slices before a design exists → **spec** (its sequencing-and-sizing does value-slicing and MoSCoW priority). decompose works downstream of an approved design.
- Actually building the units → **develop** (decompose defines the units and their order; develop implements them, and reads a decomposition via `--from-plan`).
- Recording items in the tracker or reading one back → the **project-mgmt** capability, invoked by the caller — the developing act in **work** files the units. decompose decides *what* the units are and never talks to a tracker.
- Publishing the design or a report as a team-facing document → **artifacts** (a tracked work-item is a unit of work, not a published document).

## Examples
`--from-plan=docs/plans/auth.md` — render an approved plan's buildable units into work-ready tasks, re-sized to your team's review/integration cadence and sequenced for execution.
`--checklist` — render the units as a single ordered checklist for lightweight tracking, with no tracker configured.
`--from-plan=docs/plans/auth.md` — the common path: take the approved plan and render its work-ready units. The developing act in **work** files them as tracked items.

## Gotchas
- **decompose needs no configuration of its own.** It touches no backend: it returns the units, and the developing act files them as work-items.
- **It works downstream of an approved design.** Handed a fuzzy request with no plan, it routes back — to **spec** when *what* is unclear, to **plan** when *how* is undesigned — rather than inventing the design under the guise of decomposing it. Only a request whose units are self-evident (no unmade design decision) is decomposed directly.
- **`--checklist` is a format, not a sink.** It changes how the units are rendered, never where they go.
- **Sizing is a method, not a fixed scale.** Units are sized against your team's review/integration cadence — not hours, points, or t-shirt sizes. Absent a known cadence, decompose sizes by the qualitative bar (one coherent outcome, one done-condition) and flags the missing cadence as an assumption.
- **It renders plan's units into tasks; it does not re-open the design.** decompose may split a plan unit that is too big for one review, or merge trivial ones, *along the seams the plan already drew* — but if a unit proves un-buildable as scoped, it surfaces that as a finding and routes back to plan rather than silently redesigning.
