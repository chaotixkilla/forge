The fastest mitigation is often the one that destroys what would explain the incident. This phase decides, before anything is applied, whether to capture that evidence first.

## Snapshot before you stabilize when the mitigation would erase the evidence

Before executing a mitigation that destroys volatile state, run the routing check in [mitigate-before-diagnose](../rules/mitigate-before-diagnose.md) (*When the evidence comes first*): if the action would wipe non-reproducible state (rollback/restart/failover/re-image wipe heap, in-flight requests, process state) **and** that state isn't already durable in shipped telemetry, capture it first — most-volatile-first, by [preserve-the-evidence](../../../craft/evidence/preserve-the-evidence.md). The cheap captures (a thread dump, a metrics snapshot, a log tail) are always worth the seconds; an expensive capture that would itself deepen the outage (a large heap dump at peak) is conditional on a confirmed need and a tolerable pause. When the fastest fix is evidence-neutral (shed load, scale out) or the evidence already lives in telemetry, there is no tension — just mitigate. Where you need both containment and evidence, isolate rather than terminate.

The output of this phase: what was captured, where it is, and what was deliberately left uncaptured and why, for [apply-and-confirm](03-apply-and-confirm.md).
