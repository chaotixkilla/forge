---
name: vcs
description: Carry out a version-control-host operation — fetch a change for review, post review feedback, set a status — via the configured provider's adapter; returns the result. A tool-layer interface skill, called by other skills.
metadata:
  flags:
    --dry-run: show the operation that would be performed, without performing it
  config_requires:
    - key: tools.vcs
      if_missing: guide via init:vcs, else block
---
Usage & examples — when to reach for this skill, and concrete invocations: see [usage.md](usage.md).

A thin port over the version-control host: it names the capability, and the configured provider's adapter holds the concrete calls. Callers name the operation they need; this skill resolves it to the backend.

1. Resolve the provider: read tools.vcs — the provider + transport configured for this project
2. Take the requested operation and its inputs from the caller — one of: **fetch a change** (a pull request's diff + description, by reference); **post a review summary** onto a change; **post inline feedback** anchored to specific file lines of a change; **set a pass/fail status** on a change
3. Dispatch to the matching adapter: the concrete provider calls live in adapters/&lt;provider&gt;
4. Return the result to the caller — the fetched change, the posted location/ids, or the set status — or a capability-level failure the caller can react to (unavailable / not-found / retryable), never a raw provider error
