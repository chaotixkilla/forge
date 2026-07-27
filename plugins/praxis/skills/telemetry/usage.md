# telemetry — usage

A tool-layer interface skill: the single place the observability backend is reached. It fronts the `telemetry` capability so a workflow skill names *what evidence it needs* and this skill resolves it to whichever provider is configured — the same ports-and-adapters seam `vcs` provides for the code host and `publish-artifact` for artifacts.

## When to use
- A skill needs to read live observability evidence and should stay provider-agnostic: an error-aggregate's frequency and sample traces, a distributed trace, a metric's regression onset, a dashboard, or a hosted log stream by reference. Call `telemetry` with the read instead of talking to a provider directly.
- You are adding a skill that reasons from production signals (debug and operate declare the `--from-telemetry` seed today): route its telemetry reads through here rather than giving it its own adapter, so a provider swap changes one file.

## Not for / use instead
- Reading a *local* log file for analysis → that is ambient (any skill reads it directly, e.g. debug's `--from-logs=PATH`); this skill is for a *hosted* log stream or store reached by reference.
- Gathering code, docs, history, or prior-art evidence → the explorer fleet / **gather** (that is the knowledge/evidence engine); this port reads only the observability backend.
- Configuring which telemetry provider backs the capability → **init** (`init:telemetry`); this skill consumes the config, it does not set it.
- Deciding *what the signal means* or *what to do about it* → that is the calling skill's judgment (e.g. **debug** turns a spike into a reproduction target); this skill only carries out the read it is handed.

## Operations (extended as consumers need them)
Today it serves the reads `debug` requires; new consumers add their reads to the same interface and adapter rather than forking a new one:
`read a signal` — a metric, trace, error-aggregate, or dashboard by reference: its onset/first-seen, frequency or rate, affected scope, correlated signals, and sample traces/exemplars.
`read a log stream` — a hosted log source by reference within a time or correlation window: its entries in order, plus the error signatures and correlation IDs within them.

## Gotchas
- **It reads only.** The port never writes to the backend — no alerts silenced, no incidents created, no dashboards edited. A read is safe to repeat.
- **It blocks without a configured backend.** `config_requires: tools.telemetry` with `if_missing: guide via init:telemetry, else block` — a telemetry port with no backend has nothing to read. Callers with a meaningful fallback (e.g. debug proceeding from a local log or a fresh reproduction) catch the unavailable signal and degrade on *their* side; this skill itself blocks.
- **It reports failures in capability terms.** The caller hears "the signal wasn't found" or "the backend is unavailable," never a provider error code — so the caller's degrade logic never has to learn a provider's vocabulary.
- **Provider coverage is by adapter.** Whichever providers have an adapter under `adapters/` are supported; adding a provider is a new adapter, no change to callers.
- **`--dry-run` previews the read.** It reports which signal or log window would be fetched, without performing the fetch — useful when a reference's shape is uncertain.
