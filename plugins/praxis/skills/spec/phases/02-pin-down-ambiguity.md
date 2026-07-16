This is where a spec earns its keep. Interrogation expanded the request; this phase converts the fuzz that expansion exposed into hard constraints. Most of a spec's value is created here, because this is the step a prose "requirements doc" skips — it restates the ask in more words, where spec turns it into statements a build can be held to. Every vague adjective, every "it depends," every unstated boundary is an ambiguity that will otherwise resurface downstream as a bug where the build guessed the answer you never wrote.

## Quantify every vague adjective

Every *fast, many, large, quickly, roughly, minimal* is a placeholder for a measurable condition the author knew and the sentence omitted. Replace each with something a verification method returns pass/fail on ([testable-or-its-not-a-requirement](../rules/testable-or-its-not-a-requirement.md)): "fast" → a latency number at a percentile under a stated load; "many" → a concurrency or volume figure; "large" → a size limit. The bar for done: **an adjective that has not become a measurable condition has not been pinned.**

The split the standard draws, applied here: *that* a vague quality must become a measurable condition is non-negotiable and sourced; *which* number the condition carries is contingent. So the number is **deliberately open** — a house or project call, not spec's to invent. Where a standing number exists (a perf budget, an a11y or security baseline), pull it via [gather](../../gather/SKILL.md) rather than guess; where none does, propose one and flag it as an assumption to confirm ([make-the-unsaid-explicit](../rules/make-the-unsaid-explicit.md)), never silently pick. What is not open is the requirement to have a measurable condition at all.

## Resolve every "it depends" into explicit branches

"It depends" is a decision tree the author collapsed into three words. Expand it: enumerate, for each branch, the **condition** that selects it and the **outcome** it produces. "Access depends on the user's role" becomes: owner → full control; editor → read and write, no delete; viewer → read only; no role → denied. Two discriminators keep the tree runnable and are themselves requirements: **if two conditions can both be true, state which wins; if none match, state the default.** An "it depends" left un-branched is not a simpler requirement — it is an ambiguity that ships, and the build will resolve it by guessing the branch you declined to write.

## Define the boundaries and limits

Every capability has edges the happy path ignores: minimum and maximum lengths, rate limits, pagination sizes, timeouts, the largest and the oldest thing handled. State each explicitly — a boundary unstated is a boundary the build sets arbitrarily and inconsistently. Each is a testable requirement: "uploads up to 25 MB; a larger file is rejected with a stated error" is checkable; "reasonable file sizes" is not.

## Specify the empty, error, denied, and extreme states

The happy-path-with-data case is the one every spec covers; the value is in the four it usually skips. Sweep each as its own requirement with its own acceptance criterion: the **empty** state (nothing created yet — a real behavior to design, not an oversight), the **error** state (the operation fails or a dependency is down), the **denied** state (the actor lacks permission), and the **extreme** state (too much data, the maximum, offline). A concrete example pins these faster than any amount of prose — name the input that triggers the empty case and state what must render ([prefer-examples-over-prose](../rules/prefer-examples-over-prose.md)).

The output is the hardened intent — adjectives quantified, "it depends" branched, boundaries and off-happy-path states pinned — ready to be organized into the requirement taxonomy in [requirement-structuring](03-requirement-structuring.md).
