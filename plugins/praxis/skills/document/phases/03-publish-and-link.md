## Publish the tree

Bring the task record up to date with this filing ([task-record](../rules/types/task-record.md)). Then publish the task's whole documentation through [artifacts](../../artifacts/SKILL.md) at the destination the first phase resolved — new on the task's first filing, in place on every later one (its `--idempotent` publish, with the identity the first phase resolved). Shape it as a portable page tree ([portable-tree-shape](../rules/portable-tree-shape.md)), in filing order: the task record first, as the main page's landing summary, then one subpage per document. (basis: derived — the artifacts port has no operation that adds one page beneath another)

Return each page's location to the caller. The task record's location is the link the task's memory entry keeps.

## Degraded and preview

When the artifacts port reports the backend unavailable or fails the publish, hand the shaped documents back to the caller, marked unfiled, with the reason; the caller keeps them in its report. (basis: derived from how the work orchestrator reports unfiled results) Under `--dry-run`, run the artifacts port's own `--dry-run` and return what it would publish, and where.

The output is each page's location, or the unfiled documents, for [mirror-the-task-log](04-mirror-the-task-log.md).
