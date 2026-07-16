# notify-targets (`--notify=<target>`)

Activated by `--notify=<target>`, referenced from [deliver-and-route](../phases/06-deliver-and-route.md).

Base behavior: [deliver-and-route](../phases/06-deliver-and-route.md) produces the finished artifact and returns it (the record). This module additionally announces it to a communication target. Deletion test: remove it and deliver-and-route still produces and returns the artifact; the channel announcement is additive — so it is a module.

## The delta — announce it through the communication port

Post to the communication target named by `<target>` through the [communication](../../communication/SKILL.md) port. What gets posted is shaped to the channel, not dumped — and the shape depends on whether the artifact has a durable *home* to link to. The three cases partition every artifact:

- **Durable artifact *with* a home** (published via `--publish` this run, or already living somewhere) → post a **fit-for-channel summary with a link back** to the full content, not the whole document inlined into a chat message. The summary is itself pitched to the channel's readers (their tier, per [audience-tiers](../rules/audience-tiers.md)) and carries the takeaway and the ask.
- **A short artifact** that *is* the message (a status line, a heads-up) → post it directly; it needs no home because it fits in the channel whole.
- **Durable artifact with *no* home** — durable-form (e.g. `--as=doc`) but no canonical location, because `--publish` wasn't passed and it lives nowhere yet. Do **not** post a summary linking to nothing (a dead link) and do **not** inline a whole document into a chat channel (the dump this module exists to avoid). Instead: **hold the announcement** — return the composed, channel-shaped summary for the user to post *once the artifact has a home*, noting that a durable announcement needs a durable location and that pairing `--publish` would give it one. A home-less durable artifact is announced by hand, after it's placed, not auto-posted into the void.

communicate decides *what* to say, *to whom* (the target), and *whether* to send; the port carries out the post and returns the delivered message's reference. The target is always supplied by the flag — there is no default channel — so `--notify` with no resolvable target is reported as unresolved, never sent somewhere arbitrary. This module does not decide the artifact's content or audience — those are fixed upstream; it delivers a channel-shaped announcement of it.

## Prerequisite and degrade

The post goes through the communication port (doer-owns-prerequisites; communicate declares no `tools.communication`). Degrade if communication is unavailable: **return the composed announcement and its target for the user to send by hand**, noting automated delivery was unavailable — the artifact is still produced and returned. A delivered post returns its reference, guaranteed by the port even if a follow-on link fetch fails, so **never re-post to recover a missing permalink** — that would deliver the announcement twice. Under `--draft`, this module does not fire ([draft-only](draft-only.md) holds all delivery).
