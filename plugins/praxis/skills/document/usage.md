# document — usage

File a task's documentation as its work happens: each result as the document type it belongs to, the task record kept as the hub, and the task log kept for people who don't use praxis.

## When to use
- An act is running and a step's result needs a home in the task's documentation. The work orchestrator calls it for every result.
- A task's status changed, and its record and log line should say so.

## Not for / use instead
- A message, status update or handoff pitched to people → **communicate**.
- A finished artifact that isn't part of a task's documentation → **artifacts** directly.
- A project-wide knowledge base → none. A task's documentation covers only what the task touched.

## Examples
- `document --task=review-pr-230`, handed a review's result — files it as the review record, then updates the task record and the log.
- `document --task=review-pr-230 --dry-run` — shows each document and where it would land, without writing.

## Gotchas
- It never publishes to a backend directly. Everything goes through artifacts, which owns the artifacts backend's setup.
- A task's pages aren't edited after the task ends. A later task writes its own and links back.
- Pages say what was done in plain terms. No skill, step or phase names reach them.
