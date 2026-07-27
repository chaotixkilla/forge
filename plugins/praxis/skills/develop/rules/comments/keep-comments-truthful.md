# Keep comments truthful

When you change a line of code, the judgment this rule governs is what to do about the comment sitting next to it. The reflex is to touch only the code and leave the prose alone — and that reflex is how comments go stale. The failure when it's left to taste: one builder edits the logic and moves on, leaving a comment that now describes the *old* behavior; the next reader trusts the comment over the code (that's what comments are *for*), and reasons from a false premise. A comment that lies is worse than no comment, because no comment forces the reader to actually read the code. Two builders diverge on whether the neighboring comment is their responsibility. This rule pins the discriminator.

## The discriminator

Any comment **adjacent to code you touched** must be re-read and reconciled with the new behavior — the trigger is *proximity to the change*, not whether you happened to notice it. For each such comment, one question: **does it still hold?**

- **Still true — leave it.** The change didn't touch what the comment claims. Done.
- **Now contradicts the code — fix it or delete it.** A comment that describes behavior the code no longer has actively misleads: it's a defect, carrying the same weight as a name that lies about what it names ([avoid-misleading-names](../naming/avoid-misleading-names.md)). If the *why* it captured is still worth keeping, update it to match. If it isn't worth the words anymore, delete it — a stale comment removed is debris cleared ([leave-no-debris](../change-hygiene/leave-no-debris.md)), not information lost.
- **Never leave a comment you know is now false**, even "temporarily." The gap between changing code and fixing its comment is exactly where the lie ships. Reconcile it in the same change, not "later" — later is when the reader is already misled.

(basis: convergent craft consensus — Fowler, *Refactoring* treats stale comments as a smell to remove with the code; Martin, *Clean Code* — a comment that has drifted from the code is a lie, and an old false comment is worse than no comment because readers trust it. A comment that lies is a defect, weighted like a misleading name.)

## The anchors

- *Good:* you change a function from retrying 3 times to retrying until a deadline; the comment above it that said "retries 3 times" gets rewritten to "retries until the deadline" in the same edit — code and prose land together, both true.
- *Bad:* the same logic change ships with the "retries 3 times" comment untouched. Six months later a reader debugging a slow request trusts the comment, assumes a bounded 3 attempts, and looks everywhere *but* the real cause. The comment didn't just fail to help — it steered the reader wrong.
