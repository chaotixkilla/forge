---
name: audit-contract
description: Check a target plugin's internal contract — frontmatter shape, slot placement, flag and config wiring, adapter coverage.
allowed-tools: Read, Glob, Grep
metadata:
  flags:
    --plugin=<name>: target plugin to audit
    --skill=<name>: scope the audit to one skill within the plugin (siblings and config still read as join context, not judged); default audits every skill
    --checks=<list>: subset to run — frontmatter, flags-to-modules, config-keys, adapter-coverage, load-wiring, skip-resistance, usage-doc, slot-placement, standard-closure
    --report=<fmt>: inline (default) or artifact
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies.

1. Inventory: require --plugin; build the plugin's component map — skills, slots, flags, config keys, agents, adapters (or one skill's, under --skill) — and note its config posture  — see [phases/01-inventory.md](phases/01-inventory.md)
2. Check frontmatter: each SKILL.md has name + description as recognized fields, with flags (and, for config-bearing plugins, config_requires) under metadata, read as capabilities  — see [phases/02-check-frontmatter.md](phases/02-check-frontmatter.md)
3. Cross-reference: flags↔modules, config_requires↔config keys, adapters↔config providers, load wiring (every citation a resolvable link), spine/delegation load-bearing, the usage.md pointer, body files↔right slot, standard-points closed — recruit the contract-skeptic and standards-skeptic critics  — see [phases/03-cross-reference.md](phases/03-cross-reference.md)
4. Report: return conformance findings with severity, inline or as an artifact  — see [phases/04-report.md](phases/04-report.md)
