# vcs — usage

A tool-layer interface skill: the single place the version-control host is reached. It fronts the `vcs` capability so a workflow skill names *what it needs from the host* and this skill resolves it to whichever provider is configured — the same ports-and-adapters seam `artifacts` provides for artifacts.

## When to use
- A skill needs to reach the code-hosting backend and should stay provider-agnostic: fetch a change to review, post review feedback back onto it, or set a merge-gating status. Call `vcs` with the operation instead of talking to a provider directly.
- You are adding a new skill that touches the host (land, review, security-review): route its host operations through here rather than giving it its own adapter, so a provider swap changes one file.

## Not for / use instead
- Publishing a document/artifact (a spec, plan, or report page tree) to a knowledge or artifacts backend → **artifacts** (that is the artifacts port; this is the code-host port).
- Reading the *local* working-tree diff or history, or **committing locally**, → that is ambient (plain git, no configured backend; any skill does it directly). git is praxis's declared local version-control substrate, so naming it for local operations across the skills is deliberate, not a provider leak; the hosted platforms on top of it stay behind this port. `(basis: maintainer, 2026-10-01: git declared as the ambient substrate; tool-leak finding accepted on record)` This skill is for *hosted* operations — the ones that reach the remote: push a ref, open or merge a review request, post a comment, set a status. The line is the host, not the tool: a local commit touches no host, so it is ambient even though it is a write; pushing that commit is a host operation and comes here. `(basis: maintainer, 2026-07-11)`
- Deciding *what* to post, *with which stance*, or *whether* to gate → that is the calling skill's judgment (e.g. **review** triages and ranks findings); this skill only carries out the host operation it is handed.

## Operations (extended as consumers need them)
Today it serves the operations review, land and work's acts require; new consumers add their operations to the same interface and adapter rather than forking a new one:
`fetch a change` — a review request's diff + description, by reference; or, with the description held back, its diff, base and head commits, head branch, author and size alone.
`materialize a change` — a review request's current head, checked out into an isolated working copy; returns its path.
`post a review summary` — one summary onto a change, with its stance: comment-only, approve or request changes, on the commit it reviewed when the caller names one.
`post inline feedback` — findings anchored to exact file:line on a change's diff, with the same stance and commit.
`set a status` — a pass/fail check on a change's head, for merge protection to read.
`push a branch` — publish a local branch to the remote.
`open a review request` — a review request from a head branch onto a base, with its title, description and reviewers; returns its reference.
`read a review request` — its state (open, merged, closed), its approval, and the review feedback on it, summary and inline, each with the commit it was posted on.
`read what a review request builds on` — the references of the open requests it builds on, nearest first, and nothing of their rationale.
`read a landing constraint` — whether a target branch requires an approved review or passing checks before a merge.
`merge` — an approved review request, or a branch, by the team's strategy.

## Gotchas
- **It blocks without a configured backend.** `config_requires: tools.vcs` with `if_missing: guide via init:vcs, else block` — a host port with no host has nothing to do. Callers that have a meaningful local fallback (e.g. review returning a local report) catch the unavailable signal and degrade on *their* side; this skill itself blocks.
- **It performs side effects.** Pushing, opening and merging, posting comments and setting statuses mutate the remote. Use `--dry-run` to preview the operation without performing it.
- **It reports failures in capability terms.** The caller hears "the change wasn't found" or "the backend is unavailable," never a provider error code — so the caller's degrade logic never has to learn a provider's vocabulary.
- **Provider coverage is by adapter.** Whichever providers have an adapter under `adapters/` are supported; adding a provider is a new adapter, no change to callers.
