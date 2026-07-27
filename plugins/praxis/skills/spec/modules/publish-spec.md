# publish-spec (`--publish`)

Activated by `--publish`, referenced from [sequencing-and-sizing](../phases/05-sequencing-and-sizing.md) (the finished spec is what gets published).

The base spec returns its result to the caller in the session. This module sends the finished spec onward — to the team's chosen destination — through the artifacts capability. Deletion test: remove this module and spec still produces and returns its spec; publishing it is optional behavior a flag turns on, which is why it is a module.

## The delta

- **Hand the finished spec to the artifacts capability.** Publishing is delegated *wholesale* to [publish-artifact](../../publish-artifact/SKILL.md), which resolves the configured backend and lands the document. spec composes the content and hands it over under the **`specs`** type-key — it names its type, which the port resolves to a destination; it does not itself know or name the destination.
- **Publish a clean, team-facing document — the export bar.** What lands is a spec/RFC for a **human audience**: the requirements, the acceptance criteria, the scope boundary, the priorities, the assumptions and open questions — the substance and the decisions. It carries **none** of the machinery that produced it: no interrogation transcript, no agent/critic/phase mechanics, no praxis process, no internal tool calls. Strip every internal-process reference before handing the document to the port; the port publishes faithfully and adds no process metadata of its own. `(basis: ratified house decision — artifacts are clean team-facing exports; the producing skill strips the machinery, the port publishes the substance.)` This is a content standard-point, not a passing note: a published spec that leaks the process is the defect this bar exists to prevent.

## Prerequisite and degrade

`--publish` is why spec touches the artifacts capability at all; the base path returns locally and needs no backend. Following doer-owns-prerequisites, spec **declares no artifacts prerequisite** — [publish-artifact](../../publish-artifact/SKILL.md) (the doer) owns `tools.artifacts`. If the backend is unconfigured, the port skill owns guiding the user through init:artifacts (or blocking); spec degrades by returning the finished spec locally, so the work is never lost just because there is nowhere yet to publish it.
