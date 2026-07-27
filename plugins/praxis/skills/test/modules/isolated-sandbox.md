# isolated-sandbox (`--sandbox`)

Activated by `--sandbox`, referenced from [set-up-the-harness](../phases/04-set-up-the-harness.md).

The base run uses the ambient environment. This module runs the suite in a disposable, network/filesystem-isolated **local** environment with seeded fixtures, so the result is reproducible and side-effect-free regardless of the host machine. Deletion test: without the flag, [set-up-the-harness](../phases/04-set-up-the-harness.md) provisions the ambient environment; the isolation is added behavior. It is resolved **locally** — a scratch environment test provisions itself — and declares no backend; this is the same config-less local resolution the plugin's other `--sandbox` skills use, not a delegated CI or containerization capability.

## The delta

Provision a throwaway environment before the run and tear it down after, so the run cannot touch real state and two runs on different hosts produce the same result. What "isolated" concretely guarantees, pinned so two cold runs provision the same thing:

- **no real network** — external calls are blocked or routed to the doubles [set-up-the-harness](../phases/04-set-up-the-harness.md) established at the unmanaged seams ([mock-at-the-boundary](../rules/mock-at-the-boundary.md)); the run never depends on a live external service.
- **a throwaway filesystem** — writes land in a scratch location discarded at the end; the real working tree and any real data store are untouched.
- **seeded fixtures** — the run's inputs come from fixtures provisioned into the sandbox, not from ambient host state, so the run is reproducible.
- **reset between runs** — under `--until` looping, each iteration starts from the same seeded state, so a later iteration cannot inherit an earlier one's residue.

## Degraded case

If isolation cannot be provisioned (no way to create a throwaway workspace or block the network), do not silently run un-isolated. **Default: stop and report** — state that `--sandbox` was requested but isolation is unavailable, and do not run, because the caller asked for isolation precisely so the run cannot touch real state, and running un-isolated would defeat that request and risk real side effects. The caller can then re-invoke without `--sandbox` to accept an ambient run; and if the caller has already said an ambient fallback is acceptable, run ambient and flag in the verdict that isolation and reproducibility are unverified. Either way the loss of isolation is reported, never hidden. `(basis: fail-safe on an explicit safety request — a requested isolation guarantee that cannot be met defaults to not-running rather than silently running without the guarantee; the caller who asked for the sandbox owns the decision to proceed without it.)`
