---
name: deep-research
description: Fan out multi-source web research, fetch and adversarially verify the load-bearing claims, then synthesize a cited report with explicit confidence and gaps — for a genuinely open question that in-context and repository knowledge can't settle.
metadata:
  flags:
    --deep: escalate depth — wider fan-out, more rounds of lead-chasing, and the authoritative-literature lane engaged on every sub-question rather than only where it fits, instead of a single pass (activates deep-mode)
    --budget=<n>: bound the number of searches/fetches, allocated across sub-questions by importance (activates budget-discipline)
    --timebox=<duration>: work to a wall-clock limit, degrading to a best-effort answer when it expires (activates timeboxing)
    --cited: raise rendered attribution to a formal citation for every non-obvious claim — a compose-output rigor input; provenance is tracked regardless
    --verify=<off|light|strict>: how hard the load-bearing claims are tested before they're trusted — the rigor dial (see the verification-level rule)
    --artifact: render the finished report as a publishable, team-facing document through the artifacts capability (activates artifact-output)
    --background: run the research detached so a long fan-out doesn't block the session (activates background-run)
    --notify: on completion of a detached run, signal the invoker (activates notify-on-completion)
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

deep-research owns no backend of its own. Searching the web and fetching a source is an **ambient capability** — like reading a local file — so it wires no config and no adapter for it, naming only the capability in prose, and it recruits the web-facing explorer lanes directly. The one *configured* source — org-internal knowledge (a feature's history, prior decisions, who and when) — it reaches through the `gather` port, which owns `tools.knowledge` and drops the lane with a note when no backend is configured. Publishing it delegates wholesale to the `publish-artifact` port (which owns `tools.artifacts`). Every doer owns its own prerequisite, so deep-research declares **no `config_requires`** — the org-knowledge lane is present when a backend is configured and degrades cleanly when it isn't.

One flag reshapes the whole run rather than activating inside a phase: `--background` runs the research detached — see [modules/background-run.md](modules/background-run.md). (`--notify`, its usual companion, activates at completion — see [phases/06-compose-output.md](phases/06-compose-output.md).)

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies and recruit the shared explorer/critic agents.

1. Frame the question: decompose the open question into answerable sub-questions and decide what evidence would settle each  — see [phases/01-frame-the-question.md](phases/01-frame-the-question.md)
2. Plan the search: map each sub-question to the source lanes that could answer it and set the fan-out strategy  — see [phases/02-plan-the-search.md](phases/02-plan-the-search.md)
3. Gather evidence: fan out searches and fetch sources with provenance, chase leads, and re-query to saturation  — see [phases/03-gather-evidence.md](phases/03-gather-evidence.md)
4. Verify claims: adversarially test the load-bearing claims — corroborate, chase to the primary source, hunt disconfirming evidence  — see [phases/04-verify-claims.md](phases/04-verify-claims.md)
5. Synthesize: reconcile conflicts, weight by source strength, and separate the established from the contested  — see [phases/05-synthesize.md](phases/05-synthesize.md)
6. Compose the output: render to the requested form and rigor with an explicit statement of confidence and gaps  — see [phases/06-compose-output.md](phases/06-compose-output.md)
