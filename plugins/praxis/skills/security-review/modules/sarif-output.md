# sarif-output (`--sarif=<path>`)

Activated by `--sarif=`, referenced from [reporting-findings](../phases/05-reporting-findings.md).

The base audit produces a human report. This module additionally writes the findings in **SARIF** — the OASIS Static Analysis Results Interchange Format, a vendor-neutral standard so downstream tools can ingest the findings. Deletion test: remove it and the human report is unchanged; the delta is the extra machine-readable document. It is a local file write at the given path — no external capability, exactly as the human report is a local return.

## The delta

- **Write the ranked findings** to the path as a SARIF document: each finding a `result` carrying its rule id (the attack-class taxonomy id — the OWASP category or CWE from [hunting-vulnerabilities](../phases/03-hunting-vulnerabilities.md)), its location (`file:line`), a message stating the adversary path and impact, and the traced path. The human report is **always** produced as the record; `--sarif` adds the document, it does not replace it.
- **Carry severity on both channels the format offers**, because SARIF's own severity signal and its coarse level enum are different things:
  - A **representative numeric score** in the result's (or its rule's) property bag — the primary severity channel, in the 0.0–10.0 range consuming tools read to rank findings. This skill assigns a severity *band*, not a computed vector ([severity-scale](../rules/severity-scale.md)), so the band does not carry a single canonical number; emit the **band's floor** as the score — `critical → 9.0`, `high → 7.0`, `medium → 4.0`, `low → 0.1` — deterministically, and do **not** compute a CVSS vector to obtain a finer number. The floor is a lossless stand-in for the band: every consumer maps it back to the same band it came from.
  - The result **`level`**, whose allowed values are the format's closed enum `error` / `warning` / `note` / `none`.

## The severity → level mapping

SARIF's `level` enum does not line up one-to-one with the four severity bands, and **no authority pins the mapping** (the OASIS spec defines the enum but not how a producer's severity maps onto it). So the numeric score above is the real severity channel; `level` is a coarse secondary signal, mapped by house convention:

`(basis: house convention, ratified by the maintainer 2026-07-10 — critical and high → error, medium → warning, low → note; hardening notes, if emitted at all, → none. No external standard defines the severity→level direction (OASIS defines the level enum; the numeric-score property is the conventional severity carrier), so this coarse mapping is a house choice and the band-floor numeric score remains the primary signal. Consistent with common producer practice of surfacing high-severity results as errors.)`

Emit the band's floor as the score for every finding; a consumer that ignores the property bag still gets a sensible `level`, and one that reads the score maps it back to the finding's band unambiguously.
