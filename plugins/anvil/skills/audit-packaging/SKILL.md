---
name: audit-packaging
description: Audit the ships-vs-authoring boundary across the whole marketplace — published plugins ship only consumer-facing files, authoring-only material stays out, and any plugin marked unpublished stays absent from the catalog.
allowed-tools: Read, Glob, Grep
metadata:
  flags:
    --report=<fmt>: inline (default) or artifact
    --fix: propose corrections (relocate a misplaced file, flag a catalog entry) rather than only reporting
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies.

1. Read the catalog: read marketplace.json — which plugins are published, and from which source paths  — see [phases/01-read-catalog.md](phases/01-read-catalog.md)
2. Classify files: walk each plugin and the repo, classifying every file as ships (consumer-facing) or authoring-only  — see [phases/02-classify-files.md](phases/02-classify-files.md)
3. Check the boundary: flag authoring-only files inside a shipping plugin; confirm the design/notes plane stays out and every unpublished plugin is absent from the catalog — recruit the boundary-keeper critic  — see [phases/03-check-boundary.md](phases/03-check-boundary.md)
4. Report: boundary findings inline or as an artifact; with --fix, propose relocations  — see [phases/04-report.md](phases/04-report.md)
