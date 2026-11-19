Execute the cases and read what actually happened.

## Run the suite via the project's own runner

Execute the designed cases through the project's configured runner (discovered in [map-the-surface](02-map-the-surface.md)), and capture the raw observation — pass/fail per case, output, errors, timings — as *evidence*, separately from any interpretation of it. Name the runner as the capability it is ("run the project's suite"); never assume a specific framework. **Degraded case:** if there is no runnable suite, that is a stated stop reported in [report-the-verdict](06-report-the-verdict.md), not a silent pass.

## Prove a new test can fail before trusting its green

Keep a new or changed test's run without the change and its run with it as the kit's evidence that it failed, then passed ([documentation-kit](../../../craft/writing/documentation-kit.md)). Apply [prove-the-test-can-fail](../../../craft/engineering/prove-the-test-can-fail.md): a new or changed test is confirmed to redden against the broken or un-fixed behavior before its green is trusted as evidence. For a test guarding a fix, this is the fail-before / pass-after check. Break the change where the harness reads it, as for a schema change in the migration the test environment builds from rather than the model. Name every file a mutation edits or restores by its path from the task worktree's root, whatever folder the suite runs from. When the tree holds uncommitted work, copy each file a mutation touches before mutating it and revert by restoring that copy, never through version control, and before the next run confirm the tree's diff is what it was before the mutation. (basis: field findings, 2026-11-19 — reverts wiped uncommitted work, stacked from the wrong directory, and missed the migration)

## Classify every red result

Apply [failure-classification](../rules/failure-classification.md): sort each red into **environment noise / flake / genuine failure / test defect** by the discriminators (phase, then scope, then determinism, then the contract), and apply the critical guard — never let a single green rerun auto-resolve a red to "flake." Only a genuine failure can make the claim fail — and, per [report-the-verdict](06-report-the-verdict.md), only when it is **in-claim** by that phase's scope test (an out-of-claim genuine failure is a real finding surfaced separately, not this change's failure). Flakes and environment noise are reported as themselves, and a flake is a defect to root-cause, not noise to retry past ([control-nondeterminism](../../../craft/engineering/control-nondeterminism.md)).

## Read how much of the new code the run executed

Where the project reports line coverage (the coverage convention [coverage-adequacy](../rules/coverage-adequacy.md)'s routing honours), read it from the run of the designed cases above, never from a run against a mutated tree. Coverage rides that run when it is an option or a configuration of the command the project already runs, with nothing installed; a different command, a wrapper included, is a run of its own. Under `--until`, it rides every pass, and the last pass is read. A pass of its own, the whole suite with coverage on at the same tree, runs only when the request test was given asks for the change's footprint, and after any `--until` loop ends; test never stops to offer it. Read the change's new lines against the report. The reading never sets the result.
- **New lines** are the lines the change adds or alters against its base, the merge base with the branch it merges into, following renames so a moved line isn't new, in the files the report covers, and that it counts as executable. A file the report leaves out, such as a test, a document or a configuration file, is outside the project's coverage convention: no reading names it.
- **Area** is the file's path from the repository root, cut to its first two directories (`src/billing/invoice.py` is `src/billing`). A file with fewer directories takes the ones it has, and one at the root is `(root)`.
- **The reading,** for each area that holds new lines: how many there are, how many the run executed, its scope, `whole suite` when the run was the project's test command with no path, filter, marker or narrowing such as `--changed`, else `part of the suite`, and the commit it ran at, with "and uncommitted work" when the tree held some.
- **Not measured,** as one reading for the whole change, area `(all)`, with the first of these that holds as its reason:
  - the change's base can't be read;
  - the project reports no coverage: it has no coverage option, configuration or command;
  - coverage wasn't collected: it couldn't ride the run and no pass of its own was asked for, or, with no reading from the run, the one asked for left no readable report; one that leaves none while the run's own reading stands keeps that reading;
  - the run it was read from stopped before it ended (failing tests don't stop it);
  - the report is of a commit other than the head;
  - the change has no executable new lines.

A reading from part of the suite is a floor: a new line it didn't run may be run by a test outside it. The whole suite's is exact.

Each run's readings replace every earlier one, so the footprint is always one run's.

(basis: derived from coverage-adequacy's diff-scoped diagnostic; the two-directory area, so a reader sees which part of the codebase a gap sits in without a line per file; the run already made, so an unasked reading never adds a run — maintainer, 2026-11-19, as test runs already cost the most of a round)

## Under `--until`

Loop the verification rather than running a single pass — until the caller's stop condition — see [run-until-signal](../modules/run-until-signal.md). Without the flag, a single pass.

## Output

The classified run — per-case result, each red classified, each new test proven able to fail, and the new lines' coverage by area or not measured — handed to [report-the-verdict](06-report-the-verdict.md).
