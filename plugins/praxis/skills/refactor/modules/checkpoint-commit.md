# --checkpoint-commit — commit at each green move

Activated by `--checkpoint-commit`, referenced from [make-the-change](../phases/03-make-the-change.md).

The base run commits once, in [commit-and-hand-off](../phases/05-commit-and-hand-off.md). This module adds a **local commit after each catalogue move that leaves the checks green** — the boundary [make-the-change](../phases/03-make-the-change.md) already proves before moving on — so progress is recoverable at the last green move and the change reads as a reviewable sequence of named moves. `(basis: derived from the move boundary the phase checks, as develop's checkpoints follow its verified slices)` Deletion test: remove it and refactor still commits once at hand-off; the per-move commits appear on no default run.

Each checkpoint is a local commit with no configured backend, honoring the project's message convention ([commits-tell-the-why](../../../craft/engineering/commits-tell-the-why.md)) and its commit policy ([honor-commit-policy](../../../craft/engineering/honor-commit-policy.md)). It never pushes. The final attributable commit is still written in commit-and-hand-off.
