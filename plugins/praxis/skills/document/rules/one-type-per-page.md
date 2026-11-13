# One type per page

## The rule

- Every page of a task closes with a footer line naming its type, the part of the system it covers, its task's key — with the round after it once the task has more than one — and the date its content last changed, which a republish that leaves the page as it was doesn't move, nor do the reference and title rewrites and the status change a closed round's page takes: `Review record · the invoice export module · review-230, round 2 · 2026-10-02`. It's filing data, so it sits below everything the reader came for. The task log, which belongs to no single task, closes with its type and its last update instead. (basis: maintainer, 2026-10-02; the date following content, maintainer, 2026-10-07)
- A page links to another page rather than repeating what that page says, but for a task record's current state and Iterations ([task-record](types/task-record.md)). A link to a page of the same task's documentation is an in-tree reference that resolves ([portable-tree-shape](portable-tree-shape.md)); a page of another task's is linked by its location. (basis: maintainer, 2026-10-07; the other task's pages, derived from their being in another tree)
- No page covers the whole system: a task documents only what it touched.

## Sharing and splitting a page

A type with its own page gets one. A type that joins another's page fills the section its type file names there, so a task's decision records can stand on its spec's page. A page holding several types closes with one footer, its types joined by ` + ` in the order they appear: `Spec + Decision record · …`. A document filed again is matched by type and subject, wherever it stands.

A page has grown past its types when a section holds content no type on the page declares: a threat analysis inside a design page, a decision's full context inside a review record. Split it. The content goes to its own type's page, which the plan then owes, as any added document, and the old page links to it. Content no type declares stays where it is, with an advisory naming it. A review record's brief, with its one-line decisions, is that type's own section and isn't split. (basis: maintainer, 2026-11-11, reconciling Diátaxis's one kind per page with types that share a page)
