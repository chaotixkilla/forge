# github — vcs adapter

Implements the **vcs** capability for GitHub, over the transport configured in `tools.vcs.transport` (cli, api, or mcp). The [vcs](../SKILL.md) skill names the operation and dispatches here; each operation below is one of the vcs capability's requests, translated to GitHub's concrete surface. Resolve exact field/flag names against the live tool at call time (below) — the names here are not frozen.

## Operations

1. **Fetch a change** — given a pull request reference (number), retrieve the unified diff plus the PR title, body, base/head refs, and the change-size metadata the caller cross-checks against (changed-file count, and additions/deletions where available).
   - *cli:* the GitHub CLI's PR view/diff commands (request the diff and the metadata fields the caller needs, including `changedFiles`). *api/mcp:* the pull-request read + files/diff endpoints for the repo and number.
2. **Materialize a change** — given a pull request reference, check its **current head** out into an **isolated working copy** (a worktree) so the caller can read definitions, call sites, and invariants at the reviewed revision without disturbing the user's working tree. Return the working-copy path; the caller discards it when done.
   - *cli:* fetch the PR head and add a detached worktree at it (the GitHub CLI's PR-checkout into, or combined with, a `git worktree` at the fetched head). *api/mcp:* resolve the head SHA from the pull-request read, fetch that ref, and add a worktree at the SHA. Materialize the head the fetched metadata reports — never a pre-existing local branch of the same name, which may lag a force-push.
3. **Post a review summary** — add the caller's summary text to the pull request as a review carrying the caller's **stance** (comment-only, approve, or request-changes — see the stance note below).
4. **Post inline feedback** — attach each item as a review comment anchored to its file and line on the PR's diff, submitted as a single review carrying the caller's **stance**, so they post as one batch, not N notifications.
5. **Set a status** — set a commit status / check-run on the head ref reflecting the caller's pass/fail verdict, so the platform's merge protection can read it. This is best-effort: a failed status post is reported upward but never fabricates or changes the caller's verdict.

**The review stance (operations 3 and 4).** GitHub requires every review submission to declare an event — one of `COMMENT`, `APPROVE`, or `REQUEST_CHANGES`; there is no "just attach comments" call that omits it. The caller passes a capability-neutral **stance** and this adapter maps it: *comment-only* → `COMMENT`, *approve* → `APPROVE`, *request-changes* → `REQUEST_CHANGES`. The caller decides the stance (review names the default and the `--gate` mapping); the adapter never invents one, and never posts through a raw API call that bypasses this operation.

## Failure surface

Report failures upward in capability terms — the caller hears an outcome, never a raw HTTP code:

- **Not authenticated / token missing or lacking scope** → report as "vcs backend unavailable," which the caller's degrade path handles (and which the [vcs](../SKILL.md) skill maps to guiding the user through `init:vcs`).
- **PR or repo not found / wrong repo context** → report "the requested change was not found on the configured provider" rather than a 404; do not fall back to a different change.
- **Rate-limited or transient network failure** → report as a *retryable* vcs failure, distinct from a permanent one, so the caller can back off or degrade.
- **Inline anchor rejected** (a comment on a line outside the diff hunks) → report which items could not be anchored, so the caller can fold them into the summary rather than dropping them.

## Call-time discovery

GitHub's surface shifts (flag names, endpoint shapes, review-submission payloads), so name the operation and its purpose here and resolve the exact parameters when you call: confirm the current diff-fetch flags, the review-comment payload shape (path + line + side for inline), and the check-run vs commit-status choice against the live CLI/API at call time. An adapter that pins today's exact field names ages into a confident wrong call; one that names the operation and re-derives the arguments ages gracefully.
