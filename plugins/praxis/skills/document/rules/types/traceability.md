# Traceability

One table that ties each requirement to everything that carries it, both up to the need it serves and down to what tests and gates it, so a changed requirement shows at once what it reaches.

## Reader and question

A reviewer of the change, or a maintainer later: "Is every requirement carried and verified, and if this one changes, what does it reach?"

## Page

`own page`

## Membership

Kept by document rather than produced by a step: one row per requirement in the [spec](spec.md) and one per acceptance criterion, its cells filled from the links other pages' items carry, each cell linking its source. The change requests and commits that carry a requirement are evidence on it. Its subject is the task's requirements, so a task has one. It is filed again whenever an item or link it shows changes.

## Items

Declares none. Shows `NS`, `REQ` and `AC` (home: [spec](spec.md)), `UNIT` (home: [plan](plan.md)), `TEST` (home: [test-plan](test-plan.md)), `MIT` and `THR` (home: [threat-model](threat-model.md)), `GATE` (home: [cutover-plan](cutover-plan.md)) and `FND` (home: [review-record](review-record.md)).

Each axis of a view holds one kind, so a cell never mixes a test with a gate. (basis: prototype sweep, 2026-11-11, one kind of thing per axis) A cell is never blank: it shows the ids it links, or the empty marker `none`, which every table here declares on its columns and the matrix on its cells. The required pairs are a requirement's: up to a north-star clause or an outside need, and down to a test of it or of one of its acceptance criteria. A required pair left empty shows `none` too, and section 1 lists its requirement as a gap. An acceptance criterion's row owes no required pair of its own: its up-cell is its requirement, and its other empty cells show `none`. (basis: NASA SWE-052, no empty cells; maintainer, 2026-11-11, every requirement traces up)

**A non-conformance joins the trace.** A verification on a requirement, criterion or test whose outcome is a failure stands as a non-conformance until a later verification of the same thing passes; both stay in the evidence. Sections 1 and 4 list it. (basis: NASA SWE-052, requirements to non-conformances)

**Against the baseline.** A requirement whose content differs from its baseline content is listed in section 1, with each verification taken before that change as resting on the earlier content. (basis: maintainer, 2026-09-30, a changed requirement reopens its row)

## Sections

1. **Is every requirement carried and verified?** Always. The gate coverage matrix, then, where the spec groups requirements by stream, the stream coverage view. A requirement has a test when a `TEST` verifies it, directly or through one of its acceptance criteria, and is passing when the latest verification of each test that verifies it holds. Then a list of each requirement with a gap: a required pair empty, a non-conformance standing, or a verification resting on earlier content. (basis: research, 2026-11-11, coverage per stream and gate)
2. **What carries each requirement?** Always. The requirement trace, then the criterion trace.
3. **What does a changed requirement reach?** When a requirement differs from its baseline content. The reach chains for each.
4. **Where did a check fail?** When a non-conformance stands. A list of each: the failing verification, its date, and the requirement it fails.
5. **What carries no requirement?** When a test verifies no requirement or criterion, unless its purpose isn't `requirement` and it serves a gate, or when a gate is served by no test at all. A list of each. (basis: NASA SWE-052, an orphan means unnecessary work or a missing requirement) This list is the trace's view of orphans, beside the coverage matrix.

## Checks

*Computed:* each skips `superseded` and `withdrawn` items.
- Every requirement links up to a north-star clause or a need outside the documentation. (basis: maintainer, 2026-11-11; NASA SWE-052, upward trace catches over-engineering)

A requirement with no test is the [test-plan](test-plan.md)'s check, shown here as its empty cell.

*Judgment:*
- A test that wouldn't fail if its requirement were broken.
- An orphan kept without asking whether a requirement is missing.
- A link kept in prose on some page instead of on the item, so the trace can't see it.
- A verification resting on a requirement's earlier content, treated as current.
- Requirements too coarse for their rows to show what a change to one part of them reaches.

## Views

Every column of the tables, and the matrix's cells, declare the empty marker `none`.

- **Requirement trace:** `table` of every `REQ` in spec order: what it `serves`; its `AC`s (`served-by`, only `AC` targets); the `UNIT`s that `serve` it (`served-by`, only `UNIT` targets); the `TEST`s that `verify` it (`verified-by`); the `GATE`s those tests `serve` (path `verified-by` then `serves`, only `GATE` targets); the `MIT`s it `serves` (`serves`, only `MIT` targets) and the `THR`s they `cover` (path `serves` then `covers`); the `FND`s that show it doesn't hold (`broken-by`, only `FND` targets); then its home's live fields.
- **Criterion trace:** `table` of every `AC`, grouped by the `REQ` it `serves`, so a test of a criterion shows on the criterion's row: what it `serves`; the `TEST`s that `verify` it (`verified-by`); the `GATE`s those tests `serve` (path `verified-by` then `serves`, only `GATE` targets); the `FND`s that show it doesn't hold (`broken-by`, only `FND` targets); then its home's live fields.
- **Gate coverage:** `matrix` of `REQ`, `TEST` and `GATE`, `REQ` rows against `GATE` columns, each cell the path `verified-by` then `serves`: the tests of that row that serve that gate.
- **Stream coverage:** `table` of every `REQ` grouped by its `stream`: the `TEST`s that verify it (`verified-by`), their `latest run` (`verified-by`, field `latest run`), the `TEST`s that verify one of its `AC`s (path `served-by`, only `AC` targets, then `verified-by`), and their `latest run` (the same path, field `latest run`).
- **Reach chains:** three `chain`s from each changed `REQ`, one per path: `verified-by` then `serves`, to its tests and their gates; `serves` then `covers`, to its mitigations and their threats; and `served-by`, only `AC` and `UNIT` targets, to its criteria and units. (basis: maintainer, 2026-11-11, one chain per selected item)

## Minimum form

Each always-present section keeps its heading with one line: no requirement is filed yet, so nothing is traced.
