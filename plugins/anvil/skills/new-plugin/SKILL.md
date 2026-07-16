---
name: new-plugin
description: Birth a new plugin in the marketplace — decide its config posture, scaffold the shell, and design its initial skill pool. Stops short of publishing.
allowed-tools: Read, Glob, Grep, Write, Edit
metadata:
  flags:
    --name=<plugin>: name of the new plugin (its directory and plugin.json name)
    --unpublished: mark it in-development — kept out of marketplace.json until it's built and released
    --dry-run: show the scaffold plan without writing
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies.

1. Design the pool: require --name; interrogate the plugin's purpose, design its capability set + altitude split, and decide its config posture (config-bearing vs config-less)  — see [phases/01-design-the-pool.md](phases/01-design-the-pool.md)
2. Scaffold the shell: create plugin.json, the slot folders, and a README — plus a config schema + a config-setup skill only if config-bearing  — see [phases/02-scaffold-shell.md](phases/02-scaffold-shell.md)
3. Lay out the skills: hand each designed skill to scaffold-skill to seed the pool, and to codify to fill the procedure  — see [phases/03-lay-out-skills.md](phases/03-lay-out-skills.md)
4. Hand off: report the new tree; note it is NOT yet in the catalog, and point at release  — see [phases/04-handoff.md](phases/04-handoff.md)
