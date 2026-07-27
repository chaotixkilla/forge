# Preserve the evidence

The counterpoint to [mitigate-before-diagnose](mitigate-before-diagnose.md): the fastest mitigation is often the one that destroys the evidence root-cause will need. A rollback, restart, failover, or re-image wipes the heap, the in-flight requests, the process state, and the in-memory data that would have explained the failure — and once it's gone, the postmortem is reconstructed from memory instead of fact. So mitigate-first is the default, but it is not unconditional: when the mitigating action would erase volatile, non-reproducible state, you capture that state *before* you stabilize. This rule pins the routing rule that decides which pole wins for a given incident.

## The routing rule — when to snapshot before stabilizing

Default to mitigate-first. **Override to capture-first only when both hold:**

1. the mitigating action would **destroy** the evidence — it wipes volatile, non-reproducible state (in-memory data, process/thread state, in-flight requests, ephemeral container state), as rollback/restart/failover/re-image/terminate do; **and**
2. that evidence is **gone forever** if not captured now — it is not already durable in shipped telemetry/logs and not reconstructable after the action.

When both hold, capture the volatile evidence first, **most-volatile-first**, then mitigate. When either fails — the fix is evidence-neutral (shed load, scale out, add capacity destroy nothing), or the evidence already lives in durable telemetry — there is no tension: just mitigate.

## The discriminators that route it

- **Does the mitigation destroy the evidence?** Rollback / restart / failover / re-image / terminate wipe in-memory and in-flight state; shed-load / scale-out / add-capacity do not. If the fix is evidence-neutral, mitigate freely.
- **Is the state gone-forever or durable?** RAM, process tables, open connections, heap, in-flight requests are destroyed by the action; metrics/logs/traces already shipped to a store survive it. Capture only what the action would erase and nothing else can recover.
- **Is capture cheap or expensive?** A thread dump, a metrics snapshot, a log tail cost ~seconds and are non-destructive — **grab them first, always; they are free insurance**. An expensive capture that itself worsens the outage (a full heap dump on a large heap at peak is a stop-the-world pause) is size/traffic-**conditional** — take it only if a memory issue is confirmed and the pause is tolerable, never reflexively.
- **Can you isolate instead of terminate?** When you need both containment and evidence, prefer network-isolating/quarantining the bad instance over killing it — it preserves the state so you can capture in parallel, turning an either/or into "contain now, capture next."

## The domain default

The default bias flips by incident type. An **availability/reliability** incident where evidence is usually already durable telemetry → mitigate-first (`(basis: Google SRE — "stop the bleeding, restore service, and preserve the evidence for root-causing"; the evidence is normally the shipped metrics, cheap and not destroyed by the fix)`). A **security/forensic** incident, or one that may become legal/regulatory → preservation weighs heavily and can precede destructive containment (`(basis: RFC 3227 / BCP 55 §2.1–2.2 order of volatility and "don't shut down until you've completed evidence collection"; NIST SP 800-61r2 §3.3.1 — weigh evidence-preservation against service-availability and time-to-capture deliberately)`).

`(basis: the fork is between Google SRE's mitigate-first (availability) and RFC 3227 / NIST DFIR's preserve-first (security-forensic); they do not contradict — they apply to different evidence-volatility profiles, and the routing rule above is the hinge that selects between them per incident. Non-gating: it routes the stabilize step, it does not block the run. The exact "cheap capture" threshold — what counts as fast enough to grab first — is left to the responder's read of the outage cost, deliberately open because it varies with the incident's cost-per-minute in ways no fixed number captures.)`
