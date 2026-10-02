# Calibrate certainty to rigor

A review that reports every hunch drowns its real findings in noise; a review that reports only certainties misses the risky change's subtle bugs. The resolution is to make the reporting bar a *dial*, tied to how much rigor the caller asked for.

Certainty and severity are independent axes ([severity-scale](severity-scale.md)): certainty is *how sure the finding is real*, severity is *how bad if it is*. This rule owns where a review finding sits on certainty, and the rigor dial; it is cited from [hunt-for-defects](../phases/03-hunt-for-defects.md), [assess-craft](../phases/04-assess-craft.md), and [triage-and-rank](../phases/05-triage-and-rank.md).

## Placing a finding on the certainty scale

Every finding carries one level of the certainty scale in [results-and-certainty](../../../craft/evidence/results-and-certainty.md) — **observed**, **traced**, **inferred** or **unverified** — with the meanings and adjacent-level tests defined there. Review reads code rather than running it, so a finding reaches **observed** only when a scratch probe ([confirm-before-claiming](confirm-before-claiming.md)) ran its failing input and showed the wrong behavior; without one, **traced** is the ceiling (basis: derived from the standard's execution line). For a correctness finding, what places it is *how much of the cause→effect chain you actually read*:

- **traced** — you read every line between cause and effect and can state a concrete input that yields the wrong behavior.
  - *Anchor:* "with `items=[]`, line 42 evaluates `items[0]` → error; the caller at line 88 passes an empty list on the logout path — I read both."
- **inferred** — the mechanism is clear and the path very likely reachable, but one link is reasoned: a caller you did not fully trace, an input you believe occurs but did not check, or an expected value from outside the code — a standard's rule, a published contract — taken from your own knowledge rather than read at its source. That last link is named as unread; a finding traced in every other link stays inferred until the source is read.
  - *Anchor:* "this handler almost certainly receives null when the upstream optional field is unset; I did not walk every caller."
- **unverified** — a pattern that often signals a bug, with the failing path *not* established; worth a look, not a claim.
  - *Anchor (bottom):* "a shared mutable default argument — a classic footgun; I found no call that actually mutates it."

The review-specific line is **inferred vs unverified**: is the failing path established as *reachable* by what you read, or only *plausible* from the pattern? Reading the suspect line alone is not a first-hand reading of the failure the finding claims, so a pattern hit with its path unestablished is unverified however closely the line was read. (basis: derived from the evidence ladder in [anchor-every-claim](../../../craft/evidence/anchor-every-claim.md) and [confirm-before-claiming](confirm-before-claiming.md))

### Certainty for craft findings

A craft finding has no failing input to trace ([separate-correctness-from-taste](separate-correctness-from-taste.md): craft is graded by maintainer cost, not by a wrong input). It still carries a certainty and still clears the floor like any finding; its certainty measures **how sure you are the craft claim's *premise* holds**, on the same scale: `(basis: derived from the correctness placement above)`

- **traced** — you read the premise through: the existing helper does the same job and is reachable from here (reuse); the two blocks are behaviorally identical (duplication); the simpler form preserves behavior (simplification). A probe that ran the two forms against the same inputs makes it **observed**.
- **inferred** — the premise is very likely but one link is reasoned: you believe an existing helper covers this but did not check it handles this case, or that a block duplicates another you did not read line-for-line.
- **unverified** — a pattern that usually signals a craft cost, with the premise not established: "this *looks* like it reinvents something the codebase has," without having found the thing.

The line that matters is again **inferred vs unverified**: is the premise *established* (the helper located, the blocks compared), or only *plausible*? A craft finding whose premise you have not established (the "existing helper" you never located) is unverified, and reports only where the rigor floor admits unverified findings — the same bar an unverified correctness finding faces.

## The rigor dial

`--rigor` is praxis's own dial and leaves the model's effort setting alone: a high-rigor review can run at any model effort, and the model's effort never stands in for this dial. (basis: maintainer, 2026-09-30) At low or medium rigor, a change that [scope-the-review](../phases/01-scope-the-review.md) measures as small recruits no explorers. `--rigor` moves four things together — a single dial, not four knobs — and its direction is fixed: **low favors a few of the surest findings; max broadens coverage and admits unverified ones.** (basis: the established code-review convention)

`(basis: maintainer, 2026-10-02, for the certainty floors; maintainer, 2026-07-02, for the low/medium lens split below; `comments` joined the craft lenses on 2026-09-02)`

| rigor | certainty floor (report at or above) | blast-radius depth | lens set | fan-out |
|---|---|---|---|---|
| **low** | traced | touched lines + direct callers | correctness: `logic`, `boundary`, `error-paths` · craft: none | inline, single pass |
| **medium** *(default)* | inferred | + callees and the immediate invariants they touch | correctness: all seven (adds `concurrency`, `security`, `resource-safety`, `data-integrity`) · craft: `reuse`, `simplification`, `comments` | inline, single pass |
| **high** | unverified, each labelled as such | + transitive callers of any changed signature | correctness: all seven · craft: all five (adds `efficiency`, `altitude`) | recruit the adversary + simplicity-hawk critics to attack candidates |
| **max** | unverified, each labelled as such | exhaustive reachable graph | all lenses, plus bug patterns beyond the enumerated set | full critic pass + parallel verification |

The lens cells are the **definitive** set for each level, not examples: the correctness lenses are exactly the seven enumerated in [hunt-for-defects](../phases/03-hunt-for-defects.md) (`logic`, `boundary`, `error-paths`, `concurrency`, `security`, `resource-safety`, `data-integrity`) and the craft lenses the five in [assess-craft](../phases/04-assess-craft.md) (`reuse`, `simplification`, `efficiency`, `altitude`, `comments`). The principle behind the split: **low** runs the correctness lenses that bite nearly every change; **medium** completes the correctness sweep — adding the four that bite when a change touches shared state, untrusted input, resources, or persisted data — and takes the three highest-value craft lenses, `reuse`, `simplification` and `comments`; **high** and **max** add the rest. So a default (medium) run *does* hunt resource-safety and data-integrity — a skipped-cleanup or half-write defect on a new branch is a medium-rigor finding, not a high-rigor one.

The floor is a *reporting* bar, not a *hunting* bar: hunt across the rigor's whole lens set, then withhold at delivery everything below the certainty floor. `--lenses` narrows the lens set to the named subset; `--severity-min` is a separate, severity-side filter ([severity-scale](severity-scale.md)) applied on top. `--gate` counts only traced findings and above against its floor, whatever the rigor ([gate-mode](../modules/gate-mode.md)). When no `--rigor` is given, default to **medium** — the level that reports inferred findings and above, sweeps every correctness lens, and withholds unverified ones. (basis: derived from what a caller who names no rigor most likely wants)

Blast-radius depth here is the *reporting-rigor* view of the deeper method in [read-the-diff-in-its-blast-radius](read-the-diff-in-its-blast-radius.md); that rule owns *how* to follow the radius, this row owns *how far* at each rigor.
