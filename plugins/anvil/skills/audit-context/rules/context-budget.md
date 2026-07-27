# The context budgets

Every check in this audit compares a measurement against a number, and a number with no owner is exactly the open standard the kit's other audits exist to catch. This rule is where those numbers live, what each one means, and — honestly — how firmly each is settled.

**Status: PROPOSED, pending maintainer ratification.** `(basis: context-engineering alignment pass, 2026-07-26 — derived from the observed distribution across the marketplace's two published plugins at the time this audit was built, chosen so that the sites a hand audit had already identified as defects fall outside the budget and the sites it had cleared fall inside. That is calibration against one corpus at one moment, not an external standard: no published authority sets a context budget for a skill, and the honest basis for these particular numbers is "they separate the known-bad from the known-good here." They are deliberately overridable per run via --budget so a plugin with a different shape is not forced to argue with a threshold that was never about it. Until a maintainer ratifies them, a breach is a prompt to read, never a verdict to report as settled.)`

## The four budgets

- **`amplification` — 12× (a ratio).** For one file: the token weight its own direct citations reach, over its own weight. Direct, not transitive: rules in this kit cross-link densely, so a transitive figure makes every file in a well-connected skill look like a hotspot and buries the one you want.
- **`citations` — 12 (a count).** Direct citations from one file.
- **`resident` — 3,500 tokens (a total, per plugin).** The `name` + `description` of every skill and every agent. This is the only layer with no opt-out, paid on every request whether anything is invoked or not.
- **`closure` — 25,000 tokens (a total, per skill).** What a no-flag run can reach: spine + usage + every phase + everything those phases transitively reach, stopping at each context boundary. Modules are excluded — they are flag-gated, so they cost nothing by default.

## Amplification and citations fire only together

This is the load-bearing part of the rule, and getting it wrong is what makes this kind of check untrustworthy. Neither number is a defect signal alone:

- **Ratio alone** convicts a short module that cites five heavy rules. That is ordinary and correct — a 500-token module leaning on 6,000 tokens of craft has done nothing wrong.
- **Count alone** convicts a `SKILL.md` spine, whose entire job is to cite every phase, and which the contract audit *requires* to do so.

What identifies a roster is the conjunction: **many citations, carrying many times this file's own weight, from one place.** So a breach requires both budgets to be exceeded, and `SKILL.md` is exempt from the pair entirely — measured and reported, never flagged, because a spine is an index by design. A plugin whose only high-fan-out files are spines has no finding here.

## A breach is a reading prompt, not a finding

The three file-level budgets locate; they do not judge. A high-fan-out site can be a deliberate routing index, which is correct and desirable, or a bare roster, which is the defect — and the difference is whether each link carries a firing condition, which no measurement can see. So a breach obliges the read in [read-the-hotspots](../phases/02-read-the-hotspots.md) and becomes a finding only if that read confirms it. Reporting a breach as a finding without the read is this audit's characteristic failure mode: it produces a long, confident list that a maintainer correctly learns to ignore.

The `closure` budget is softer still, and should be read as a *shape* signal rather than a defect. A large skill can legitimately reach a lot; what the number is really asking is whether the reach is *conditional*. A 40,000-token ceiling behind well-triggered citations is a deep library that costs little per run; the same ceiling behind a roster is 40,000 tokens the executor cannot triage. Report the ceiling with the fan-out read that explains it, never on its own.

## When to override rather than fix

`--budget=<k=v,…>` exists because a threshold calibrated on one corpus will be wrong for a plugin shaped differently, and arguing with a number is a waste of a run. Override, and record why, when the plugin's shape genuinely differs — a kit whose skills are all thin ports has no business being measured against a budget calibrated on deep procedural skills. Do *not* override to silence a site you have read and judged a roster; that is the finding, and moving the line to cover it is how a check stops meaning anything.
