---
name: decompose
description: Break an approved design or plan into an ordered set of independently shippable work units — cut along natural seams, right-size each to the team's review/integration cadence, order by dependency then risk, make each unit actionable with a one-sentence done-condition and explicit cross-unit links, and prove the set covers the source with no orphans or overlaps; then present the breakdown for review, or emit it as tracked work-items or an ordered checklist. The bridge from approved design to work-ready tasks.
metadata:
  flags:
    --from-plan=<path>: consume an approved plan's buildable units and ordering as the authoritative inventory to render into work-ready tasks (the preferred driving artifact); a phase-1 input, not a mode
    --ticket: emit the units as tracked work-items via the project_mgmt capability — one item per unit, carrying dependencies and sequence
    --checklist: emit the units as a single ordered checklist for lightweight tracking, with no tracker needed
    --plan-only: present the proposed decomposition for review without emitting to any tracker or artifact (the default when no output flag is given)
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

decompose owns no backend of its own: its only external touch is the project_mgmt capability (the `--ticket` emit), delegated wholesale to the `project-mgmt` skill, which owns the `tools.project_mgmt` prerequisite — so decompose declares no `config_requires`. When the project_mgmt backend is unavailable, `--ticket` degrades to `--checklist` / `--plan-only` output rather than blocking (the `project-mgmt` skill owns guiding the user through `init:project_mgmt`). The output sink is chosen by flag: `--ticket` (tracked items) and `--checklist` (one ordered list) are behaviors activated by their flag — see [modules/emit-tickets.md](modules/emit-tickets.md) and [modules/emit-checklist.md](modules/emit-checklist.md); `--plan-only` is the base behavior of the final phase and the default when none is given. The three are mutually exclusive sinks.

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies.

1. Ingest the source: load the plan/design (or a spec, or a framed request), decide whether it is ready to decompose or must route back, and extract the raw inventory of work it implies  — see [phases/01-ingest-the-source.md](phases/01-ingest-the-source.md)
2. Carve into units: cut the work into independently completable units along the lowest-coupling seams, each owning a single coherent outcome  — see [phases/02-carve-into-units.md](phases/02-carve-into-units.md)
3. Size and sequence: right-size each unit against the team's review/integration cadence (split the too-big, merge the trivial), then order by dependency then risk  — see [phases/03-size-and-sequence.md](phases/03-size-and-sequence.md)
4. Make units actionable: give each unit an unambiguous scope, a one-sentence done-condition, explicit dependency links, and just-enough context to start without re-deriving the plan  — see [phases/04-make-units-actionable.md](phases/04-make-units-actionable.md)
5. Check coverage and hand off: prove the units cover the source with no orphans or overlaps, flag residual risks as spikes, then emit in the requested form  — see [phases/05-check-coverage-and-handoff.md](phases/05-check-coverage-and-handoff.md)
