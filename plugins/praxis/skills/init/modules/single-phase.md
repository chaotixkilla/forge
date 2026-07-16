# single-phase (`--phase=<name|n>`, and `init:<cap>`)

Activated by `--phase=<name|n>`, referenced from [write-and-validate](../phases/04-write-and-validate.md) and the SKILL.md body. This is also the module every sibling skill's `guide via init:<cap>` resolves to.

The base run configures the whole file from scratch. This module runs *one section* against an *existing* config instead — to fix or add a single slot without re-walking the other six and the roster. Deletion test: remove it and init still does a full run; the targeted, non-destructive re-resolution is the added behavior.

## The delta

- **The target is one *resolving* section.** A scoped run always targets a section that resolves values — never detection or validation alone, which are steps every scoped run already runs around its target. `--phase` accepts one of three target forms:
  - a **capability-slot name** — one of the seven `tools.<cap>` keys, spelled exactly as the template spells them: `vcs`, `ci`, `knowledge`, `artifacts`, `project_mgmt`, `communication`, `telemetry` (the underscore token, not the readable "project-management" prose form) — scoping the run to that single slot;
  - a **phase name** — `tools` (the resolve-tools phase) or `team` (the resolve-team phase) — scoping to that whole phase;
  - an **ordinal** — the phase's position in the SKILL.md run order (`1` detect-environment, `2` resolve-tools, `3` resolve-team, `4` write-and-validate). Only the two *resolving* phases are standalone targets: `2` (`tools`) and `3` (`team`). `--phase=1` and `--phase=4` are **not** standalone — detection only stages for a resolving section and validation runs as part of every scoped write, so neither resolves anything on its own; reject them with a pointer to the valid targets rather than running an empty section.
- **`init:<cap>` ≡ `--phase=<cap>`.** The entry point sibling skills invoke — `init:vcs`, `init:knowledge`, `init:artifacts`, `init:project_mgmt`, `init:communication`, and the same for `ci`/`telemetry` — resolves to running this module scoped to that one capability slot. `(basis: derived from the ratified template keys — the entry-point vocabulary is pinned to one set of names: the seven capability-slot targets are the seven tools.<cap> template keys verbatim (vcs, ci, knowledge, artifacts, project_mgmt, communication, telemetry), which are also the seven init:<cap> tokens, so every guide via init:<cap> has exactly one runnable target and no capability is stranded by a spelling mismatch.)`
- **Detection and resolution narrow to the target.** [detect-environment](../phases/01-detect-environment.md) reads only the target slot's signals; [resolve-tools](../phases/02-resolve-tools.md) (or [resolve-team](../phases/03-resolve-team.md)) resolves only that section.

## Read-modify-write — never clobber the siblings

The base write emits the template shape filled by the run. A scoped run must not do that: it would overwrite the six untargeted slots with empty template placeholders and re-stamp the version. Instead:

1. **Load the existing `praxis.json` as the base** — not the template. If no config exists yet, a scoped run has nothing to patch: report that and direct the user to a full `init` first.
2. **Resolve only the targeted section** against that base (existing values are the current state to confirm or replace).
3. **Write back the merge** — the resolved section over the existing file, with every other slot and the `version` untouched.

`(basis: derived — a targeted edit that starts from the template rather than the existing file is silent data loss; the read-modify-write base is what makes --phase safe to re-run, resolving the seed's read-modify-write question in favor of an explicit merge distinct from the initial write.)`

The validation in [write-and-validate](../phases/04-write-and-validate.md) runs on the merged result, so a scoped run still leaves a valid file.
