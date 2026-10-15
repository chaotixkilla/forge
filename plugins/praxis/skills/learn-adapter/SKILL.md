---
name: learn-adapter
description: Map a tool praxis has no adapter for onto one of its ports — read the connected tool's surface without writing anything, match each of the port's operations to its calls, judge each guarantee the port states, and write a per-user learned map the port then dispatches through; or show, relearn or forget a map. A tool-layer skill, called by a port at first contact with a provider it has no adapter for, and runnable by the user.
metadata:
  flags:
    --port=<name>: the port to map (required, but for --forget given only --provider)
    --provider=<name>: the provider to map it onto, instead of the one the port's slot names
    --entry=<name>: for knowledge or artifacts, the source or audience space whose transport and credential to use
    --show: show the map operation by operation, with each verdict, instead of learning (activates the show module)
    --relearn: map the port again from the tool's current surface, replacing the map (activates the relearn module)
    --forget: delete the map, so the port's next call learns afresh (activates the forget module)
    --dry-run: explore and show the map that would be written, writing nothing
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

This skill maps a provider praxis has no adapter for, from the tool the user has connected. It reads what the connected tool offers, maps the port's operations onto it, and records which of the port's guarantees each mapping keeps. An operation whose guarantees it can't show kept answers `unsupported`, never something weaker. The map is the user's own: it lives in the plugin's per-user data folder and is never versioned. `(basis: maintainer, 2026-10-13)`

`--show`, `--relearn` and `--forget` replace the run: see [modules/show.md](modules/show.md), [modules/relearn.md](modules/relearn.md) and [modules/forget.md](modules/forget.md). A port dispatching through a map follows [dispatch-through-a-learned-map](rules/dispatch-through-a-learned-map.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies.

1. Resolve the target: the port, the provider, its transport, and where the map lives  — see [phases/01-resolve-the-target.md](phases/01-resolve-the-target.md)
2. Read the tool's surface: every call the connected tool offers, its inputs and outputs, and its signature, without writing anything  — see [phases/02-read-the-surface.md](phases/02-read-the-surface.md)
3. Map the operations: match each of the port's operations to the calls that perform it, with how inputs, outputs and failures translate  — see [phases/03-map-the-operations.md](phases/03-map-the-operations.md)
4. Judge the guarantees: for each operation, whether its mapping keeps every guarantee the port states  — see [phases/04-judge-the-guarantees.md](phases/04-judge-the-guarantees.md)
5. Write the map: in the fixed shape the ports read, and report what was mapped, what wasn't, and why  — see [phases/05-write-the-map.md](phases/05-write-the-map.md)
