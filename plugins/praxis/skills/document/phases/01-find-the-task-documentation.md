A result filed into the wrong task, or a second copy of a task's documentation, splits the record the next reader depends on.

## Find it

The caller names the task (`--task=<key>`) and passes its state: the task's memory entry, and every document filed for it so far. document rebuilds nothing from the backend. When the entry links the task's documentation, that's where this filing goes. When it links none, the task has no documentation yet: start it with its task record ([task-record](../rules/types/task-record.md)).

## Where it lives

A task's documentation is one artifact with a destination of its own. It's handed to artifacts as type `task-documentation`, which no destinations key names, so it resolves under the artifacts backend's default destination. On a file backend its destination is the directory `tasks/<key>/` under that default — passed as the artifacts port's base directory (`--dest-dir=<default>/tasks/<key>/`), since `--to` would replace the default rather than nest under it — and that path is its identity, so no two tasks collide; on a page backend it's a page titled `<key> · <title>` under the default, and on a backend that takes no destination, a document of that title. On any backend but a file one, after the first filing its identity is the location the task's entry links: pass that location as the artifacts port's `--to` on every later filing. (basis: derived from the artifacts port's stable-identity rule)

On the local backend, the task's documentation sits inside the repository, so it is kept out of the work: it's never part of a change any step judges, tests or commits — a step's window and develop's clean-tree check leave its directory out — and it reaches version control only in its own commit, made on the task's branch just before a review request links it. (routed to maintainer: committed separately when a review request links it, else left to the user.)

## Refuse a task that has ended

A task whose record says it's closed takes no more filings ([pages-belong-to-their-task](../rules/pages-belong-to-their-task.md)). Say so and stop.

The output is where the task's documentation is, or will be, and its task record as it stands, for [shape-the-document](02-shape-the-document.md).
