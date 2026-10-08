# Task history

What the task was asked to do and what each round did, in the order it happened, for a reader checking how the [task record](task-record.md) came to say what it says.

## Membership

One page per task, the first beneath the group [publish-and-link](../../phases/03-publish-and-link.md) titles Rounds and working records. It holds what every filing adds about the task's intent and the steps its rounds ran, and nothing about where the task stands now, which is the task record's, but for which round last reviewed each change of a stack. Its footer names no round, since it covers them all. (basis: maintainer, 2026-10-08)

## Sections

In this order, each present even when empty; an empty section says so in a line.

1. **The task** — its key and title, its owner, the intent it serves (the ticket or requirement, linked, with its requirements and acceptance criteria as they stood when the task opened, labelled as that baseline), and what kind of work it is: for a review of a teammate's change, which change, or for a stack, one line per change, base-most first, each with the latest round that reviewed it, or "not reviewed".
2. **Rounds** — one section per round, latest first, headed by the round's name, its kind after it for an act that authors a change: what it reviewed and the date it opened, `Review of a1b2c3d · 2026-10-02`, with the change first in a stack, `Review of request 231 at 9ab12cd · 2026-10-02`, or, for other work, `Work of 2026-10-02`. Each gives what was done, in the order it happened, in plain terms, each with where its result lives; the work that wasn't done, with why — the reason whoever decided gave, or the condition that ruled it out; and the round's pages, each as an in-tree reference ([portable-tree-shape](../portable-tree-shape.md)), its [round record](round-record.md) first when it has one, then its other pages, on one line, the round record then holding the round's detail. A round with no round record gives what was done in its section itself, its reviewers' verdicts and the link to its diff included. A folded earlier task's round says it was recorded as a task of its own and refers to its record's page by in-tree reference. A round whose record predates rounds — a folded task's, or round 1 below — is named from what its record gives: the change and the earliest date its record carries, with the commit where it gives one.

A record written before tasks had rounds is its round 1: its "What was done" is carried as round 1's section, with its list of documents given as in-tree references to those pages under their current titles; a round section that names its pages in plain text, as records before in-tree references did, gives them the same way. (basis: maintainer, 2026-09-30; rounds and their names, maintainer, 2026-10-02; pages named by in-tree reference, derived from a reference following its page wherever the tree places it; owner, baseline label and round records, maintainer, 2026-10-07; the page of its own, maintainer, 2026-10-08)
