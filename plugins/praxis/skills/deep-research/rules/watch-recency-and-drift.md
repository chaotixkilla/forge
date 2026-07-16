# Watch recency and drift

A finding that was true when it was written may not be true now — a library changed its default, a standard was revised, a study was contradicted. The most-cited answer is often the oldest, and the field may have moved past it. But the inverse trap is just as real: newer is not truer, and a fresh weak source does not overturn an established body by virtue of being recent. This rule holds both against each other. Cited from [verify-claims](../phases/04-verify-claims.md) and [synthesize](../phases/05-synthesize.md).

1. **Date every finding against the subject's cadence, not the calendar.** A claim predating the subject's last breaking change (a new major version, a revised standard, a superseding ruling) is presumed stale until re-confirmed against the current state. Currency matters most where the subject moves fast and little where it is settled — a decades-old theorem does not go stale.
2. **Prefer the current state over the most-repeated stale answer.** When the live source of truth (the current spec, the shipping behavior) contradicts a widely-cited older claim, weight the current state and flag that the field moved — a popular answer can be a fossil everyone still copies.

## The recency-vs-authority fork

When the most *authoritative* source is stale and a newer, *weaker* source contradicts it, neither wins by fiat — the tension is real and is routed, not ranked:

- The newer source's contradiction is a **trigger to re-examine**, not an automatic reversal. Weigh the two by *method and corroboration*, not by date: does the newer source expose a genuine flaw in the older one, or reach comparable strength and independent corroboration ([weight-by-source-strength](weight-by-source-strength.md), [triangulate-before-trusting](triangulate-before-trusting.md))?
- **If yes** — a real flaw, or comparable-strength corroborated contradiction — the newer finding supersedes, and you say the field moved.
- **If no** — a lone weak contradiction of a strong established body — the established body stands, but the challenge is **surfaced, not buried** ([surface-disagreement](surface-disagreement.md)): report it as a contested edge ([claim-confidence-scale](claim-confidence-scale.md)), not a settled reversal.

(basis: the practitioner and clinical consensus that recency is a tie-breaker within comparable strength, never an override of an accumulated body — ~16% of highly-cited clinical findings were later contradicted, so a single new contrary study prompts investigation, not reversal, unless it exposes a real methodological flaw; GRADE weights a body of evidence over any single study, and Wikipedia's WP:RS cautions that breaking/recent reports often carry inaccuracies later corrected. The fork is non-gating — it routes the judgment to method-over-date, it does not pick a winner in advance.)
