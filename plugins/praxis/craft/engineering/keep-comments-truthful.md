# Keep comments truthful

When you change a line of code, the judgment this rule governs is what to do about the comment sitting next to it. The failure when it's left to taste: one engineer edits the logic and moves on, leaving a comment that now describes the *old* behavior; the next reader trusts the comment over the code (that's what comments are *for*), and reasons from a false premise. A comment that lies is worse than no comment, because no comment forces the reader to actually read the code.

## The discriminator

Any comment **adjacent to code you touched** must be re-read and reconciled with the new behavior — the trigger is *proximity to the change*, not whether you happened to notice it. For each such comment, one question: **does it still hold?**

- **Still true — leave it.** The change didn't touch what the comment claims. Done.
- **Now contradicts the code — fix it or delete it.** A comment that describes behavior the code no longer has actively misleads: it's a defect, carrying the same weight as a name that lies about what it names ([avoid-misleading-names](avoid-misleading-names.md)). If the *why* it captured is still worth keeping, update it to match. If it isn't worth the words anymore, delete it — a stale comment removed is debris cleared ([leave-no-debris](leave-no-debris.md)), not information lost.
- **Never leave a comment you know is now false**, even "temporarily." The gap between changing code and fixing its comment is exactly where the lie ships. Reconcile it in the same change, not "later".

(basis: convergent craft consensus: Fowler, *Refactoring*; Martin, *Clean Code*)

## The anchors

- *Good:* you change a function from retrying 3 times to retrying until a deadline; the comment above it that said "retries 3 times" gets rewritten to "retries until the deadline" in the same edit — code and prose land together, both true.
- *Bad:* the same logic change ships with the "retries 3 times" comment untouched. Six months later a reader debugging a slow request trusts the comment, assumes a bounded 3 attempts, and looks everywhere *but* the real cause. The comment didn't just fail to help — it steered the reader wrong.
