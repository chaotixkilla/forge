Make the verified upgrade *reviewable and attributable*: the deliverable is a clean diff — manifest, lockfile and adaptations — committed, with the reasoning behind it and the follow-ups it surfaced. Reviewing it, landing it and recording it elsewhere belong to whoever delivers the change.

## Make the diff self-explaining

Read your own change as a hostile reviewer before committing it (**judgment**): is the diff about this upgrade alone, or has unrelated cleanup crept in? Are there leftovers — a stray debug print, a half-applied adaptation? Fold in nothing that fails the [leave-the-campsite-cleaner](../../../craft/engineering/leave-the-campsite-cleaner.md) line; strip what doesn't belong.

## Commit it

**Commit the change locally** — ambient plain git, no backend; upgrade never pushes — with the lockfile, its message by [commits-tell-the-why](../../../craft/engineering/commits-tell-the-why.md) and the commit by the repo's policy ([honor-commit-policy](../../../craft/engineering/honor-commit-policy.md)). **Stage only the paths this change actually modified** and leave all other uncommitted work untouched, so the commit is attributable to this upgrade and nothing else. If `--checkpoint-commit` was set, the milestone commits already exist; this is the final attributable commit.

## `--changelog`

When `--changelog` is set, add a user-facing changelog entry for the upgrade too — see [changelog-entry](../modules/changelog-entry.md).

## Surface the follow-ups

Record the out-of-scope needs the upgrade deliberately did *not* fold in: the next major still to take in sequence, a co-importer a shared bump motivates moving, a labeled stopgap's real fix, and coverage the upgrade itself made necessary. A pre-existing gap the upgrade merely revealed is a **routine hygiene note**, surfaced as advice for test design, and doesn't make the run partial.

## The outcome — a decided partition

Every run ends in exactly one of three outcomes. Decide it with two questions, **in order**:

**Q1 — did the in-scope upgrade land?** (get made, reach a trustworthy verdict, and get committed.) A run does **not** land when a gate refused it, for *any* cause: `--require-clean` refused a dirty tree; the verdict was **not-verified** or **inconclusive** and the correction lies outside this change's scope; or the upgrade is `exposed` and no migration path can be built within scope, including a bump that moves a separately-deploying co-importer. Any of these → **blocked-and-reported**: report what blocked and what would unblock it, including whom to coordinate with (the owners of a co-importer the bump would move). Nothing further is committed: an inconclusive or not-verified change is left uncommitted in the working tree, so whoever supplies the missing confirmation or fix commits it. Checkpoint commits a `--checkpoint-commit` run already made stay where they are — each is a green step — and the report lists them as the partial history, with the uncommitted remainder. `(basis: derived from a commit here meaning landed)`

**Q2 — if it landed, did it surface out-of-scope WORK that still must be done?**
- **Yes** → **committed-with-follow-ups**.
- **No** → **committed**. A routine hygiene note doesn't make a run partial.

## Return

Return the outcome with what a caller needs to deliver the change: the commit, the versions moved, the rationale (the changes taken and their sources, the risk tier and its reason), the verdict with its caveats, the follow-ups and hygiene notes, and, under `--module`, the owners its ownership metadata names.
