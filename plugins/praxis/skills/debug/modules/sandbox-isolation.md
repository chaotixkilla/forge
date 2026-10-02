# sandbox-isolation (`--sandbox`)

Activated by `--sandbox`, referenced from the SKILL.md body — this flag changes *every* side-effecting step, not one phase, so it is wired from the body rather than a single activation site.

Deletion test: remove it and debug still runs against the working tree; sandboxing is opt-in safety a flag turns on.

## The delta

Route all side-effecting work — reproduction, instrumentation, risky toggles — into an isolated throwaway environment (a branch, a worktree, or a container) instead of the working tree or shared services. This is local isolation only; it needs no external capability. It matters most for debugging that must *mutate to observe*: adding instrumentation ([make-the-invisible-observable](../rules/make-the-invisible-observable.md)), toggling suspected causes ([change-one-thing-at-a-time](../../../craft/evidence/change-one-thing-at-a-time.md)), or probing against a scratch copy of state, none of which should ever touch the real tree.

## What escapes the sandbox

Isolation must not silently discard the result. At the end of the run, one thing crosses back out of the throwaway environment:

- **The diagnosis** — the mechanism, its certainty, blast radius, and reproduction — always, since it is the run's deliverable.

Everything else — instrumentation, reverted probes, experimental state — is thrown away with the sandbox, and the report says so; debug carries no change out, since making the fix is the recipient's.
