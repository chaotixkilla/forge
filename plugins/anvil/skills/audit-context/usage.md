# audit-context — usage

Measures what a plugin's skills cost to load, and judges whether the cost is earned. Two directions of defect: weight made reachable from one place that an executor cannot triage, and a load-bearing citation phrased so it never gets opened.

## When to reach for it

- **Before a release**, alongside the other audits. A plugin can pass every conformance check and still make 40,000 tokens reachable from one bullet list.
- **After adding a rule library** to a skill, or after a `codify` run that grew a phase. This is when a routing index quietly becomes a roster: the conditions were adequate at six entries and are not at twenty.
- **When a consumer reports that a skill "ignores its own rules"** — the symptom of a load-bearing citation in the depth-on-demand register. This audit locates it; no other check does.
- **When the always-resident cost needs watching.** Every skill and agent description is paid on every request, and a skill pool grows one description at a time with no natural moment to notice.
- **On anvil itself.** The kit is not exempt, and its own audit skills are among the heaviest things it ships.

## Not for

- **Whether a citation resolves, or a slot is placed right** → `audit-contract`. That audit asks whether files *can* load; this one asks how much can, and whether the ones that matter will. A dangling link found here is routed there, not fixed here.
- **Whether a passage earns its keep** → the economy-skeptic lens, on `codify`'s gate or `dogfood`'s challenge pass. This audit is indifferent to whether prose is good; it measures where weight sits and whether routing is decidable.
- **Whether a phase, rule or flag should exist at all** → the scaffolding-skeptic. Cutting structure is not this audit's remedy, and proposing it is the characteristic way to do damage here.
- **Whether the skill layer leaks a tool name** → `audit-tool-leaks`.

## Examples

`--plugin=praxis` — the full audit: layer table, ceilings, fan-out reads, register checks, inline report.

`--plugin=anvil --skill=audit-contract` — one skill. The whole plugin's resident total is still reported (a per-skill view of an always-resident layer means nothing), but only this skill's ceiling and hotspots are judged.

`--plugin=praxis --checks=resident-weight` — just the always-resident layer. Cheap; the right check to run repeatedly as a skill pool grows.

`--plugin=praxis --checks=citation-register` — skip the measurement entirely and read only for load-bearing citations phrased as asides. The check to run when a skill is reportedly ignoring its own standards.

`--plugin=miyamoto --budget=closure=40000,citations=20` — audit a plugin whose shape differs from the corpus the budgets were calibrated on, without arguing with a threshold that was never about it. Record why in the report.

`--plugin=praxis --report=artifact` — publish the layer table as a document; useful when the table is the deliverable and the findings are secondary.

## Gotchas

- **The budgets are proposed, not ratified.** They were calibrated on two plugins at one moment, chosen to separate sites a hand audit had already judged from ones it had cleared. A breach is a prompt to read, never a verdict — see [context-budget](rules/context-budget.md).
- **A breach that the read clears is not a finding.** High fan-out is how a *good* routing index looks. The number and the verdict are different things, and the report keeps them in separate sections for that reason.
- **The intuitive remedy for a roster is the wrong one.** Do not thin the library; add firing conditions to the citations already there. Where those citations are a rule's only registration, thinning also manufactures orphan findings at the release gate — the read checks for this before proposing anything.
- **Measurement is delegated to a script and is not to be reproduced by hand.** If a figure looks wrong, that is a finding about the script. A hand count nobody can reproduce is worse than a wrong number everybody can.
- **Two seams end a load path rather than extending it** — a sibling skill's spine (an invocation, running in its own window) and a recruited agent (a forked context). A measurement that expanded through either would report every well-connected file as reaching the whole plugin, which is how this class of metric becomes noise.
