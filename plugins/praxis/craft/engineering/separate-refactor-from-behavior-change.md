# Separate refactor from behavior change

Most real changes tempt you to do two things at once: reshape the code *and* change what it does — rename and extract while also fixing the bug, restructure the module while adding the feature it needed. The judgment this rule governs is whether those two go in one step or two. Left to taste they get braided together, and the cost lands later on someone else: a reviewer staring at a diff where a moved function and a changed behavior are indistinguishable can't tell which lines are supposed to alter output, and a `bisect` chasing a regression lands on a commit that both restructured and re-behaved, isolating nothing.

## The discriminator

The test is on **what a single step does to observable behavior**: a refactor is behavior-preserving by definition — structure moves, outputs are identical. If one step **both reshapes code and alters what it does**, split it in two:

- **Refactor first** — move, rename, extract, reshape, with **zero behavior delta**, and prove it green before touching behavior. Nothing it does should change any output or contract; if a test changes its expected result, that wasn't a refactor.
- **Behavior change on top** — the bug fix, the new feature, the altered output — as its own step over the now-clean structure, so its diff shows *only* the lines that change behavior.

Split, each step is independently reviewable and independently revertable. This is why a "while I'm here" refactor doesn't ride along in a feature diff ([keep-the-diff-focused](keep-the-diff-focused.md)) — and the in-scope cleanup that *is* allowed stays bounded to lines the task already touches ([leave-the-campsite-cleaner](leave-the-campsite-cleaner.md)). When the work is committed in checkpoints, the refactor and the behavior change are separate checkpoints.

(basis: Fowler, *Refactoring*, the two hats)

## The anchors

- *Good:* first commit extracts a tangled function into three named helpers, tests unchanged and green (pure refactor, no behavior delta); second commit changes one helper to fix the off-by-one, and its diff shows exactly the behavior that moved.
- *Bad:* one commit that renames and reorganizes a module *and* fixes a bug inside it — the reviewer can't tell the rename from the fix, and when a regression surfaces a week later, the bisect stops at a commit that did both, pointing at nothing in particular.
