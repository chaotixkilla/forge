---
name: knowledge
description: Carry out a knowledge read — search the configured knowledge space, fetch a document by reference, or list a document's children for walking a tree — from the configured provider's adapter; returns the material with its provenance. A tool-layer interface skill, called by other skills.
metadata:
  flags:
    --dry-run: show the read that would be performed, without performing it
  config_requires:
    - key: tools.knowledge
      if_missing: guide via init:knowledge, else block
---
Usage & examples — when to reach for this skill, and concrete invocations: see [usage.md](usage.md).

A thin port over the knowledge backend: it names the capability, and the configured provider's adapter holds the concrete calls. Callers name the read they need; this skill resolves it to the backend. It reads only — it never writes to the backend. It carries out the read it is handed and returns what came back: it chooses no queries, selects no documents, grades no staleness, and draws no conclusion from what it reads — those belong to the calling skill.

1. Resolve the provider: read tools.knowledge — the provider + transport configured for this project
2. Take the requested read and its inputs from the caller — one of: **search the space** (a query, optionally scoped to a subtree — returns ranked references, not full documents); **fetch a document** (by reference — its content plus the provenance the backend exposes); **list a document's children** (by reference — the immediate child documents in the backend's order, for walking a tree one level at a time)
3. Dispatch to the matching adapter: the concrete provider calls live in adapters/&lt;provider&gt;
4. Return the result to the caller — for a search, the ranked references; for a fetch, the content plus its provenance; for a children list, the child references in order — each carrying the resolved space it was read from — or one of the capability-level outcomes in [outcome-taxonomy](rules/outcome-taxonomy.md), never a raw provider error

**The provenance floor.** Every fetched document carries three fields without exception: its **title**, its **reference** (the durable id or path a caller can re-open it by — never a title, which renames), and the **resolved space** it was read from. Three more are best-effort, because backends expose different subsets: **author**, **created**, **last-edited**. A best-effort field the backend does not expose comes back as an explicit *not-exposed*, never omitted and never defaulted — an omission reads as an undated or unattributed document, and a caller grading staleness cannot tell "this backend exposes no dates" from "this document has none." `(basis: derived — the three required fields are exactly what a calling lane needs to anchor a claim so a second reader can re-open the same passage; the explicit not-exposed marker is what stops a backend's thin metadata from being read as a property of the document.)`
