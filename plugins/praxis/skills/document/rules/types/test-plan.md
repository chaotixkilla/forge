# Test plan

How the work will show that each requirement holds: which tests, where they run, what must pass before each stage, and, where versions meet or a step is undone, how that is tested too.

## Reader and question

A reviewer of the change: "How will we know each requirement holds, where is it checked, and what has to pass before the work moves on?"

## Page

`own page`

## Membership

The tests the work plans and runs, and the criteria a stage is entered on. Whether a requirement is carried at all is the [traceability](traceability.md)'s; what a gate's go/no-go card reads is the [cutover-plan](cutover-plan.md)'s. Its subject is the task's verification, so a task has one. It is filed again when a test or a criterion changes. A test's runs are verifications on it, never edits to it.

## Items

**Test `TEST`.** One check that can pass or fail on its own.
- Fields:
  - `method`: enum `test`, `demonstration`, `analysis`, `inspection`. A requirement checked by review or analysis has a test item too, so every requirement's verification has one home. (basis: ISO/IEC/IEEE 29148's verification methods, unverified at source)
  - `purpose`: enum `requirement`, `upgrade`, `downgrade`, `version skew`, `rollback rehearsal`, `restore rehearsal`.
  - `environments`: list of text. Where it runs.
  - `pass when`: text. The observable result that counts as a pass.
  - `before`: when. The gate the test must pass before.
- Links: it `verifies` the requirements or acceptance criteria it checks; a test whose purpose isn't `requirement` `serves` the gate it protects; a restore rehearsal `rests-on` the gate's restore path (`RST`).
- A rehearsal is a verification on its rehearsal test, not on the gate.
- Change regime: `baseline`.
- Live field: `latest run`, text, `ci: this test's latest run on the change's head`, for a test that runs in a pipeline.

**Graduation criterion `GRAD`.** One condition that must hold before the work enters a stage, such as wider exposure or general availability. (basis: Kubernetes KEP, graduation criteria)
- Fields:
  - `stage`: text. The stage it lets the work enter.
  - `before`: when. The gate that opens the stage.
- Links: it `serves` the gate that opens the stage, and `rests-on` the tests and metrics whose results it reads.
- Change regime: `baseline`.

Both kinds take Agreement `needed`, and each one's `before` is its decide-by. When a test's `before` names a gate, file a `serves` link to that gate.

Shows `REQ` and `AC` (home: [spec](spec.md)), `GATE` (home: [cutover-plan](cutover-plan.md)) and `RST` (home: [backup-restore-plan](backup-restore-plan.md)).

## Sections

1. **How is each requirement checked?** Always. The requirement table.
2. **Where does each test run?** Always. The test table.
3. **What must hold before each stage?** When a graduation criterion exists. The graduation table.
4. **Do old and new versions work together?** When parts of the change deploy separately, a shared contract changes, or clients or data hold the old form across a switch. Which pairs of versions can meet, in prose, then the skew table. (basis: Kubernetes KEP, upgrade and downgrade, version skew)
5. **Have we rehearsed undoing it?** When a gate exists. The rehearsal table.

## Checks

*Computed:* each skips `superseded` and `withdrawn` items.
- Every requirement is verified by a test, directly or through one of its acceptance criteria. (basis: NASA SWE-052, requirements to verifications)
- Every test verifies a requirement or criterion, or, when its purpose isn't `requirement`, serves a gate.
- Every test has its method, environments and pass-when.
- When a gate exists, every gate not filed already run ([cutover-plan](cutover-plan.md)) is served by a rehearsal test: a two-way gate users see by a `rollback rehearsal`; a one-way gate by a `restore rehearsal`, which `rests-on` its `RST` when one is filed. A two-way preparatory gate needs none. (basis: prototype sweep, 2026-11-11, rollback tested with a date and environment per gate)
- Every graduation criterion serves a gate and rests on at least one test or metric.

*Judgment:*
- A test whose pass-when couldn't fail while its requirement is broken.
- An inspection standing in where a runnable test was possible.
- A test environment that differs from production in what the requirement depends on.
- Old and new versions that can meet with nothing testing how each copes with the other, such as clients holding old credentials across a switch.
- A rehearsal run somewhere it couldn't fail the way production would.

## Views

- **Requirement table:** `table` of every `REQ` and `AC`: the `TEST`s that verify it (`verified-by`), their `method` and their `latest run` (`verified-by`, one named field each).
- **Test table:** `table` of every `TEST` grouped by purpose: method, environments, pass when, what it `verifies` or `serves`, latest run.
- **Graduation table:** `table` of every `GRAD`: stage, the `GATE` it `serves`, what it `rests-on`.
- **Skew table:** `table` of the `TEST`s whose purpose is `upgrade`, `downgrade` or `version skew`: environments, pass when, latest run.
- **Rehearsal table:** `table` of the `TEST`s whose purpose is `rollback rehearsal` or `restore rehearsal`: the `GATE` it `serves`, purpose, the `RST` it `rests-on`, environments, pass when, and the latest verification's date and environment, each with the empty marker "not rehearsed yet".

## Minimum form

One planned test per requirement, with its method, an environment and its pass-when. Before any requirement exists, each always-present section keeps its heading with one line: nothing to test yet.
