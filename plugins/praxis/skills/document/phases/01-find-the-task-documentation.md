A result filed into the wrong task, or a second copy of a task's documentation, splits the record the next reader depends on.

## Find it

The caller names the task (`--task=<key>`) and passes its state: the task's memory entry, and every document filed for it so far. document rebuilds nothing from the backend. When the entry links the task's documentation, that's where this filing goes. When it links none, the task has no documentation yet: start it with its task record ([task-record](../rules/types/task-record.md)).

## Where it lives

A task's documentation is one artifact with a destination of its own. It's handed to artifacts as type `task-documentation` and lands in the artifacts home, under the home's destination — read as [artifacts](../../artifacts/SKILL.md) step 1 reads it, older configs included. On a file backend its destination is the directory `tasks/<key>/` under that destination — passed as the artifacts port's base directory (`--dest-dir=<destination>/tasks/<key>/`), since `--to` would replace the destination rather than nest under it — and that path is its identity, so no two tasks collide; on a page backend it's a page titled `<key> · <title>` under the destination, and on a backend that takes no destination, a document of that title. On any backend but a file one, after the first filing its identity is the location the task's entry links: pass that location as the artifacts port's `--to` on every later filing. (basis: derived from the artifacts port's stable-identity rule)

When the home is a file backend inside the repository, the task's documentation sits in the working tree, so it is kept out of the work: it's never part of a change any step judges, tests or commits — a step's window and develop's clean-tree check leave its directory out — and it reaches version control only in its own commit, which the act opening a review request makes on the task's branch just before linking it ([open-the-review-request](../../work/rules/open-the-review-request.md)); without a review request, committing it is left to the user. (routed to maintainer: committed separately when a review request links it, else left to the user, since documentation committed with the change would enter the window every step judges.)

## Refuse a task that has ended

A task whose record says it's closed takes no more filings ([pages-belong-to-their-task](../rules/pages-belong-to-their-task.md)). Say so and stop.

The output is where the task's documentation is, or will be, and its task record as it stands, for [shape-the-document](02-shape-the-document.md).
