# --checkpoint-commit — commit at each green step of the upgrade

Activated by `--checkpoint-commit`, referenced from [bump-and-fix](../phases/03-bump-and-fix.md).

The base run commits once, in [commit-and-hand-off](../phases/05-commit-and-hand-off.md). This module adds a **local commit at each step of the upgrade that leaves the checks green**: after each major version taken in sequence, and, within a version, after each call-site adaptation that brings its consumers back to green. So progress is recoverable at the last green step and the upgrade reads as a reviewable sequence. A bump whose consumers need no adaptation is one step and one checkpoint. `(basis: derived from the steps the phase already proves green, as develop's checkpoints follow its verified slices)` Deletion test: remove it and upgrade still commits once at hand-off; the per-step commits appear on no default run.

Each checkpoint is a local commit with no configured backend, honoring the project's message convention ([commits-tell-the-why](../../../craft/engineering/commits-tell-the-why.md)) and its commit policy ([honor-commit-policy](../../../craft/engineering/honor-commit-policy.md)). It never pushes. The final attributable commit is still written in commit-and-hand-off.
