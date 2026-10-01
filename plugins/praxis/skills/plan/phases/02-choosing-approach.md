Close the solution space so that two competent designers, given the same map, commit to the same approach and can say why the others lost — never by defaulting to the first path that came to mind or by an unrepeatable gut call.

## Enumerate the real candidates

List the genuinely viable ways to build it — the real alternatives the map admits, not one foregone path with two strawmen beside it. If a decision has only one real option, say so and move on; manufacturing a fork wastes the scoring. Investigate how the problem has been solved before by **delegating to `gather`** (the `community` lane for how others solved it, `official-documentation` for what the stack officially supports, `authoritative-literature` for genuinely hard algorithmic cases). With `--prior-art`, seed the search from the referenced design and carry its reusable shape in as a first-class candidate ([seed-prior-art](../modules/seed-prior-art.md)).

## Gate, then score — the approach scale

`(basis: maintainer, 2026-07-05; after Kepner-Tregoe, ISO/IEC 25010 and Alexander's forces, Bezos's door types, SEI ATAM and ISO/IEC/IEEE 42010; axes ④ and ⑤ are house rungs)`

**Step 1 — gate on the MUSTs.** Split the map's constraints into **MUSTs** (hard requirements — a non-negotiable performance floor, a security boundary, a platform limit) and **WANTs** (preferences). A statement that merely *describes the current system* ("backed by Postgres", "a single deployable") is a MUST only where changing it is out of scope or a genuine platform limit; if the change could legitimately introduce a new store or service, treat it as a strong WANT so that option is *scored*, not silently gated out. Any candidate that fails even one MUST is **rejected**, and its recorded reason is the named MUST it violated. The gate is what makes the eligible set converge before any judgment enters.

**Step 2 — score each survivor on five axes.** Each axis has three named rungs; assign by the test, and the anchors fix the ends:

| Axis | Top rung | Middle rung | Bottom rung |
|---|---|---|---|
| **① Fit-to-constraints** — how well it satisfies the drivers | *Strong* — satisfies all drivers with margin | *Partial* — satisfies them only via workarounds or accepted exceptions | *Poor* — leaves a driver unmet |
| **② Complexity / cost to build** | *Low* — reuses existing patterns and components; adds nothing new | *Moderate* — adds a new component (a table, module, or interceptor) within existing patterns and infra | *High* — a new subsystem / datastore / infra, or cross-team coordination |
| **③ Reversibility** ([design-for-reversibility](../../../craft/engineering/design-for-reversibility.md)) | *Two-way door* — undo in one deploy, no external coordination | *Partial* — undo needs a migration or coordinated rollback | *One-way door* — practically permanent (persisted format, public/contractual commitment) |
| **④ Blast radius** — how far a *fault* reaches, measured by **user reach** alone (not code footprint — structural size is ②; not cascade/operational severity — that is phase 4's risk scale) | *Contained* — a fault degrades a component but the user-facing flow it sits in still completes; no flow goes down | *Bounded* — a fault takes a whole user-facing flow down, for a bounded subset of users | *Wide* — a fault takes flows down for most or all users |
| **⑤ Operability** | *Turnkey* — existing platform, runbooks, observability | *Standard* — minor new ops | *Demanding* — new operational tooling or added on-call load |

Assignment test per axis: match the candidate to the rung whose description fits; when two seem to fit, take the *worse* rung unless you can name why the better one holds.

**Step 3 — compare, structured-qualitative.** Among the MUST-passers, choose by reading the five axes as a **lexicographic chain in priority order**: strongest **fit-to-constraints (①)** first; break a tie by lower **complexity/cost (②)**, then better **reversibility (③)**, then lower **blast radius (④)**, then better **operability (⑤)**. All five axes are decision-bearing, in that priority order. It's a lexicographic read of the rungs, not a weighted numeric total: weights would dress judgment as arithmetic. If two candidates are genuinely tied on **all five** axes, they are equivalent for this design: commit to either and record the other as an **equal-standing alternative** the build can fall back to ([record-rejected-alternatives](../rules/record-rejected-alternatives.md)) — do not treat the residual tie as unresolved. Under `--deep`, **lay the full comparison out** as a legible scored table of every survivor — beyond the committed approach's own rung assignments and the reject reasons the base run records — so a reviewer can audit it ([deep-mode](../modules/deep-mode.md)).

## Commit and record why the others lost

Commit to one approach. Then record the rejected alternatives — each with the axis or MUST it lost on, in one line — per the content contract in [record-rejected-alternatives](../rules/record-rejected-alternatives.md). Every new component the chosen approach introduces must itself earn its place against a constraint ([justify-every-moving-part](../../../craft/engineering/justify-every-moving-part.md)), and where the approach could conform to a strong local convention or import a foreign pattern, resolve that per [match-the-surrounding-code](../../../craft/engineering/match-the-surrounding-code.md).

## Stress-test the choice

Recruit the **trade-off-analyst** to find the fork this choice silently resolved and price the road not taken, and the **simplicity-hawk** to attack any part not pulling its weight; fold surviving objections back into the choice or the record. Without fan-out, apply each lens yourself, as its own pass: first the fork the choice silently resolved and the price of the road not taken, then what isn't pulling its weight. `--critics=<n>` scales how many perspective-diverse passes run this stress-test ([adversarial-critics](../modules/adversarial-critics.md)).

The output is one committed approach with its five-axis rung assignments, and the recorded rejected alternatives each with its losing axis — the closed solution space [specify-interfaces](03-specify-interfaces.md) turns into contracts. (Under `--deep` this is written out as a full cross-candidate scored table.)
