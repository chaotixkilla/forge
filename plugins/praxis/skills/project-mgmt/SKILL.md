---
name: project-mgmt
description: Carry out a work-tracking operation — fetch a tracked work-item by reference, create tracked work-items from an ordered set of units — via the configured provider's adapter; returns the result. A tool-layer interface skill, called by other skills.
metadata:
  flags:
    --dry-run: show the operation that would be performed, without performing it
  config_requires:
    - key: tools.project_mgmt
      if_missing: guide via init:project_mgmt, else block
---
Usage & examples — when to reach for this skill, and concrete invocations: see [usage.md](usage.md).

A thin port over the work-tracking backend: it names the capability, and the configured provider's adapter holds the concrete calls. Callers name the operation they need; this skill resolves it to the backend.

1. Resolve the provider: read tools.project_mgmt — the provider + transport configured for this project
2. Take the requested operation and its inputs from the caller — one of: **fetch a work-item** (a tracked item by reference — its title, description, acceptance criteria, labels, status); **create work-items** (turn an ordered set of units into tracked items, carrying their dependencies and sequence)
3. Dispatch to the matching adapter: the concrete provider calls live in adapters/&lt;provider&gt;
4. Return the result to the caller — for a fetch, the item's fields; for a create, a **per-unit** outcome: each unit is either created (its reference, plus anything the backend accepted the item but couldn't yet set — a field or a dependency link — flagged against that reference) or not created (a failure — retryable when the cause is transient, or a mismatch for the caller to reconcile when a required field blocked creation). A partial set always returns the references of what it created — so the caller completes or retries only what's flagged, never re-creating — instead of one verdict that hides created items and drives a re-run to duplicate them. Report any capability-level failure (unavailable / not-found / retryable) in those terms, never a raw provider error
