A stale line in the task log tells a colleague a task is still open when it isn't.

## When the log is on

Read `tools.artifacts.task_log` from the project's praxis settings: `true` keeps the log, and `false` skips this phase; absent or unreadable, keep it. (basis: maintainer, 2026-09-30)

Mirror only a filing whose task record's publish landed, a `partial` one that left the task record's page published included. A failed filing leaves the log as it stood, and the next filing that lands rebuilds it. (basis: derived — the entry a filing is handed reaches the memory only once it lands, so a log mirrored from a failed one would show a status the memory never held)

## Rebuild it

Rebuild the page from the task memory entries — every `task-<key>` entry, closed tasks included, with the entry this filing was handed in place of its task's own — one line each in the shape [task-log](../rules/types/task-log.md) pins, newest update first. Publish it through [artifacts](../../artifacts/SKILL.md) as type `task-log`, at the directory `task-log/` under the home's destination ([find-the-task-documentation](01-find-the-task-documentation.md)) on a file backend, or as a page titled `Task log` on any other: new the first time, in place (`--idempotent`) after. Off a file backend, keep the location the first publish returns in a memory file named `praxis-task-log` (not `task-…`, which would read as a task's entry), and pass it as `--to` on every later publish. (routed to maintainer: the log's location kept in memory beside the task entries it mirrors, since a second store for it would drift from them.) The page holds this user's tasks alone. (routed to maintainer: rebuilt from one user's entries, since other developers don't run praxis.)

When the artifacts port reports the backend unavailable, say the log wasn't updated; the task's documentation is unaffected. Under `--dry-run`, show the page and write nothing.
