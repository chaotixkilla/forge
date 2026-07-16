---
name: dogfood
description: Run a target plugin's own skills against itself (or a chosen subject) to prove they work end-to-end and surface friction the static audits can't. --self proves the kit self-hosts.
allowed-tools: Read, Glob, Grep, Write
metadata:
  flags:
    --plugin=<name>: plugin whose skills are exercised
    --self: target the kit itself — run the kit's skills on the kit (the self-hosting proof)
    --subject=<path>: run the skills against a different subject instead of the plugin itself
    --report=<fmt>: inline (default) or artifact for the dogfood log
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies.

1. Pick scenarios: require --plugin or --self; choose representative invocations that exercise the plugin's real paths, not happy-path smoke tests  — see [phases/01-pick-scenarios.md](phases/01-pick-scenarios.md)
2. Run and observe: invoke each skill on the subject as a fresh executor; record what it did, where it stalled, what it assumed  — see [phases/02-run-and-observe.md](phases/02-run-and-observe.md)
3. Challenge: send the run logs to the cold-executor and standards-skeptic critics — surface the guesses and the open bars a single run concealed  — see [phases/03-challenge.md](phases/03-challenge.md)
4. Report friction: convert friction, gaps, and contract drift into graded, ranked findings with pointers back to the responsible files  — see [phases/04-report-friction.md](phases/04-report-friction.md)
