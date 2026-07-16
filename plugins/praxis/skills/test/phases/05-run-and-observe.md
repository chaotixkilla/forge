Execute the cases and read what actually happened. The discipline is that a red result is a signal to *classify*, not a verdict to report raw — a genuine failure, a flaky test, and environment noise look identical until you sort them, and reporting any of them as another wastes someone's time or ships a bug.

## Run the suite via the project's own runner

Execute the designed cases through the project's configured runner (discovered in [map-the-surface](02-map-the-surface.md)), and capture the raw observation — pass/fail per case, output, errors, timings — as *evidence*, separately from any interpretation of it. Name the runner as the capability it is ("run the project's suite"); never assume a specific framework. **Degraded case:** if there is no runnable suite, that is a stated stop reported in [report-the-verdict](06-report-the-verdict.md), not a silent pass.

## Prove a new test can fail before trusting its green

Apply [prove-the-test-can-fail](../rules/prove-the-test-can-fail.md): a new or changed test is confirmed to redden against the broken or un-fixed behavior before its green is trusted as evidence. A test that has only ever passed may be asserting nothing — its green is not proof. For a test guarding a fix, this is the fail-before / pass-after check.

## Classify every red result

Apply [failure-classification](../rules/failure-classification.md): sort each red into **genuine failure / flake / environment noise** by the discriminators (phase, then scope, then determinism), and apply the critical guard — never let a single green rerun auto-resolve a red to "flake." Only a genuine failure feeds a FAIL verdict — and, per [report-the-verdict](06-report-the-verdict.md), only when it is **in-claim** by that phase's scope test (an out-of-claim genuine failure is a real finding surfaced separately, not this change's FAIL). Flakes and environment noise are reported as themselves, and a flake is a defect to root-cause, not noise to retry past ([control-nondeterminism](../rules/control-nondeterminism.md)).

## Under `--until`

Loop the verification rather than running a single pass — until the caller's stop condition — see [run-until-signal](../modules/run-until-signal.md). Without the flag, a single pass.

## Output

The classified run — per-case result, each red classified, each new test proven able to fail — handed to [report-the-verdict](06-report-the-verdict.md).
</content>
