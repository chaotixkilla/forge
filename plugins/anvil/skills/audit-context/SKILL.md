---
name: audit-context
description: Measure what a target plugin's skills cost to load and judge whether the cost is earned — always-resident weight, per-skill load-path ceilings, fan-out hotspots where one file cites many, and whether each load-bearing citation will actually be opened.
allowed-tools: Read, Glob, Grep, Bash
metadata:
  flags:
    --plugin=<name>: target plugin to audit
    --skill=<name>: scope the audit to one skill within the plugin (siblings still measured for the resident total, not judged); default audits every skill
    --checks=<list>: subset to run — resident-weight, skill-ceilings, fan-out, citation-register, licensed-skips
    --budget=<k=v,…>: override a proposed budget for this run — amplification, citations, resident, closure — where a plugin has ratified its own
    --report=<fmt>: inline (default) or artifact
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

The sibling audits ask whether a plugin's files *can* load: [audit-contract](../audit-contract/SKILL.md) resolves every citation, and its `skip-resistance` rule checks that the spine and the delegation seam cannot be acted on from a summary. This audit asks the two questions that remain once wiring is sound — **how much becomes reachable, and will the loads that matter actually happen.** Both directions are defects, and they pull against each other: a phase that makes 34,000 tokens reachable from one bullet list is over-eager, while a pinned scale cited as a trailing aside is never opened at all. A plugin can fail either without failing any other audit.

Measurement is delegated: `scripts/measure_context.py` computes the layer weights, the ceilings, and the fan-out hotspots deterministically, because counting tokens and resolving a citation graph by hand is slow, costs the context this audit exists to protect, and gets the subdirectory-relative cases wrong. What the script cannot do is read — whether a high-fan-out site is a routing index or a roster, and whether a citation's register matches what the cited file holds, are judgments. The script locates; the phases read.

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies.

1. Measure the load path: require --plugin; run the measurement script over the target and establish the layer table — always-resident weight, per-skill ceilings, and the ranked fan-out hotspots — then sanity-check its output against the tree  — see [phases/01-measure.md](phases/01-measure.md)
2. Read the hotspots: for each site the measurement flags, decide whether it is a routing index or a roster, applying the discriminator in [index-vs-roster](rules/index-vs-roster.md) — this is where the audit earns its keep, because the number alone convicts nothing  — see [phases/02-read-the-hotspots.md](phases/02-read-the-hotspots.md)
3. Check the citation registers: for every citation into a file holding a scale, vocabulary, threshold, or named set, confirm the citation is phrased so the step cannot be completed without it — and that every genuinely optional read carries its firing condition  — see [phases/03-check-registers.md](phases/03-check-registers.md)
4. Report: return findings with severity, separating measured breaches from read judgments, inline or as an artifact  — see [phases/04-report.md](phases/04-report.md)
