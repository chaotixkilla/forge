# Prefer examples over prose

"The discount applies to eligible orders" reads as agreement and conceals a dozen unanswered questions — eligible how, which orders, what discount, applied when. A single worked example — *order of $120 with a loyalty tier of Gold → $12 off; order of $120 with no loyalty tier → $0 off* — forces every one of those questions to an answer, and forces the disagreement (someone expected non-members to get 5%) into the open where it is cheap to resolve.

## The discriminator: does the prose admit more than one reading?

The test for whether a statement needs an example: **can you write two different input→output tables both consistent with this sentence?** If yes, the prose is ambiguous by construction — add the example that picks the intended reading, and the counter-example that fences the boundary the positive example leaves open. If no — the sentence already admits exactly one reading (a flat, measurable constraint like "responses are gzip-compressed") — an example adds nothing and prose is fine. Reach for an example precisely where the prose forks, not everywhere.

## Include the counter-example

A positive example shows what must work; it leaves the boundary undefined, because "$120 Gold → $12 off" doesn't say what a $0 order or a fraud-flagged account does. The **counter-example** — the input that must be *rejected*, or the case that must produce *nothing* — fences the boundary the positive case opens: *fraud-flagged account → discount refused; $0 order → no discount, no error.* A requirement pinned with a positive example and its counter-example is far harder to build wrong than one pinned with either alone.

## Match the example's shape to the requirement

An example takes one of three shapes, and the fit is the choice made in [making-it-concrete](../phases/04-making-it-concrete.md)'s acceptance-criteria fork:

- **A scenario (Given/When/Then)** — for a *single behavior with context*: given a state, when an action, then an observable result. One behavior per scenario, stated declaratively rather than drifting into imperative UI steps. `(basis: BDD and Gherkin practice)`
- **An example / decision table** — for *one rule with many discrete input→output cases* (pricing tiers, eligibility matrices, tax bands). Use **key examples per equivalence class**, not every combination — full enumeration explodes and obscures intent. `(basis: Adzic's key examples; decision-table practice)`
- **A bounded assertion** — for *continuous ranges or quality attributes* that aren't scenario-shaped: a measurable condition stated as a pass/fail assertion.

The tell for switching from scenarios to a table: you find yourself writing near-identical Given/When/Then blocks that differ only in their data values.

Examples do not replace the requirement — they pin it. This is the concrete-and-testable discipline of [testable-or-its-not-a-requirement](testable-or-its-not-a-requirement.md), applied through instances instead of adjectives.
