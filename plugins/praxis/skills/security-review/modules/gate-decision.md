# gate-decision (`--gate`)

Activated by `--gate`, referenced from [reporting-findings](../phases/05-reporting-findings.md).

The base audit is informational — it delivers findings and the reader decides what to do. This module turns the audit into a *decision*: a gate result the calling pipeline maps to a non-zero exit when disqualifying findings remain, so it can stand as a merge barrier. Deletion test: remove it and the audit still reports; the gate result is the added, flag-gated behavior.

## The delta

- **Compute the result from the floored, ranked list** [assessing-severity](../phases/04-assessing-severity.md) produced against [severity-scale](../rules/severity-scale.md). Gating does not re-judge or re-grade; it thresholds the list that already exists.
- **Resolve to one result** on the results scale in [results-and-certainty](../../../craft/evidence/results-and-certainty.md), by whether the audit worked the surface it was asked to and what it found there:
  - **holds** — the audit completed and no finding counts against the floor. Its scope is the surface, breadth and adversary in the scope line, read and not run. An empty `--changed` window is a completed audit of nothing changed: holds, with the empty window stated.
  - **fails** — the audit completed and at least one finding counts against the floor.
  - **not checked** — nothing was audited: the subject couldn't be resolved or read, or the run stopped before any work (an `--exhaustive` run whose cost question couldn't be asked). Give the reason. `--changed` with no derivable base isn't this case: it audits the whole subject instead ([scoping-the-surface](../phases/01-scoping-the-surface.md)).

  Every run lands in exactly one: it either worked its surface or it didn't, and a completed one either has a counting finding or doesn't. `(basis: derived, for the partition and for not checked, since a run that audited nothing exercised nothing)`
- **A finding counts against the floor** when its severity meets the floor and its certainty is **traced**, this audit's ceiling ([confirm-reachability-before-flagging](../rules/confirm-reachability-before-flagging.md)). An inferred or unverified finding is reported but never fails the gate. `(basis: maintainer, 2026-10-02)`
- **Return the result** so a pipeline can block on fails, and signal not checked distinctly from both, so "we could not check" is not read as "clean."

## The gate floor

The floor is `--severity-min` when the caller sets one, which always overrides the default. When they don't, the default floor is **high**: the gate fails on high and critical findings and treats medium and below as advisory. A floor below high makes the gate noisy enough that teams disable it; one above high lets landing-blocking breaches through. `(basis: maintainer, 2026-07-10; after common CI code-scanning and SAST gate practice)`

State the floor in the gate's output either way, so a failing check tells the reader *what* threshold it failed against — and, when the result is not checked, that the floor was never applied because nothing was audited.
