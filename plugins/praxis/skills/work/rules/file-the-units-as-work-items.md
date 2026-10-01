# File the units as work-items

When an act plans work in units, the units go where the team tracks work, one tracked item per unit, so the plan is something people pick up and close rather than a list in a document. This rule is how the developing act delivers decompose's units.

## Render each unit as a work-item

Hand the covered, ordered unit set to the **project_mgmt capability's `create work-items` operation** (served by the [project-mgmt](../../project-mgmt/SKILL.md) skill, which dispatches to whichever provider is configured). Per unit, supply:

- **Title** — the unit's single outcome, stated as its done-condition names it ([one-unit-one-outcome](../../decompose/rules/one-unit-one-outcome.md)).
- **Body** — the unit's scope, its one-sentence done-condition/acceptance criteria, and its just-enough context with the link back to the source ([carry-just-enough-context](../../decompose/rules/carry-just-enough-context.md)).
- **Dependency links** — each cross-unit prerequisite as a relation to the item it depends on ([make-dependencies-explicit](../../decompose/rules/make-dependencies-explicit.md)); the capability maps these to the provider's relation mechanism.
- **Sequence** — the dependency-then-risk order decompose returns, carried as the provider's order field.

## Rendered labels — what carries a scale, and what does not

Three label classes could ride on a work-item; each is pinned so a bare label never ships:

- **Size — no grade is rendered.** By the time units are filed they are all *right-sized* (decompose split the too-big and merged the trivial), so a size label would read "right-sized" on every item — noise, not signal. No size grade goes onto the item: the [unit-size-scale](../../decompose/rules/unit-size-scale.md) verdict governs the internal carve, not the output. `(basis: maintainer, 2026-07-10)`
- **Priority — relayed from the source in full, never minted, never mapped here.** The filer doesn't assign priority; where the source carries one (spec's MoSCoW rungs, or a plan unit's inherited priority), relay it **faithfully and in full** — hand the source's *complete* vocabulary (MoSCoW: **Must / Should / Could / Won't** — all four) to the project_mgmt capability as the unit's priority. It does **not** map those rungs onto the provider's priority field, collapse them, or reason about how many levels that field has: that normalization is **adapter-domain, below the seam**, where the configured provider's field shape is actually known. Where the provider's field cannot represent a rung (fewer levels, no matching option), the capability reports it per unit in capability terms and the act surfaces that in its report — it never silently coerces a rung at the skill layer. Where the source carries **no** priority, render none — do not invent one. `(basis: maintainer, 2026-07-10; after the project-mgmt port's contract and spec's MoSCoW scale)`
- **Risk — a spike flag, not a graded scale.** A unit that is a timeboxed investigation ([size-the-unknowns-as-spikes](../../decompose/rules/size-the-unknowns-as-spikes.md)) is flagged as a spike (a boolean marker / label the tracker supports), and its body states the question and time box. No graded "risk level" is rendered — risk enters the decomposition as the sequencing pass and the spike carve, neither of which is a rated label. `(basis: derived from the sequencing pass and the spike carve)`

## Prerequisite and degrade

Filing goes through the [project-mgmt](../../project-mgmt/SKILL.md) port, which owns `tools.project_mgmt`. When it reports the backend unavailable, **degrade rather than block**: file the units as an ordered checklist in the task's plan instead, and say plainly that the tracker couldn't be reached. Never silently drop the decomposition. `(basis: maintainer, 2026-07-10; per the project-mgmt skill's usage)`

The port reports a per-unit outcome — created, with anything it couldn't yet set flagged against the item, or not created, with a cause the caller can act on ([project-mgmt](../../project-mgmt/SKILL.md)) — so surface each to the caller, to complete or retry a partial filing, never re-create it wholesale.
