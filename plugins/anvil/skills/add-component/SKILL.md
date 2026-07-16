---
name: add-component
description: Add one non-skill component — adapter, explorer, critic, rule, module, or hook — to a target plugin in its canonical place.
allowed-tools: Read, Glob, Grep, Write, Edit
metadata:
  flags:
    --plugin=<name>: target plugin to add the component to
    --kind=<k>: component kind — adapter | explorer | critic | rule | module | hook
    --name=<name>: the component's filename; for an adapter, defaults to --tool
    --skill=<skill>: for adapter/rule/module — which skill the component attaches to
    --tool=<provider>: for adapter — the provider/transport it wraps (the only place a concrete tool is named)
    --dry-run: show what would be created without writing
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies.

1. Resolve the kind and its home: require --plugin, --kind, and --name; from --kind, locate the canonical directory (the file lands as <name>.md) and the sibling files to mirror  — see [phases/01-resolve-kind-and-home.md](phases/01-resolve-kind-and-home.md)
2. Mirror the conventions: read existing components of this kind in the plugin; match their structure, headers, and altitude  — see [phases/02-mirror-conventions.md](phases/02-mirror-conventions.md)
3. Write the component: seed its body — an adapter's concrete tool calls, an agent's gather/challenge procedure, a rule's craft, a module's flag-behavior  — see [phases/03-write-component.md](phases/03-write-component.md)
4. Wire it up: register it where it's consumed (a dispatch line in the parent skill, the agent listing) and report every path created  — see [phases/04-wire-up.md](phases/04-wire-up.md)
