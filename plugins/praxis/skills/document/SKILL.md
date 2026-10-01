---
name: document
description: File a task's documentation — each result it's handed, as the document type it belongs to — the task record, a work record such as the spec, the plan or a review record, a decision record, or system documentation of the part the task touched — plus the task log — on the configured artifacts backend. Called by the work orchestrator as an act runs; for a message or update pitched to people, use communicate.
metadata:
  flags:
    --task=<key>: the task whose documentation receives the result (a phase input, not a behavior module)
    --dry-run: show each document and where it would land, without writing — carried into the publish step's own preview (a phase input, not a behavior module)
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies. document owns no backend of its own: it publishes through [artifacts](../artifacts/SKILL.md), the doer that owns the artifacts prerequisite, so it declares no `config_requires`.

1. Find the task's documentation: locate it on the backend, or start it with the task record  — see [phases/01-find-the-task-documentation.md](phases/01-find-the-task-documentation.md)
2. Shape the document: decide which type the result is, and shape it to that type  — see [phases/02-shape-the-document.md](phases/02-shape-the-document.md)
3. Publish and link: publish it, and bring the task record up to date  — see [phases/03-publish-and-link.md](phases/03-publish-and-link.md)
4. Mirror the task log: bring the task's line in the log up to date, when the log is on  — see [phases/04-mirror-the-task-log.md](phases/04-mirror-the-task-log.md)
