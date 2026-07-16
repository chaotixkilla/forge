# seed-prior-art (`--prior-art=<ref>`)

Activated by `--prior-art=<ref>`, referenced from [choosing-approach](../phases/02-choosing-approach.md) (it seeds the approach search).

The base run enumerates candidate approaches from the constraints. This module anchors that search on an existing design, system, or pattern at `<ref>` — something already proven — before inventing alternatives from scratch. Deletion test: remove it and plan still enumerates approaches; the flag only grounds the starting point.

## The delta

- **Mine `<ref>` for reusable shape.** Read the referenced design and extract the structure worth carrying over — the boundaries it draws, the sequencing it uses, the failure handling it already solved. It enters [choosing-approach](../phases/02-choosing-approach.md) as a first-class candidate, scored on the same axes as the others, not privileged for being the seed.
- **Name the divergences deliberately.** Where this design departs from `<ref>`, say *where* and *why* — a divergence is a decision, and it is recorded like a rejected alternative in reverse ([record-rejected-alternatives](../rules/record-rejected-alternatives.md)): "we followed `<ref>` except here, because …". Silent divergence from the model you cited is the failure mode.
- **Adopt only what earns its place.** A shape reused from `<ref>` still passes [justify-every-moving-part](../rules/justify-every-moving-part.md); prior art is a source of proven options, not a license to import machinery this problem does not need.

`<ref>` may be an internal system (recruit the `code`/`repository` lanes via `gather` to read it) or an external design (the `community`/`official-documentation` lanes); either way it feeds the candidate set, it does not replace the scoring.
