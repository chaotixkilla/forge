# gate-mode (`--gate`)

Activated by `--gate`, referenced from [deliver-findings](../phases/06-deliver-findings.md).

The base review is informational — it delivers findings and the reader decides what to do. This module turns the review into a *decision*: a pass/fail check that exits non-zero when disqualifying findings remain, so it can stand in a CI pipeline as a merge barrier. Deletion test: remove it and review still reports; the pass/fail status and exit behavior are the added, flag-gated behavior.

## The delta

- **Compute a status from the floored list.** After triage, if any finding remains at or above the gate floor, the review **fails**; otherwise it **passes**. Exit accordingly (non-zero on fail), so a pipeline can block on it.
- **Read the same triaged findings the report shows** — gating does not re-judge or re-grade; it thresholds the list [triage-and-rank](../phases/05-triage-and-rank.md) already produced against [severity-scale](../rules/severity-scale.md). Composition with `--typed` is defined in [deliver-findings](../phases/06-deliver-findings.md).

## The gate floor

The floor is `--severity-min` when the caller sets one, and an explicit `--severity-min` always overrides the default. When they don't set one, the floor is **high**: the gate blocks on high and critical findings and treats medium and below as advisory. A lower floor makes the gate noisy enough that teams disable it; a higher one lets landing-blocking bugs through. `(basis: maintainer, 2026-07-02)`

State the floor in the gate's output either way, so a failed check tells the reader *what* threshold it failed against, not just that it failed.
