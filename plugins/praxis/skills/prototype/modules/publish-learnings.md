# publish-learnings (`--publish`)

Activated by `--publish`, referenced from [capture-and-discard](../phases/06-capture-and-discard.md).

By default prototype is a leaf: it returns the findings blob to its caller and writes nothing. This module is the one path that persists the learnings durably — it hands them to the artifacts capability as a clean, team-facing findings document. **Deletion test:** remove it and prototype returns the findings blob to the caller (the default); the durable publish is the added, flag-gated behavior.

## The delta — wholesale delegation

Hand the findings blob to the `publish-artifact` skill, which owns the `tools.artifacts` prerequisite, naming its type — a **spike / prototype findings write-up**. That type has no dedicated `destinations` key, so the port resolves it to `destinations.default` (it names its type, never the destination or the literal `default` key). This is *wholesale* delegation: prototype does not touch the backend, so it declares no `config_requires` of its own — the doer owns the prerequisite. If artifacts isn't configured, `publish-artifact` guides the caller through `init:artifacts` (or blocks), and prototype **degrades** by returning the findings locally, exactly as the default leaf would.

## The clean-export bar

What gets published is a clean export for a human audience — the **verdict, the observed evidence, the rejected paths, and the caveats** ([capture-and-discard](../phases/06-capture-and-discard.md)'s findings blob) — and *nothing else*. Strip every internal-process reference before handing off: no tool calls, no agent/critic/explorer names, no phase or skill mechanics, no `--flag` vocabulary, no praxis machinery. The reader gets the findings and the decision they unblock, never how the sausage was made. `(basis: ratified capability decision — artifacts are clean, team-facing exports carrying content and decisions, never internal process; the producing skill strips process before publishing and the port adds none.)`
