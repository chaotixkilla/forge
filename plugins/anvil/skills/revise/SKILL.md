---
name: revise
description: Apply a batch of findings or maintainer feedback to an existing plugin as the smallest, verified set of changes — triage and size each item, then dispatch it to the engine that owns its fix (codify, add-component) or wire it directly. The repair counterpart to dogfood's diagnosis.
allowed-tools: Read, Glob, Grep, Write, Edit
metadata:
  flags:
    --plugin=<name>: target plugin whose findings/feedback batch is being applied (required — stop and ask if absent)
    --from=<ref>: seed the batch from a findings/feedback source (a dogfood report, review report, or notes file) instead of interrogating live
    --dry-run: triage and size the batch and show the change set that would apply, writing nothing and invoking no mutating engine
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies.

1. Intake: normalize a heterogeneous batch (dogfood findings, maintainer change-requests, freeform feedback) into one actionable shape  — see [phases/01-intake.md](phases/01-intake.md)
2. Triage and dedup: cluster survivors by root cause, assign each a disposition (act / hold / defer / won't-do / drop)  — see [phases/02-triage-and-dedup.md](phases/02-triage-and-dedup.md)
3. Size the intervention: for each item to act on, assign the lowest intervention tier that resolves it  — see [phases/03-size-intervention.md](phases/03-size-intervention.md)
4. Dispatch: route each sized item to the engine that owns its fix, or make the one wiring edit directly  — see [phases/04-dispatch.md](phases/04-dispatch.md)
5. Verify and report: recruit the concern-matched critics + audits on the diff, loop until clean, then report the whole change set  — see [phases/05-verify-and-report.md](phases/05-verify-and-report.md)
