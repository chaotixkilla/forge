# Reviewing

**Entry condition.** The request is to judge a change someone else made — a review request, or a branch or diff whose author isn't the requester — before it lands. Reviewing the requester's own change, or asking for the review step alone, goes to the [review](../../review/SKILL.md) skill directly. (basis: maintainer, 2026-09-30)

**Done when** the review has its fitness verdict, every finding and open question for the author has been delivered on the change — or, for a local branch no host carries, handed to the author by the requester, who confirms it — and the reviewer's task documentation records the review with where each part went. A review whose delivery waits on an unavailable host isn't done. (basis: maintainer, 2026-09-30)

## Rationale last

The author's rationale reaches only step 5 ([form-your-own-view-first](../../../craft/evidence/form-your-own-view-first.md)). Until then, every step, and every explorer a step recruits, reads the change's history only at or before its base, and reads no review-request or issue threads and no author notes. (basis: maintainer, 2026-09-30)

## Before the steps

The change is hosted or local, and each is brought in its own way:

- **A hosted change** — a review request. Fetch it through [vcs](../../vcs/SKILL.md) with its description held back — its diff, base and head commits, head branch, author and size — and materialize it into an isolated working copy at that head. If vcs can't hold the description back, the act stops here, with that as the task's next step. (basis: maintainer, 2026-09-30)
- **A local branch** — no host carries it. Read its head, author and size with local version control, its base being the merge base with the integration line, and check it out in an isolated working copy on a fresh local branch made at that head — never the author's branch itself — so the steps' default window, the branch against its base, is exactly the change. Read no commit message, note or branch description of the range: they're its rationale. A command that prints the head commit's subject as it runs — a checkout often does — runs with its output discarded. (routed to maintainer: a local-branch path, since the entry condition admits a branch and a hosted-only fetch can't review one.)

Steps 1 to 5 work in that copy, and close-out discards it.

## Steps

(basis: maintainer, 2026-09-30)

| # | step | inputs | skipped by the act when |
|---|---|---|---|
| 1 | [understand](../../understand/SKILL.md) `--from-code=<the files the change touches>` | the change's diff, and the files it touches as they stood at its base, with their history up to it | never |
| 2 | [gather](../../gather/SKILL.md) `--explorers=official-documentation`, adding `authoritative-literature` when step 1's map lists a published standard the change implements (a format, a protocol, a code list) | the question: what is the published contract of each external contract step 1's map lists for the changed lines or the diff's additions, at the version the project pins, or, where it pins none, the version the environment runs (say which)? | step 1's map lists no external contract for the changed lines or the diff's additions |
| 3 | [test](../../test/SKILL.md) | the claims step 1's map carries as *inferred* or *assumed-unverified*, that step 2's evidence doesn't settle, about the behavior a changed line's correctness depends on — each with the behavior expected of it: the intent's, else the code's documented contract, else its behavior at the base — as claims added to the change's own behaviors; and that the change is under review, not being built, so test commits nothing | steps 1 and 2 leave no such claim |
| 4 | [review](../../review/SKILL.md) `--hold-rationale`, with `--change=<the change>` for a hosted change, or its default window in the copy for a local branch | the intent, and the results of steps 1 to 3 | never |
| 5 | [review](../../review/SKILL.md) `--prior=<step 4's result>`, with `--change=<the change>` for a hosted change | the rationale — the description `--change` brings, or, for a local branch, the range's commit messages, notes and branch description — and step 4's result | never |

Step 3's cases are removed from the copy before step 4, so the windows of steps 4 and 5 hold the author's change and nothing of the reviewer's. When a step fails — produces no result ([skip-only-with-a-reason](../rules/skip-only-with-a-reason.md)) — the steps after it take the failure as input, except when step 4 fails: that stops the act, since nothing after it has a review to build on. A negative result, a failing test or a review that doesn't satisfy, is a result. (routed to maintainer: the skip conditions for steps 2 and 3, and this failure rule, since a failed step's absence is evidence the later steps can weigh, while a failed review leaves nothing to build on.)

## Filed

The results of steps 1 to 4 file as sections of the task's scratchpad; step 4's files with no decision records. Step 5's result files as the review record, with a decision record for each of its decisions that is a one-way door, and close-out's delivery updates the review record with where each part went. (basis: derived from the document types' membership tests)

## Delivered

For a hosted change, close-out posts step 5's review on the change through vcs, comment-only: its brief and findings as the review summary, and each open question inline at its `file:line`, folding any anchor the host rejects into the summary. Closed questions and the marks of what the rationale changed stay in the review record. The act never approves or requests changes; that decision stays with the people on the change. (basis: derived from the decision belonging to the people on the change)

For a local branch, no host carries the change: close-out returns the review in its report for the requester to hand to the author, and records it as sent by hand once the requester confirms it was. (routed to maintainer: the local-branch path, since with no host the requester is the only route to the author.)
