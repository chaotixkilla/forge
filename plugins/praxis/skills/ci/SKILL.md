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
3. Dispatch to the matching adapter: the concrete provider calls live in adapters/&lt;provider&gt;
4. Return the result to the caller — the run's status and pass/fail verdict, the settled terminal outcome, the promotion's state and resolved target environment, or the fetched logs — or a capability-level failure the caller can react to (unavailable / not-found / retryable), never a raw provider error
