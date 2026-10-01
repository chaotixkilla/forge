# require-clean (`--require-clean`)

Activated by `--require-clean`, referenced from [read-the-upgrade-path](../phases/01-read-the-upgrade-path.md).

The base run makes its change against whatever state the working tree is in. This module adds a **precondition gate** at the very top of the run: refuse to start unless the tree is clean, so the upgrade can't get entangled with pre-existing uncommitted work and the resulting diff stays wholly attributable to this change. **Deletion test:** remove it and upgrade still runs against any tree state; the refuse-to-start gate is the added, flag-gated behavior.

## The delta

- **Check tree state before reading anything for editing.** Read the working-tree status directly (an ambient local read) as the first action of [read-the-upgrade-path](../phases/01-read-the-upgrade-path.md), before locating or reproducing.
- **Clean means no uncommitted changes** — no modified, staged, or untracked files in the working tree (standard clean-tree semantics). Under a `--scope`/`--module` bound, restrict the check to files within the bound; a bare `--require-clean` (no bound) treats *any* untracked file as dirty.
- **On a dirty tree, refuse and report** — stop with a specific message naming what's dirty and the two ways forward (commit or set aside the pre-existing work, or re-run without `--require-clean` to proceed anyway). It **refuses; it does not stash** — moving the user's work aside is a decision that's theirs, not this gate's.
- **Edge (no readable tree state):** if the working tree can't be read as version-controlled (not a repository, or its status is unavailable), the gate can't certify the tree is clean. The gate then fails, since a gate that can't check doesn't pass: stop and report that the precondition can't be evaluated, never proceeding as if clean.
