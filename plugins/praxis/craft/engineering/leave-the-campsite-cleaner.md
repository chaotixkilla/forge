# Leave the campsite cleaner

Leave the code a little better than you found it — a vague name on a line you're editing anyway, dead code your change just orphaned, a comment that no longer matches. It's good citizenship, and a real trap: the same impulse, unbounded, turns a one-line fix into a forty-file reformat, and the actual change drowns in the cleanup — the reviewer can't find it, the revert can't isolate it, and a regression can't be bisected to it. Left to taste it goes wrong at both ends: one engineer cleans nothing and lets rot accumulate, another "improves" halfway across the module and buries the task.

## The line: in-scope improvement vs. unrelated refactor

An improvement earns its place in this diff only when **all** of these hold; fail any one and it's a follow-up, not a fold-in:

- **It's in code the change already touches** for its primary purpose — the lines and files the task already makes you edit. Cleanup that reaches into untouched code is a separate errand.
- **It's behavior-preserving or independently safe** — a rename, a dead-code removal (once you know why the code is there: [decode-intent-from-history](decode-intent-from-history.md)), an extracted helper — so it can't be the thing that broke something.
- **It doesn't raise the diff's risk tier.** If folding it in pushes the change up a [change-risk-scale](change-risk-scale.md) tier (a "tidy" that now touches a contract), it's no longer incidental — it's a second change wearing the first one's clothes.

In scope, do it: a clearer name on a line you're already editing, deleting dead code your change just orphaned, fixing a comment your edit just made false. The task already has your hands on these lines, so leaving them better costs nothing extra and adds no files. Out of scope — a cleanup that pulls in files the task didn't touch, or grows the diff materially beyond the change itself — is scope creep however worthy ([keep-the-diff-focused](keep-the-diff-focused.md)): do it as a **separate change** with its own diff and verification ([separate-refactor-from-behavior-change](separate-refactor-from-behavior-change.md)). When an improvement is worth doing but fails the line, don't silently drop it and don't silently do it: **surface it as a follow-up** with the change, so it's captured rather than lost.

`(basis: maintainer, 2026-07-11; Martin, the Boy Scout Rule)`

## Comment curation reaches the enclosing unit

Delete the comments that carry nothing in the smallest **named unit** enclosing your edit — the function or method it lands in, or the case arm where that's the unit. Not the innermost brace block (an `if` body isn't the reach), and not merely the exact lines you edited. Which comments carry nothing is [comment-the-why-not-the-what](comment-the-why-not-the-what.md)'s call, not a fresh judgment here. This doesn't fire when a project has asked for local comment density to be followed (praxis's `output.comments`, read per [report-style-settings](../writing/report-style-settings.md)); at its default it always does.

Comment curation is the one reach that is deliberately wider, and it doesn't generalize. The asymmetry is the point: a bad name or a dead branch gets edited the moment it breaks something, while a comment that merely restates its line never breaks anything and so is never revisited — an exact-lines bound would leave narration to accumulate indefinitely. The reach stops at the enclosing unit precisely so it stays a cleanup and not a sweep; a whole-file pass is the out-of-scope case above, however tempting the file. `(basis: maintainer, 2026-09-01)`

## The fork it sits on

This standard and [smallest-reversible-change](smallest-reversible-change.md) pull in opposite directions on purpose — one biases toward improving, the other toward the minimal edit — and the line above is where they're reconciled. When in genuine doubt on a specific improvement, the tie-breaker is the diff's *legibility to a reviewer*: if folding it in makes the change harder to read as one coherent thing, it's a follow-up.

## Anchors

- *Good:* fixing a bug in a function, you rename its confusingly-named local, delete a now-unreachable branch your fix orphaned, and drop the two comments in that function that only restated the lines beneath them — all within the function you were already editing. The diff is still about the fix, only tidier.
- *Bad:* fixing that same bug, you also reformat the whole file, rename a function three modules away "since it bugged me," and refactor an unrelated helper — the two-line fix is now a two-hundred-line diff, and the cleanup that should have been its own change has swallowed the task.
