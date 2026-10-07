# Reviewing

**Entry condition.** The request is to judge a change someone else made — a review request, or a branch or diff whose author isn't the requester — before it lands. Reviewing the requester's own change, or asking for the review step alone, goes to the [review](../../review/SKILL.md) skill directly. (basis: maintainer, 2026-09-30) Each round reviews one change ([open-the-task](../phases/02-open-the-task.md)'s Rounds): a request naming several changes of one stack reviews the base-most one no round has reviewed yet, and the report names the rest for later rounds. (basis: derived from the steps' window being one change)

**Done when** the round's review has its Fitness, one result per acceptance; every finding and open question for the author has been delivered on the change — or, for a local branch no host carries, handed to the author by the requester, who confirms it — and the reviewer's task documentation records the review with where each part went. A review whose delivery waits on an unavailable host isn't done. (basis: maintainer, 2026-09-30)

## Rationale last

The author's rationale reaches only step 5 ([form-your-own-view-first](../../../craft/evidence/form-your-own-view-first.md)). Until then, every step, and every explorer a step recruits, reads the change's history only at or before its base, and reads no review-request or issue threads and no author notes. (basis: maintainer, 2026-09-30)

## Before the steps

The change is hosted or local, and each is brought in its own way:

- **A hosted change** — a review request. Fetch it through [vcs](../../vcs/SKILL.md) with its description held back — its diff, base and head commits, head branch, author and size — and materialize it into an isolated working copy at that head. If vcs can't hold the description back, the act stops here, with that as the task's next step. (basis: maintainer, 2026-09-30)
- **A local branch** — no host carries it. Read its head, author and size with local version control, its base being the merge base with the integration line, and check it out in an isolated working copy on a fresh local branch made at that head — never the author's branch itself — so the steps' default window, the branch against its base, is exactly the change. Read no commit message, note or branch description of the range: they're its rationale. A command that prints the head commit's subject as it runs — a checkout often does — runs with its output discarded. (routed to maintainer: a local-branch path, since the entry condition admits a branch and a hosted-only fetch can't review one.)

Record the copy's path in the act marker's `copy` ([keep-the-act-marker](../rules/keep-the-act-marker.md)). When the marker already records a copy, as after a takeover, use it instead of making another while it stands at the change's head, and otherwise discard it first. Steps 1 to 5 work in that copy, and close-out discards it, whichever session made it.

## Steps

(basis: maintainer, 2026-09-30; understand's diagram, maintainer, 2026-10-07)

| # | step | inputs | skipped by the act when |
|---|---|---|---|
| 1 | [understand](../../understand/SKILL.md) `--diagram --from-code=<the files the change touches>` | the change's diff, and the files it touches as they stood at its base, with their history up to it | never |
| 2 | [gather](../../gather/SKILL.md) `--explorers=official-documentation`, adding `authoritative-literature` when step 1's map lists a published standard the change implements (a format, a protocol, a code list) | the question: what is the published contract of each external contract step 1's map lists for the changed lines or the diff's additions, at the version the project pins, or, where it pins none, the version the environment runs (say which)? | step 1's map lists no external contract for the changed lines or the diff's additions |
| 3 | [test](../../test/SKILL.md) | the claims step 1's map carries as *inferred* or *unverified*, that step 2's evidence doesn't settle, about the behavior a changed line's correctness depends on — each with the behavior expected of it: the intent's, else the code's documented contract, else its behavior at the base — as claims added to the change's own behaviors; and that the change is under review, not being built, so test commits nothing | steps 1 and 2 leave no such claim |
| 4 | [review](../../review/SKILL.md) `--hold-rationale`, with `--change=<the change>` for a hosted change, or its default window in the copy for a local branch | the intent, and the results of steps 1 to 3 | never |
| 5 | [review](../../review/SKILL.md) `--prior=<step 4's result>`, with `--change=<the change>` for a hosted change | the rationale — the description `--change` brings, or, for a local branch, the range's commit messages, notes and branch description — and step 4's result | never |

Step 3's cases are removed from the copy before step 4, so the windows of steps 4 and 5 hold the author's change and nothing of the reviewer's. When a step breaks down — produces no result ([skip-only-with-a-reason](../rules/skip-only-with-a-reason.md)) — the steps after it take the breakdown as input, except when step 4 breaks down: that stops the act, since nothing after it has a review to build on. A negative result, a test that `fails` or an acceptance that `fails`, is a result. (routed to maintainer: the skip conditions for steps 2 and 3, and this breakdown rule, since a broken-down step's absence is evidence the later steps can weigh, while a review that broke down leaves nothing to build on.)

## Filed

The results of steps 1 to 4 file as sections of the round's scratchpad; step 4's files with no decision records. Step 5's result files as the round's review record, with a decision record for each of its decisions that is a one-way door, and close-out's delivery updates the review record with where each part went. (basis: derived from the document types' membership tests)

## Delivered

For a hosted change, close-out posts step 5's review on the change through vcs, with a stance, on the commit the round reviewed, the entry's `at`: its brief and findings as the review summary, linking the task's documentation by [deliver-through-the-ports](../rules/deliver-through-the-ports.md), and each open question inline at its `file:line`, folding any anchor the host rejects into the summary. Closed questions and the marks of what the rationale changed stay in the review record.

Close-out proposes the stance from step 5's result, its Fitness one result per acceptance ([results-and-certainty](../../../craft/evidence/results-and-certainty.md)), and the reviewer confirms or changes it in close-out's question; with no answer, it's comment-only. (basis: maintainer, 2026-10-02)

- **Request changes** — a finding stands that would fail review's gate at its default floor ([gate-mode](../../review/modules/gate-mode.md)) — high or above, graded `traced` or higher — or any acceptance `fails`.
- **Approve** — no finding above low stands, no question for the author is open, and every acceptance `holds`.
- **Comment-only** — any other result, an acceptance `unsettled` or `not checked` among them.

For a local branch, no host carries the change: close-out returns the review in its report for the requester to hand to the author, and records it as sent by hand once the requester confirms it was. (routed to maintainer: the local-branch path, since with no host the requester is the only route to the author.)
