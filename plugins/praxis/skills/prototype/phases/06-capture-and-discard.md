The learning is easy to lose — it lives in your head and in code that's about to be deleted, so if you don't extract it deliberately it vanishes with the throwaway. And the code is easy to *keep* — a spike that runs invites being grafted into production, and the discard step is, in the field, the single most-skipped step of prototyping.

## Extract the durable learnings — the findings blob

Assemble what survives the spike into one findings blob:

- **The verdict** — `holds` / `fails` / `unsettled` / `not checked` (with its reason) on the [verdict-scale](../rules/verdict-scale.md), leading the blob.
- **The observed evidence** it rests on — the run, the input, the result ([observation-over-inference](../../../craft/evidence/observation-over-inference.md)) — so the verdict is reconstructable by someone who wasn't there.
- **The rejected paths** — the dead-ends with their causes ([record-dead-ends](../rules/record-dead-ends.md)), including the runner-up approaches under `--max-agents` and why each lost.
- **The generalization caveats** — the shortcuts that wouldn't survive production scale, data, or constraints ([keep-the-real-thing-in-view](../rules/keep-the-real-thing-in-view.md)), so the reader knows the boundary between demonstrated and assumed.

`(basis: maintainer, 2026-07-09)`

## Route the findings

**Return the blob to the caller** — prototype composes nothing downstream, and writes the findings to no memory or knowledge store, which would need config it doesn't carry. Filing or publishing them is the caller's. `(basis: maintainer, 2026-07-09)`

## Before it goes out, read it as its reader

Put the finished report through [deliver-at-the-readers-register](../../../craft/writing/deliver-at-the-readers-register.md) before delivering it, applying its honesty floor item by item from the rule, not from memory.

## Dispose of the code explicitly — never by default

Make a deliberate disposition of the spike code; do not leave it lying around to accrete commits:

- **Discard** — delete it, or quarantine it clearly labeled as a throwaway spike (not importable, not runnable in production paths). This is the default and the point of a spike ([favor-disposability](../rules/favor-disposability.md)).
- **Schedule a rebuild** — if the spike revealed that some piece is worth keeping, the disposition is *"rebuild it properly,"* not *"promote this code."* The learning transfers; the throwaway code does not — grafting a spike into production ships the learning-optimized shortcuts as load-bearing.
- Under **`--sandbox`**, discarding is wholesale: tear down the isolated environment and everything in it — see [sandbox-isolation](../modules/sandbox-isolation.md).

State which disposition was taken. An unstated disposition is how a throwaway quietly becomes permanent.

The output of this phase — and of prototype: the findings blob, returned, and a disposed spike.
