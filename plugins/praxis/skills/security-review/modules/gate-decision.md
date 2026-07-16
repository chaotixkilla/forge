# gate-decision (`--gate`)

Activated by `--gate`, referenced from [reporting-findings](../phases/05-reporting-findings.md).

The base audit is informational — it delivers findings and the reader decides what to do. This module turns the audit into a *decision*: a pass/fail verdict with a non-zero exit when disqualifying findings remain, so it can stand in a pipeline as a merge barrier. Deletion test: remove it and the audit still reports; the verdict and exit behavior are the added, flag-gated behavior.

## The delta

- **Compute the verdict from the floored, ranked list** [assessing-severity](../phases/04-assessing-severity.md) produced against [severity-scale](../rules/severity-scale.md). Gating does not re-judge or re-grade; it thresholds the list that already exists.
- **Resolve to one of three outcomes** — pass / fail / inconclusive — the partition pinned in [reporting-findings](../phases/05-reporting-findings.md). An audit that could not scope its surface is **inconclusive**, never a silent pass.
- **Exit accordingly** so a pipeline can block: non-zero on fail. Signal inconclusive distinctly from both pass and fail, so "we could not check" is not read as "clean."

## The gate floor

The floor is `--severity-min` when the caller sets one. When they don't, the gate needs a default floor to threshold against:

`(basis: default gate floor = high — the gate fails on high and critical findings and treats medium and below as advisory — ratified by the maintainer, 2026-07-10. Sourced from corroborated CI-gate practice: blocking on high+critical is the common, survivable baseline (it is the out-of-the-box behavior of widely-used code-scanning gates, and the practitioner-recommended threshold for dependency/SAST gates), because a floor below high makes the gate noisy enough that teams disable it, while a floor above high lets landing-blocking breaches through. A minority "start at critical-only during rollout" practice exists but is weakly corroborated. An explicit --severity-min always overrides this default.)`

State the floor in the gate's output either way, so a failed check tells the reader *what* threshold it failed against — and, when the run is inconclusive, that the floor was never applied because the audit did not complete.
