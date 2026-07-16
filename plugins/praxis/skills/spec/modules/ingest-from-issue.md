# ingest-from-issue (`--from-issue=<ref>`)

Activated by `--from-issue=<ref>`, referenced from [interrogating-prompts](../phases/01-interrogating-prompts.md).

The base spec starts from the prompt in front of it — a sentence, a paragraph, a pasted ask. This module changes *where the raw request comes from*: instead of a blank page, seed the spec from a tracked work item — its title, description, and any acceptance criteria already written on it. Deletion test: remove this module and spec still runs on whatever prompt it was handed; seeding from a tracker is genuinely optional, which is why it is a module and not part of the interrogation phase.

## The delta

- **Fetch the work item** named by `<ref>` — its title, description, labels, and any acceptance criteria or linked context — through the **project_mgmt capability** (the tracked-work-item lane). The fetched content becomes the seed the interrogation phase attacks, replacing the blank prompt.
- **Reconcile, don't inherit.** A tracker issue is a *starting point, not ground truth* — it carries the same fuzz, silent assumptions, and untestable adjectives any prompt does, often more (it was written to open a conversation, not to close one). Run it through the full interrogation and hardening anyway: the module changes the *source* of the request, never the bar it's held to. Where the issue's stated scope and what interrogation surfaces disagree, surface the divergence as an open question ([make-the-unsaid-explicit](../rules/make-the-unsaid-explicit.md)) rather than silently overriding either.
- **Trace the spec back to the item.** Record the `<ref>` the spec was seeded from, so each requirement stays traceable to the originating need ([trace-each-requirement-to-a-need](../rules/trace-each-requirement-to-a-need.md)) and a reader can find the conversation the ask came from.

## Prerequisite and degrade

`--from-issue` is a reason spec reaches the project_mgmt capability at all; the base path touches no backend. Following doer-owns-prerequisites, spec **declares no project_mgmt prerequisite** — the capability is owned by its port skill, exactly as spec's `--publish` hands the artifacts prerequisite to [publish-artifact](../../publish-artifact/SKILL.md) and review's `--pr` hands `tools.vcs` to the `vcs` port.

Where the item lives in a version-control host (a repository's issues), the existing `vcs` port may serve the fetch. Where it lives in a dedicated tracker, the serving port is a **`project_mgmt` port skill that is ratified but not yet built** (basis: ratified by the maintainer, 2026-07-04 — a `project_mgmt` port owning `tools.project_mgmt`, mirroring `vcs`, is the chosen route; the spec-local-adapter alternative, which would make spec config-bearing and duplicate what the port will own, was set aside). Until that port exists, degrade cleanly: report that the item could not be fetched and fall back to interrogating whatever request content the caller can provide inline — do **not** silently spec a blank page as though no `<ref>` was given, which would answer a different ask than the caller made.
