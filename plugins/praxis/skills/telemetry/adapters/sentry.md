# sentry — telemetry adapter

Implements the **telemetry** capability for Sentry, over the transport configured in `tools.telemetry.transport` (api or mcp). The [telemetry](../SKILL.md) skill names the read and dispatches here; each read below is one of the telemetry capability's requests, translated to Sentry's concrete surface. Resolve exact field/parameter names against the live tool at call time (below) — the names here are not frozen.

## Operations

1. **Read a signal** — given a signal reference, retrieve its onset/first-seen, frequency, affected scope, correlated signals, and sample traces. Sentry models the common cases as:
   - *An error-aggregate* (an issue reference, e.g. `issue/991`) — read the issue's first-seen/last-seen timestamps, the event count and its rate over a window (the frequency), the affected releases/environments/and impacted-user count (the scope), the issue's tags and culprit, and one or more sample events with their full stack traces and breadcrumbs (the exemplars). *api:* the organization/project issues read plus the issue-events read for samples. *mcp:* the Sentry connector's issue-and-events read tools.
   - *A performance trace* (a trace or transaction reference) — read the trace's spans, their timings, and the correlated errors on the same trace.
   - *A metric or dashboard* (a query or dashboard reference) — read the series values over the window and the regression's onset point.
2. **Read a log stream** — given a log source reference within a time or correlation window, retrieve the entries in order with their error signatures and correlation IDs. Sentry serves this as its structured **logs** view where the project emits them, and otherwise as the **breadcrumb trail** attached to the events of the referenced issue/trace (the ordered log-like entries leading up to the failure). Return the entries in timestamp order, carrying each entry's level, message, and any trace/correlation id. *api:* the logs query endpoint, else the event-detail read for breadcrumbs. *mcp:* the connector's log/event read tools.

## Failure surface

Report failures upward in capability terms — the caller hears an outcome, never a raw Sentry response code:

- **Not authenticated / auth token missing or lacking scope** → report as "telemetry backend unavailable," which the caller's degrade path handles (and which the [telemetry](../SKILL.md) skill maps to guiding the user through `init:telemetry`).
- **Issue / trace / dashboard reference not found, or wrong org/project context** → report "the requested signal was not found on the configured provider" rather than a 404; do not silently substitute a different signal.
- **Rate-limited or transient network failure** → report as a *retryable* telemetry failure, distinct from a permanent one, so the caller can back off or degrade.
- **Log read unsupported for this reference** (no structured logs emitted and no event breadcrumbs on the reference) → report "no log stream available for this reference" rather than returning an empty stream as if the source were quiet, so the caller can fall back to another evidence lane instead of concluding the logs were clean.

## Call-time discovery

Sentry's surface shifts (endpoint shapes, query parameter names, the logs product's availability and payload, MCP tool names), so name the read and its purpose here and resolve the exact parameters when you call: confirm the current issues/events read shape, the stats-period/window parameters, the trace read, and whether structured logs are available for the project (versus breadcrumbs) against the live API/connector at call time. An adapter that pins today's exact field names ages into a confident wrong call; one that names the read and re-derives the arguments ages gracefully.
