# standard-mapping (`--standard=<framework>`)

Activated by `--standard=`, referenced from [hunting-vulnerabilities](../phases/03-hunting-vulnerabilities.md) (map each finding onto the framework's controls as it is found) and [reporting-findings](../phases/05-reporting-findings.md) (the coverage section).

The base audit hunts and reports findings against its default taxonomy. This module maps the audit onto a **named** standard/compliance framework's control taxonomy and reports coverage against it. Deletion test: remove it and the audit still hunts and reports; the delta is the framework mapping *and* the coverage report — the added behavior a compliance context needs.

## The delta

- **Select the taxonomy** the framework names — the fork in [attack-class-taxonomy](../rules/attack-class-taxonomy.md) (OWASP Top 10 / CWE / ASVS) — and tag each finding with its control id in that framework as it is found. A finding maps to a control by *what weakness it is*, not by name-matching: an authorization gap maps to the framework's access-control control, an injection to its injection control.
- **Report coverage** in the report's coverage section ([reporting-findings](../phases/05-reporting-findings.md)): one result per framework control, on the results scale in [results-and-certainty](../../../craft/evidence/results-and-certainty.md), with the findings that map to it listed. Ask in order: no surface element exercised the control → **not checked**, saying so; a traced finding maps to it → **fails**; an inferred finding maps to it → **unsettled**; a threat on the surface touched it and nothing above maps to it → **holds**, an unverified finding listed without moving the result. The first line matters most — an unexamined control is a coverage gap, never a holds. `(basis: derived from the standard's placement questions and the gate's traced bar)`

## Reproduce the framework's own vocabulary

A finding's control id is **relayed verbatim from the named framework**, not normalized into this skill's own terms: report the framework's actual control identifier (an OWASP category label, a CWE id, an ASVS requirement number), because a coverage report a compliance reader trusts must speak the framework's vocabulary, not a paraphrase. When a finding maps to more than one control, list each; when a finding maps to none the framework defines, say so rather than forcing a nearest-fit. `(basis: derived from a coverage report's job: legibility against the named framework)`
