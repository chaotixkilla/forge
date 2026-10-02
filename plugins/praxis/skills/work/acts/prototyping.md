# Prototyping

**Entry condition.** The request is to answer a feasibility question by building something small and throwaway: will this approach work, how fast is it, does this library do what it claims. Building the thing for real goes to the developing act. (basis: maintainer, 2026-09-30)

**Done when** the spike findings are filed, with the question read as answered, refuted or still open, and the spike's code is discarded. (basis: derived from the step's outcome)

## The code is thrown away

Prototyping keeps its learnings, not its code. The spike runs in a throwaway sandbox (prototype's `--sandbox`), and close-out discards it; what carries into a later spec or plan is the findings. When the task goes on to developing, the findings are its input, and its code is written fresh. (basis: maintainer, 2026-09-30)

## Steps

(basis: maintainer, 2026-09-30)

| # | step | inputs | skipped by the act when |
|---|---|---|---|
| 1 | [prototype](../../prototype/SKILL.md) `--sandbox` | the question, and any prior art the request names | never |

## Filed

Step 1's result files as the spike findings. (basis: derived from the document types' membership tests)

## Delivered

When the request names an audience or a place, the findings' link goes there per [deliver-through-the-ports](../rules/deliver-through-the-ports.md); otherwise close-out's report carries it to the user.
