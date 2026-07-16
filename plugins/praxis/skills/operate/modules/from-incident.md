# from-incident (`--from-incident`)

Activated by `--from-incident=<ref>`, referenced from [assess-and-triage](../phases/01-assess-and-triage.md) (the intake site).

Base behavior: triage starts from a firing telemetry signal or a user report. This module seeds it instead from an existing incident record. Deletion test: remove it and triage still runs from the signal/report; seeding from a record is optional intake a flag turns on — so it is a module.

## The delta — hydrate triage from the record

Read the incident record by reference through the [project-mgmt](../../project-mgmt/SKILL.md) or [communication](../../communication/SKILL.md) port (whichever holds it) and pull its reported symptom, severity, timeline, and prior actions, so triage starts from known context rather than cold. Fold this into [assess-and-triage](../phases/01-assess-and-triage.md):

- Treat the record as a **claim to reconcile**, not ground truth: reconcile its reported blast radius and symptom against what the live signal actually shows — the gap between reported and observed is itself evidence.
- A severity already on the record is a **starting point**, re-assessed against [severity-scale](../rules/severity-scale.md), not adopted unquestioned.
- Prior actions on the record (a mitigation already tried) carry into [stabilize-first](../phases/02-stabilize-first.md) so you don't repeat or undo them blindly.

## Prerequisite and degrade

The read goes through the project-mgmt / communication port (each owns its own prerequisite — doer-owns-prerequisites; operate declares none). If the backend is unavailable, the record can't be pulled: degrade to triaging from the live signal or the user's report, noting the seed was unavailable. A missing record backend narrows the *starting context*; it does not stop the response.
