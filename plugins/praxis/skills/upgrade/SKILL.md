---
name: upgrade
description: Move a dependency to a new version — read its changelogs and migration guides for the version span, capture the current green state, grade the upgrade's reach, bump it to the posture the project keeps, fix what breaks at its cause, and prove the checks green again. Returns the committed upgrade and its outcome; delivering it is the caller's job.
metadata:
  flags:
    --scope=<pattern>: constrain every read, edit and check to paths matching the glob, and surface needed changes outside it as follow-ups rather than making them silently
    --module=<name>: resolve a named subsystem to its boundary — paths, entrypoints, owners — and work within it, returning its owners with the change
    --changed: derive the working set from the current version-control changes, targeting the upgrade and its verification at exactly what moved
    --checkpoint-commit: commit at safe, self-contained milestones — at least one per major taken in sequence — so progress is recoverable
    --require-clean: refuse to start unless the working tree is clean, keeping the diff attributable and unmixed with pre-existing work (activates require-clean)
    --changelog: add a user-facing changelog entry for the upgrade, matching the project's existing format (activates changelog-entry)
    --dry-run: plan the upgrade and report it — the versions, consumers, upgrade path, baseline, risk tier and intended bump — without mutating the working tree
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

upgrade owns no backend of its own. Reading the working tree and committing locally are ambient; the publisher's changelogs and migration guides come through the [gather](../gather/SKILL.md) skill, and the hosted pipeline through the [ci](../ci/SKILL.md) skill, each the doer that owns its prerequisite.

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the craft where it applies.

1. Read the upgrade path: locate the dependency, its versions and who uses it, read what its publisher says changes across the span, and capture the green baseline  — see [phases/01-read-the-upgrade-path.md](phases/01-read-the-upgrade-path.md)
2. Grade the upgrade: map what the bump actually moves — call sites, co-importers, contracts — and grade its risk before bumping  — see [phases/02-grade-the-upgrade.md](phases/02-grade-the-upgrade.md)
3. Bump and fix: bump to the project's posture and fix each break at its cause, in the shape the risk tier allows  — see [phases/03-bump-and-fix.md](phases/03-bump-and-fix.md)
4. Prove it green: show the baseline checks green again and every behavior change accounted for, and reach the verdict  — see [phases/04-prove-it-green.md](phases/04-prove-it-green.md)
5. Commit and hand off: commit the upgrade attributably, surface the follow-ups, and return the outcome  — see [phases/05-commit-and-hand-off.md](phases/05-commit-and-hand-off.md)
