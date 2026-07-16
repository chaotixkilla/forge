# emit-checklist (`--checklist`)

Activated by `--checklist`, referenced from [check-coverage-and-handoff](../phases/05-check-coverage-and-handoff.md).

The base run ends at `--plan-only` — the decomposition presented for review. This module changes the delivery form: render the units as a single ordered checklist for lightweight tracking, for when there is no tracker to emit to and none is wanted. Deletion test: remove this module and decompose still presents the decomposition; the checklist rendering is optional, which is why it is a module. It has a second role — it is the **fallback sink** [emit-tickets](emit-tickets.md) degrades to when the project_mgmt backend is unavailable.

## The delta — render one ordered checklist

Render the covered, ordered unit set as a single checklist, in the dependency-then-risk order from [size-and-sequence](../phases/03-size-and-sequence.md): one checkbox item per unit, each carrying the unit's one-sentence done-condition as the item text ([one-unit-one-outcome](../rules/one-unit-one-outcome.md)) and its dependencies noted inline ([make-dependencies-explicit](../rules/make-dependencies-explicit.md)) so the order stays readable if items are worked out of sequence. Spike units are marked as investigations ([size-the-unknowns-as-spikes](../rules/size-the-unknowns-as-spikes.md)).

This is a **local, config-less rendering** — a plain ordered checklist (markdown) returned to the caller or written locally — not a publish through the artifacts capability. A checklist is lightweight tracking, not a team-facing published document; decompose declares no artifacts prerequisite and does not reach that backend here. (A caller who wants the decomposition published as a document routes it through the artifacts capability separately.)

## When it is a fallback

When reached as [emit-tickets](emit-tickets.md)'s degrade path (tracker unavailable), render the same checklist and make the degrade explicit to the caller: the requested tracker could not be reached, so the units are delivered as a checklist instead — nothing about the decomposition is lost, only the sink narrowed.
