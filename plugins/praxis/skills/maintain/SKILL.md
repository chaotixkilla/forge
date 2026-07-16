---
name: maintain
description: Perform a scoped, reversible maintenance change to living code — a dependency upgrade, refactor, deprecation, tech-debt paydown, or security/compliance hardening — sized to its blast radius, verified and regression-guarded, and left as a clean reviewable diff; optionally gated on a security pass. Reach for it to change existing code safely — not to build new work (develop), root-cause a failure that already bit (debug), or judge a change someone else made (review).
metadata:
  flags:
    --scope=<pattern>: constrain every read, edit, and check to paths matching the glob, and surface needed changes outside it as follow-ups rather than making them silently
    --module=<name>: resolve a named subsystem to its boundary — paths, entrypoints, owners — and operate within it, using the ownership metadata to route review and any notification
    --changed: derive the working set from the current version-control changes, targeting the upkeep, verification, and review at exactly what moved
    --dry-run: plan the change and report it — the located target, its risk tier, the blast radius, and the intended edit — without mutating the working tree
    --checkpoint-commit: commit at safe, self-contained milestones so progress is recoverable and the change reads as a reviewable sequence
    --changelog: emit a user-facing changelog / release-note entry for the change, matching the project's existing format and categorization (activates changelog-entry)
    --require-clean: refuse to start unless the working tree is clean, keeping the maintenance diff attributable and unmixed with pre-existing work (activates require-clean)
    --security: layer a gating security/compliance pass over the change and gate completion on it rather than treating it as advisory (activates security-pass)
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

maintain owns no backend of its own. Reading the local working tree — its status (for `--require-clean`/`--changed`), the diff, and version-control history (for the intent check) — **and committing locally** (at landing / `--checkpoint-commit`) are **ambient**, done directly with plain git like any file read, needing no configured backend; the `vcs` skill is for version-control *host* operations (push, PR, status), not local reads or a local commit, and maintain never pushes. Every *external* touch is delegated wholesale to the skill that owns it: cross-lane prior-art and gotchas to the `gather` skill; check/build confirmation to the `ci` skill; the `--security` audit and the signals it needs to the `security-review`, `telemetry`, and `ci` skills; and any ticket or notification record to the `project-mgmt` and `communication` skills. Each of those skills owns its `tools.*` prerequisite, so maintain declares **no `config_requires`**.

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies, and phase 04 is gated by the security pass when `--security` is set.

1. Locate and reproduce: anchor the request to the living code that owns the behavior, and reproduce its current state before changing anything  — see [phases/01-locate-and-reproduce.md](phases/01-locate-and-reproduce.md)
2. Understand the blast radius: map what depends on the target — callers, contracts, data, downstream consumers — and grade the change's risk before editing  — see [phases/02-understand-blast-radius.md](phases/02-understand-blast-radius.md)
3. Make the change: apply the smallest correct, reversible edit that fits the surrounding code, staging a risky change behind a guard rather than a flag-day switch  — see [phases/03-make-the-change.md](phases/03-make-the-change.md)
4. Verify and guard: prove the change does what's intended and breaks nothing reachable, and capture the specific failure it fixes as a regression guard  — see [phases/04-verify-and-guard.md](phases/04-verify-and-guard.md)
5. Review and record: produce a clean, self-explaining, attributable diff and the record the project expects  — see [phases/05-review-and-record.md](phases/05-review-and-record.md)
