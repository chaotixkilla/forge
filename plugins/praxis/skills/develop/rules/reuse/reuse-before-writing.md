# Reuse before writing

The cheapest code to maintain is the code you didn't add. Before writing a helper, a parser, a retry loop, a date formatter, the judgment is whether the codebase already has one — because a re-implementation isn't neutral: it's a second thing to keep correct, a second place a bug hides, and a divergence that drifts from the original until they subtly disagree. But the opposite failure is real too: a search so shallow it misses the existing helper, or so exhaustive it burns the afternoon. This rule pins *how hard to look* before you're justified in writing new.

## The discriminator

The search bar scales with the **cost of the thing you're about to write** and the **likelihood it already exists** — you are done searching when the expected cost of one more look exceeds the cost of the duplicate.

- **Always do the cheap search first.** Grep the codebase for the capability by its *behavior*, not the name you'd give it — search for what it does (the operation, the domain noun, the signature shape), because the existing one is named in someone else's words, not yours. One or two well-chosen searches across the repo is the floor, never zero.
- **Search harder the more the thing costs to own.** A three-line formatting helper: a quick look at the obvious module, then write it if absent. A non-trivial mechanism — auth, ret/backoff, pagination, money math, a cache — search the codebase *and* the platform/standard library *and* already-imported dependencies before adding your own, because these are exactly what a mature codebase already solved and exactly where a divergent re-implementation does the most damage.
- **Stop when the marginal look stops paying.** If two behavior-searches and a scan of the natural module turn up nothing, you've cleared the bar — write it. Searching is reconnaissance, not a research project; the goal is to not *miss* an obvious existing solution, not to prove a negative exhaustively.

(basis: DRY — "every piece of knowledge must have a single, unambiguous, authoritative representation" — Hunt & Thomas, *The Pragmatic Programmer*; and the orient-phase reading that surfaced the neighborhood ([match-surrounding-conventions](../change-hygiene/match-surrounding-conventions.md)). The search-by-behavior-not-name tactic is the practical edge that makes reuse actually happen.)

## When you find something close but not exact

Finding a near-match is where reuse turns into a real decision, so name it rather than defaulting:

- If the existing helper does the job with a small, honest extension, extend it — and migrate its callers if the contract changes ([keep-callers-working](../change-hygiene/keep-callers-working.md)).
- If bending it to fit would distort it (twist its contract, add a flag that changes its meaning for existing callers), that is *incidental* similarity, not shared knowledge — write the new one and don't force the merge ([dry-vs-incidental-duplication](dry-vs-incidental-duplication.md)). Two things that look alike today but answer to different reasons-to-change should stay separate.

## The anchors

- *Good:* you need to clamp a value to a range, you search `clamp|bound|min.*max` across the repo, find an existing `clamp()` in the shared utils, and call it.
- *Bad:* you write a fresh `clampToRange()` next to the module's existing `clamp()` because you searched for your name, not its behavior — the exact duplication the review dogfood caught, now shipped instead of avoided.
