---
name: project-mgmt
description: Carry out a work-tracking operation — fetch a tracked work-item by reference, update one, or create tracked work-items from an ordered set of units — via the configured provider's adapter; returns the result. A tool-layer interface skill, called by other skills.
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
2. Take the requested operation and its inputs from the caller — one of: **fetch a work-item** (a tracked item by reference — its title, description, acceptance criteria, labels, status); **create work-items** (turn an ordered set of units into tracked items, carrying their dependencies and sequence); **update a work-item** (by reference, set its status or fields, or add a comment)
3. Dispatch to the matching adapter: the concrete provider calls live in adapters/&lt;provider&gt;. With no adapter for the provider, or with the slot's `adapter` set to `learned`, dispatch through the user's learned map instead ([dispatch-through-a-learned-map](../learn-adapter/rules/dispatch-through-a-learned-map.md)), which [learn-adapter](../learn-adapter/SKILL.md) writes at first contact.
4. Return the result to the caller — for a fetch, the item's fields; for an update, the item's reference and the fields as they now stand, with any change the backend refused named; for a create, a **per-unit** outcome: each unit is either created (its reference, plus anything the backend accepted the item but couldn't yet set — a field or a dependency link — flagged against that reference) or not created (a failure — retryable when the cause is transient, or a mismatch for the caller to reconcile when a required field blocked creation). A partial set always returns the references of what it created — so the caller completes or retries only what's flagged, never re-creating — instead of one verdict that hides created items and drives a re-run to duplicate them. Report any capability-level failure (unsupported, when a learned map can't perform it or show a guarantee kept / unavailable / not-found / retryable) in those terms, never a raw provider error

## Guarantees

What every adapter, and every learned map, keeps; an operation that can't be shown to keep one is `unsupported`:

- **A fetch changes nothing.**
- **Create never duplicates**: each item's reference is returned once it exists, before any later step can fail.
- **Update changes only the fields named**, and adds a comment only when asked, on exactly the item the reference resolves to.
- **A field the backend can't hold is named**, never dropped.

**`--dry-run`** runs steps 1–2 and stops: it returns the operation that would be dispatched — its inputs and the provider and transport it would reach — and dispatches nothing, so no backend is written to or read.
