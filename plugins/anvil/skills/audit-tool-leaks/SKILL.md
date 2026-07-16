---
name: audit-tool-leaks
description: Scan a target plugin's skill layer for concrete tool/provider names that escaped from adapters — the HARD RULE that skills name only capabilities.
allowed-tools: Read, Glob, Grep
metadata:
  flags:
    --plugin=<name>: target plugin to audit
    --fix: propose or apply rephrasings/relocations rather than only reporting
    --report=<fmt>: inline (default) or artifact
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies.

1. Collect the skill layer: require --plugin; enumerate SKILL.md + usage.md + phases/ + rules/ + modules/ + agent and hook files across the plugin, excluding adapters/ (the one place tools are allowed)  — see [phases/01-collect-skill-layer.md](phases/01-collect-skill-layer.md)
2. Detect leaks: scan each file for tool-name signals, then recruit the leak-hunter critic to challenge every capability claim  — see [phases/02-detect-leaks.md](phases/02-detect-leaks.md)
3. Rank and suggest: for each true leak, give file:line + a capability-level rephrasing, or a "move it into an adapter" recommendation  — see [phases/03-rank-and-suggest.md](phases/03-rank-and-suggest.md)
4. Report: return findings inline or as an artifact; with --fix, apply the rephrasings and relocations  — see [phases/04-report.md](phases/04-report.md)
