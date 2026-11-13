# Spike findings

What a prototyping task learned. The code it built is thrown away.

**Reader and question.** Maintainer: "does the assumption hold, and what should we build differently because of what we saw?"

**Page.** `own page`

## Membership

The prototype step's result. (basis: derived from the deliverable of the act that files it)

## Items

**Spike result `SPK`.** One per page: the assumption tested and its result.
- Fields: `result` enum `holds`, `fails`, `unsettled`, `not checked` ([results-and-certainty](../../../../craft/evidence/results-and-certainty.md)); `reason` text, why it is `not checked`, when it is; `observation` text, what was seen that the result rests on.
- Change regime: `baseline`.
- Agreement: `none`.

**Learning `LRN`.**
- Fields: `observation` text, the observation behind it; `for` enum `spec`, `plan`, `both`.
- Granularity: one thing a later spec or plan should do differently. A learning a later item takes up is what that item `rests-on`.
- Change regime: `baseline`.
- Agreement: `none`.

## Sections

(basis: maintainer, 2026-10-02, for the order)

1. **Does the assumption hold?** Always. `SPK`: the assumption, its result and the observation.
2. **What was built to find out?** Always. Prose: the probe, and what it left out that a production build would need.
3. **What should we build differently?** Always. The learning table.

## Checks

- *Computed:*
  - exactly one `SPK`;
  - a `SPK` at `not checked` has `reason` filled;
  - every `LRN` has an `observation`.
- *Judgment:*
  - a result read from more than the probe exercised;
  - a probe that leaves out the part the assumption is about;
  - a learning with no observation behind it, carried from belief.

## Views

- **Learning table** (section 3): `table` of every `LRN`, grouped by `for`: observation.

## Minimum form

The result `not checked` with why, the probe "not built", and "no learnings yet".
