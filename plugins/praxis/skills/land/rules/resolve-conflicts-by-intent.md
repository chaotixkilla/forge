# Resolve conflicts by intent

A merge conflict is two changes that each meant something, colliding on the same lines, and the two mechanical escapes both lose behavior: "accept ours / accept theirs" throws away one side wholesale, so a fix that lived only on the discarded side vanishes with no textual trace; "accept both" concatenates the hunks, so two implementations of the same thing now both run, or an import lands twice.

## The method — reconstruct intent, don't pick a side

- **Read the change that introduced each side, not just the conflicting hunk.** A hunk in isolation doesn't say why it exists; the commit/PR that added it does. Recover each side's *intent* — what behavior it was trying to establish — before touching the markers.
- **Reassemble both intents.** The resolved code should honor what *both* sides meant, unless one supersedes the other (below). Never resolve by deleting a side you didn't understand.
- **Reject the mechanical shortcuts.** Neither "accept both" nor "accept current/incoming" is a resolution. Use them only when you have *confirmed* that side is genuinely the whole answer.

## The supersede test — when one side wins

Preserve both behaviors **unless one side truly supersedes the other**. One side supersedes when its change makes the other's obsolete rather than parallel — e.g. one side deletes the very function the other side was patching, or reimplements the behavior the other side changed. The discriminator: **does keeping both produce a coherent single behavior, or a contradiction/duplication?** Coherent → keep both. Contradiction (both can't be true) or duplication (both do the same job) → keep the superseding side, and state in the merge/commit message which intent was dropped and why, so the drop is a recorded decision, not a silent loss.

## A resolved merge is untested — re-verify it

The resolved tree is a third artifact neither side ever tested — the same mechanism as the semantic conflict in [integrate-against-current-target](integrate-against-current-target.md). So after resolving any conflict, **re-run the gate on the resolved result** ([green-before-land](green-before-land.md) then applies to that result). `(basis: practitioner accounts of rebase resolutions that compiled but changed behavior, whose guards for a rebase are testing each replayed commit and reusing a correct resolution across replays)`

## The revert-a-merge trap (for the failure path)

When a merge must be undone (a `--on-fail=rollback` on a landed merge, per [failure-policy](../modules/failure-policy.md)), reverting a merge commit is not symmetric: it requires choosing the mainline parent, and once reverted the branch will **not** re-merge cleanly — its commits are treated as already-present and are not reapplied, so re-landing needs a revert-of-the-revert or a rebuilt branch. `(basis: the Linux kernel's "reverting a faulty merge" howto)` Flag this rather than issue a naive re-merge that silently lands nothing.
