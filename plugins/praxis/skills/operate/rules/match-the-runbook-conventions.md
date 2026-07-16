# Match the runbook conventions

operate ships house defaults — a 3-level severity ladder, a cadence matrix, a resolution bar — but a project that already runs incidents has its *own* conventions: a severity vocabulary (P1–P5, SEV0–4), an escalation path, a runbook doc structure, an on-call rotation. Imposing the house default over an established local convention creates two vocabularies for one thing and breaks every cross-reference to the team's existing incidents. So where the surrounding context has a convention, it wins. This rule is the routing rule the graded standards defer to — [severity-scale](severity-scale.md) and [right-sized-status-updates](right-sized-status-updates.md) both point here — and it governs [assess-and-triage](../phases/01-assess-and-triage.md) (severity vocabulary), [remediate-and-verify](../phases/04-remediate-and-verify.md) (the fix-forward/escalation convention and the resolution-bar fork), and [learn-and-harden](../phases/06-learn-and-harden.md) (doc/follow-up structure).

## The precedence

Resolve any operational-convention standard in this order:

1. **The surrounding runbook's convention**, when one exists — its severity vocabulary and boundaries, its escalation path, its retrospective template, its incident-doc structure. Adopt it as-is.
2. **operate's house default**, when no runbook convention covers the point (the 3-level ladder, the cadence matrix).
3. **The maintainer**, when neither settles it and the call is genuinely house-specific.

## The discriminators

- **Adopt the runbook's vocabulary even when it differs from the default.** A project on P1–P5 stays on P1–P5 — do not re-map its incidents onto SEV1–3; the mapping itself is a source of error and it orphans references to past incidents. The house ladder's *discriminators* (functional impact, blast radius, user impact) still do the placing; only the labels and boundaries follow the runbook.
- **Follow the runbook's doc structure and escalation, not an invented one.** A retrospective goes into the team's existing template and escalation follows their defined path; operate contributes the content, not a new format.
- **Detect the convention before assuming its absence — on surfaces you can actually reach.** Search the **repository** for a runbook, incident template, or severity definition before falling back to the house default — an existing convention you didn't look for is the same error as no convention at all. If incident tooling that might define a convention is not reachable from the run, default to the house ladder and **note the assumption** so it can be corrected — an unreachable tool is not evidence that no convention exists.

`(basis: the kit's fork-don't-side routing discipline — where authorities conflict, the established convention of the surrounding context outranks a private house ladder; this is the operational application of that rule, and the reason the severity and cadence standards are house *defaults* rather than mandates.)`
