# --checkpoint-commit — commit at each verified slice

`--checkpoint-commit` records a commit at every verified-slice boundary in phase 3, instead of only at landing. Two things follow: progress is recoverable — a slice that goes wrong later can be rolled back to its last green boundary — and the history reads as the build's actual shape, one commit per proven unit. A verified slice ([verified-slice](../rules/verified-slice.md)) is exactly the right commit boundary: it is the smallest independently-green state, so each checkpoint is a point the tree is known-good.

## Capability, not tool

The commit is a **local commit** — ambient plain git, needing no configured backend, exactly as develop reads the working tree. It **commits locally only**: no push, no review request, no merge. Each checkpoint message states the slice's intent, written by [commits-tell-the-why](../../../craft/engineering/commits-tell-the-why.md) — whose format resolution decides between the house baseline and a convention the history shows — and each commit honors the repo's policy ([honor-commit-policy](../../../craft/engineering/honor-commit-policy.md)).

## The commit-granularity fork — routed, not resolved

Whether the finished change lands as **per-slice checkpoint commits** (this flag's default) or as **one squashed commit** is a genuine, contested fork, and develop does not pick a house winner:

- **Per-slice checkpoints (atomic commits).** Each verified slice is its own commit; history preserves the build's steps, each commit is individually revertible, and — every slice being green — a bisect never lands on a broken commit. Cost: the trunk history carries intermediate states some teams consider noise, and a bisect crosses more commits. Best where the review unit is the commit and recoverability matters. (basis: the Linux kernel's `submitting-patches`)
- **Squash to one coherent commit.** The slices collapse into a single commit at hand-off; the trunk sees one clean change, revertible by a single hash. Cost: the build's intermediate recoverable states are lost from history. Best where the review unit is the whole change and the team keeps a linear, one-change-per-commit trunk. (basis: trunk-based development's squash-merge convention)

**Routing rule (non-gating): surrounding convention → house rule → maintainer.** Read the repo's existing history — if commits are habitually squashed at merge, checkpoint locally for recoverability but expect the squash downstream; if the trunk preserves per-step commits, keep the checkpoints. Absent a clear signal, `--checkpoint-commit` keeps the per-slice commits (its literal behavior) and notes that the squash decision belongs to `land` / the team, since the actual merge-time collapse is downstream of develop: this flag governs only whether checkpoints are recorded during the build. `(basis: maintainer, 2026-07-10)`

Without `--checkpoint-commit`, phase 3 records no intermediate commits and the change is committed once at landing — the base behavior; the flag adds the per-slice commits, which appear on no default run.
