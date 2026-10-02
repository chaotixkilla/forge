# github — vcs adapter

Implements the **vcs** capability for GitHub, over the transport configured in `tools.vcs.transport` (cli, api, or mcp). The [vcs](../SKILL.md) skill names the operation and dispatches here. Resolve exact field/flag names against the live tool at call time (below) — the names here are not frozen.

## Operations

1. **Fetch a change** — given a pull request reference (number), retrieve the unified diff plus the PR title, body, base/head refs, and the change-size metadata the caller cross-checks against (changed-file count, and additions/deletions where available).
   - *cli:* the GitHub CLI's PR view/diff commands (request the diff and the metadata fields the caller needs, including `changedFiles`). *api/mcp:* the pull-request read + files/diff endpoints for the repo and number.
   - *With the description held back*, return the diff, the base and head commits, the head branch, the author and the size metadata only, and never request the title or body. *cli:* name only those fields in the PR view request. *api:* select only those fields (a GraphQL pull-request query takes a field list; the REST diff media type returns the diff alone). *mcp:* only through a read the server offers that leaves the body out; without one, this is the failure below, never a full read with the body ignored.
2. **Materialize a change** — given a pull request reference, check its **current head** out into an **isolated working copy** (a worktree) so the caller can read definitions, call sites, and invariants at the reviewed revision without disturbing the user's working tree. Return the working-copy path; the caller discards it when done.
   - *cli:* fetch the PR head and add a detached worktree at it (the GitHub CLI's PR-checkout into, or combined with, a `git worktree` at the fetched head). *api/mcp:* resolve the head SHA from the remote's pull-request head ref (`refs/pull/<number>/head`) rather than from a pull-request read, which carries the body; fetch that ref and add a worktree at the SHA. Materializing never reads or returns the description. Materialize the head the fetched metadata reports — never a pre-existing local branch of the same name, which may lag a force-push.
3. **Post a review summary** — add the caller's summary text to the pull request as a review carrying the caller's **stance** (comment-only, approve, or request-changes — see the stance note below).
4. **Post inline feedback** — attach each item as a review comment anchored to its file and line on the PR's diff, submitted as a single review carrying the caller's **stance**, so they post as one batch, not N notifications.
5. **Set a status** — set a commit status / check-run on the head ref reflecting the caller's pass/fail verdict, so the platform's merge protection can read it. This is best-effort: a failed status post is reported upward but never fabricates or changes the caller's verdict.

6. **Push a branch** — publish the local branch to the remote, setting its upstream. Never force-push: a rejected push (the remote moved) is reported, so the caller reconciles, never overwritten.
   - *cli:* a plain `git push` with upstream tracking (pushing is git itself, whichever transport serves the rest). *api/mcp:* the same local push; the API has no push of local commits.
7. **Open a review request** — open a pull request from the head branch onto the base, with the caller's title and description, and request review from the caller's reviewers. Return the request's number and link. A request already open for the same head is returned as-is, never duplicated.
   - *cli:* the GitHub CLI's PR-create command, then its reviewer-request flag or edit. *api/mcp:* the create-pull-request endpoint, then the request-reviewers endpoint.
8. **Read a review request** — given its number, or a head branch (the open request whose head it is; none open is *not-found*), return its base branch, its state (open, merged, closed), whether it is approved and by whom, any changes requested, and the review feedback on it: each review's summary and each inline comment with its author, file and line, and whether its thread is resolved.
   - *cli:* the GitHub CLI's PR-view with the review and comment fields, plus the review-comments API for inline threads. *api/mcp:* the pull-request read, the list-reviews endpoint, and the list-review-comments endpoint.
9. **Read a landing constraint** — given a target branch, return whether it requires an approved review (and how many approvals), which status checks must pass, and whether it blocks direct pushes, from the branch's protection rules and rulesets. A branch with no protection returns "no constraint", never an error.
   - *cli/api/mcp:* the branch-protection and rulesets reads for the branch; a protection the token may not read is the *not authenticated* failure below, never "no constraint".
10. **Merge** — merge an approved review request, or a branch onto its target, by the caller's strategy: merge commit, squash or rebase. Merge only what protection allows; never use an admin bypass or force past a required review or check. Return the merged commit.
   - *cli:* the GitHub CLI's PR-merge with the strategy flag (or a plain `git merge` and push for a branch with no request). *api/mcp:* the merge-pull-request endpoint with its merge method.

**The review stance (operations 3 and 4).** GitHub requires every review submission to declare an event — one of `COMMENT`, `APPROVE`, or `REQUEST_CHANGES`; there is no "just attach comments" call that omits it. The caller passes a capability-neutral **stance** and this adapter maps it: *comment-only* → `COMMENT`, *approve* → `APPROVE`, *request-changes* → `REQUEST_CHANGES`. The caller decides the stance — the reviewing act posts comment-only; the adapter never invents one, and never posts through a raw API call that bypasses this operation.

## Failure surface

Report failures upward in capability terms — the caller hears an outcome, never a raw HTTP code:

- **Not authenticated / token missing or lacking scope** → report as "vcs backend unavailable," which the caller's degrade path handles (and which the [vcs](../SKILL.md) skill maps to guiding the user through `init:vcs`).
- **PR or repo not found / wrong repo context** → report "the requested change was not found on the configured provider" rather than a 404; do not fall back to a different change.
- **Rate-limited or transient network failure** → report as a *retryable* vcs failure, distinct from a permanent one, so the caller can back off or degrade.
- **Description can't be held back** (a transport whose only pull-request read returns the body) → report that the change can't be fetched without its description, so the caller can stop rather than read it.
- **Inline anchor rejected** (a comment on a line outside the diff hunks) → report which items could not be anchored, so the caller can fold them into the summary rather than dropping them.
- **Merge refused** (protection requires a review or a check the change lacks, or the request isn't mergeable — a conflict, a stale head) → report which requirement refused it, so the caller stops at the right outcome; never retry with a bypass.
- **Push rejected** (the remote moved since the branch was last fetched) → report it as needing a reconcile, never resolve it by forcing.

## Call-time discovery

GitHub's surface shifts (flag names, endpoint shapes, review-submission payloads), so name the operation and its purpose here and resolve the exact parameters when you call: confirm the current diff-fetch flags, the review-comment payload shape (path + line + side for inline), the check-run vs commit-status choice, the PR-create and merge flags, and the protection and rulesets reads against the live CLI/API at call time.
