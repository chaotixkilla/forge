# knowledge — usage

A tool-layer interface skill: the single place the org's knowledge sources are reached. It fronts the `knowledge` capability so a workflow skill names *what it needs to read* and this skill resolves it to whichever sources are configured — the same ports-and-adapters seam `telemetry` provides for observability and `artifacts` for artifacts.

## When to use
- A skill needs to read a human-authored org document — a plan, RFC, spec, glossary, runbook, decision record — out of the configured knowledge sources, and should stay backend-agnostic. Call `knowledge` with the read instead of talking to a backend directly.
- A lane or skill needs to walk a knowledge tree: search broad, then fetch the documents that bear on the question, then list a document's children to reach the level below. Those reads, and listing the sources, are this port's whole surface.

## Not for / use instead
- Reading a *local* file or a docs tree checked into the repo → that is ambient (any skill or agent reads it directly with ordinary file access); this port is for a knowledge space reached by reference through a configured backend. A `local` provider is served here only when it is the *configured* knowledge backend rather than the working tree.
- Deciding *what to search for*, *which document answers the question*, or *how stale a document is* → the calling skill's judgment, and the `knowledge-base` lane's method in particular; this port carries out the read it is handed and nothing more.
- Weighing what a document says against the code, the history, or the open web → **gather**, which recruits the lanes and composes them; this port is one lane's transport, not the evidence engine.
- *Writing* a document to a docs backend → **artifacts**, which owns `tools.artifacts`. This port never writes, and the two capabilities are configured separately even when they point at the same product; it does read the artifacts home as one of its sources.
- Configuring which backend serves the capability → **init** (`init:knowledge`); this skill consumes the config, it does not set it.

## Operations (extended as consumers need them)
`list the sources` — each resolved source's name, note, the reads it supports and its entry references, the artifacts home included, so a caller can choose which to search and where to start a walk; reaches no backend.
`search` — a query, across every source or the named ones, optionally scoped to a subtree of one: returns each source's ranked references, not full documents.
`fetch a document` — by reference and the source it came from: its content plus the provenance the backend exposes.
`list a document's children` — by reference and its source: the immediate child documents in the backend's order, for walking a page→subpage tree a level at a time.

## Gotchas
- **It reads only.** The port never writes to the backend — no page created, edited, moved, or archived. A read is safe to repeat.
- **It blocks without a configured source.** `config_requires: tools.knowledge` with `if_missing: guide via init:knowledge, else block` — a knowledge port with no source has nothing to read. Consumers that can proceed without the lane (**gather** dropping it with a note, **communicate** falling back to what the session holds) catch the unavailable signal and degrade on *their* side; this skill itself blocks.
- **Not every source can be searched.** A backend with no search, or a source with no root, answers a search `unsupported`. Reach it by fetching its entry references and following children and links from there — a walk, which can show a document is there but never that one isn't.
- **"Could not reach it" and "it holds nothing" are different answers.** The port returns them as distinct outcomes, because a caller that conflates them reports an absence it never established. Callers must branch on which one came back rather than treating any empty return as a finding about the org.
- **Results come back per source, unmerged.** Each source answers with its own outcome and references, tagged with its name; one source down leaves the others' answers intact. Deduplicating, ranking and weighing across sources is the caller's.
- **An older config shape still reads, with an advisory.** Each entry read as its current equivalent, or ignored, comes back as an advisory naming the init setup that rewrites the slot.
- **It reports failures in capability terms.** The caller hears "the backend is unavailable" or "that document wasn't found," never a backend error code — so a caller's degrade logic never has to learn one backend's vocabulary.
- **Backend coverage is by adapter.** Whichever providers have an adapter under `adapters/` are supported; adding a provider is a new adapter, no change to callers.
- **`--dry-run` previews the read.** It reports which query or reference would be read, from which sources, and which would answer `unsupported`, without reading anything — useful when a reference's shape is uncertain.
