# Skip only with a reason

A step skipped quietly is rigor the record claims and the work never got. So every step on an act's checklist ends in exactly one of three ways:

- **ran** — its skill was invoked and returned a result. A step that broke down still ran; the breakdown is its result. A step **breaks down** when its skill can't produce its result — a missing input, an error, a block in its own run, as opposed to a result such as verify's `not checked`. A result that judges the work negatively — a test, a verify unit or a review acceptance that `fails` ([results-and-certainty](../../../craft/evidence/results-and-certainty.md)) — isn't a breakdown, it's the result; the act file says what each kind does next.
- **skipped by the act** — a condition the act file names held: this step's skip condition, or a stop earlier in the act; the record names it.
- **skipped by the user** — the user removed it, and the record holds their reason. Abandoning an act records this outcome, with one reason, for every step not yet run.

A step skipped any other way — including on the model's own judgment — has no outcome, and the act cannot close. (basis: maintainer, 2026-09-30.)

Cited by [run-the-act](../phases/03-run-the-act.md) and [close-out](../phases/04-close-out.md).
