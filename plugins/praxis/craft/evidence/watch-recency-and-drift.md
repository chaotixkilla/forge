# Watch recency and drift

A finding that was true when it was written may not be true now — a library changed its default, a standard was revised, a study was contradicted. The most-cited answer is often the oldest, and the field may have moved past it. But the inverse trap is just as real: newer is not truer, and a fresh weak source doesn't overturn an established body by virtue of being recent.

1. **Date every finding against the subject's change cadence, not the calendar.** A claim predating the subject's last breaking change (a new major version, a revised standard, a superseding ruling) is presumed stale until re-confirmed against the current state. Currency matters most where the subject moves fast and little where it's settled — a decades-old theorem doesn't go stale.
2. **Prefer the current state over the most-repeated stale answer.** When the live source of truth (the current spec, the shipping behavior) contradicts a widely-cited older claim, weight the current state and flag that the field moved.

## The recency-vs-authority fork

When the most *authoritative* source is stale and a newer, *weaker* source contradicts it, neither wins by fiat — the tension is real and is routed, not ranked:

- The newer source's contradiction is a **trigger to re-examine**, not an automatic reversal. Weigh the two by *method and corroboration*, not by date: does the newer source expose a genuine flaw in the older one, or reach comparable strength with independent corroboration?
- **If yes** — a real flaw, or a corroborated contradiction of comparable strength — the newer finding supersedes, and you say the field moved.
- **If no** — a lone weak contradiction of a strong established body — the established body stands, and the claim doesn't grade **contested** ([results-and-certainty](results-and-certainty.md)), since the clearly stronger side carries the conflict. But the challenge is **surfaced, not buried**: report it alongside the claim as a challenge that didn't overturn it, not as a settled reversal.

(basis: practitioner and clinical consensus; GRADE; WP:RS)
