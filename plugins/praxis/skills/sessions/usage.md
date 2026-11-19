# sessions — usage

A tool-layer interface skill: the single place one working session reaches another on the same task. It fronts the `sessions` capability so work's coordinator and worker sessions name what they need to say, and this skill carries it over whichever transport is configured.

## When to use
- A coordinating session briefs, answers or tells the sessions working beside it when to rebase.
- A worker session reports in, reports a commit or asks the coordinator a question.

## Not for / use instead
- Messages to people or a team channel → **communication**, the conversation backend.
- Publishing a page for readers → **artifacts**.
- Deciding what to send, to whom, or whether → the caller: work's [coordinate](../work/modules/coordinate.md) and [worker](../work/modules/worker.md) modules.

## Examples
- `this session's address` — the coordinator learns the name it gives each worker to report to.
- `send` to a worker — a brief, an answer, a rebase notice.
- `read` — a session collects what was sent to it since it last read.
- `--dry-run send …` — shows the message and the transport it would use, sending nothing.

## Gotchas
- **It works with no configuration**, by step 1's fallback.
