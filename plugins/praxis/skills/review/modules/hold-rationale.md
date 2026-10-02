# hold-rationale (`--hold-rationale`)

Activated by `--hold-rationale`, referenced from [scope-the-review](../phases/01-scope-the-review.md) and [build-the-mental-model](../phases/02-build-the-mental-model.md).

The base review reads the author's rationale, meaning the change's description and commit messages, as evidence of what the change sets out to do. This module holds it back, so the review forms its own view of the change first ([form-your-own-view-first](../../../craft/evidence/form-your-own-view-first.md)) and a later pass reads the rationale against that view ([prior-pass](prior-pass.md)). Deletion test: remove it and review still runs, reading the rationale as it always has; keeping it unread is what the flag turns on.

## The delta

- **The intent comes from the caller.** Hold the change to the intent its caller supplies (a ticket, a spec, a requirement) in place of the description and commit messages. With none supplied, fitness is judged against the change's own apparent intent, as the no-stated-requirement case in [deliver-findings](../phases/06-deliver-findings.md) already does. (basis: maintainer, 2026-09-30)
- **Nothing the author wrote about the change is read.** That excludes its title and description, its commit messages, its linked discussion threads, and any work-item found only through them. With `--change`, fetch the change through the vcs capability with its description held back, and materialize it the same way ([hosted-change](hosted-change.md)). In any window, read the history of the changed lines only up to the change's base, and give every explorer this pass recruits the same limit: the base commit, history at or before it, and no review-request or issue threads. A document the diff adds that argues for the change, such as a design note, is held whole for the pass that reads the rationale. (routed to maintainer: holding it keeps this pass clean, at the cost of reviewing part of the diff later.)
- **In the default window, the hold is local.** With nothing fetched, what the author wrote is what local version control would show: the range's commit messages, its notes and the branch's description. Read none of them, and run any command that prints them as it works — a checkout often echoes the head commit's subject — with its output discarded.
- **The description/behavior divergence check waits** for the pass that reads the rationale, since there's no stated goal here to compare the behavior with. The decisions and the questions for the author ([questions-for-the-author](../rules/questions-for-the-author.md)) come from the reviewer's own reading, and that later pass checks them.
- **The scope line says the author's description and commit messages weren't read**, so no reader takes the report's silence about them for agreement.

## Degrade

With `--change`, when the vcs capability can't fetch the change with its description held back, stop and say so. Don't fall back to reading it: a pass that has read the rationale is not the pass the caller asked for.
