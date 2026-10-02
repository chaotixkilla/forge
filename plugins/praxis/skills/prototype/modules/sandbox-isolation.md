# sandbox-isolation (`--sandbox`)

Activated by `--sandbox`, referenced from [build-the-spike](../phases/04-build-the-spike.md) (where the isolated environment is created and the spike built inside it); its teardown is in [capture-and-discard](../phases/06-capture-and-discard.md).

The base spike builds and runs in place. This module runs it in a throwaway isolated environment so it can't touch real state and is trivial to discard wholesale — the safety posture for a spike that would otherwise mutate a real workspace, database, or service. **Deletion test:** remove it and prototype still builds and runs the spike (in place); the isolation and the wholesale teardown are the added, flag-gated behavior.

## The delta

- **Create an isolated throwaway environment before building** — a place the spike can write, run, and fail without reaching real state — and build the spike inside it ([build-the-spike](../phases/04-build-the-spike.md)).
- **Tear it down wholesale at the end** — discarding the environment discards the spike code with it, which is the disposability the spike wants ([favor-disposability](../rules/favor-disposability.md), [capture-and-discard](../phases/06-capture-and-discard.md)).

## The isolation mechanism

Resolve isolation **locally** by default, and name the capability, never a concrete tool: a scratch workspace or a throwaway local runtime the spike runs inside. If the caller needs *version-controlled* isolation, cut a discardable local branch — ambient local version control, no port, since nothing leaves the machine — and delete it at discard. prototype declares no `config_requires` either way.

`(basis: maintainer, 2026-07-09)`
