# newrelic — telemetry adapter

Implements the **telemetry** capability for New Relic, over the transport configured in `tools.telemetry.transport` (api or mcp). The [telemetry](../SKILL.md) skill names the read and dispatches here; each read below is one of the telemetry capability's requests, translated to New Relic's concrete surface. Resolve exact query/field names against the live tool at call time (below) — the names here are not frozen.

## Operations

1. **Read a signal** — given a signal reference, retrieve its onset/first-seen, frequency, affected scope, correlated signals, and sample traces. New Relic models the common cases through queries over its telemetry data types:
   - *An error-aggregate* (an error-group reference or a query over the error data) — read the group's first-seen/last-seen, the occurrence count and rate over a window (the frequency), the facets that scope it (application/entity, host, transaction), and one or more sample error traces with their stack traces. *api:* a query over the error/event data (a NRQL-style count/facet query) plus the entity read for the group; *mcp:* the New Relic connector's query + entity read tools.
   - *A distributed trace* (a trace reference) — read the trace's spans, their timings and services, and the errors correlated on the same trace id.
   - *A metric or dashboard* (a metric query or dashboard reference) — read the metric series over the window, its regression onset, and the dashboard's constituent queries.
2. **Read a log stream** — given a log source reference within a time or correlation window, retrieve the entries in order with their error signatures and correlation IDs. New Relic serves this as a query over its **log** data, filtered by the window and by the correlation key (a trace id, entity, or attribute) the caller supplies. Return the entries in timestamp order, carrying each entry's level, message, and trace/correlation attributes. *api:* a log query (a NRQL-style select over the log data, time-bounded); *mcp:* the connector's log query tool.

## Failure surface

Report failures upward in capability terms — the caller hears an outcome, never a raw New Relic response code:

- **Not authenticated / API key or account context missing or lacking scope** → report as "telemetry backend unavailable," which the caller's degrade path handles (and which the [telemetry](../SKILL.md) skill maps to guiding the user through `init:telemetry`).
- **Reference not found / wrong account or entity context** → report "the requested signal was not found on the configured provider" rather than an empty result set; do not silently substitute a different entity or widen the account.
- **Query rejected** (malformed query, or a window exceeding the data-retention horizon) → report as a *permanent* telemetry failure the caller must reconcile (narrow the window or fix the reference), distinct from a transient one it should retry.
- **Rate-limited or transient network failure** → report as a *retryable* telemetry failure so the caller can back off or degrade.
- **Log read returns nothing for the reference** → distinguish "no logs match this reference/window" (a genuine empty result) from "log data is not being ingested for this account" (a capability gap), and report which, so the caller does not read an ingestion gap as a quiet system.

## Call-time discovery

New Relic's surface shifts (the query language's functions and data-type names, NerdGraph schema, the logs and traces payloads, MCP tool names), so name the read and its purpose here and resolve the exact query text and parameters when you call: confirm the current query syntax for count/facet over the error and log data, the trace read, the time-window clause, and the correlation-attribute names against the live API/connector at call time. An adapter that pins today's exact query fields ages into a confident wrong call; one that names the read and re-derives the query ages gracefully.
