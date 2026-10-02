# Maintaining

**Entry condition.** The request is to keep existing code healthy: restructure it or clean it up, retire a switch, move a dependency to a new version, deprecate an interface or harden a boundary. Building new behavior goes to the developing act and fixing a defect to the fixing-a-bug act. (basis: maintainer, 2026-09-30)

**Done when** the change step's outcome is committed (with or without follow-ups) with a verified verdict, or an inconclusive one said plainly — for step 3, develop's *landed*; its *blocked* is a blocked-and-reported outcome; the change has passed its own review by [open-the-review-request](../rules/open-the-review-request.md)'s test, and its review request has been approved, read through vcs or, where no host carries it, confirmed by the user; and its review request is open, with its follow-ups filed. A blocked-and-reported outcome isn't done: what would unblock it becomes the task's next step. (basis: derived from the steps' outcomes)

## Behavior stays put

Maintaining preserves behavior where developing changes it: each step proves its own kind of preservation, and a deprecation or a hardening changes behavior only as far as the maintenance asks — the warning, the rejected input — and no further. (basis: maintainer, 2026-09-30)

## After approval

Before step 1, [give the task a branch](../rules/give-the-task-a-branch.md).

## Steps

(basis: maintainer, 2026-09-30)

| # | step | inputs | skipped by the act when |
|---|---|---|---|
| 1 | [refactor](../../refactor/SKILL.md) | the request, and the scope or module it names | the change moves a dependency, or must change behavior |
| 2 | [upgrade](../../upgrade/SKILL.md) | the request, its dependency and target version, and the scope or module it names | the change moves no dependency |
| 3 | [develop](../../develop/SKILL.md) | the request, and the behavior change the maintenance asks for and no more | the change is a restructuring or a dependency move |
| 4 | [test](../../test/SKILL.md) `--changed` | the coverage the change step's follow-ups say the change made necessary | the change step names none |
| 5 | [verify](../../verify/SKILL.md) | the user flows the change step's blast-radius map reaches | the change reaches no flow a user runs |
| 6 | [security-review](../../security-review/SKILL.md) `--changed` | the change and its blast radius | the request asks for no security pass |
| 7 | [review](../../review/SKILL.md) `--changed` | the change, and the change step's rationale | never |

Exactly one of steps 1 to 3 runs, chosen by the kind of change the request names. When step 4's verdict is FAIL, step 5's headline is `defective`, or the change doesn't pass step 7, the change goes back to the change step that ran, with that step's whole result as its input, and the steps after it run again; after the second failed pass, the act stops with its last result as the task's next step. A result that settles nothing — step 4 INCONCLUSIVE, step 5 `blocked`, `indeterminate` or `framing-unestablished` — sends nothing back: its gap becomes the task's next step. The steps after it still run, and the review request opens with the gap stated in its description; the task isn't done until the gap is settled. Step 5's `no-observable-surface` settles it like a skip, recorded as that, never as `works`. (routed to maintainer: two passes before stopping, since a second failure on the same change says it needs more than another try.) When the change step ends blocked-and-reported — develop's *blocked* included — the act stops there, with the blocker as the task's next step. Step 6 gates delivery: a finding at or above security-review's high floor stops the act before anything is delivered, until it's fixed and the pass re-run or the maintainer lowers the bar. (basis: maintainer, 2026-07-11)

## Filed

The change step's result — the rationale, risk tier, verdict and follow-ups — files as sections of the task's scratchpad, and step 7's result as the review record. A deliberate contract change taken through a migration path files a decision record. (basis: derived from the document types' membership tests)

## Delivered

- **The review request.** Open it per [open-the-review-request](../rules/open-the-review-request.md).
- **The work-item.** When the change traces to one, update it through [project-mgmt](../../project-mgmt/SKILL.md).
- **A notice to the owners, for an exposed-tier change** — its reach extends past the team, so affected owners and consumers need warning — or when the request asks for one. Route it through [communication](../../communication/SKILL.md) by the change step's owners when it was scoped to a module: an owner whose version-control handle matches a roster member's is reached at that member's messaging handle, and a notice for any other owner the repository names is returned for hand delivery, with that owner named. Without a module, post to the broad channel praxis settings record (`tools.communication.channels.default`), or with none recorded, return the notice for hand delivery ([who-may-be-reached](../../communication/rules/who-may-be-reached.md)). A contained or bounded internal change warrants none. (basis: derived from change-risk-scale)
- **The follow-ups.** File each one the change step surfaced through project-mgmt, so deferred work isn't lost.
