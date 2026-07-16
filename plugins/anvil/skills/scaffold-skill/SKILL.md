---
name: scaffold-skill
description: Generate the file skeleton for a new skill in a target plugin — frontmatter and slots, not procedure.
allowed-tools: Read, Glob, Grep, Write, Edit
metadata:
  flags:
    --plugin=<name>: target plugin whose skills/ gets the new skill
    --name=<skill>: name of the skill to scaffold
    --kind=port: scaffold a thin tool-layer PORT — a phase-less inline-dispatch skill plus an empty adapters/, owning its capability's config_requires — instead of a phased skill; its first adapter is added with add-component
    --slots=<list>: which earned slots to seed — phases (when the procedure has depth), rules, modules; usage.md is always seeded regardless
    --with-codify: hand the skeleton to codify to fill the procedure
    --dry-run: show the files that would be created without writing
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies.

1. Interrogate the intent: what single capability does this skill own, at what altitude — is it already covered by a skill (or a flag/module on one), and where will it grade, select, or default (its standard-points)? Name the capability, never the tools.  — see [phases/01-interrogate-intent.md](phases/01-interrogate-intent.md)
2. Shape the frontmatter: name + description as the skill format's recognized fields; the flags it answers to (and, for config-bearing plugins, config_requires) under metadata.  — see [phases/02-shape-frontmatter.md](phases/02-shape-frontmatter.md)
3. Seed the slots: create only the body files it needs — a phase per ordered step, a rule per reusable craft, a module per flag-activated behavior — each an honest stub, with the standard-points seeded as explicit demands.  — see [phases/03-seed-slots.md](phases/03-seed-slots.md)
4. Hand off or finish: return the skeleton, or hand to codify to fill the procedure from the maintainer's process; report every path created.  — see [phases/04-hand-off.md](phases/04-hand-off.md)
