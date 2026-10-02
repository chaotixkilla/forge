Make the verified change *reviewable and attributable*: an opaque diff with no rationale is one the next person can't trust or safely build on. The deliverable is a clean, self-explaining diff, committed, with the reasoning behind it and the follow-ups it surfaced. Reviewing it, landing it and recording it elsewhere belong to whoever delivers the change.

## Make the diff self-explaining

Read your own change as a hostile reviewer before committing it (**judgment**): is the diff about the one thing it set out to do, or has unrelated cleanup crept in? Are there leftovers — debug prints, dead scaffolding, a half-applied rename? Does each hunk explain itself, or does it need a comment the change should carry? Fold in nothing that fails the [leave-the-campsite-cleaner](../../../craft/engineering/leave-the-campsite-cleaner.md) line; strip what doesn't belong.

## Commit it

**Commit the change locally** — a local commit done directly (ambient plain git, no backend; refactor never pushes), its message by [commits-tell-the-why](../../../craft/engineering/commits-tell-the-why.md) and the commit by the repo's policy ([honor-commit-policy](../../../craft/engineering/honor-commit-policy.md)). **Stage only the paths this change's edits actually modified** — not the whole working set (a `--scope`/`--module` bound can contain files this change never touched) — and leave *all* other uncommitted work untouched, whether unrelated or merely in-scope-but-unedited, so the commit is attributable to this change and nothing else. If `--checkpoint-commit` was set the milestone commits already exist; this is the final attributable commit.

## Surface the follow-ups

Record the out-of-scope needs the change deliberately did *not* fold in ([leave-the-campsite-cleaner](../../../craft/engineering/leave-the-campsite-cleaner.md)) — the deferred cleanups, and coverage the *change itself made necessary*. For a refactor that is rare: the tell is *is the coverage gap new*, not *is the code new*. A behavior-preserving refactor's extracted or relocated code is covered by the same baseline, so its lack of dedicated tests is a **pre-existing** gap — a **routine hygiene note**, surfaced as advice for test design, that does **not** make the run partial.

## The outcome — a decided partition

Every run ends in exactly one of three outcomes. Decide it with two questions, **in order**:

**Q1 — did the in-scope change land?** (get made, reach a trustworthy verdict, and get committed.) A run does **not** land when a gate refused it, for *any* cause:
- `--require-clean` refused a dirty tree ([phase 01](01-locate-and-baseline.md));
- the verdict was **not-verified** or **inconclusive** *and* the correction lies outside this change's scope ([phase 04](04-prove-it-unchanged.md)) — an *in-scope* failure instead loops back to [make-the-change](03-make-the-change.md) and is not terminal;
- the change is `exposed` and no migration path can be built within scope ([phase 03](03-make-the-change.md)).

Any of these → **blocked-and-reported**: report what blocked and what would unblock it, including whom to coordinate with. Nothing further is committed: an inconclusive or not-verified change is left uncommitted in the working tree, so whoever supplies the missing confirmation or fix commits it. Checkpoint commits a `--checkpoint-commit` run already made stay where they are — each is a green step — and the report lists them as the partial history, with the uncommitted remainder. `(basis: derived from a commit here meaning landed)` This outcome is defined by its *cause* — a gate refused — not by a fixed list, so a novel refusal still lands here rather than escaping the partition.

**Q2 — if it landed, did the change surface out-of-scope WORK that still must be done?** — a needed change outside the working set ([leave-the-campsite-cleaner](../../../craft/engineering/leave-the-campsite-cleaner.md)).
- **Yes** → **committed-with-follow-ups**: the in-scope change landed and reached a verdict; the deferred work is returned so it isn't lost.
- **No** → **committed**: the normal landing. A *routine hygiene note* is **not** the deferred work that makes a run partial; it's surfaced as advice and the run is still **committed**.

The two questions partition every run: it either landed (Q1) or it didn't; if it landed, it either carries change-made-necessary follow-up work (Q2) or it doesn't.

## Return

Return the outcome with what a caller needs to deliver the change: the commit, the rationale (what was restructured and why, the risk tier and its reason, the contracts it kept), the verdict with its caveats, the follow-ups and hygiene notes, and, under `--module`, the owners its ownership metadata names.
