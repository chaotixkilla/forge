# Calibrate confidence to rigor

A review that reports every hunch drowns its real findings in noise; a review that reports only certainties misses the risky change's subtle bugs. The resolution is to make the reporting bar a *dial*, tied to how much rigor the caller asked for.

Confidence and severity are independent axes ([severity-scale](severity-scale.md)): confidence is *how sure the finding is real*, severity is *how bad if it is*. This rule owns confidence and the rigor dial; it is cited from [hunt-for-defects](../phases/03-hunt-for-defects.md), [assess-craft](../phases/04-assess-craft.md), and [triage-and-rank](../phases/05-triage-and-rank.md).

## The confidence scale

Every finding carries one of three confidence levels. The discriminator is *how much of the cause→effect chain you actually read* versus inferred.

- **confirmed** — you traced the exact path and can state a concrete input that yields the wrong behavior, having read every line between cause and effect.
  - *Anchor (top):* "with `items=[]`, line 42 evaluates `items[0]` → error; the caller at line 88 passes an empty list on the logout path — I read both."
- **probable** — the mechanism is clear and the path very likely reachable, but one link is inferred: a caller you did not fully trace, an input you believe occurs but did not confirm, or an expected value from outside the code — a standard's rule, a published contract — taken from your own knowledge rather than read at its source. That last link is named as unread; a finding confirmed in every other link stays probable until the source is read.
  - *Anchor:* "this handler almost certainly receives null when the upstream optional field is unset; I did not walk every caller."
- **speculative** — a pattern that often signals a bug, with the failing path *not* established; worth a look, not a claim.
  - *Anchor (bottom):* "a shared mutable default argument — a classic footgun; I found no call that actually mutates it."

Discriminators between adjacent levels: **confirmed vs probable** — is *every* link in the chain read, or is one inferred? **probable vs speculative** — is the failing path established as *reachable*, or only *plausible*? (basis: derived from the evidence ladder in [anchor-every-claim](../../../craft/evidence/anchor-every-claim.md) and [confirm-before-claiming](confirm-before-claiming.md))

### Confidence for craft findings

The three levels above are anchored to a *correctness* cause→effect chain — but a craft finding has no failing input to trace ([separate-correctness-from-taste](separate-correctness-from-taste.md): craft is graded by maintainer cost, not by a wrong input). A craft finding still carries a confidence, and still clears the floor like any finding — its confidence measures **how sure you are the craft claim's *premise* holds**, on the same three-level ladder: `(basis: derived from the correctness ladder above)`

- **confirmed** — you verified the premise: you read the existing helper and confirmed it does the same job and is reachable from here (reuse); you confirmed the two blocks are behaviorally identical (duplication); you confirmed the simpler form preserves behavior (simplification).
- **probable** — the premise is very likely but one link is unverified: you believe an existing helper covers this but did not confirm it handles this case, or that a block duplicates another you did not read line-for-line.
- **speculative** — a pattern that usually signals a craft cost, with the premise unverified: "this *looks* like it reinvents something the codebase has," without having found the thing.

The discriminator mirrors the correctness ladder: **confirmed vs probable** — did you *read and verify* the premise (the helper exists and applies, the blocks match), or infer it? **probable vs speculative** — is the premise *established*, or only *plausible*? A craft finding whose premise you have not established (the "existing helper" you never located) is speculative, and reports only where the rigor floor admits speculation — the same bar a speculative correctness finding faces.

## The rigor dial

`--rigor` is praxis's own dial and leaves the model's effort setting alone: a high-rigor review can run at any model effort, and the model's effort never stands in for this dial. (basis: maintainer, 2026-09-30) At low or medium rigor, a change that [scope-the-review](../phases/01-scope-the-review.md) measures as small recruits no explorers. `--rigor` moves four things together — a single dial, not four knobs — and its direction is fixed: **low favors a few high-confidence findings; max broadens coverage and admits uncertain ones.** (basis: the established code-review convention)

`(basis: maintainer, 2026-07-02, for the confidence floors and the low/medium lens split below; `comments` joined the craft lenses on 2026-09-02)`

| rigor | confidence floor (report at or above) | blast-radius depth | lens set | fan-out |
|---|---|---|---|---|
| **low** | confirmed only | touched lines + direct callers | correctness: `logic`, `boundary`, `error-paths` · craft: none | inline, single pass |
| **medium** *(default)* | confirmed + probable | + callees and the immediate invariants they touch | correctness: all seven (adds `concurrency`, `security`, `resource-safety`, `data-integrity`) · craft: `reuse`, `simplification`, `comments` | inline, single pass |
| **high** | + speculative, flagged as unverified | + transitive callers of any changed signature | correctness: all seven · craft: all five (adds `efficiency`, `altitude`) | recruit the adversary + simplicity-hawk critics to attack candidates |
| **max** | anything worth a look, flagged | exhaustive reachable graph | all lenses, plus speculative patterns beyond the enumerated set | full critic pass + parallel verification |

The lens cells are the **definitive** set for each level, not examples: the correctness lenses are exactly the seven enumerated in [hunt-for-defects](../phases/03-hunt-for-defects.md) (`logic`, `boundary`, `error-paths`, `concurrency`, `security`, `resource-safety`, `data-integrity`) and the craft lenses the five in [assess-craft](../phases/04-assess-craft.md) (`reuse`, `simplification`, `efficiency`, `altitude`, `comments`). The principle behind the split: **low** runs the correctness lenses that bite nearly every change; **medium** completes the correctness sweep — adding the four that bite when a change touches shared state, untrusted input, resources, or persisted data — and takes the three highest-value craft lenses, `reuse`, `simplification` and `comments`; **high** and **max** add the rest. So a default (medium) run *does* hunt resource-safety and data-integrity — a skipped-cleanup or half-write defect on a new branch is a medium-rigor finding, not a high-rigor one.

The floor is a *reporting* bar, not a *hunting* bar: hunt across the rigor's whole lens set, then withhold at delivery everything below the confidence floor. `--lenses` narrows the lens set to the named subset; `--severity-min` is a separate, severity-side filter ([severity-scale](severity-scale.md)) applied on top. When no `--rigor` is given, default to **medium** — the level that reports findings you have traced or all-but-traced, sweeps every correctness lens, and skips pure speculation. (basis: derived from what a caller who names no rigor most likely wants)

Blast-radius depth here is the *reporting-rigor* view of the deeper method in [read-the-diff-in-its-blast-radius](read-the-diff-in-its-blast-radius.md); that rule owns *how* to follow the radius, this row owns *how far* at each rigor.
