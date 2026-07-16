# Weight by impact, not count

A long findings list feels thorough and is often the opposite: the three findings that matter are buried under twenty that don't, and the author — who has finite attention — spends it on the nits and lands the bug. Review's value is *signal*, not volume. This rule governs two decisions that protect signal: what to surface at all, and how to order what survives. It is cited from [triage-and-rank](../phases/05-triage-and-rank.md) (where the cut and the ordering happen) and [deliver-findings](../phases/06-deliver-findings.md) (where the order reaches the author).

## Silence is a valid result

The default expectation is not "produce findings." A change that is correct and well-crafted returns **no findings** — and saying so plainly is a stronger review than manufacturing observations to look diligent. Never pad the list. A finding earns its place by clearing the confidence floor for the effort level ([calibrate-confidence-to-effort](calibrate-confidence-to-effort.md)) *and* carrying a real consequence ([anchor-every-finding-to-evidence](anchor-every-finding-to-evidence.md)); one that clears neither is noise, and noise costs the author more than the finding is worth. The discriminator for keeping a finding: **would the author be right to spend attention on this?** If declining the *fix* is the reasonable call, it is at most `info`. Then a second cut decides `info` versus silence: **keep it as `info` only if a thoughtful author would be glad you surfaced it — a genuine heads-up, or something worth knowing even if they don't act on it; drop it entirely if surfacing it would neither change what they do nor teach them anything.** When you're unsure between `info` and dropping, drop — signal over volume.

## The ranking key

Order the survivors so the author reads them in the order they should act:

1. **Severity, descending** — critical before high before medium, per [severity-scale](severity-scale.md). What can hurt most, first.
2. **Confidence, descending, as the tie-break** — among equal severity, confirmed before probable before speculative. A sure high-severity bug outranks a suspected one.
3. **Blast radius, as the final tie-break** — among equal severity *and* confidence, the finding that reaches more of the system first. Measure reach concretely as the **count of distinct callers or modules the finding touches** (the same radius the hunt already traced, per [read-the-diff-in-its-blast-radius](read-the-diff-in-its-blast-radius.md)) — a four-module finding orders ahead of a one-caller one. This tie-break is reached only when severity and confidence are both equal, and it only reorders adjacent same-grade findings, so the measure is a light one — but it is *pinned* (distinct callers/modules reached), not left to each run to read "more of the system" its own way.

(basis: severity-first — most-severe-first — is the standard findings-ordering convention, as the harness's own findings channel uses it; the confidence tie-break follows from wanting the author to act on certainties before suspicions. The blast-radius measure is pinned to distinct callers/modules reached — a countable proxy over "touches more of the system," which otherwise let two runs order the same pair oppositely; the count is deliberately coarse because this tie-break only reorders findings already equal on both graded axes.)

## Impact over count, concretely

Resist two specific temptations. First, **splitting one issue into many** to raise the count — three symptoms of one root cause are one finding with three locations, not three findings. Second, **inflating severity to justify inclusion** — if a finding only merits `info`, report it as `info` or drop it; do not promote it to `medium` so it survives a floor. The list's length should track the change's actual problems, nothing more. A review that surfaces two real bugs and says the rest is clean is more useful, and more trusted, than one that lists twenty items of mixed worth.
