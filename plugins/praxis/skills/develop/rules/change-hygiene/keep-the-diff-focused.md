# Keep the diff focused

While making a change, your cursor passes over code that isn't the task: a variable you'd have named differently, a block whose formatting bugs you, a small bug you notice in passing. The judgment this rule governs is which of those edits belong in *this* diff. Left to taste it goes wrong in a predictable direction — the "while I'm here" edit sneaks in, and a three-line feature arrives as a forty-line diff where the real change is buried among reformats and drive-by fixes, so the reviewer can't see the change for the noise and the blast radius quietly widened past what the task justified. Two builders left to instinct draw the line in very different places.

## The discriminator

A line belongs in the diff if **the task would fail without it** — the change doesn't work, doesn't compile, or doesn't meet its acceptance criteria unless that line changes. Apply the test to every edit:

- **Required by the task** — the feature/fix is incomplete or broken without this line. It belongs. This includes the honest ripple: a caller you *must* migrate because you changed a contract ([keep-callers-working](keep-callers-working.md)) is required, not drive-by.
- **A drive-by** — a rename, a reformat, a "while I'm here" fix, a tidy-up of neighbouring code the task never touched. The task passes without it. It does **not** belong in this diff — even when the edit is genuinely an improvement. The improvement isn't wrong; being *here* is.
- **The tidy-up may still be worth doing** — so do it as its own change, before or after, with its own diff and its own verification ([separate-refactor-from-behavior-change](separate-refactor-from-behavior-change.md)). The one exception is an *in-footprint* cleanup — a good-citizen tidy of lines the task already touches — and exactly how far that reaches before it becomes scope creep is [boy-scout-rule-bounded](boy-scout-rule-bounded.md)'s bound to draw, not this rule's to restate.

The cost a drive-by imposes is concrete: it widens the blast radius (more files to regress, more to review), and it buries the real change so a reviewer approves the noise to get to the signal, or a bisect later can't tell the feature from the reformat.

(basis: Google *eng-practices* — small, single-purpose CLs; a change should address **one reviewable concern**, small enough that a reviewer can hold the whole thing and see exactly what it does. The "one concern per change" principle is what a drive-by violates.)

## The anchors

- *Good:* the feature touches only the files the feature needs — the new handler, its caller, its wiring — and every hunk in the diff traces to an acceptance criterion. A reviewer reads it in one sitting and sees exactly one thing happen.
- *Bad:* a diff that adds the feature *and* reformats a neighbouring module you happened to open, *and* renames an unrelated variable that annoyed you. The feature is three files; the diff is nine. The review stalls, and the reformat hides a real change to logic in the same file.
