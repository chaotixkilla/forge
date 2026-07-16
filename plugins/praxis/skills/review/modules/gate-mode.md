# gate-mode (`--gate`)

Activated by `--gate`, referenced from [deliver-findings](../phases/06-deliver-findings.md).

The base review is informational — it delivers findings and the reader decides what to do. This module turns the review into a *decision*: a pass/fail check that exits non-zero when disqualifying findings remain, so it can stand in a CI pipeline as a merge barrier. Deletion test: remove it and review still reports; the pass/fail status and exit behavior are the added, flag-gated behavior.

## The delta

- **Compute a status from the floored list.** After triage, if any finding remains at or above the gate floor, the review **fails**; otherwise it **passes**. Exit accordingly (non-zero on fail), so a pipeline can block on it.
- **Read the same triaged findings the report shows** — gating does not re-judge or re-grade; it thresholds the list [triage-and-rank](../phases/05-triage-and-rank.md) already produced against [severity-scale](../rules/severity-scale.md). Composition with `--comment` and `--fix` is defined in [deliver-findings](../phases/06-deliver-findings.md) — with `--fix`, the status is computed against what *remains* after fixing.

## The gate floor

The floor is `--severity-min` when the caller sets one. When they don't, the gate needs a default floor to threshold against:

`(basis: ratified by the maintainer, 2026-07-02. Default gate floor = high — the gate blocks on high and critical findings, treating medium and below as advisory; a floor below high makes the gate noisy (teams disable it), a floor above high lets landing-blocking bugs through. An explicit --severity-min always overrides this default.)`

An explicit `--severity-min` always overrides the default. State the floor in the gate's output either way, so a failed check tells the reader *what* threshold it failed against, not just that it failed.
