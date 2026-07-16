# notify-stakeholders (`--notify`)

Activated by `--notify`, referenced from the SKILL.md body — the flag spans phase boundaries (it fires at each status transition), so it has no single activation phase.

Base behavior: [communicate-status](../phases/05-communicate-status.md) composes each update and returns it locally. This module **pushes** those updates out at transitions instead of only returning them. Deletion test: remove it and communicate-status still composes and returns updates; the push is additive — so it is a module.

## The delta — push transitions at phase boundaries

At each status transition — acknowledged (incident declared), mitigated, resolved (and any severity change or material impact change) — push the update out through the [communication](../../communication/SKILL.md) port to the target `--channel` (absent, the configured incident channel). The *content* and the *cadence* still come from [communicate-status](../phases/05-communicate-status.md) and [right-sized-status-updates](../rules/right-sized-status-updates.md) — this module does not decide what to say or how often; it only delivers what that phase composed, at the transitions. The audience-appropriate content bar (jargon-free for public, business framing for stakeholders) is the phase's, applied to whatever is pushed.

## Prerequisite and degrade

The post goes through the communication port (doer-owns-prerequisites; operate declares none). Degrade if communication is unavailable: **return the composed message for the user to send by hand**, noting automated delivery was unavailable — the response still runs and the update is still produced, it just isn't auto-posted. A delivered post returns its reference (the port guarantees this even if a follow-on link fetch fails), so operate never re-posts and duplicates an update.
