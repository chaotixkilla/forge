---
name: ci
description: Carry out a continuous-integration operation — trigger or read the checks for a ref, wait for a run to settle, promote a build to an environment, or fetch a run's logs — against the configured CI/CD provider via its adapter; returns the result. A tool-layer interface skill, called by other skills.
metadata:
  flags:
    --dry-run: show the operation that would be performed, without performing it
  config_requires:
    - key: tools.ci
      if_missing: guide via init:ci, else block
---
Usage & examples — when to reach for this skill, and concrete invocations: see [usage.md](usage.md).

A thin port over the continuous-integration backend: it names the capability, and the configured provider's adapter holds the concrete calls. Callers name the operation they need; this skill resolves it to the backend.

1. Resolve the provider: read tools.ci — the provider + transport configured for this project
2. Take the requested operation and its inputs from the caller — one of: **run the checks** (trigger the checks for a ref, or read a run's current status and pass/fail verdict, by reference); **await a run** (block until a run settles within a timeout, returning its terminal verdict — for a caller staying attached after landing); **promote to an environment** (trigger, or read the state of, a deployment/promotion of a ref to a named environment); **fetch a run's logs** (the log output of a run, or of a failed job within it, by reference — so a caller can diagnose or report a failure)
3. Dispatch to the matching adapter: the concrete provider calls live in adapters/&lt;provider&gt;. With no adapter for the provider, or with the slot's `adapter` set to `learned`, dispatch through the user's learned map instead ([dispatch-through-a-learned-map](../learn-adapter/rules/dispatch-through-a-learned-map.md)), which [learn-adapter](../learn-adapter/SKILL.md) writes at first contact.
4. Return the result to the caller — the run's verdict — **pass**, **fail**, or **unsettled** (queued or still running when read, or when an await ends first) — the promotion's state — **succeeded**, **failed**, **pending** (awaiting an approval or an enforced delay) or **in progress** — with its resolved target environment, or the fetched logs. Or a capability-level failure, never a raw provider error: **unsupported** (a learned map can't perform it, or can't show a guarantee kept, named), **unavailable**, **not-found**, **retryable**, or **permanent** (the request is invalid as asked; the caller must change it). A run that concludes red is a result, not a failure. `(basis: derived from the adapter's states)`

## Guarantees

What every adapter, and every learned map, keeps; an operation that can't be shown to keep one is `unsupported`:

- **Reads change nothing**: reading a run, awaiting it and fetching its logs trigger nothing.
- **Run the checks triggers only for the ref given.**
- **Promote targets only the named environment**, and never skips an approval or an enforced delay.
- **Pass means every required check succeeded**; a run still going, or an await that times out, is `unsettled`; a red run is a result, never a failure outcome.

**`--dry-run`** runs steps 1–2 and stops: it returns the operation that would be dispatched — its inputs and the provider and transport it would reach — and dispatches nothing, so no backend is written to or read.
