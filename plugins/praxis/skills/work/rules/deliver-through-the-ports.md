# Deliver through the ports

An act's delivery reaches people through more than one channel — a review request, a status post, a published document, a work-item — and two failures recur: an announcement that links a document not yet published, and a channel that failed quietly and reads as delivered. This rule is how close-out delivers.

## Publish before you announce

When a delivery both publishes a durable document and announces it, publish first and post the announcement with a link to the published location. Never post before the publish resolves, or the link dangles. When the publish degrades, there is nothing to link to: the announcement is *held* until the document has a home.

A short message that *is* the announcement, with nothing to link, posts directly.

## Every channel lands in one disposition

- **sent** — posted, published or filed, with the reference or location the port returned.
- **held** — composed but deliberately not sent because a precondition isn't met: an announcement whose document has no home yet, or a target no one confirmed ([who-may-be-reached](../../communication/rules/who-may-be-reached.md)). Returned for hand delivery once the precondition is met, with what's missing named.
- **degraded-return** — the channel's backend was unavailable: the finished content is returned for hand delivery, saying automated delivery was unavailable.
- **sent by hand** — held or returned content the user has since confirmed they delivered themselves; it counts as delivered.

When two blockers apply to one channel, **held outranks degraded-return**: a missing precondition binds even when the backend is also down, so record the channel as held and note the outage beside it. A channel whose only blocker is its own backend is degraded-return. A failed channel is never reported as sent, and never left without a disposition.

## Never deliver twice

A port that returns a delivered reference guarantees it even when a follow-on step, such as fetching a permalink, failed. Never re-post or re-publish to recover missing metadata, or the reader gets the message twice.

## Report what landed where

Close-out's report leads with what was delivered and where, then says plainly what was held or returned and what that now needs from the user. Each channel's disposition is part of the task's record. (basis: derived from communicate's delivery partition, which this rule now holds for every act)
