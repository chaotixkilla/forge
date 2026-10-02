# Task record

Every other page of a task hangs beneath its task record, so a reader who has only the record can find the rest.

## Sections

In this order, each present even when empty; an empty section says so in a line.

1. **Status** — open or closed, what it's waiting on, and the date it was last updated.
2. **What's next** — the next step, or "nothing: closed".
3. **The task** — its key and title, the intent it serves (the ticket or requirement, linked, with its requirements and acceptance criteria as they stood when the task opened), and what kind of work it is: for a review of a teammate's change, which change, or for a stack, one line per change, base-most first, each with the latest round that reviewed it, or "not reviewed".
4. **Rounds** — one section per round, latest first, headed by the round's name: what it reviewed and the date it opened, `Review of a1b2c3d · 2026-10-02`, with the change first in a stack, `Review of request 231 at 9ab12cd · 2026-10-02`, or, for other work, `Work of 2026-10-02`. Each gives what was done, in the order it happened, in plain terms, each with where its result lives; the work that wasn't done, with why — the reason whoever decided gave, or the condition that ruled it out; and the round's pages by title, which the main page's table of contents links. A folded earlier task's round says it was recorded as a task of its own and names its record's page. A round whose record predates rounds — a folded task's, or round 1 below — is named from what its record gives: the change and the earliest date its record carries, with the commit where it gives one.

When the status changes, its section is rewritten, not appended to. A record written before tasks had rounds is its round 1: its "What was done" is carried as round 1's section, with its list of documents given as the round's page titles. The record links to the other pages rather than summarizing them ([one-type-per-page](../one-type-per-page.md)). (basis: maintainer, 2026-09-30; rounds and their names, and what to act on first, maintainer, 2026-10-02; pages named by title, derived from a page's position in the tree changing as rounds join)
