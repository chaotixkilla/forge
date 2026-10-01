---
name: refactor
description: Restructure existing code with its behavior unchanged — locate the code and capture how it behaves now, map its blast radius and grade the change, make the smallest reversible edit, prove the behavior unchanged against the baseline, and commit an attributable diff. Covers refactors, cleanups and retiring a switch; returns the outcome, and delivering the change is the caller's job.
metadata:
  flags:
    --scope=<pattern>: constrain every read, edit and check to paths matching the glob, and surface needed changes outside it as follow-ups rather than making them silently
    --module=<name>: resolve a named subsystem to its boundary — paths, entrypoints, owners — and work within it, returning its owners with the change
    --changed: derive the working set from the current version-control changes, targeting the change and its verification at exactly what moved
    --checkpoint-commit: commit at safe, self-contained milestones so progress is recoverable and the change reads as a reviewable sequence
    --require-clean: refuse to start unless the working tree is clean, keeping the diff attributable and unmixed with pre-existing work (activates require-clean)
    --dry-run: plan the change and report it — the located target, its baseline, its risk tier, the blast radius and the intended edit — without mutating the working tree
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

refactor owns no backend of its own. Reading the local working tree — its status, the diff and version-control history — and committing locally are ambient; the hosted pipeline goes through the [ci](../ci/SKILL.md) skill, the doer that owns its prerequisite.

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the craft where it applies.

1. Locate and baseline: anchor the request to the code that owns the behavior, bind the working set, and capture how it behaves now  — see [phases/01-locate-and-baseline.md](phases/01-locate-and-baseline.md)
2. Map the blast radius: trace what depends on the target — callers, contracts, data, downstream consumers — and grade the change's risk before editing  — see [phases/02-map-the-blast-radius.md](phases/02-map-the-blast-radius.md)
3. Make the change: apply the smallest correct, reversible edit the risk tier allows, staging a risky change behind a guard or a migration path rather than a flag-day switch  — see [phases/03-make-the-change.md](phases/03-make-the-change.md)
4. Prove it unchanged: show the baseline still holds and the checks in scope pass, and reach the verdict  — see [phases/04-prove-it-unchanged.md](phases/04-prove-it-unchanged.md)
5. Commit and hand off: make the diff self-explaining, commit it attributably, surface the follow-ups, and return the outcome  — see [phases/05-commit-and-hand-off.md](phases/05-commit-and-hand-off.md)
