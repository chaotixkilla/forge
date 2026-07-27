# run-until-signal (`--until=<condition>`)

Activated by `--until=<condition>`, referenced from [run-and-observe](../phases/05-run-and-observe.md).

The base run executes the designed cases once. This module loops that execution — re-running until a stop condition is met — which is how you drive a change-and-re-run inner loop, or repeat a flake-prone case enough times to expose its nondeterminism. Deletion test: without the flag, [run-and-observe](../phases/05-run-and-observe.md) does a single pass; the loop is genuinely added behavior, so it is a module and not part of the phase.

## The delta

Loop [run-and-observe](../phases/05-run-and-observe.md) — re-executing the run (or a named subset of cases) — until `<condition>` is satisfied, then proceed to [report-the-verdict](../phases/06-report-the-verdict.md) with the final classified run. Every iteration still classifies its reds ([failure-classification](../rules/failure-classification.md)); a loop does not suspend the critical guard — repeating a case to expose a flake is the sanctioned use, but a green on one iteration still does not clear the production code.

## The stop condition — open-by-design, bounded

What `<condition>` means is the caller's per-run choice, and **deliberately open-by-design**: pinning a single stop condition would be false precision, because the useful signal differs by intent (a tight edit loop wants "green"; a flake hunt wants a repeat count; a triage wants "first failure"). What *is* pinned is the shape of legal conditions and a hard bound:

- **`green`** — stop when the run passes against the framed claim; report the first passing run. Bounded by a maximum attempt count so an always-red change terminates and reports FAIL rather than looping forever.
- **`first-failure`** — stop at the first genuine failure; report it immediately (fast triage of a suspected break).
- **`<N>`** (a repeat count) — run the case(s) N times regardless of outcome; report the pass/fail distribution — the flake-exposure mode ([control-nondeterminism](../rules/control-nondeterminism.md)).
- **change-triggered** — re-run on each change to the watched surface; the loop is bounded by the caller ending the watch, not by an outcome.

Every condition carries a bound: an explicit count, an outcome that must eventually occur, or a caller-ended watch. A loop with no terminating bound is a defect — never re-run "until green" without a maximum attempt count, or an always-failing change hangs the run instead of reporting FAIL.
