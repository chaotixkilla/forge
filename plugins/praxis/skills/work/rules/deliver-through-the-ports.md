# Deliver through the ports

An act's delivery reaches people through more than one channel — a review request, a status post, a published document, a work-item — and three failures recur: an announcement that links a document not yet published, a link its readers can't open, and a channel that failed quietly and reads as delivered. This rule is how work delivers — at an act's close-out, or for a lone step it runs outside an act.

## Publish before you announce

When a delivery both publishes a durable document and announces it, publish first and post the announcement through [communication](../../communication/SKILL.md) with a link to the published location. Never post before the publish resolves, or the link dangles. When the publish degrades, there is nothing to link to: the announcement is *held* until the document has a home.

A short message that *is* the announcement, with nothing to link, posts directly.

## Link only what its readers can open

A delivery that links the task's documentation, such as a review summary, a review request's description or an announcement, goes by the reach the [artifacts](../../artifacts/SKILL.md) port returned for that location, which an act keeps in its marker's `docs` with the port's share line:

- **`open`** — link it.
- **`private-until-shared`** — before delivering, give the user the port's share line and ask them to share it. Link it once they say it's shared; otherwise treat it as `local-only`.
- **`local-only`** — say instead that the full record is kept locally by the person delivering it, with no path or link. A documentation directory inside the repository is the exception, once [open-the-review-request](open-the-review-request.md) has committed it on the change's branch: link it there.

A reach the marker records came from the port, and holds in any session that reads it, after a takeover too. A reach not known, because the marker records none for the location, is read as `private-until-shared`: ask the user whether its readers can open it, and link it only on a yes. (basis: maintainer, 2026-10-02; the unknown case derived from the artifacts port reading an undecidable reach the same way)

## Publish where the document is meant to go

The task's documentation lands in the artifacts home, through [document](../../document/SKILL.md). A durable document [communicate](../../communicate/SKILL.md) hands back lands where it says it is meant to go: the home, or an audience space for the reader it names. Choose that space from the configured audience spaces by their `for`: a space fits when its `for` names the reader's role or a group that plainly holds it, and in doubt it doesn't; of several that fit, one naming the role itself beats one naming a wider group. Publish through [artifacts](../../artifacts/SKILL.md) with `--space=<its name>`. When several still fit, ask the user which if they can still be asked — a lone step's delivery, right after their request; inside an act, past its opening question, the document is **held** with the candidate spaces named. When no space fits, or none is configured, it is **held** too: it never falls back to the home, and the report says an audience space can be set up with init's artifacts setup. `(basis: maintainer, 2026-10-01)`

## Every channel lands in one disposition

- **sent** — posted, published or filed, with the reference or location the port returned.
- **held** — composed but deliberately not sent because a precondition isn't met: an announcement whose document has no home yet, or a target no one confirmed ([who-may-be-reached](../../communication/rules/who-may-be-reached.md)). Returned for hand delivery once the precondition is met, with what's missing named.
- **degraded-return** — the channel's backend was unavailable: the finished content is returned for hand delivery, saying automated delivery was unavailable.
- **sent by hand** — held or returned content the user has since confirmed they delivered themselves; it counts as delivered.

When two blockers apply to one channel, **held outranks degraded-return**: a missing precondition binds even when the backend is also down, so record the channel as held and note the outage beside it. A channel whose only blocker is its own backend is degraded-return. A failed channel is never reported as sent, and never left without a disposition. The ports' other returns collapse onto these: **retryable** is retried once, then degraded-return; a **partial** send is sent for what went through and held for the rest, naming it; every other failure a port returns — refused, permanent, unauthorized, a target not found, unsupported content, a conflict, a mismatch — is held, with the port's reason as what's missing, since each needs a change or a decision before the content can go. `(basis: derived from held meaning a precondition someone must meet, and degraded-return meaning only the backend failed)`

## Never deliver twice

A port that returns a delivered reference guarantees it even when a follow-on step, such as fetching a permalink, failed. Never re-post or re-publish to recover missing metadata, or the reader gets the message twice. A channel is delivered once per round: a later round's channels are its own, never repeats of an earlier round's. (basis: derived from a round's delivery being its own)

## Report what landed where

Close-out's report — or, for a lone step, the reply to the request — leads with what was delivered and where, then says plainly what was held or returned and what that now needs from the user. Each channel's disposition is part of the task's record. (basis: derived from communicate's delivery partition, which this rule now holds for every act)
