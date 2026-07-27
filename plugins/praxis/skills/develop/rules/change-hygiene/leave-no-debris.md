# Leave no debris

Writing a change leaves a trail: a print you added to watch a value, a commented-out old version you kept while trying the new one, an import orphaned when you deleted the line that used it, a TODO you actually closed. The judgment this rule governs is what of that trail comes out before the change is done. Left to taste it goes wrong by omission — the scaffolding felt useful *while building*, so it stays, and the diff ships with debug noise and dead code that the next reader must now decode as if it were meaningful. Two builders left to instinct clean up to different lines.

## The discriminator

Anything that was a **means to writing the change but is not part of the change** is debris — remove it before done. Walk the diff and test each artifact by that question:

- **Debug scaffolding** — a print/log added to watch a value while building, a temporary hard-coded shortcut, a scratch helper. It served the writing, not the change. Remove it. (A log that genuinely belongs in the running system is not debris — but then it's a deliberate choice governed by [logging-what-matters](../verification/logging-what-matters.md), not a leftover.)
- **Commented-out code** — the old version kept "just in case." That is exactly what version control is for; the previous state is one command away in the version-control history, so the commented block earns nothing and rots into a lie as the code around it moves ([keep-comments-truthful](../comments/keep-comments-truthful.md)). Delete it.
- **Orphans** — an import, variable, or dead branch left behind when the line that used it was deleted or a condition became unreachable. Remove it; unreferenced code is a false signal that something still uses it.
- **A TODO you closed** — a marker for work now done. Delete the marker.

The one thing that is **not** debris and stays: a **deliberate, documented TODO tied to a tracked follow-up** — a real deferral, carrying its reference to the tracked item so the next reader can find the plan. That is a signal, not a leftover; keep it, with the reference. The line is: does the artifact carry meaning *forward*, or was it only ever scaffolding for *writing*? Debris removal is also what keeps the diff to task-relevant lines ([keep-the-diff-focused](keep-the-diff-focused.md)) — scaffolding left in is scope the reviewer must wade through.

(basis: the boy-scout / clean-as-you-go practice — don't leave a mess for the next person; commented-out code as a recognized anti-pattern (Fowler and Martin converge: delete it, version control remembers). Version control is precisely what makes "keep it just in case" unnecessary.)

## The anchors

- *Good:* the finished diff contains only lines that are part of the change — no stray prints, no commented-out predecessor, no unused imports; the single TODO left carries a tracked-issue reference explaining the deliberate deferral.
- *Bad:* the diff ships a `print("here")`, a commented-out block of the old implementation "in case we revert," and an import left dangling by a deleted call — three pieces of noise the next maintainer must each investigate to confirm they mean nothing.
