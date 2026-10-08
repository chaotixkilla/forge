# One type per page

## The rule

- Every page of a task closes with a footer line naming its type, the part of the system it covers, its task's key — with the round after it once the task has more than one — and the date its content last changed, which a republish that leaves the page as it was doesn't move, nor do the reference and title rewrites and the status change a closed round's page takes: `Review record · the invoice export module · review-230, round 2 · 2026-10-02`. It's filing data, so it sits below everything the reader came for. The task log, which belongs to no single task, closes with its type and its last update instead. (basis: maintainer, 2026-10-02; the date following content, maintainer, 2026-10-07)
- A page links to another page rather than repeating what that page says, but for a task record's current state and Iterations ([task-record](types/task-record.md)). A link to a page of the same task's documentation is an in-tree reference that resolves ([portable-tree-shape](portable-tree-shape.md)); a page of another task's is linked by its location. (basis: maintainer, 2026-10-07; the other task's pages, derived from their being in another tree)
- No page covers the whole system: a task documents only what it touched.

## The split test

A page has started a second topic when describing one of its sections would take another type's name (a format reference inside an explanation; a decision's full context and consequences inside a review record), or when a reader looking for that section wouldn't think to open this page. Split it: the new content becomes a page of its own type, and the old page links to it. A review's brief, with its one-line decisions, is delivered content and isn't split. (basis: maintainer, 2026-09-30; Diátaxis, Procida)
