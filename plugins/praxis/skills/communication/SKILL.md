---
name: communication
description: Carry out a messaging operation — read a discussion thread, post a message or status update — against the configured conversation backend via its provider's adapter; returns the result. A tool-layer interface skill, called by other skills.
metadata:
  flags:
    --dry-run: show the operation that would be performed, without performing it
  config_requires:
    - key: tools.communication
      if_missing: guide via init:communication, else block
---
Usage & examples — when to reach for this skill, and concrete invocations: see [usage.md](usage.md).

A thin port over the conversation backend: it names the capability, and the configured provider's adapter holds the concrete calls. Callers name the operation they need; this skill resolves it to the backend.

1. Resolve the provider: read tools.communication — the provider + transport configured for this project
2. Take the requested operation and its inputs from the caller — one of: **read a thread** (a discussion thread's messages, participants, and ordering, by reference — for the caller to distill its decisions, constraints, and open points); **post a message** (a notification or status update to a channel or a person)
3. Dispatch to the matching adapter: the concrete provider calls live in adapters/&lt;provider&gt;
4. Return the result to the caller — for a read, the thread's messages, participants, and ordering; for a post, the delivered message's reference (a stable id or link), always returned once the message is delivered even if a follow-on step (fetching the link) couldn't complete — that step is flagged against the reference so the caller never re-posts and duplicates the message — or a capability-level failure the caller can react to: unavailable, not-found, retryable (back off and re-attempt), or permanent (the caller must reconcile, not retry), never a raw provider error
