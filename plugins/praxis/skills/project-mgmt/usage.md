# project-mgmt — usage

A tool-layer interface skill: the single place the work-tracking backend is reached. It fronts the `project_mgmt` capability so a workflow skill names *what it needs from the tracker* and this skill resolves it to whichever provider is configured — the same ports-and-adapters seam `vcs` provides for the code host and `publish-artifact` provides for artifacts.

## When to use
- A skill needs to reach the work-tracking backend and should stay provider-agnostic: fetch a tracked item to seed from, or create tracked items from a set of units. Call `project_mgmt` with the operation instead of talking to a tracker directly.
- You are adding a new skill that touches the tracker (integrate, operate, maintain): route its tracker operations through here rather than giving it its own adapter, so a provider swap changes one file.

## Not for / use instead
- Publishing a spec, plan, or report as a team-facing document → **publish-artifact** (that is the artifacts port); a tracker item is a unit of work, not a published document.
- Fetching or posting on a pull request, or setting a merge-gating status → **vcs** (the code-host port); `project_mgmt` fronts the dedicated work-tracking backend. Where an item lives as an issue *inside* the version-control host rather than a dedicated tracker, the `vcs` port is the one that reaches it.
- Deciding *what* the work-items should be, how to slice or sequence them → the calling skill's judgment (e.g. **decompose** derives the units and their dependencies, **spec** interrogates a fetched item); this skill only reads or records the items it is handed.

## Operations (extended as consumers need them)
Today it serves the operations `spec` (`--from-issue`) and `decompose` (`--ticket`) require; new consumers add their operations to the same interface and adapter rather than forking a new one:
`fetch a work-item` — a tracked item by reference: its title, description, acceptance criteria, labels, and status. (`spec --from-issue` seeds a spec from it.)
`create work-items` — turn an ordered set of units into tracked items carrying their dependencies and sequence. (`decompose --ticket` emits them.)

The natural next operation is `update a work-item` — set status or fields on an existing item — deliberately **not** exposed yet: no built consumer needs it. It lands with its first consumer (e.g. `integrate` closing an item on merge).

## Gotchas
- **It blocks without a configured backend.** `config_requires: tools.project_mgmt` with `if_missing: guide via init:project_mgmt, else block` — a work-tracking port with no tracker has nothing to do. Callers that have a meaningful fallback (spec degrades to interrogating whatever request content it was handed; decompose degrades to `--checklist` / `--plan-only` output) catch the unavailable signal and degrade on *their* side; this skill itself blocks.
- **It performs side effects.** Creating work-items mutates the remote tracker. Use `--dry-run` to preview the items that would be created without creating them. (Fetching is read-only.)
- **It reports failures in capability terms.** The caller hears "the work-item wasn't found" or "the backend is unavailable," never a provider error code — so the caller's degrade logic never has to learn a provider's vocabulary.
- **Provider coverage is by adapter.** Whichever providers have an adapter under `adapters/` are supported; adding a provider is a new adapter, no change to callers.
