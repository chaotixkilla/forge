---
name: gather
description: Gather evidence across chosen source lanes — recruit the explorer fleet, collect their anchored findings, and synthesize one weighted picture (authority over anecdote, corroboration across independent origins, conflicts and gaps surfaced, the transfer-to-this-project call left to the caller). The delegated engine other skills call for their gather-and-weigh step; not user-facing — reach for understand to map a system, or deep-research for an open-world cited report.
metadata:
  flags:
    --explorers=<list>: restrict the gather to specific source lanes (code, repository, knowledge-base, official-documentation, authoritative-literature, community-practices)
    --deep: wider lane set and fan-out, more rounds of lead-chasing, adding the authoritative-literature lane where the question turns on a domain result or standard — activates the deep-mode module
    --rounds=<n>: how many lead-chasing rounds to run before returning (the fan-out phase's iteration count)
    --budget=<n>: cap the number of recruit/fetch operations and allocate across lanes by importance — activates the budget-discipline module
    --inputs-only: gather only from provided inputs and the project-internal lanes; forbid the open-web lanes — activates the inputs-only module
  config_requires:
    - key: tools.knowledge
      if_missing: guide via init:knowledge, else degrade
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

`--deep` widens the whole gather (lane set, fan-out, lead-chasing rounds): see [modules/deep-mode.md](modules/deep-mode.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies.

1. Frame and scope the gather: turn the caller's ask into a precise gather question, pick which lanes to consult, and set fan-out breadth before recruiting anyone  — see [phases/01-frame-and-scope.md](phases/01-frame-and-scope.md)
2. Fan out and collect: recruit the chosen explorers in parallel and capture their anchored, lane-tagged findings, re-querying until the picture stops changing  — see [phases/02-fan-out-and-collect.md](phases/02-fan-out-and-collect.md)
3. Synthesize and weigh: apply the sourcing model — tier every finding, resolve conflicts by authority, corroborate across independent origins, surface divergences  — see [phases/03-synthesize-and-weigh.md](phases/03-synthesize-and-weigh.md)
4. Return the picture: hand back the weighted, anchored findings with conflicts, gaps, and transfer calls flagged for the caller  — see [phases/04-return-the-picture.md](phases/04-return-the-picture.md)
