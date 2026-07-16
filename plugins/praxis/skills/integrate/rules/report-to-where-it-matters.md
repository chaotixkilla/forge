# Report to where it matters

A ship outcome that lands in a channel nobody watches, or addressed to nobody in particular, is an outcome nobody acts on — the regression rolls on because the person who owns the affected area never saw it. Reporting is not "post a message somewhere"; it is getting the *right* outcome to the *right* audience through the channel the team actually reads. This rule pins how the channel and the audience are resolved, what the report contains, and what to do when ownership can't be determined — so the report reaches someone accountable rather than a void.

## Resolve the channel and the audience

- **Audience = whoever owns the affected area.** Derive the owner from the change's touched area (the files/paths/components the diff changed) matched against the ownership data in config — the team roster's `owns` mappings and each member's messaging handle. The owner of the code the change touched is who hears about its landing and its health.
- **Channel = where that audience actually watches.** Route through the [communication](../../communication/SKILL.md) capability to the channel configured for the team/area, not a generic firehose. The dispatch names the capability; the concrete destination lives in config and the adapter.
- **Unresolvable ownership degrades to broad, never to dropped.** If the touched area maps to no owner, or ownership data is absent, report to the team's default/broad channel and say the owner could not be resolved — a report to everyone is worse than a report to the right person, but far better than silence. Do not drop the report because you couldn't find its ideal audience.

## What the report says — the outcome, not the machinery

The report is a **clean, team-facing account of what happened**: what change landed (and shipped), where it landed (which line, which environment), the health verdict from [confirm-and-report](../phases/06-confirm-and-report.md) (healthy / needs-rollback / indeterminate), and — when not healthy — what is being done or what the owner should do. It renders the *outcome and the decision*, and nothing about how integrate produced it: no phase/agent/tool trace, no account of the run's internal steps, no praxis process. `(basis: this is the ratified clean-export bar for team-facing output — "artifacts are team-facing documents … the content and the decisions, never the machinery" (USING-ANVIL-ON-PRAXIS.md §2). A channel report is team-facing output the same as a published artifact, so it carries the same no-internal-process discipline; the audience wants to know what shipped and whether it's healthy, not which skill or agent ran.)`

## The reach never blocks the land

`--on-fail` and the land/ship outcome are decided before this report; a reporting failure never undoes them. If the [communication](../../communication/SKILL.md) capability is unavailable (`tools.communication` unconfigured), **degrade**: return the outcome locally so the caller still has it, and note that it could not be posted (the `communication` skill owns guiding the user through `init:communication`). `(basis: doer-owns-prerequisites — integrate declares no communication prerequisite; the report is the last, most-degradable step, and a missing channel narrows delivery to local, it never rolls back a landed change. USING-ANVIL §2.)`
