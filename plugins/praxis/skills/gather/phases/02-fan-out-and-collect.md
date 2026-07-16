This phase turns the recruitment plan into raw material: each chosen lane's explorer runs and returns anchored findings in its own lane's shape. Your job is to run them, capture what they hand back without editing it, and know when the picture has stopped moving.

## Recruit the lanes in parallel
1. Recruit one explorer per chosen lane, in parallel via the available fan-out mechanism — or, without fan-out available, run each lane's gather yourself in sequence, following that lane's own method (its explorer agent in [agents/explorers/](../../../agents/explorers/)) before moving to the next. Pass the `knowledge-base` lane the backend the caller resolved and handed in; never resolve it here.
2. Capture each explorer's findings verbatim, tagged with its lane and carrying its own anchors (file:line, commit/PR, page + provenance, URL + section, origin links) and its intra-lane grade. Do not weigh or edit yet — collection is neutral; weighing is phase 03.

## Chase leads to saturation
3. Harvest the leads a lane surfaces (a referenced commit, a cited spec, a named pitfall) and re-query the lane that owns them. Keep chasing across rounds until new sources stop changing the picture — the saturation test in [know-when-to-stop](../rules/know-when-to-stop.md), not "until queries run out." `--rounds=<n>` caps the rounds; `--budget=<n>`, when it binds first, stops the chase early — see [budget-discipline](../modules/budget-discipline.md).

## Handle the degraded and empty cases
4. A lane whose capability is unavailable (the knowledge backend unconfigured, the web lanes off under `--inputs-only`) is dropped with an explicit note — `lane X not consulted: <reason>` — never silently skipped; the picture must show which lanes it rests on.
5. A lane that returns nothing returns a documented absence — `no finding in lane X; searched <where>` — which is carried forward: an absence is a result, not a gap to hide.

The output of this phase: the pooled, lane-tagged, anchored findings — every consulted lane represented by findings or a documented absence, ready to weigh.
