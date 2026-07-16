# adversarial-critics (`--critics=<n>`)

Activated by `--critics=<n>`, referenced from the [SKILL.md](../SKILL.md) body (it scales scrutiny that spans phases, chiefly the stress-tests in [choosing-approach](../phases/02-choosing-approach.md) and [slice-and-validate](../phases/06-slice-and-validate.md)).

The base run recruits critics at the natural points — the trade-off-analyst on the approach choice, the future-self on reversibility, the adversary on the hard flows, the simplicity-hawk on complexity. This module sets *how many* perspective-diverse passes attack the committed design and folds their surviving objections back in. Deletion test: remove it and plan still recruits its default critics; the flag only turns the dial on how hard the design is stress-tested.

## The delta

- **Spawn `n` perspective-diverse passes, not `n` identical ones.** Diversity is the point: give each pass a distinct lens — approach trade-offs (trade-off-analyst), maintainability and reversibility (future-self), failure paths (adversary), unjustified complexity (simplicity-hawk) — so `n` critics cover `n` failure modes rather than redundantly re-checking one. When `n` exceeds the distinct lenses, add rounds or split a lens by area before duplicating it.
- **Fold surviving objections back into the design.** An objection that holds up changes the design — a re-scored approach, a named reversal path, a specified failure case, a cut part. An objection that does not survive its own scrutiny is dropped. The output of the pass is a *revised* design, not an appendix of complaints.
- **Default count, and composition.** Unset, plan uses its natural per-phase critics; `--deep` ([deep-mode](deep-mode.md)) raises the default panel; `--critics=<n>` sets the exact number and overrides the default.

## Grading objections

plan declares no severity scale of its own for critique findings — this is **open by design**: each critic reports on its own contract, stating the consequence and how load-bearing the gap is in plain terms (the "no scale declared" branch every praxis critic already carries), and the designer weighs each objection against plan's own bars — does it violate [justify-every-moving-part](../rules/justify-every-moving-part.md), open a one-way door ([design-for-reversibility](../rules/design-for-reversibility.md)), or leave the design not-closed ([slice-and-validate](../phases/06-slice-and-validate.md))? Manufacturing a numeric critique-severity scale here would be a fiat bar with no consumer; the design bars are the real filter.
