# Boy-scout rule, bounded

While making a change you pass through code that could be a little better — a vague name on a line you're editing anyway, dead code your change just orphaned, a comment that no longer matches. The judgment this rule governs is how much of that to fix: leaving touched code cleaner than you found it is good citizenship, but the same impulse, unbounded, is how a focused change metastasizes into a sprawling one. Left to taste it goes wrong at both ends — one builder cleans nothing and lets rot accumulate, another "improves" halfway across the module and buries the task. Two builders draw the cleanup line in very different spots. This rule pins the discriminator so two builders converge on how far the cleanup goes.

## The discriminator

The bound is a single test: **does the cleanup stay within the change's existing footprint** — the lines and files the task already makes you touch?

- **In-scope cleanup (do it)** — a clearer name on a line you're *already* editing ([name-for-the-reader](../naming/name-for-the-reader.md)), deleting dead code your change just orphaned, fixing a comment that your edit just made false. The task already has your hands on these lines; leaving them better costs nothing extra and adds no files. This is the good-citizenship the rule licenses.
- **Out-of-scope cleanup (don't — split it)** — a cleanup that pulls in files the task didn't touch, or that grows the diff materially beyond the change itself. However worthy, it crosses into scope creep: it widens the blast radius and buries the real change ([keep-the-diff-focused](keep-the-diff-focused.md)). Do it as a **separate change** with its own diff and verification ([separate-refactor-from-behavior-change](separate-refactor-from-behavior-change.md)).

The line is *footprint*, not worth. A valuable cleanup that reaches outside the change's existing footprint is still out of scope — its value is an argument for doing it *as its own change*, not for smuggling it into this one.

(basis: Robert C. Martin — the **"Boy Scout Rule"**: always leave the code a little cleaner than you found it. Bounded here against [keep-the-diff-focused](keep-the-diff-focused.md) so the rule improves what you touch without licensing the scope creep an unbounded reading invites.)

## The anchors

- *Good:* fixing a bug in a function, you rename its confusingly-named local and delete a now-unreachable branch your fix orphaned — all within the function you were already editing. The diff is still about the fix, only tidier.
- *Bad:* fixing that same bug, you also reformat the whole file, rename a function three modules away "since it bugged me," and refactor an unrelated helper — the two-line fix is now a two-hundred-line diff, and the cleanup that should have been its own change has swallowed the task.
