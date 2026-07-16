# from-spec (`--from-spec=<path>`)

Activated by `--from-spec=<path>`, referenced from [mapping-to-system](../phases/01-mapping-to-system.md) (the ingest point) and honored again at [slice-and-validate](../phases/06-slice-and-validate.md) (the trace-back check).

The base run designs against the settled requirements as understood in-session. This module locks a *written* spec at `<path>` as the authoritative input the design is held accountable to. Deletion test: remove it and plan still designs against in-session requirements; the flag only fixes *where* the requirements come from and raises the accountability bar.

## The delta

- **Treat the spec's requirements as fixed constraints, not open questions.** Phase 1 does not re-interrogate the *what* — it trusts the spec's requirements wholesale and re-derives only the *system mapping* (blast radius, constraints, the open "how" forks the spec deliberately left). This resolves the seam between `spec` and `plan`: with the flag present, the spec's intent is locked and plan designs the how; absent the flag, plan works from in-session requirements and still surfaces gaps but will not invent missing intent.
- **Trace each design decision back to a spec clause.** Every committed decision names the requirement it serves; a decision that traces to no clause is either scope creep (flag it) or a sign the spec is thin there (surface the gap — plan reveals missing intent, it does not fabricate it).
- **Close the loop at validation.** [slice-and-validate](../phases/06-slice-and-validate.md) confirms *every* spec requirement is addressed by some part of the design — an unaddressed requirement is an open the plan is not done with.

If the file at `<path>` is missing or unreadable, say so plainly and fall back to in-session requirements rather than designing against a spec you could not load.
