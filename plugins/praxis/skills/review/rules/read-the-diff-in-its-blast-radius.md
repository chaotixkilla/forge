# Read the diff in its blast radius

The lines the diff changed are where the author was looking; the bug is often where they weren't. A changed function has callers who relied on its old behavior, callees whose contracts it now leans on differently, and invariants elsewhere in the system that the change quietly breaks. Reviewing only the touched lines catches typos and misses exactly the class of defect review exists to catch: the one that surfaces two files away. This rule is the method for following a change out to the edge of what it can break — and for knowing where that edge is.

## Follow the radius outward

For each symbol the diff touches, read outward along three directions until you can predict the change's effect on each:

- **Callers** — who invokes the changed code, and did they depend on the behavior that changed? A widened return type, a new thrown error, a changed default, a removed side effect — each is safe only if every caller tolerates it. Changed a signature? Every call site is in the radius.
- **Callees** — what does the changed code now call, and does it hold up its end? A new argument passed to a helper, a call moved outside a lock, an error now swallowed instead of propagated.
- **Invariants** — the assumptions that span the change: an ordering two functions both rely on, a field that must stay non-null, a cache that must be invalidated when the source changes. These are the hardest and the highest-value; they are why the mental model built in [build-the-mental-model](../phases/02-build-the-mental-model.md) precedes the hunt.

## Where the edge is — the stopping test

The radius is bounded, not infinite, and the bound is a *test*, not a fixed hop count: **stop following a direction when you can predict the change's runtime effect on everything reachable that way, and reading one more hop would not change a verdict.** A change to a pure leaf function with three local callers has a small radius; a change to a shared signature with thirty callers, or to a data invariant, has a large one. `--effort` sets how far to push before withholding (the depth row in [calibrate-confidence-to-effort](calibrate-confidence-to-effort.md)); this rule sets *how* to push and *when* the pushing is done.

`(basis: this is the understand craft's blast-radius method applied to a diff — callers/callees/invariants is the standard reachability decomposition; the stopping test is derived from the same "stop when answered" discipline understand uses, adapted to "stop when the change's effect is predictable.")`

The failure this prevents is the confident local review: "the changed function is correct" is a true and useless statement if the change broke a caller that assumed the old contract. Judge the *change*, which lives in the radius, not the *lines*, which are only its center.
