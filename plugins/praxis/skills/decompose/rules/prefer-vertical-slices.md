# Prefer vertical slices

When you introduce a boundary — carving a unit in phase 2, or splitting a too-big one in phase 3 — the cut can run two ways. A **vertical** slice goes end-to-end through every layer needed to produce one observable outcome; a **horizontal** slice takes one layer (the data model, the API, the UI) across the whole feature. The pull toward horizontal is strong because the layers are the most visible seams — but a horizontal unit is inert until the units above and below it land, so its "independence" is a fiction and its "done" is unverifiable alone. This rule pins vertical as the default and names the bounded exceptions where a horizontal cut genuinely earns its place, so two people splitting the same unit converge. It is cited by [carve-into-units](../phases/02-carve-into-units.md) and [size-and-sequence](../phases/03-size-and-sequence.md).

## The default: cut vertically

Favor the thin vertical slice — a path from entry through to storage and back that delivers one user-observable or system-observable outcome — over a horizontal layer that only integrates at the end. The test is the same single-outcome test carving uses: a vertical slice has a done-condition you can state and verify on its own; a horizontal layer's done-condition is "the layer exists," which nothing can exercise until its neighbors do.

`(basis: the vertical-slice default rests on Bill Wake's INVEST (2003) — "the best way is to slice vertically through the layers" — because a horizontal split fails INVEST's *Independent* and *Valuable*; corroborated by the Humanizing Work Guide to Splitting User Stories (Lawrence & Green): "splitting by architectural layer … may satisfy small, but it fails at independent and valuable." This is craft consensus traceable to INVEST, not a standards-body mandate.)`

## The bounded exceptions — when a horizontal / architectural-enabler unit is legitimate

Vertical is the rule, not an absolute: there are *named, sanctioned* cases where a non-vertical unit is the right cut. This is not a symmetric fork (the authorities do not genuinely conflict on vertical-as-default); it is a rule with recognized exceptions. A horizontal or architectural-enabler unit earns its own place only when it matches one:

- **An architectural enabler** — infrastructure or an architectural runway item that later vertical units build on, where wiring it once as its own unit is cheaper and clearer than smearing it across every vertical slice. `(basis: SAFe Enablers — Scaled Agile Framework — sanctions Exploration / Architecture / Infrastructure / Compliance enabler items as legitimate non-user-facing backlog units.)` Prefer, where possible, the **walking-skeleton** form of this — a *thin vertical* slice deliberately chosen to wire the architecture end-to-end (Cockburn) — over a purely horizontal layer, because it validates the architecture *and* delivers a traceable outcome.
- **A spike** — a research/investigation unit is non-vertical by nature and is the correct cut for genuine uncertainty ([size-the-unknowns-as-spikes](size-the-unknowns-as-spikes.md); SPIDR's "Spike", Cohn).
- **A component-team boundary** — where the team is organized around a component and structurally lacks the cross-functionality to complete a vertical slice, coordinating around a larger marketable feature is an explicit, deliberate decision not to slice vertically (Humanizing Work's own caveat).

**Routing rule (non-gating): surrounding convention → house rule → maintainer.** Whether a given case warrants an architectural-enabler exception is read from what the codebase and team already do — if the surrounding plans carry enabler/infra units, match that; if everything is a vertical slice, hold the line. Absent a convention, default to vertical and surface the proposed enabler as an exception for the maintainer to confirm rather than silently cutting horizontally.

## The anchors

- *Good (vertical):* "a user can grant another account read access to a document and the grantee can open it" — through UI, API, and storage; ships and verifies as one outcome.
- *Bad (horizontal to reject):* "build the sharing data model" — a table with no reader and no writer; nothing exercises it until three later units land, and "done" means only that the migration ran.
- *Legitimate exception (enabler):* "stand up the background-job runner the notify, audit, and digest units all dispatch to" — an architectural-runway unit three later vertical slices depend on; cheaper to wire once, and matched to a codebase that already carries infra units.
