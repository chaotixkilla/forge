---
name: understand
description: Build an accurate, anchored mental model of an unfamiliar system, feature, or area — trace how it actually behaves, where things live, and why — and produce a certainty-graded map, not a change. The read-only orientation pass to run before touching unfamiliar code; distinct from gather (the delegated evidence engine it consumes) and deep-research (open-world cited reports).
metadata:
  flags:
    --deep: maximum-rigor mode — widen the blast radius, follow secondary paths and edge cases, and corroborate harder across history and ground truth (activates the deep-dive module)
    --symbol=<name>: seed the investigation from a named symbol — start at its definition and fan out through its references (a seeding mode, applied in frame-the-question)
    --from-code=<glob|symbol>: bottom-up — start from given code locations and reconstruct intent and behavior outward, rather than from a question (a seeding mode, applied in frame-the-question)
    --read-only: hard guarantee of zero mutations — pure static observation, no runs, edits, or state changes to the system under study (activates the read-only-boundary module)
    --diagram: emit a diagram of the traced structure or flow (control/data/sequence) as part of the map (activates the render-diagram module)
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

`--deep` widens the whole investigation (blast radius, secondary paths, corroboration depth): see [modules/deep-dive.md](modules/deep-dive.md). understand owns no backend of its own: it delegates its evidence-gathering (the locate and corroborate steps) to the `gather` skill — the doer that owns the `tools.knowledge` prerequisite — so it declares no `config_requires`.

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies.

1. Frame the question: turn the ask into a precise, answerable investigation question and set scope/depth before touching code  — see [phases/01-frame-the-question.md](phases/01-frame-the-question.md)
2. Locate the surfaces: delegate to gather to find where the relevant code, data, and config live before reading whole files  — see [phases/02-locate-the-surfaces.md](phases/02-locate-the-surfaces.md)
3. Trace the behavior: follow the real execution and data-flow paths end to end, grading each claim by how much you actually observed  — see [phases/03-trace-the-behavior.md](phases/03-trace-the-behavior.md)
4. Corroborate against reality: delegate to gather to check the traced behavior against history, recorded decisions, and ground truth — why it's this way, what was tried before  — see [phases/04-corroborate-against-reality.md](phases/04-corroborate-against-reality.md)
5. Synthesize the answer: assemble a coherent, certainty-graded map anchored to file:line and commits, separating what is established from what is inferred from what stays unknown  — see [phases/05-synthesize-the-answer.md](phases/05-synthesize-the-answer.md)
