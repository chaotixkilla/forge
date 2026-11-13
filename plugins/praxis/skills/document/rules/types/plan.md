# Plan

The design a task builds against.

**Reader and question.** Reviewer and maintainer: "what are we building, why this way, and in what order?"

**Page.** `own page`

## Membership

The plan step's result. Each choice the plan makes that earns a [decision record](decision-record.md) also files as one. (basis: maintainer, 2026-09-30; 2026-11-13) A later round that changes the plan, its rollout included, files its own plan, restated whole. (basis: maintainer, 2026-10-07)

## Items

**Interface `IFC`.**
- Fields: `scope` enum `external`, `internal`; `change` enum `new`, `altered`.
- Granularity: one contract the change introduces or alters, specified to the field in its body. A unit that builds it `serves` it, and a test may `verify` it. It `rests-on` the `ASM` it assumes, when it assumes one.
- Change regime: `baseline`.
- Agreement: `needed`.

**Unit `UNIT`.**
- Fields: `order` number; `ships in` text, the review request it lands through, named by its branch, empty until the branch is cut; for a unit already shipped, the merged request it shipped in.
- Granularity: one slice that can be built and verified on its own. It is `blocked-by` the units it rests on, and `serves` the requirements it builds toward and the spec's slice (`SLC`) it builds part of, when the spec has slices.
- Change regime: `baseline`.
- Agreement: `needed`.
- Live field: `request state`, text, `vcs: the state of the review request its ships in names, approved, merged, changes requested or awaiting review`.

Shows `ASM` (home: [raid-log](raid-log.md)) for the riskiest assumption. When the RAID log isn't owed, it stands where [type-files](../type-files.md) places a kind whose home isn't owed.

## Sections

1. **What are we building, and why this way?** Always. The chosen approach, the alternatives weighed and why each lost, in prose, linking each decision record.
2. **What does it touch?** Always. The components it changes and where, drawn where [when-a-visual-is-owed](../../../../craft/writing/when-a-visual-is-owed.md) owes it.
3. **What are the contracts?** When the change introduces or alters an interface. The interface cards, each with its shape in the body.
4. **What could bite?** Always. The hard flows and their failure mechanics, in prose, each flow naming its `RISK` (home: [raid-log](raid-log.md)) by in-tree reference, then the riskiest assumption, its `ASM` in prose, and the step that validates it.
5. **How does it reach production?** Always. The rollout: order, flags, exposure, how to undo it, and what can't be undone.
6. **In what order do we build it?** Always. The unit table and the unit graph, then the end-to-end path traced through them.

## Checks

- *Computed:*
  - every `UNIT` has a distinct `order`, and none is `blocked-by` a unit with a higher one;
  - every `UNIT` is `blocked-by` only `UNIT` items;
  - when a spec is owed, every `UNIT` `serves` a `REQ`;
  - an `IFC` with `scope` `external` has evidence linking the vendor's contract, or `rests-on` an `ASM`.
- *Judgment:*
  - one alternative named, as a strawman, beside the chosen one;
  - a seam two developers would build differently;
  - an end-to-end path with a gap between units;
  - a rollout with no way back named, or a one-way step not called out;
  - the riskiest assumption with no validation step.

## Views

- **Interface cards** (section 3): `cards` of every `IFC`: scope, change, its body (the contract).
- **Unit table** (section 6): `table` of every `UNIT`, sorted by `order` ascending: order, what it is `blocked-by`, what it `serves`.
- **Unit graph** (section 6): `graph` of every `UNIT` over `blocked-by`.

## Minimum form

Each always-present section in one line: the approach "not chosen", the touch "not mapped", the hard parts and rollout "not worked", and "no units yet".
