---
name: vcs
description: Carry out a version-control-host operation — fetch or materialize a change, push a branch, open a review request and read its state, feedback and what it builds on, read a target's landing constraint, merge, post review feedback, set a status — via the configured provider's adapter; returns the result. A tool-layer interface skill, called by other skills.
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
2. Take the requested operation and its inputs from the caller — one of: **fetch a change** (a review request's diff + description, by reference — or, with the description held back, its diff, base and head commits, head branch, author and size alone); **materialize a change** (a review request's current head, checked out into an isolated working copy whose path is returned); **post a review summary** onto a change, with its stance (comment-only, approve, or request changes) and, optionally, the commit it reviewed, which it is posted on instead of the change's current head; **post inline feedback** anchored to specific file lines of a change, with the same stance and commit inputs; **set a pass/fail status** on a change; **push a branch** to the remote; **open a review request** (title, description, base, head and reviewers; returns its reference); **read a review request** (by reference, or the open one whose head is a given branch — its base branch, its state, its approval, and the review feedback on it — summary and inline comments, each with its author, its anchor and the commit it was posted on); **read what a review request builds on** (by reference: the references of the open requests it builds on, nearest first, and nothing of their rationale); **read a landing constraint** (whether a target branch requires an approved review or passing checks before a merge); **merge** (an approved review request, or a branch, by the team's strategy: merge commit, squash or rebase)
3. Dispatch to the matching adapter: the concrete provider calls live in adapters/&lt;provider&gt;
4. Return the result to the caller — the fetched change, the posted location/ids, the set status, the opened request's reference, the request's state and feedback, the requests it builds on, the constraint, or the merged commit — or a capability-level failure, never a raw provider error. The failures, as a cascade where the first "no" wins: reached an authenticated backend? (no → **unavailable**) does the named target exist? (no → **not-found**) did a transient fault stop it? (yes → **retryable**) is the request itself invalid as asked? (yes → **permanent**, the caller must change it) did the host decline it for a stated reason — a merge a requirement blocks, a push that needs a reconcile, a description it can't hold back? (yes → **refused**, returned with the reason; never retried with a bypass) did all of it complete? (no → **partial**: inline feedback with some anchors rejected, or a builds-on read cut short, returned with what posted or was read and what wasn't). The adapter maps its failure surface onto these. `(basis: derived from the adapter's failure surface)`

**`--dry-run`** runs steps 1–2 and stops: it returns the operation that would be dispatched — its inputs and the provider and transport it would reach — and dispatches nothing, so no backend is written to or read.
