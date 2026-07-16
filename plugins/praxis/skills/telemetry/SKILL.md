---
name: telemetry
description: Carry out a telemetry read — fetch an observability signal (a metric, trace, error-aggregate, or dashboard) or a log stream, by reference — from the configured provider's adapter; returns the anchored evidence. A tool-layer interface skill, called by other skills.
metadata:
  flags:
    --dry-run: show the read that would be performed, without performing it
  config_requires:
    - key: tools.telemetry
      if_missing: guide via init:telemetry, else block
---
Usage & examples — when to reach for this skill, and concrete invocations: see [usage.md](usage.md).

A thin port over the observability backend: it names the capability, and the configured provider's adapter holds the concrete calls. Callers name the read they need; this skill resolves it to the backend. It reads only — it never writes to the backend.

1. Resolve the provider: read tools.telemetry — the provider + transport configured for this project
2. Take the requested read and its inputs from the caller — one of: **read a signal** (a metric, trace, error-aggregate, or dashboard by reference — its onset/first-seen, frequency or rate, affected scope, correlated signals, and sample traces/exemplars); **read a log stream** (a log source by reference, within a time or correlation window — its entries in order, plus the error signatures and correlation IDs within them)
3. Dispatch to the matching adapter: the concrete provider calls live in adapters/&lt;provider&gt;
4. Return the result to the caller — for a signal read, the signal's fields (onset, frequency, scope, correlated signals, sample traces); for a log read, the entries in order with their signatures and correlation IDs — or a capability-level failure the caller can react to (unavailable / not-found / retryable), never a raw provider error
