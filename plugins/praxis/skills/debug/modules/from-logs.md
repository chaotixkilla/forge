# from-logs (`--from-logs`)

Activated by `--from-logs=<path|ref>`, referenced from [reproduce-and-frame](../phases/01-reproduce-and-frame.md) (the intake site).

Deletion test: remove it and debug still frames from the user's report; seeding from logs is optional intake a flag turns on.

## The delta

Seed the investigation from a log source, resolved by the reference's shape:

- **A local path** (`./var/log/app.log`) → a plain file read; no external capability, no configuration.
- **A store reference** (a hosted log stream by id) → the [telemetry](../../telemetry/SKILL.md) port's *read a log stream*; debug sheds this prerequisite to the port, and degrades to the other evidence lanes if it's unavailable.

## Reconstruct the ordering; find the first-cause line

Raw logs are mostly downstream noise around a few load-bearing lines. Work them into evidence:

- **Extract the correlation keys** — the request/trace/session IDs that tie the failing operation's lines together — and filter to that one failing path, so you are reading one story, not the interleaving of thousands.
- **Reconstruct the event ordering** along that path, and find the **first-cause line**: the earliest entry where state first goes wrong, not the loudest error where it finally surfaces ([follow-the-first-divergence](../rules/follow-the-first-divergence.md)). A stack trace or exception is usually the surfacing point; the cause is an earlier, quieter line.

Treat the logs as observations to reason from, believing what they record over what the code's names suggest ([trust-observations-over-assumptions](../rules/trust-observations-over-assumptions.md)) — while remembering that absence of a log line is not absence of the event, only absence of the logging.
