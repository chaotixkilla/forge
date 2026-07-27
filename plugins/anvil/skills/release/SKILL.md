---
name: release
description: Release a target plugin to the marketplace — preflight audits, version bump, catalog entry, and release notes. Gated so unpublished plugins can't be shipped.
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
metadata:
  flags:
    --plugin=<name>: target plugin to publish or update in the catalog
    --bump=<level>: version bump — major | minor | patch
    --report=<fmt>: how release notes come back — inline (default) or artifact
    --dry-run: show the bump, catalog entry, and notes without writing or tagging
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies.

1. Preflight gate: require --plugin; run audit-packaging + audit-contract + audit-tool-leaks as the blocking gate, plus audit-context as advisory; refuse to release a plugin that fails a blocking audit, or one marked unpublished  — see [phases/01-preflight-gate.md](phases/01-preflight-gate.md)
2. Bump the version: apply the --bump semver step to the plugin's plugin.json  — see [phases/02-bump-version.md](phases/02-bump-version.md)
3. Update the catalog: add or update the plugin's entry in marketplace.json (name, source, description)  — see [phases/03-update-catalog.md](phases/03-update-catalog.md)
4. Notes and tag: produce release notes, then commit + tag the release in the repo  — see [phases/04-notes-and-tag.md](phases/04-notes-and-tag.md)
