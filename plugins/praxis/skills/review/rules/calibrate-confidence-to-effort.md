# Calibrate confidence to effort

A review that reports every hunch drowns its real findings in noise; a review that reports only certainties misses the risky change's subtle bugs. The resolution is to make the reporting bar a *dial*, tied to how much rigor the caller asked for. This rule defines two interlocking scales — the **confidence** a finding carries, and the **effort** level that sets how low a confidence review will report. Get this wrong and two reviewers at the same effort disagree on what's worth surfacing; pinned, they report the same set.

Confidence and severity are independent axes ([severity-scale](severity-scale.md)): confidence is *how sure the finding is real*, severity is *how bad if it is*. This rule owns confidence and the effort dial; it is cited from [hunt-for-defects](../phases/03-hunt-for-defects.md), [assess-craft](../phases/04-assess-craft.md), and [triage-and-rank](../phases/05-triage-and-rank.md).

## The confidence scale

Every finding carries one of three confidence levels. The discriminator is *how much of the cause→effect chain you actually read* versus inferred.

- **confirmed** — you traced the exact path and can state a concrete input that yields the wrong behavior, having read every line between cause and effect.
  - *Anchor (top):* "with `items=[]`, line 42 evaluates `items[0]` → error; the caller at line 88 passes an empty list on the logout path — I read both."
- **probable** — the mechanism is clear and the path very likely reachable, but one link is inferred: a caller you did not fully trace, or an input you believe occurs but did not confirm.
  - *Anchor:* "this handler almost certainly receives null when the upstream optional field is unset; I did not walk every caller."
- **speculative** — a pattern that often signals a bug, with the failing path *not* established; worth a look, not a claim.
  - *Anchor (bottom):* "a shared mutable default argument — a classic footgun; I found no call that actually mutates it."

Discriminators between adjacent levels: **confirmed vs probable** — is *every* link in the chain read, or is one inferred? **probable vs speculative** — is the failing path established as *reachable*, or only *plausible*? (basis: this is the evidence ladder that [anchor-every-finding-to-evidence](anchor-every-finding-to-evidence.md) and [confirm-before-claiming](confirm-before-claiming.md) already demand — the levels name how far up that ladder a finding has climbed.)

### Confidence for craft findings

The three levels above are anchored to a *correctness* cause→effect chain — but a craft finding has no failing input to trace ([separate-correctness-from-taste](separate-correctness-from-taste.md): craft is graded by maintainer cost, not by a wrong input). A craft finding still carries a confidence, and still clears the floor like any finding — its confidence measures **how sure you are the craft claim's *premise* holds**, on the same three-level ladder:

- **confirmed** — you verified the premise: you read the existing helper and confirmed it does the same job and is reachable from here (reuse); you confirmed the two blocks are behaviorally identical (duplication); you confirmed the simpler form preserves behavior (simplification).
- **probable** — the premise is very likely but one link is unverified: you believe an existing helper covers this but did not confirm it handles this case, or that a block duplicates another you did not read line-for-line.
- **speculative** — a pattern that usually signals a craft cost, with the premise unverified: "this *looks* like it reinvents something the codebase has," without having found the thing.

The discriminator mirrors the correctness ladder: **confirmed vs probable** — did you *read and verify* the premise (the helper exists and applies, the blocks match), or infer it? **probable vs speculative** — is the premise *established*, or only *plausible*? A craft finding whose premise you have not established (the "existing helper" you never located) is speculative, and reports only where the effort floor admits speculation — the same bar a speculative correctness finding faces.

## The effort dial

`--effort` moves four things together — a single dial, not four knobs — and its direction is fixed: **low favors a few high-confidence findings; max broadens coverage and admits uncertain ones.** (basis: the direction mirrors the established code-review convention — fewer, high-confidence findings at low effort; broader coverage that admits uncertain ones at high — as the harness's own code-review skill encodes it.)

`(basis: ratified by the maintainer, 2026-07-02. The per-level calibration below — confidence floor, blast-radius depth, lens set, and fan-out per effort level. The direction is basis'd above; the confidence floors and the low/medium lens split are the maintainer's ratified house calibration.)`

| effort | confidence floor (report at or above) | blast-radius depth | lens set | fan-out |
|---|---|---|---|---|
| **low** | confirmed only | touched lines + direct callers | correctness: `logic`, `boundary`, `error-paths` · craft: none | inline, single pass |
| **medium** *(default)* | confirmed + probable | + callees and the immediate invariants they touch | correctness: all seven (adds `concurrency`, `security`, `resource-safety`, `data-integrity`) · craft: `reuse`, `simplification` | inline, single pass |
| **high** | + speculative, flagged as unverified | + transitive callers of any changed signature | correctness: all seven · craft: all four (adds `efficiency`, `altitude`) | recruit the adversary + simplicity-hawk critics to attack candidates |
| **max** | anything worth a look, flagged | exhaustive reachable graph | all lenses, plus speculative patterns beyond the enumerated set | full critic pass + parallel verification |

The lens cells are the **definitive** set for each level, not examples: the correctness lenses are exactly the seven enumerated in [hunt-for-defects](../phases/03-hunt-for-defects.md) (`logic`, `boundary`, `error-paths`, `concurrency`, `security`, `resource-safety`, `data-integrity`) and the craft lenses the four in [assess-craft](../phases/04-assess-craft.md) (`reuse`, `simplification`, `efficiency`, `altitude`). The principle behind the split: **low** runs the correctness lenses that bite nearly every change; **medium** completes the correctness sweep — adding the four that bite when a change touches shared state, untrusted input, resources, or persisted data — and takes the two highest-value craft lenses; **high** and **max** add the rest. So a default (medium) run *does* hunt resource-safety and data-integrity — a skipped-cleanup or half-write defect on a new branch is a medium-effort finding, not a high-effort one.

The floor is a *reporting* bar, not a *hunting* bar: hunt across the effort's whole lens set, then withhold at delivery everything below the confidence floor. `--lenses` narrows the lens set to the named subset; `--severity-min` is a separate, severity-side filter ([severity-scale](severity-scale.md)) applied on top. When no `--effort` is given, default to **medium** — the level that reports findings you have traced or all-but-traced, sweeps every correctness lens, and skips pure speculation. (basis: medium is the level a caller who names no effort most likely wants — a complete correctness sweep and trustworthy findings without noise; the default is named so a cold run does not invent one.)

Blast-radius depth here is the *reporting-effort* view of the deeper method in [read-the-diff-in-its-blast-radius](read-the-diff-in-its-blast-radius.md); that rule owns *how* to follow the radius, this row owns *how far* at each effort.
