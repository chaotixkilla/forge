Convert the fuzz interrogation exposed into hard constraints a build can be held to. Every vague adjective, every "it depends," every unstated boundary is an ambiguity that will otherwise resurface downstream as a bug where the build guessed the answer you never wrote.

## Quantify every vague adjective

Replace every *fast, many, large, quickly, roughly, minimal* with something a verification method returns pass/fail on ([testable-or-its-not-a-requirement](../rules/testable-or-its-not-a-requirement.md)): "fast" → a latency number at a percentile under a stated load; "many" → a concurrency or volume figure; "large" → a size limit. The bar for done: **an adjective that has not become a measurable condition has not been pinned.**

*That* a vague quality must become a measurable condition is non-negotiable; *which* number the condition carries is **deliberately open** — a house or project call, not spec's to invent. Where a standing number exists (a perf budget, an a11y or security baseline), pull it via [gather](../../gather/SKILL.md) rather than guess; where none does, propose one and flag it as an assumption to confirm ([make-the-unsaid-explicit](../rules/make-the-unsaid-explicit.md)), never silently pick.

## Resolve every "it depends" into explicit branches

"It depends" is a decision tree the author collapsed into three words. Expand it: enumerate, for each branch, the **condition** that selects it and the **outcome** it produces. "Access depends on the user's role" becomes: owner → full control; editor → read and write, no delete; viewer → read only; no role → denied. Two discriminators keep the tree runnable and are themselves requirements: **if two conditions can both be true, state which wins; if none match, state the default.**

## Define the boundaries and limits

Every capability has edges the happy path ignores: minimum and maximum lengths, rate limits, pagination sizes, timeouts, the largest and the oldest thing handled. State each explicitly — a boundary unstated is a boundary the build sets arbitrarily and inconsistently. Each is a testable requirement: "uploads up to 25 MB; a larger file is rejected with a stated error" is checkable; "reasonable file sizes" is not.

## Specify the empty, error, denied, and extreme states

Beyond the happy path with data, sweep the four states a spec usually skips, each as its own requirement with its own acceptance criterion: the **empty** state (nothing created yet — a real behavior to design, not an oversight), the **error** state (the operation fails or a dependency is down), the **denied** state (the actor lacks permission), and the **extreme** state (too much data, the maximum, offline). Pin them with a concrete example — name the input that triggers the empty case and state what must render ([prefer-examples-over-prose](../rules/prefer-examples-over-prose.md)).

The output is the hardened intent — adjectives quantified, "it depends" branched, boundaries and off-happy-path states pinned — ready to be organized into the requirement taxonomy in [requirement-structuring](03-requirement-structuring.md).
