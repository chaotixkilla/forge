# sarif-output (`--sarif=<path>`)

Activated by `--sarif=`, referenced from [reporting-findings](../phases/05-reporting-findings.md).

The base audit produces a human report. This module additionally writes the findings in **SARIF** — the OASIS Static Analysis Results Interchange Format, a vendor-neutral standard so downstream tools can ingest the findings. Deletion test: remove it and the human report is unchanged; the delta is the extra machine-readable document. It is a local file write at the given path — no external capability, exactly as the human report is a local return.

## The delta

- **Write the ranked findings** to the path as a SARIF document: each finding a `result` carrying its rule id (the attack-class taxonomy id — the OWASP category or CWE from [attack-class-taxonomy](../rules/attack-class-taxonomy.md)), its location (`file:line`), a message stating the adversary path and impact, the traced path, and its certainty (traced / inferred / unverified, per [results-and-certainty](../../../craft/evidence/results-and-certainty.md)) in the result's property bag under `certainty`, so a consumer can tell an asserted finding from an unverified one. The human report is **always** produced as the record; `--sarif` adds the document, it does not replace it.
- **Carry severity on both channels the format offers**, because a numeric score in the property bag and the format's coarse level enum are different things:
  - A **representative numeric score** in the result's (or its rule's) property bag — under the key the downstream consumer the caller names reads; with no consumer named, the score is omitted and `level` carries severity alone, since a guessed key is read by nothing — a producer extension the format allows, not part of its own vocabulary — in the 0.0–10.0 range consumers commonly rank on. This skill assigns a severity *band*, not a computed vector ([severity-scale](../rules/severity-scale.md)), so the band does not carry a single canonical number; emit the **band's floor** as the score — `critical → 9.0`, `high → 7.0`, `medium → 4.0`, `low → 0.1` — deterministically `(basis: derived — the band's floor is the one score every finding in the band meets)`, and do **not** compute a CVSS vector to obtain a finer number. The floor is a lossless stand-in for the band: every consumer maps it back to the same band it came from.
  - The result **`level`**, whose allowed values are the format's closed enum `error` / `warning` / `note` / `none`.

## The severity → level mapping

SARIF's `level` enum does not line up one-to-one with the four severity bands, and **no authority pins the mapping** (the OASIS spec defines the enum but not how a producer's severity maps onto it). So the numeric score above is the real severity channel; `level` is a coarse secondary signal, mapped by house convention:

- **critical** and **high** → `error`
- **medium** → `warning`
- **low** → `note`
- hardening notes → `none`, with no numeric score, since the report leaves them unscored; they are emitted, so the document carries the same set the report does

`(basis: maintainer, 2026-07-10)`

A consumer that ignores the property bag still gets a sensible `level`.
