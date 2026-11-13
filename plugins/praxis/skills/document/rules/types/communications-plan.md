# Communications plan

What the people a change affects are told, when and through what, and what support says when they ask.

## Reader and question

Support, who answer people and send the notices: "What do we tell people, when, and what do we answer when they ask?"

## Page

`own page`

## Membership

The notices to people who use the product, to customers and to the teams who face them, the support replies, and where a case goes when support can't solve it. A notice to developers whose code consumes a contract is the [breaking-change-notice](breaking-change-notice.md)'s. Its subject is how the task's change is told, so a task has one. It is filed again when a notice is added, redated or rewritten.

## Items

**Notice `MSG`.** One message to one audience through one channel at one moment. Its translations are its copy, not further notices.

- `purpose`: enum `notice`, `support reply`. A notice is sent unasked; a support reply is sent when someone asks.
- `audience`: text.
- `channel`: text.
- `send on`: when. For a support reply, the day it is ready.
- `with`: id. The `GATE` it goes out with, when it goes with one.
- `lead time`: period. How long before its gate opens it must reach its audience. Its owner sets it per notice. (basis: audiences differ in the warning they need, so no default is set; open by design)
- `copy`: text. The ready-to-send wording, or a link to it. When no source holds it, it is drafted ([items-and-agreements](../items-and-agreements.md)) from what changes, for whom, when, and what they do about it, in the words of the notice's `audience` ([match-reader-vocabulary](../../../../craft/writing/match-reader-vocabulary.md)), in the first of its `locales`, else the task's language.
- `locales`: list of text. The languages its copy exists in.

(basis: prototype sweep, 2026-11-11, dated notices, ready-to-send wording, localised copy; no authoritative template exists)

Agreement `needed`, change regime `baseline`. Its decide-by is its `send on`.

Shows `GATE` (home: [cutover-plan](cutover-plan.md)).

## Sections

1. **Who hears what, and when?** Always. The notice timeline.
2. **What does support say when asked?** Always. The reply cards.
3. **Where does a case go when support can't solve it?** Always. Prose: each step of the escalation path, a team or a role and how to reach it, including for someone who can no longer get in.
4. **Can everyone use what changed?** When an [accessibility-check](accessibility-check.md) is owed. Its sections.

## Checks

*Computed:*
- Every notice has its purpose, audience, channel, send-on date, copy and at least one locale, and its lead time when it goes with a gate.
- A notice that goes with a gate is sent no later than the gate's opens on minus its lead time, when the opens on is a date.

*Judgment:*
- People learn of the change by meeting it: a notice dated after the change they would notice.
- The teams who face customers told after the customers.
- No support reply for the question most people will ask.
- An escalation path that ends at nobody, or has no step for someone locked out.
- Copy in fewer languages than the people it reaches use.

## Views

- **Notice timeline:** `timeline` of `MSG` whose purpose is `notice`, by send on: audience, channel, with, lead time, locales.
- **Reply cards:** `cards` of `MSG` whose purpose is `support reply`: audience, copy, locales.

## Minimum form

Each section keeps its heading with one line: nothing is planned yet, and who plans it.
