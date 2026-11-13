A result filed into the wrong task, or a second copy of a task's documentation, splits the record the next reader depends on.

## Find it

The caller names the task (`--task=<key>`) and passes its state: the task's memory entry, and every document filed for it so far, in every round, each with its round and the location the last publish or fetch returned for it, a folded earlier task's pages among them ([open-the-task](../../work/phases/02-open-the-task.md)). document rebuilds nothing from the backend but the item store, below. With a step's result it passes the step's key, `<row>:<skill>`, and what it ran for when the act runs it more than once, `unit 2`, or the review requests it covered, `review requests 405, 406`; a finding made outside the steps that changes no step's result comes with none, and may carry one of work's labels: `attached:` and the request that added it, `research:` and its question, kind and runs, `moved:` and the moved task's key, `suggestion:` and its answer, `revision:` and its number, request and what it changed, `pending:` and the request that added it, or `outside:` and what happened to a request outside praxis, with an outside revision's number, which the task history gives as its rules say. The caller may also hand over pieces earlier filings shaped but couldn't publish, each labelled with its type and arriving under its unfiled file name ([keep-the-act-marker](../../work/rules/keep-the-act-marker.md)) — `<row>-<skill>.md`, `delivery.md`, `closing.md` or `finding.md`, each piece labelled with its step key or `no step`, and with what it ran for when it came with one; they skip [shape-the-document](02-shape-the-document.md) but for its Items, pages and checks, and file with this filing ([publish-and-link](03-publish-and-link.md)). When the entry links the task's documentation, that's where this filing goes. When it links none, the task has no documentation yet: start it with its task record ([task-record](../rules/types/task-record.md)).

## Where it lives

A task's documentation is one artifact with a destination of its own. It's handed to artifacts as type `task-documentation` and lands in the artifacts home, under the home's destination — read as [artifacts](../../artifacts/SKILL.md) step 1 reads it, older configs included. On a file backend its destination is the directory `tasks/<key>/` under that destination — passed as the artifacts port's base directory (`--dest-dir=<destination>/tasks/<key>/`), since `--to` would replace the destination rather than nest under it — and that path is its identity, so no two tasks collide; on a page backend it's a page titled `<key> · <title>` under the destination, and on a backend that takes no destination, a document of that title. On any backend but a file one, after the first filing its identity is the location the task's entry links: pass that location as the artifacts port's `--to` on every later filing. On a file backend the path is known before anything lands, so every filing, the first included, publishes in place: a tree a failed first filing left there is rewritten, never refused as a conflict. (basis: derived from the artifacts port's stable-identity rule, under which a file backend's path is its identity and a page backend's id is known only once a publish returns it)

When the home is a file backend, its destination, and a local audience space's, is resolved to an absolute path against the main checkout before it is handed to artifacts, whichever worktree a task runs in, and the location recorded is that absolute path; and the task's documentation is never versioned: it's never part of a change any step judges, tests or commits, and praxis never stages it, wherever it sits. (basis: maintainer, 2026-10-14)

## The item store and feedback

When the entry links the task's documentation, fetch it through [artifacts](../../artifacts/SKILL.md) at that location and keep its item store ([item-store-and-views](../../artifacts/rules/item-store-and-views.md)). When the entry's `restricted` field holds a location, fetch that store from its space too, and merge the two. While it holds only a destination, the restricted store starts empty, and the waiting restricted pieces carry its ids. The merge:
- every item and agreement of both, an agreement in both being one, with the restricted store's content;
- each prefix counting on from the highest id either store used, or any waiting piece carries;
- every link resolving across both;
- each store's `dismissed` list kept as its own, and handed back to its store when the two are published apart.

**A documentation with no store**, filed before stores existed:
- **A closed task** keeps its layout. A filing into it adds its pages as that layout did, with no store, no plan pages and no renames.
- **An open task** starts from an empty store, and from this filing on takes the current layout. Its earlier pages' prose isn't turned into items, since laying out adds nothing a result doesn't carry.

(basis: maintainer, 2026-11-11, leave closed tasks alone and convert open ones on their next filing)

**Feedback.** When the backend reads feedback, read each documentation's comments and approvals with the same fetch, the restricted copy's included, leaving out those its own store's `dismissed` list names. Each is a proposal, never applied:
- **An approval of a page** proposes the agreement [items-and-agreements](../rules/items-and-agreements.md) says it makes; where it makes none, the approvals become evidence on the page's `proposed` items.
- **A resolved comment thread** proposes the change its resolution states, to the item its anchor names. A thread resolved without stating a change proposes nothing. A thread whose anchor names no item goes to the developer as a note, attached to nothing.
- **An open comment thread** goes to the developer as a note, with its page, its anchor and its item when it names one, until it is resolved, since an open question on a page is someone waiting on an answer.

document never asks: it returns every proposal to the caller unconfirmed, and each note beside them, marked a note, which proposes nothing and needs no settling. A caller may hand back proposals it has settled: a confirmed one enters this filing, and a confirmed or dropped one's id joins the `dismissed` list of the store whose documentation it came from.

(basis: maintainer, 2026-11-11, read back and propose, never apply)

## Refuse a round that has ended

A filing goes to the latest round the entry it's handed names, a line `<n>.<m>` naming round `<n>` ([keep-the-task-memory-entry](../../work/rules/keep-the-task-memory-entry.md)). Read the task's entry as the memory holds it: when that names a later round, or its status is closed, the filing's round has ended and takes no more filings ([pages-belong-to-their-task](../rules/pages-belong-to-their-task.md)); say so and stop — unless every result it carries is labelled `attached:` or `moved:`, which goes into a closed task's latest round. The memory turns an entry closed only once the filing that closes it lands ([close-out](../../work/phases/04-close-out.md)), so that filing is taken.

The output is where the task's documentation is, or will be, its merged item store, the feedback proposals, and its task record as it stands, for [shape-the-document](02-shape-the-document.md).
