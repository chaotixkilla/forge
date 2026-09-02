# Integrate and wire up

A verified slice can be correct and useless — a function nothing calls, a handler no route reaches, a config key nothing reads. This phase closes the gap between "the code exists and passes its loop" and "the change actually happens in the running system." It is a distinct step because the failure it prevents is specific and common: a build that is green in isolation and inert in production, because the last wire was never connected. Integration is also where a change most often breaks *other* code — the callers that relied on the old contract.

## Make the change reachable

Connect each new unit to the entry point phase 1 identified: the caller, route, command, event, or schedule that will exercise it, plus the config, flags, and dependency wiring it needs to run. The bar is concrete and is what the [definition of done](../rules/definition-of-done.md)'s *integrated / reachable* criterion checks against: **there is an invocation path from a real entry point to the new behavior, and it has been exercised end-to-end at least once** (drive the loop across the seam, per [prove-the-path-actually-runs](../rules/verification/prove-the-path-actually-runs.md)). "It's imported somewhere" is not reachable; "the app, run, reaches it" is. Match the wiring to how this system already wires such things — registration, DI, config — rather than a foreign pattern ([match-surrounding-conventions](../rules/change-hygiene/match-surrounding-conventions.md)).

## Keep every caller working

When the change altered an existing contract — a signature, a return shape, an invariant, an error mode — the change is not done until **every caller is migrated or confirmed unaffected** ([keep-callers-working](../rules/change-hygiene/keep-callers-working.md)). Find the callers (the code explorer, or a usage search) and carry the change out through its blast radius; a locally-correct change that silently breaks a caller is a regression, not an integration. This is the reverse-dependency reading orient set up. When carrying the change through that radius turns out to reach materially further than the task implied — a migration across callers the task never mentioned — that is the escalation case, not a bigger day's work: put it to the user before migrating ([orient-in-the-code](01-orient-in-the-code.md)).

## Get the boundaries right where the change meets the rest of the system

Integration is where the change's boundaries are real, so it is where the boundary rules land:

- Decide, deliberately, where each failure crossing the new seam is caught, surfaced, or propagated ([handle-errors-at-the-boundary](../rules/errors/handle-errors-at-the-boundary.md)) — not swallowed, not scattered.
- Validate untrusted input where it enters the change's surface and trust it inward ([validate-at-the-trust-boundary](../rules/errors/validate-at-the-trust-boundary.md)); convert it to a trusted shape once at that edge ([parse-dont-validate](../rules/data-and-types/parse-dont-validate.md)).
- Release resources and roll back partial writes on every failing branch of the newly-wired path ([clean-up-on-the-failing-path](../rules/errors/clean-up-on-the-failing-path.md)).

## Gate a risky integration behind a switch

When wiring the change makes it live on a path that is hard to undo — a user-facing flow, a data migration, a change to a shared hot path — put it behind a feature flag or equivalent switch with a defined removal path, so the integration is reversible and can be turned off without a revert ([feature-flagging-risky-changes](../rules/risk/feature-flagging-risky-changes.md)). Whether a given change is "risky enough" to flag is that rule's discriminator; apply it here.

The output of this phase is a change that is reachable and exercised in the running system, with its callers intact. Reading it as a hostile reviewer, before anyone else does, is [self-review-the-diff](05-self-review-the-diff.md)'s work.
