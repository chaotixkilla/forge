# Resolve conflicts by intent

A merge conflict is not a prompt to pick a side — it is two changes that each meant something, colliding on the same lines. The two mechanical escapes both lose behavior: "accept ours / accept theirs" throws away one side wholesale, so a fix that lived only on the discarded side vanishes with no textual trace; "accept both" concatenates the hunks, so two implementations of the same thing now both run, or an import lands twice. The only resolution that preserves what the code was supposed to do is to reconstruct what *each side intended* and reassemble that intent. This rule pins how, the test for when one side genuinely supersedes the other, and the re-verification that a resolved merge always needs.

## The method — reconstruct intent, don't pick a side

- **Read the change that introduced each side, not just the conflicting hunk.** A hunk in isolation doesn't say why it exists; the commit/PR that added it does. Recover each side's *intent* — what behavior it was trying to establish — before touching the markers.
- **Reassemble both intents.** The resolved code should honor what *both* sides meant, unless one supersedes the other (below). Never resolve by deleting a side you didn't understand — a silent "accept ours" that drops the other side's bugfix is the failure this rule exists to prevent.
- **Reject the mechanical shortcuts.** "Accept both" is not a resolution — it stacks code (duplicate imports, double-executed logic). "Accept current/incoming" is not a resolution — it discards intent. Use them only when you have *confirmed* that side is genuinely the whole answer.

## The supersede test — when one side wins

Preserve both behaviors **unless one side truly supersedes the other**. One side supersedes when its change makes the other's obsolete rather than parallel — e.g. one side deletes the very function the other side was patching, or reimplements the behavior the other side changed. The discriminator: **does keeping both produce a coherent single behavior, or a contradiction/duplication?** Coherent → keep both. Contradiction (both can't be true) or duplication (both do the same job) → keep the superseding side, and state in the merge/commit message which intent was dropped and why, so the drop is a recorded decision, not a silent loss.

## A resolved merge is untested — re-verify it

`(basis: the resolved tree is a THIRD artifact that neither side ever tested — "green on both branches" does not imply "green on the merge," the same mechanism as the semantic conflict in [integrate-against-current-target](integrate-against-current-target.md). Practitioners re-run tests after resolving precisely because the merge/rebase produces code no prior run exercised (corroborated across independent accounts of rebase resolutions that compiled but changed behavior). The concrete guards they cite: run the test suite on the resolved tree before landing; for a rebase, run tests at each replayed commit rather than only at the tip, and reuse a correct resolution across replays rather than re-deriving it per commit.)`

So: after resolving any conflict, **re-run the gate on the resolved result** ([green-before-land](green-before-land.md) then applies to that result) — a conflict resolution is exactly the point where a clean-looking merge hides a broken one.

## The revert-a-merge trap (for the failure path)

When a merge must be undone (a `--on-fail=rollback` on a landed merge, per [failure-policy](../modules/failure-policy.md)), reverting a merge commit is not symmetric: it requires choosing the mainline parent, and once reverted the branch will **not** re-merge cleanly — its commits are treated as already-present and are not reapplied, so re-landing needs a revert-of-the-revert or a rebuilt branch. `(basis: the Linux-kernel "reverting a faulty merge" howto — a reverted merge records that "we never want these changes," so a later merge of the same branch brings in nothing; corroborated widely.)` Flag this rather than issue a naive re-merge that silently lands nothing.
