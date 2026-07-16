A research run is only as good as the question it starts from. A vague topic fans out into noise; a decomposed question, each part naming what would answer it, fans out into a plan. This phase turns the ask into answerable sub-questions and draws the line between what the open web must settle and what context or the repository already answers — so the fan-out spends only on what's genuinely open.

## Decompose into answerable sub-questions

Break the question into the sub-questions that must each be settled for the whole to be answered. A sub-question is **answerable** when you can state, *in advance*, the evidence that would decide it — the kind of source and the concrete observation that would confirm or refute each candidate answer. If you cannot name what evidence would move it, it is not yet a research question: sharpen it or split it until you can. (basis: the standard research-framing discipline — name what would change your mind before searching, so the fan-out targets deciding evidence rather than confirming prose.)

Separate the sub-questions from the *assumptions* smuggled into the ask ([separate-claim-from-inference](../rules/separate-claim-from-inference.md)): "which cache library is fastest?" assumes caching is the bottleneck. Surface that assumption as its own sub-question — *is caching the bottleneck?* — rather than inheriting it unexamined.

## Draw the open-vs-known line

For each sub-question, decide whether it genuinely needs the open web or is already answerable from the session context or the repository. deep-research is for what in-context and repository knowledge can't settle; a sub-question the context already answers is recorded with that answer and its source, not re-researched. If *nothing* is genuinely open — the whole question is answerable from what you already hold — say so and stop, rather than manufacturing a web run to look thorough.

## Set scope and depth

Fix what is in and out of scope, and the depth the caller asked for — a single broad pass by default, a wider multi-round sweep under [deep-mode](../modules/deep-mode.md) (`--deep`). Flag any sub-question whose answer would reorder the others' priority, so planning can sequence it first.

The output is the ordered set of answerable sub-questions — each carrying the evidence that would settle it and its open/known status — the plan the next phase maps to source lanes.
