# first-pass-draft (`--first-pass`)

Activated by `--first-pass`, referenced from [SKILL.md](../SKILL.md) and [requirement-structuring](../phases/03-requirement-structuring.md) (where the skeleton is returned).

The base spec runs all five phases and returns a finished, hardened spec. This module makes it stop early and *on purpose*: run through structuring, return the skeleton, and pause for the caller to steer before any detail is invested. Its whole reason to exist is catching **scope drift early** — a wrong shape corrected after phase 03 costs a conversation; the same wrong shape corrected after phases 04–05 costs a rewritten spec. Deletion test: remove this module and spec runs to a full spec; the early return and pause is the added, flag-gated behavior.

## The delta

- **Return after structuring, not after hardening.** Run interrogation ([interrogating-prompts](../phases/01-interrogating-prompts.md)), ambiguity ([pin-down-ambiguity](../phases/02-pin-down-ambiguity.md)) only as far as it shapes structure, and structuring ([requirement-structuring](../phases/03-requirement-structuring.md)) to produce the **skeleton**: the buckets and the obvious requirements in each, plus the actors and the scope boundary. Then stop — do not run the concrete-and-testable pass ([making-it-concrete](../phases/04-making-it-concrete.md)) or the sequencing pass ([sequencing-and-sizing](../phases/05-sequencing-and-sizing.md)).
- **Mark the gaps open, don't close them.** The skeleton's incompleteness is deliberate and must be *visible*: each unfilled bucket, each requirement not yet made testable, each unresolved ambiguity is flagged as an explicit open gap for the next pass ([make-the-unsaid-explicit](../rules/make-the-unsaid-explicit.md)) — never quietly finished with a guess. A `--first-pass` output that reads finished has failed; the marked gaps are the product.
- **It is a checkpoint, not a deliverable.** State plainly that the skeleton is for steering, not for shipping — a caller must not mistake it for a partial spec they can hand to a build. The pause invites one thing: *correct the shape now.*

## Composition

`--first-pass` takes precedence over `--strict`: it returns a deliberately incomplete skeleton, so [strict-gate](strict-gate.md)'s completeness/testability block does **not** fire on the early return (the gate applies to the finished spec, not the skeleton). With `--from-issue`/`--from-discussion`, the skeleton is built from the seeded material exactly as from a hand-entered prompt.
