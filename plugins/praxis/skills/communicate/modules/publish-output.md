# publish-output (`--publish`)

Activated by `--publish`, referenced from [deliver-and-route](../phases/06-deliver-and-route.md).

Base behavior: [deliver-and-route](../phases/06-deliver-and-route.md) produces the artifact and returns it (the record). This module additionally publishes it as a durable, team-facing document and returns its canonical location. Deletion test: remove it and deliver-and-route still produces and returns the artifact; the durable publish is additive — so it is a module.

## The delta — publish through the publish-artifact port

Hand the finished artifact to the [publish-artifact](../../publish-artifact/SKILL.md) port as a durable document, and return the canonical location the port reports (the main page and any subpages, in tree order). What communicate owns at this boundary:

- **Hand over sectioned content and the artifact's type** — the port carves the page tree and resolves the destination from the type via its config. communicate names its **type** — the one already fixed in [frame-the-message](../phases/01-frame-the-message.md), whose adjacent-type discriminators settle the borderline calls (a decision-record vs a doc). A **decision record** names the `decisions` type-key; its other durable types (a doc, an onboarding note, a handoff) name their own type, which has no dedicated key and so resolves to `default` in the port. communicate never hands the literal `default` — it names its type and the port maps it; it supplies the content organized into sections and does not choose the backend.
- **Re-apply the clean-export bar** — publishing puts the artifact somewhere durable and often public, so [clean-export](../rules/clean-export.md) re-applies at the handoff: every internal-process reference is already stripped in [tighten-and-verify](../phases/05-tighten-and-verify.md), and this is the last checkpoint before it becomes a permanent record. The port publishes faithfully and adds no process metadata of its own.

This module does not re-author or re-pitch the artifact — the content, tier, and altitude are fixed upstream; it delivers the finished export to a durable home.

## Prerequisite and degrade

The publish goes through the publish-artifact port (doer-owns-prerequisites; communicate declares no `tools.artifacts`). Degrade if the artifacts backend is unavailable: **return the clean export for the user to publish by hand**, noting automated publishing was unavailable — the artifact is still produced and returned. When `--publish` and `--notify` both fire, publish **first**, then hand the canonical location to [notify-targets](notify-targets.md) so the announcement links to a live document, never a dangling reference. Under `--draft`, this module does not fire ([draft-only](draft-only.md) holds all delivery).
