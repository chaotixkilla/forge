# strict-gate (`--strict`)

Activated by `--strict`, referenced from [SKILL.md](../SKILL.md) (it raises the bar across the whole run) and enforced at [making-it-concrete](../phases/04-making-it-concrete.md) and [sequencing-and-sizing](../phases/05-sequencing-and-sizing.md).

Testability is not optional in spec — [testable-or-its-not-a-requirement](../rules/testable-or-its-not-a-requirement.md) runs on every requirement in the base flow, and an unverifiable requirement, an unresolved ambiguity, or an unconfirmed assumption is **surfaced as a warning** and delivered alongside the spec. The base flow warns and ships; the reader decides. This module changes the *consequence*, not the check: it turns every one of those warnings into a **hard block** — spec refuses to finish while any of them stands. Deletion test: remove this module and spec still produces its spec and still flags the same weaknesses as warnings; `--strict` only escalates warn → block, which is exactly why the escalation is a flag-gated module and the check underneath it is an always-on rule.

## The delta

- **Escalate, don't re-check.** The three conditions are already assessed in the base flow — this module does not introduce a new pass, it changes what happens when one fails. Under `--strict`, the run does not return while **any** of these holds:
  1. a requirement is not pass/fail verifiable to the bar in [testable-or-its-not-a-requirement](../rules/testable-or-its-not-a-requirement.md) (the skill's completion condition, sourced there);
  2. an ambiguity surfaced in [pin-down-ambiguity](../phases/02-pin-down-ambiguity.md) is unresolved — a vague adjective not yet quantified, an "it depends" not yet branched;
  3. an inferred assumption ([make-the-unsaid-explicit](../rules/make-the-unsaid-explicit.md)) is written but unconfirmed.
- **Block with the list, not a verdict.** A blocked `--strict` run returns *what is blocking it* — the specific requirements, ambiguities, and assumptions that failed, each anchored so the caller can close it — never a bare "spec incomplete." The block is actionable or it is noise.
- **Resolution, not deletion, clears the block.** A requirement made verifiable, an ambiguity quantified, an assumption confirmed clears its block; **dropping** a requirement to silence its warning does not — a requirement removed to pass the gate is recorded as out-of-scope with its reason ([make-the-unsaid-explicit](../rules/make-the-unsaid-explicit.md)), not quietly deleted. The gate exists to force resolution, and deleting-to-pass is the failure mode it must not reward.

## Composition

`--strict` composes with `--first-pass` by yielding to it: `--first-pass` returns a deliberately incomplete skeleton, so the strict block does not fire on that early return ([first-pass-draft](first-pass-draft.md) owns the skeleton's open-by-design gaps). The gate applies to the *finished* spec, not the skeleton. With `--from-issue`/`--from-discussion`, the escalation covers the seeded requirements exactly as it covers hand-entered ones — an inherited-but-untestable requirement blocks under `--strict` like any other.
