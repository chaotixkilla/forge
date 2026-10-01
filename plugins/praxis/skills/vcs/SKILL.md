---
name: vcs
description: Carry out a version-control-host operation — fetch or materialize a change, push a branch, open a review request and read its state and feedback, read a target's landing constraint, merge, post review feedback, set a status — via the configured provider's adapter; returns the result. A tool-layer interface skill, called by other skills.
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
2. Take the requested operation and its inputs from the caller — one of: **fetch a change** (a pull request's diff + description, by reference — or, with the description held back, its diff, base and head commits, head branch, author and size alone); **materialize a change** (a pull request's current head, checked out into an isolated working copy whose path is returned); **post a review summary** onto a change; **post inline feedback** anchored to specific file lines of a change; **set a pass/fail status** on a change; **push a branch** to the remote; **open a review request** (title, description, base, head and reviewers; returns its reference); **read a review request** (its state, its approval, and the review feedback on it — summary and inline comments, each with its author and anchor); **read a landing constraint** (whether a target branch requires an approved review or passing checks before a merge); **merge** (an approved review request, or a branch, by the team's strategy: merge commit, squash or rebase)
3. Dispatch to the matching adapter: the concrete provider calls live in adapters/&lt;provider&gt;
4. Return the result to the caller — the fetched change, the posted location/ids, the set status, the opened request's reference, the request's state and feedback, the constraint, or the merged commit — or a capability-level failure the caller can react to (unavailable / not-found / retryable), never a raw provider error
