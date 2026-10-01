# Report to where it matters

A shipping outcome that lands in a channel nobody watches, or addressed to nobody in particular, is an outcome nobody acts on — the regression rolls on because the person who owns the affected area never saw it.

## Resolve the channel and the audience

- **Audience = whoever owns the affected area.** Derive the owner from the change's touched area (the files/paths/components the diff changed) matched against the ownership data in config — the team roster's `owns` mappings and each member's messaging handle. The owner of the code the change touched is who hears about its landing and its health.
- **Channel = where that audience actually watches.** Route through the [communication](../../communication/SKILL.md) capability to the owner, at the messaging handle the roster records for them, not a generic firehose. The dispatch names the capability; the concrete destination lives in config and the adapter.
- **Unresolvable ownership degrades to broad, never to dropped.** If the touched area maps to no owner, or ownership data is absent, report to the broad channel praxis settings record (`tools.communication.channels.default`) and say the owner could not be resolved — a report to everyone is worse than a report to the right person, but far better than silence. With no broad channel recorded either, return the outcome locally, as below, and say why ([who-may-be-reached](../../communication/rules/who-may-be-reached.md)).

## What the report says — the outcome, not the machinery

The report is a **clean, team-facing account of what happened**: what change landed and where (which line, which environment), the gate status, the rollout's exposure and its health verdict (healthy / needs-rollback / indeterminate), and — when not healthy — what is being done or what the owner should do. It renders the *outcome and the decision*, and nothing about how the act produced it: no phase/agent/tool trace, no account of the run's internal steps, no praxis process ([clean-export](../../../craft/writing/clean-export.md)).

## The reach never blocks the landing

The landing and rollout outcomes are decided before this report; a reporting failure never undoes them. If the [communication](../../communication/SKILL.md) capability is unavailable (`tools.communication` unconfigured), **degrade**: return the outcome locally so the caller still has it, and note that it could not be posted (the `communication` skill owns guiding the user through `init:communication`). `(basis: doer-owns-prerequisites)`
