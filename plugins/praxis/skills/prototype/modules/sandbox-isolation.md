# sandbox-isolation (`--sandbox`)

Activated by `--sandbox`, referenced from [build-the-spike](../phases/04-build-the-spike.md) (where the isolated environment is created and the spike built inside it); its teardown is in [capture-and-discard](../phases/06-capture-and-discard.md).

The base spike builds and runs in place. This module runs it in a throwaway isolated environment so it can't touch real state and is trivial to discard wholesale — the safety posture for a spike that would otherwise mutate a real workspace, database, or service. **Deletion test:** remove it and prototype still builds and runs the spike (in place); the isolation and the wholesale teardown are the added, flag-gated behavior.

## The delta

- **Create an isolated throwaway environment before building** — a place the spike can write, run, and fail without reaching real state — and build the spike inside it ([build-the-spike](../phases/04-build-the-spike.md)).
- **Tear it down wholesale at the end** — discarding the environment discards the spike code with it, which is the disposability the spike wants ([favor-disposability](../rules/favor-disposability.md), [capture-and-discard](../phases/06-capture-and-discard.md)).

## The isolation mechanism

Resolve isolation **locally**, and name the capability, never a concrete tool: a scratch workspace or a throwaway local runtime the spike runs inside. If the caller needs *version-controlled* isolation (a discardable branch), that is **wholesale delegation to the `vcs` port** — which owns the `tools.vcs` prerequisite — so prototype declares no `config_requires` in either case; it either isolates locally or hands the branch operation to the doer that owns it.

`(basis: ratified by the maintainer, 2026-07-09. Default isolation = a local scratch workspace: config-less, trivially discardable, and matching the disposable ethos. The vcs-branch variant is offered as wholesale delegation (config stays shed). Either way prototype declares nothing — this is the config-adjacent call the maintainer ratified deliberately rather than by default.)`
