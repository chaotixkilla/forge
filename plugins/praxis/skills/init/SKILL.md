---
name: init
description: Detect and fill the per-project praxis config — the tools map, team roster, and report-style settings — proposing every inference for confirmation and asking only where the environment is silent.
metadata:
  flags:
    --phase=<name|n>: run one section of setup in isolation — a capability-slot key, a phase name (`tools`/`team`), or an ordinal; this is the target `init:<cap>` resolves to (see modules/single-phase.md)
    --guide: walk the user through configuring, explaining options and re-confirming even inferred values
    --degrade: fill only what is inferable and disable the rest, running with no user prompts
    --dry-run: show the config that would be written, without writing it
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

init fills the shipped `config.template.json` (at `${CLAUDE_PLUGIN_ROOT}/config.template.json`) — read it first; it is the canonical shape, slot set, and version init fills (never invent keys). init declares **no `config_requires`** of its own: it is the bootstrap that *creates* the config every other skill's gate reads.

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies. A scoped run (`--phase`/`init:<cap>`) runs one section against the existing file — see [single-phase](modules/single-phase.md).

1. Detect the environment: read the cheap signals once, grade each, and stage proposals — commit nothing yet  — see [phases/01-detect-environment.md](phases/01-detect-environment.md)
2. Resolve the tools: walk the seven capability slots — provider, transport, per-category fields, secret reference — proposing inferences and asking gaps  — see [phases/02-resolve-tools.md](phases/02-resolve-tools.md)
3. Resolve the team: fill `me`, the `team[]` roster, and `teams`, asking for ownership and reviewer status the environment can't know  — see [phases/03-resolve-team.md](phases/03-resolve-team.md)
4. Write and validate: emit the config preserving shape + version (a scoped run merges, and the `output` style section is carried not resolved), then check every slot is resolved and no placeholder remains  — see [phases/04-write-and-validate.md](phases/04-write-and-validate.md)
