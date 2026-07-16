# Make units actionable

A right-sized, well-ordered unit is still not work-ready if whoever picks it up has to re-read the whole design to understand it. This phase closes that gap: it gives each unit enough to be started *cold* — an unambiguous scope, a done-condition anyone can check, its dependencies named, and just enough context to act — without forcing the executor to reconstruct the plan. The bar is a specific reader: a competent teammate who was not in the room, handed this one unit. If they would have to guess at scope, or open the design to know when they are finished, the unit is not yet actionable.

## Give each unit a checkable done-condition

State, in one sentence, what is true when the unit is done — the same single-outcome test that carving used, now written as the unit's acceptance condition ([one-unit-one-outcome](../rules/one-unit-one-outcome.md)). A done-condition an executor can check without a judgment call is the difference between a unit and a wish: "the `/logout` endpoint clears the session cookie and returns 204" is checkable; "handle logout properly" is not. Where the source (a spec or plan) already carries acceptance criteria for the unit's outcome, carry them through rather than paraphrasing them into something looser.

## Carry just enough context — link, don't duplicate

Each unit restates the *why* and the constraints it must respect — the decision it serves, the invariant it must not break, the interface it must match — so the executor acts with intent rather than blindly. But it **links back to the source for the full design** rather than copying it: a unit that duplicates the whole plan goes stale the moment the plan changes, and buries the one constraint that matters under the ninety-nine that do not ([carry-just-enough-context](../rules/carry-just-enough-context.md)). The test for "just enough": the context answers *what this unit must respect and why*, and points to the source for everything else.

## Name the scope and its edges

Make the unit's boundary explicit on both sides: what is in scope, and — where a reader would plausibly assume more — what is deliberately *not* in this unit (it belongs to a named sibling unit, or is out of scope entirely). An unstated boundary is where scope creep and double-ownership both start; naming it is what lets phase 5 prove the units tile the source cleanly. Carry forward the explicit dependency links from phase 3 as part of the unit's context ([make-dependencies-explicit](../rules/make-dependencies-explicit.md)), so a reader sees what must exist before this unit can start.

The output is the set of units, each self-sufficient to start — scope, done-condition, dependencies, and just-enough context — handed to [check-coverage-and-handoff](05-check-coverage-and-handoff.md).
