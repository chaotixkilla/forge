The spike has produced its verdict; now harvest the part worth keeping and throw the rest away. This phase exists because both halves are easy to get wrong. The learning is easy to lose — it lives in your head and in code that's about to be deleted, so if you don't extract it deliberately it vanishes with the throwaway. And the code is easy to *keep* — a spike that runs invites being grafted into production, and the discard step is, in the field, the single most-skipped step of prototyping. Capture forces both: pull the durable learnings out, and make an explicit decision about the code rather than letting it linger.

## Extract the durable learnings — the findings blob

Assemble what survives the spike into one findings blob:

- **The verdict** — `answered` / `refuted` / `still-open` on the [verdict-scale](../rules/verdict-scale.md), leading the blob.
- **The observed evidence** it rests on — the run, the input, the result ([ground-claims-in-a-run](../rules/ground-claims-in-a-run.md)) — so the verdict is reconstructable by someone who wasn't there.
- **The rejected paths** — the dead-ends with their causes ([record-dead-ends](../rules/record-dead-ends.md)), including the runner-up approaches under `--max-agents` and why each lost.
- **The generalization caveats** — the shortcuts that wouldn't survive production scale, data, or constraints ([keep-the-real-thing-in-view](../rules/keep-the-real-thing-in-view.md)), so the reader knows the boundary between demonstrated and assumed.

`(basis: ratified by the maintainer, 2026-07-09 — the durable-output contract. prototype is a leaf: by default it returns this blob to its caller and invokes no downstream skill. The blob is also the artifact that crosses the boundary to plan (which invokes prototype on a needs-a-spike) and upstream to spec (which the findings de-risk before commit) — both, and neither is invoked by prototype.)`

## Route the findings

By default, **return the blob to the caller** — prototype composes nothing downstream. With **`--publish`**, hand it wholesale to the artifacts capability as a clean, team-facing findings document — see [publish-learnings](../modules/publish-learnings.md). `(basis: ratified by the maintainer, 2026-07-09 — leaf by default; opt-in --publish delegates wholesale to publish-artifact, which owns the artifacts prerequisite, so prototype stays config-less. A direct memory/knowledge sink was rejected: it would need its own adapter and config_requires and break the config-less directive.)`

## Dispose of the code explicitly — never by default

Make a deliberate disposition of the spike code; do not leave it lying around to accrete commits:

- **Discard** — delete it, or quarantine it clearly labeled as a throwaway spike (not importable, not runnable in production paths). This is the default and the point of a spike ([favor-disposability](../rules/favor-disposability.md)).
- **Schedule a rebuild** — if the spike revealed that some piece is worth keeping, the disposition is *"rebuild it properly,"* not *"promote this code."* The learning transfers; the throwaway code does not — grafting a spike into production ships the learning-optimized shortcuts as load-bearing.
- Under **`--sandbox`**, discarding is wholesale: tear down the isolated environment and everything in it — see [sandbox-isolation](../modules/sandbox-isolation.md).

State which disposition was taken. An unstated disposition is how a throwaway quietly becomes permanent.

The output of this phase — and of prototype: the findings blob (returned or published) and a disposed spike. The uncertainty is reduced; the code is gone.
