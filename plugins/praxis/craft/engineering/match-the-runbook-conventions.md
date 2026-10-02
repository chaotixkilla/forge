# Match the runbook conventions

praxis ships house defaults for incident response — a 3-level severity ladder, a cadence matrix, a resolution bar — but a project that already runs incidents has its *own* conventions: a severity vocabulary (P1–P5, SEV0–4), an escalation path, a runbook doc structure, an on-call rotation. Imposing the house default over an established local convention creates two vocabularies for one thing and breaks every cross-reference to the team's existing incidents. It is the routing rule every graded incident standard defers to: the severity vocabulary, the status cadence, escalation and the resolution bar, and the retrospective's structure.

## The precedence

Resolve any operational-convention standard in this order:

1. **The surrounding runbook's convention**, when one exists — its severity vocabulary and boundaries, its escalation path, its retrospective template, its incident-doc structure. Adopt it as-is.
2. **praxis's house default**, when no runbook convention covers the point (the 3-level ladder, the cadence matrix).
3. **The maintainer**, when neither settles it and the call is genuinely house-specific.

## The discriminators

- **Adopt the runbook's vocabulary even when it differs from the default.** A project on P1–P5 stays on P1–P5 — do not re-map its incidents onto SEV1–3; the mapping itself is a source of error and it orphans references to past incidents. The house ladder's *discriminators* (functional impact, blast radius, user impact) still do the placing; only the labels and boundaries follow the runbook.
- **Follow the runbook's doc structure and escalation, not an invented one.** A retrospective goes into the team's existing template and escalation follows their defined path; the response contributes the content, not a new format.
- **Detect the convention before assuming its absence — on surfaces you can actually reach.** Search the **repository** for a runbook, incident template, or severity definition before falling back to the house default — an existing convention you didn't look for is the same error as no convention at all. If incident tooling that might define a convention is not reachable from the run, default to the house ladder and **note the assumption** so it can be corrected — an unreachable tool is not evidence that no convention exists.

`(basis: derived from the kit's fork-don't-side routing discipline)`
