This is the closure gate: prove the design buildable, sliceable into units each verifiable on its own, with nothing load-bearing left open. What it catches is the "figure it out later" that detonates mid-build: an open decision from mapping never closed, a seam too loose for two developers to converge, an untested assumption the whole thing rests on.

## Slice into independently buildable units

Break the design into units that can each be built and verified on their own, in an order where each rests only on what came before. The test that the slicing is real: at least one **end-to-end function** can be traced through the units with no gap — a thin path from entry to storage and back that exercises every main component the design introduces. That walking-skeleton trace is what proves the pieces actually connect, not just that they were each named.

## The buildable / closed bar

`(basis: maintainer, 2026-07-05; after Cockburn 2004, Hunt and Thomas's tracer bullets, and Fairbanks 2010)`

A design is **closed / buildable** when all of these hold — check them explicitly, and a failure is an open, not a nit:

- **Every main component is named**, and one real end-to-end function traces through them with no gap (the walking-skeleton test above).
- **Each seam/contract is specified precisely enough that two independent developers would build the same interface** — the convergence bar from [specify-interfaces](03-specify-interfaces.md).
- **Every open decision surfaced in [mapping-to-system](01-mapping-to-system.md) is now closed** — nothing deferred to "later". (With `--from-spec`, additionally: every spec requirement is addressed by some part of the design — [from-spec](../modules/from-spec.md).)
- **Every moving part earns its place** against a constraint ([justify-every-moving-part](../../../craft/engineering/justify-every-moving-part.md)) — the closure pass is also the last chance to cut what doesn't.
- **The single riskiest assumption — chosen by the ranking in [surface-assumptions](../rules/surface-assumptions.md) — has a named validation step** — the design does not bet the build on an unchecked premise.

Do **not** substitute Scrum's Definition of Done (that is "increment shipped", downstream of this handoff) or a full IEEE-1016 design document (documentation completeness, not buildability) for this bar unless the domain contractually requires the formal artifact.

## Before it goes out, read it as its reader

Put the finished report through [deliver-at-the-readers-register](../../../craft/writing/deliver-at-the-readers-register.md) before delivering it, applying its honesty floor item by item from the rule, not from memory.

**And a visual where prose would carry it worse:** where the report describes a *structure* — a shape, a flow, a set of relationships — show it rather than describe it, per `output.diagrams` ([report-style-settings](../../../craft/writing/report-style-settings.md)) and [when-a-visual-is-owed](../../../craft/writing/when-a-visual-is-owed.md), which decides whether one is owed.

## Flag residual risk, stress-test, and hand off

Flag the known unknowns that remain and what needs a spike or throwaway prototype *before* committing to build — the design can be closed on paper and still name a risk that a small experiment should retire first. Run the final perspective-diverse critic panel on the closed design and fold surviving objections back in — without fan-out, apply the panel's lenses yourself, one pass each; `--critics=<n>` sets how many lenses attack it ([adversarial-critics](../modules/adversarial-critics.md)).

The output is a validated, sliced, closed design — buildable in independent units, every open resolved, residual risks flagged — ready to hand to `decompose` or `develop`, or to publish.

## Its content as items

Once the panel's objections are folded in, the plan's result carries its content as the pieces of the documents it feeds, each new under a handle or keeping the id it carried, as [items-and-agreements](../../document/rules/items-and-agreements.md) says, and each linked as its type says. Which documents are owed is read from the documentation plan the run's brief carries; a run with none emits only the first set.

Always, for the [plan](../../document/rules/types/plan.md):
- **Interfaces `IFC`.** One per contract from [specify-interfaces](03-specify-interfaces.md), its shape to the field in its body.
- **Units `UNIT`.** One per unit sliced above, `order` its place in the build order, linked as the type says to the spec's ids. Work the sources show already merged is a unit too, its `ships in` the merged request ([mine-the-sources](../../../craft/evidence/mine-the-sources.md)).
- **Assumptions `ASM`** (home: [raid-log](../../document/rules/types/raid-log.md)), `status` `open`. Each surfaced by [surface-assumptions](../rules/surface-assumptions.md), with what breaks if it is false and its validation step, the riskiest marked by that rule's ranking. Each residual risk flagged above is one too, its spike as its validation.
- **Risks `RISK`** (home: [raid-log](../../document/rules/types/raid-log.md)), `direction` `downside`, `status` `open`. One per hard flow the [risk scale](../rules/risk-scale.md) rates: `if` and `then` from its failure mechanics, `trigger` from the signal that would show it, `probability` and `impact` by that type's own tests, and `proximity` the earliest gate whose step exercises the flow, else `build start`. `response`, `actionee` and `contingency` only when the run names them. (basis: benchmark, 2026-11-12, rated risks absent from the RAID log)
- **Decisions `DEC`** (home: [decision-register](../../document/rules/types/decision-register.md)). One per choice this run closed: the committed approach, each open decision from [mapping-to-system](01-mapping-to-system.md), and each fork the rollout settled.
  - `options`: every candidate, those a MUST gated out included, each with the MUST or axis it lost on; `chosen` the one committed.
  - It `answers` the filed question whose subject is the choice it closes, when the spec or an earlier register filed one.
  - `reversibility` by [design-for-reversibility](../../../craft/engineering/design-for-reversibility.md)'s test, the approach's reversibility rung as its input: two-way and one-way map across, and partial is `one-way` only when the undo needs a party outside the team's control.
  - `reach` by the register's test, never from blast radius: an external interface, or a format or contract others read, is beyond the change. `tier` follows from the two, as the type says.
  - `architectural` by the register's test. Which decisions also take a page is [decision-record](../../document/rules/types/decision-record.md)'s rule.
- **Questions `Q`.** Each sign-off [planning-rollout](05-planning-rollout.md) leaves open, its decider the sign-off's owner when that is one person. Its `reversibility` is that of the flow whose risk it accepts, `one-way` when the flow has a one-way step, and its `reach` and `tier` follow as a decision's do.

When the documentation plan owes a [design document](../../document/rules/types/design-document.md), its design sections `DES`, linked as the type says:
- `context` from the map of the existing system; a `goal` per north-star clause and a `non-goal` per spec non-goal;
- `structure` per main component and `data` per store the map names; `runtime` per hard flow from [working-the-hard-parts](04-working-the-hard-parts.md); one `deployment` from the rollout; `version skew` when the rollout opens a compatibility window;
- `interface` per interface, its contract left to its `IFC`;
- `alternative` per rejected candidate, `why not` its losing MUST or axis; `drawback` per cost of the committed approach's decision;
- `security` and `privacy` with `applies` `yes` when the map names a trust boundary or personal data, and `observability` `yes` when the rollout names the signals it watches; each `not known yet` otherwise.

Its quality goals `QG`: one per spec requirement of type `quality`, at most five, ranked by the requirement's priority, then id. The scenario fields come from that requirement's criteria and stay missing where they say nothing, but a measure they don't give is a `TBR` with the goal `blocked-by` its question. A requirement whose number is already a `TBR` hands the goal that question. Otherwise a new question is filed under a handle, its `reversibility` `two-way`, since a target is restated without undoing work, its `reach` by the register's test, so its `tier` is `2`; its decider the requirement's owner, and its decide-by `build start`, since the design document it blocks is due before the build. The requirement is handed back under its id with a `serves` link to its goal added, nothing else changed.

When the documentation plan owes a [cutover plan](../../document/rules/types/cutover-plan.md):
- **Gates `GATE`.** One per step as that type defines a gate, each phase of a parallel change its own. Its title opens with its step's code, `<code> · <name>`: the code the rollout or the sources name for the step, else its phase's letter (`E` expand, `M` migrate, `C` contract, `S` single) and its order within that phase, such as `M2`. Each spec slice whose units the gate is the earliest to expose is handed back under its id with the same code opening its title, nothing else changed. From the rollout: `phase`, `exposure`, `touches`, `one-way`, `rollback`; `go when` from the signals it calls healthy and `abort when` from those that trigger a rollback, each naming the metric it reads; its body and its undo steps as that type files them. `rollback` also names what undoing it leaves in place, from the rollout and the outside service's documented behaviour. `users see it` `yes`, or `no` for a preparatory step. `opens on`, `bake`, `driver`, `decides` and `fix forward when` only when the run names them; `rollback tested on` and `in` never. A step the sources show run or running is filed as that type files a gate filed already run. The gates not filed already run that miss any of their day, driver or decider share one question under a handle, "When do the undated gates open, and who runs each and calls go?", `reversibility` `two-way`, its `reach` by the register's test, its decider the task's owner, else missing, and its decide-by `build start`, so the register carries one entry for them rather than one per gate. Each such gate is `blocked-by` it until its day, driver and decider are all set; a later undated gate joins the question while it is open. When no gate is left blocked by it and it is still `open`, it is `withdrawn`, why: every gate it held now has its day, driver and decider; an answered question keeps its state. After that, a later undated gate opens a new question under a new handle, which never takes the closed one's id. Meanwhile the gate's own decide-by, its `opens on` elsewhere, is `build start` until that day is set. (basis: benchmark, 2026-11-12, no gate dated, so nothing it owed ever fell due)
- **Metrics `MET`.** One per signal a gate reads: `role` `goal` for what the step exists to move, `guardrail` for a rollback trigger, missing otherwise. Its `baseline` comes from a source that measured it; without one it is missing, and the metric's body says what would measure it before the first gate that reads it, when the cutover plan's checks first require it.

Every piece is `proposed` but a question, which is `open`, and a piece the run carries an agreement on, which takes that agreement. The owner is the task's owner when the run names one. A decider, driver or `decides` is the one person the run names for it; several, or a team, leave it missing. A decide-by is the date or gate the run gives, else left missing for documenting it to fill with the type's due point.
