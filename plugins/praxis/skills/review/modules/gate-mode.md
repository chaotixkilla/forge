# gate-mode (`--gate`)

Activated by `--gate`, referenced from [deliver-findings](../phases/06-deliver-findings.md).

The base review is informational — it delivers findings and the reader decides what to do. This module turns the review into a *decision*: a check that returns a result the calling pipeline can block on when disqualifying findings remain, so it can stand in a CI pipeline as a merge barrier. Deletion test: remove it and review still reports; the gate result is the added, flag-gated behavior.

## The delta

- **Compute one result from the floored list**, on the results scale in [results-and-certainty](../../../craft/evidence/results-and-certainty.md):
  - **fails** — after triage, a finding at **traced** certainty or above (observed or traced, per [calibrate-certainty-to-rigor](../rules/calibrate-certainty-to-rigor.md)) remains at or above the gate floor.
  - **holds** — the change was judged and no such finding remains. Its scope is the resolved window at its endpoint commit, read and not run, at the stated floor.
  - **not checked** — the review halted before judging the change: the change couldn't be fetched, its description couldn't be held back, or a prior pass couldn't be read. Give the reason. The pipeline must not read it as holds.

  An inferred or unverified finding at the floor is reported but never fails the gate: severity no longer carries reachability, and a path not read end to end is what keeps a finding below traced ([severity-scale](../rules/severity-scale.md)). Every run lands in exactly one result, since it either judged the change or didn't, and a judged one either has a traced finding at the floor or doesn't. `(basis: maintainer, 2026-10-02, for the traced bar; derived, for the partition)`
- **Read the same triaged findings the report shows** — gating does not re-judge or re-grade; it thresholds the list [triage-and-rank](../phases/05-triage-and-rank.md) already produced against [severity-scale](../rules/severity-scale.md). Composition with `--typed` is defined in [deliver-findings](../phases/06-deliver-findings.md).

## The gate floor

The floor is `--severity-min` when the caller sets one, and an explicit `--severity-min` always overrides the default. When they don't set one, the floor is **high**: the gate blocks on high and critical findings and treats medium and below as advisory. A lower floor makes the gate noisy enough that teams disable it; a higher one lets landing-blocking bugs through. `(basis: maintainer, 2026-07-02)`

State the floor in the gate's output either way, so a failing check tells the reader *what* threshold it failed against, not just that it failed.
