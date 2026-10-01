# Size the unknowns as spikes

Sometimes a unit cannot be sized — not because it is big or small, but because you genuinely do not yet know what building it involves: an unfamiliar library, an unproven approach, a performance question no one has answered. The wrong move is to guess a size anyway and commit the plan to a number built on nothing; the guess is invisible in the output and detonates mid-build. This rule is cited by [size-and-sequence](../phases/03-size-and-sequence.md).

## The discriminator: is the uncertainty about the outcome, or just the effort?

Not every unknown becomes a spike — most units carry ordinary effort-uncertainty that a size range absorbs. Separate the two:

- **Effort-uncertainty → size it as a range, keep it a normal unit.** You know *what* to build and roughly *how*, you are just unsure how long — that is what estimation ranges are for; do not spike it.
- **Outcome-uncertainty → carve a spike.** You cannot size the unit because you cannot yet say what building it even entails — the approach is unproven, a key fact is unknown, the feasibility is in question. Carve a **timeboxed investigation unit**: its scope is the *question to answer*, its done-condition is *the answer reached* (or the time box hit), and it is sized by its **time box**, not by the unknown work it will reveal. The box's *length* is deliberately open — it depends on the depth of the question and the team's tolerance for investigation, which the executor holds at run time and the author cannot enumerate; pinning a fixed duration would be false precision. The method that bounds it: box it to the **smallest duration that could plausibly answer the question, and never longer than the work the answer de-risks** — a spike that costs more than the uncertainty it retires is not worth running. (The "2-day" figure in the anchor below is an illustration of applying that method to that question, not a fixed bar.)
- **The tell:** can you write a checkable done-condition for the unit right now ([one-unit-one-outcome](one-unit-one-outcome.md))? If yes, it is a normal unit with effort-uncertainty. If the only honest done-condition is "we understand X well enough to size it," it is a spike.

Use spikes *sparingly* — a spike per unit means the design is not ready and belongs back with plan ([ingest-the-source](../phases/01-ingest-the-source.md)'s readiness gate), not decomposed into a wall of investigations.

`(basis: Beck, Extreme Programming Explained, 1999; Cohn, User Stories Applied, 2004)`

## Anchors

- *Spike (outcome-uncertainty):* "can the existing job queue sustain 10k notifications/min, or do we need a new transport?" — no feature done-condition is writable until this is answered; carve a 2-day spike whose deliverable is the answer, and sequence it early ([order-by-dependency-then-risk](order-by-dependency-then-risk.md)).
- *Not a spike (effort-uncertainty):* "migrate the users table to add an index" — you know exactly what to do and how; you are only unsure whether it takes an hour or a day. Size it as a range; do not spike it.
