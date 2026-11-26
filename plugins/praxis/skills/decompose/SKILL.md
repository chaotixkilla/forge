---
name: decompose
description: Break an approved design or plan into ordered, independently shippable work-ready tasks cut on natural seams, sized to review cadence, ordered by dependency then risk, each with a done-condition and explicit links, covering the source without orphans or overlaps, returned for review or as a checklist. Filing them as work-items is the caller's.
metadata:
  flags:
    --from-plan=<path>: consume an approved plan's buildable units and ordering as the authoritative inventory to render into work-ready tasks (the preferred driving artifact); a phase-1 input, not a mode
    --checklist: emit the units as a single ordered checklist for lightweight tracking, with no tracker needed
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

decompose touches no backend and declares no `config_requires`: it returns the units, and filing them as work-items is the caller's delivery. `--checklist` renders the units as one ordered checklist instead of the default presentation: see [modules/emit-checklist.md](modules/emit-checklist.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies.

1. Ingest the source: load the plan/design (or a spec, or a framed request), decide whether it is ready to decompose or must route back, and extract the raw inventory of work it implies  — see [phases/01-ingest-the-source.md](phases/01-ingest-the-source.md)
2. Carve into units: cut the work into independently completable units along the lowest-coupling seams, each owning a single coherent outcome  — see [phases/02-carve-into-units.md](phases/02-carve-into-units.md)
3. Size and sequence: right-size each unit against the team's review/integration cadence (split the too-big, merge the trivial), then order by dependency then risk  — see [phases/03-size-and-sequence.md](phases/03-size-and-sequence.md)
4. Make units actionable: give each unit an unambiguous scope, a one-sentence done-condition, explicit dependency links, and just-enough context to start without re-deriving the plan  — see [phases/04-make-units-actionable.md](phases/04-make-units-actionable.md)
5. Check coverage and hand off: prove the units cover the source with no orphans or overlaps, flag residual risks as spikes, then emit in the requested form  — see [phases/05-check-coverage-and-handoff.md](phases/05-check-coverage-and-handoff.md)
