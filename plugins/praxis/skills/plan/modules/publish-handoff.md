# publish-handoff (`--publish`)

Activated by `--publish`, referenced from [slice-and-validate](../phases/06-slice-and-validate.md) (the finished, closed design is what gets published).

The base run returns the plan to the caller in the session. This module sends the finished design onward — to the team's chosen destination — through the artifacts capability, formatted for review handoff rather than working notes. Deletion test: remove this module and plan still produces and returns its design; publishing it is optional behavior a flag turns on, which is why it is a module.

## The delta

- **Hand the finished plan to the artifacts capability.** Publishing is delegated *wholesale* to [publish-artifact](../../publish-artifact/SKILL.md), which resolves the configured backend and lands the document. plan composes the content and hands it over under the **`plans`** type-key — it names its type, which the port resolves to a destination; it does not itself know or name the destination.
- **Publish a clean, team-facing design document — the export bar.** What lands is a design doc / RFC for a **human audience**: the problem framing, the chosen approach and *why* (with its rejected alternatives), the interface contracts, the hard-flow resolutions, the rollout and its ship bar, the open risks. It carries **none** of the machinery that produced it — no phase names, no agent/critic mechanics, no praxis process, no internal tool calls. Strip every internal-process reference before handing the document to the port; render the design and its decisions, never how they were arrived at. `(basis: ratified house decision — artifacts are clean team-facing exports; the producing skill strips the machinery, the port publishes the substance and adds no process metadata of its own.)` This is a content standard-point, not a passing note: a published plan that leaks the process is the defect this bar exists to prevent.

## Prerequisite and degrade

`--publish` is the only reason plan touches the artifacts capability; the base path returns locally and needs no backend. Following doer-owns-prerequisites, plan **declares no artifacts prerequisite** — [publish-artifact](../../publish-artifact/SKILL.md) (the doer) owns `tools.artifacts` and owns guiding the user through `init:artifacts` (or blocking) if it is unconfigured. plan degrades by returning the finished design locally, so the work is never lost just because there is nowhere yet to publish it.
