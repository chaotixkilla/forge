# Read the diff in its blast radius

The lines the diff changed are where the author was looking; the bug is often where they weren't. Reviewing only the touched lines catches typos and misses exactly the class of defect review exists to catch: the one that surfaces two files away. "The changed function is correct" is a true and useless statement if the change broke a caller that assumed the old contract.

## Follow the radius outward

For each symbol the diff touches, read outward along three directions until you can predict the change's effect on each:

- **Callers** — who invokes the changed code, and did they depend on the behavior that changed? A widened return type, a new thrown error, a changed default, a removed side effect — each is safe only if every caller tolerates it. Changed a signature? Every call site is in the radius.
- **Callees** — what does the changed code now call, and does it hold up its end? A new argument passed to a helper, a call moved outside a lock, an error now swallowed instead of propagated.
- **Invariants** — the assumptions that span the change: an ordering two functions both rely on, a field that must stay non-null, a cache that must be invalidated when the source changes. These are the hardest and the highest-value; they are why the mental model built in [build-the-mental-model](../phases/02-build-the-mental-model.md) precedes the hunt.

## Where the edge is — the stopping test

The radius is bounded, not infinite, and the bound is a *test*, not a fixed hop count: **stop following a direction when you can predict the change's runtime effect on everything reachable that way, and reading one more hop would not change a verdict.** A change to a pure leaf function with three local callers has a small radius; a change to a shared signature with thirty callers, or to a data invariant, has a large one. `--rigor` sets how far to push before withholding (the depth row in [calibrate-certainty-to-rigor](calibrate-certainty-to-rigor.md)); this rule sets *how* to push and *when* the pushing is done.

`(basis: derived from understand's blast-radius method and its stop-when-answered test)`
