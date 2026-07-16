# ingest-from-discussion (`--from-discussion=<ref>`)

Activated by `--from-discussion=<ref>`, referenced from [interrogating-prompts](../phases/01-interrogating-prompts.md).

The base spec starts from a request stated as a request. This module seeds it from a *threaded conversation* instead — a discussion where the ask, the constraints, and the decisions are scattered across many messages and many voices, never collected in one place. Deletion test: remove this module and spec still runs on a stated prompt; reconstructing intent from a thread is optional behavior a flag turns on. It is a separate module from [ingest-from-issue](ingest-from-issue.md), not one parameterized ingest: the source shape differs (unstructured chatter vs. a structured item), the capability differs (communication vs. project_mgmt), and the extraction method differs (distill and attribute a conversation vs. reconcile a written item) — enough divergence that folding them into one module would bury both methods.

## The delta

- **Fetch the thread** named by `<ref>` — its messages, participants, and ordering — through the **communication capability** (the discussion-thread lane). The reconstructed intent becomes the seed the interrogation phase attacks.
- **Distill decisions from chatter.** A thread is mostly noise around a few signal points: the decisions that were actually reached, the constraints that were agreed, the options that were rejected and why, and the questions that were raised but never resolved. Extract those four; drop the rest. A rejected option recorded with its reason is worth keeping — it stops the spec from re-proposing what the thread already argued down.
- **Attribute who asked for what.** Unlike a single-author issue, a thread has many voices with different stakes; carry the attribution (who wanted a capability, who raised a constraint) so a requirement traces to a real stakeholder need ([trace-each-requirement-to-a-need](../rules/trace-each-requirement-to-a-need.md)), not to the loudest message.
- **Open points stay open.** A question raised in the thread and never answered is an **open question in the spec**, not a gap for the executor to silently fill ([make-the-unsaid-explicit](../rules/make-the-unsaid-explicit.md)). Reconstructing intent from a conversation is inference-heavy; every inference gets written down to be challenged.

## Prerequisite and degrade

`--from-discussion` is a reason spec reaches the communication capability; the base path touches no backend. Following doer-owns-prerequisites, spec **declares no communication prerequisite** — the capability is owned by its port skill, as spec's `--publish` hands its prerequisite to [publish-artifact](../../publish-artifact/SKILL.md).

The serving port is a **`communication` port skill that is ratified but not yet built** (basis: ratified by the maintainer, 2026-07-04 — a `communication` port owning `tools.communication`, mirroring `vcs`, is the chosen route; the spec-local-adapter alternative, which would make spec config-bearing and duplicate what the port will own, was set aside). Until that port exists, degrade cleanly: report that the thread could not be fetched and fall back to interrogating whatever the caller can summarize inline — do **not** silently proceed as though no `<ref>` was given.
