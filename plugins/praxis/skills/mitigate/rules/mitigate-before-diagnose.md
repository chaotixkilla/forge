# Mitigate before diagnose

Under a live incident, the goal is to stop users being hurt — not to understand why they are being hurt — and the first comes first. It is the authority a plain investigation defers to: diagnosis never patches a symptom from its own read of production, because that authority lives here, under a declared incident. This rule is one pole of a genuine tension; its counterpart is preserving the evidence ([preserve-the-evidence](../../../craft/evidence/preserve-the-evidence.md)), and the two are held as a fork, not a ranking — settled in *When the evidence comes first*, below.

## The method

- **Separate stopping the harm from explaining it.** In [choose-the-mitigation](../phases/01-choose-the-mitigation.md) the only question is "what restores service fastest and safely?" — not "what caused this?" Finding the cause comes after, and isn't mitigate's.
- **Prefer the fastest *reversible* mitigation.** "Safe" means reversible and bounded in blast radius: a rollback, a feature-flag off, a failover to a known-good replica and shedding load are reversible; a schema migration or a data backfill to "fix" it forward is not. Reach for the reversible one first, because if it makes things worse you can undo it. An irreversible mitigation is a last resort, taken only with the user's confirmation ([choose-the-mitigation](../phases/01-choose-the-mitigation.md)).
- **Know whether the mitigation is provisional or durable — one test decides it: can the offending behavior recur through normal operation?** If **no** — the offending change is gone or permanently disabled — the mitigation is **durable**: it can stand as the resolution once baseline holds, with any forward re-fix (re-landing the feature correctly) or dead-code cleanup tracked as a separate follow-up, not an open incident. A rollback of the bad deploy, a revert of the bad config, and a feature-flag kept off for good (the feature killed, the now-dead code tracked for removal) are durable — the offending path won't return by itself. If **yes** — the offending behavior resumes as soon as normal operation does — the mitigation is **provisional**: a failover that leaves the bad code running, a feature-flag off you intend to re-enable, a rate-limit you'll lift, a restart that clears transient state — a stop-gap with the real fix still owed. Record which it is: it's the primitive the incident's resolution turns on, and a provisional stop-gap left unaudited becomes a permanent "temporary" workaround hiding a live cause. `(basis: derived from whether the cause is gone)`

## Speed now, attribution later

Stopping the harm and explaining it pull in opposite directions, and the resolution is knowing which one you're doing. **While mitigating, speed wins**: apply the reversible mitigation and stop the bleeding, even if it's several things at once, because restoring service outranks clean attribution. **While diagnosing, attribution wins**: one change at a time ([change-one-thing-at-a-time](../../../craft/evidence/change-one-thing-at-a-time.md)). The failure is reading a mitigation, batched and fast, as if it were a diagnostic experiment: you get neither restored service you can trust nor a clean signal. Record what each mitigation changed, so whoever diagnoses can tell it apart from the failure. `(basis: controlled-experiment and scientific-debugging discipline)`

## When the evidence comes first

Default to mitigate-first. **Override to capture-first only when both hold:**

1. the mitigating action would **destroy** the evidence — it wipes volatile, non-reproducible state (in-memory data, process and thread state, in-flight requests, ephemeral container state), as rollback, restart, failover, re-image and terminate do; **and**
2. that evidence is **gone forever** if not captured now — it is not already durable in shipped telemetry or logs, and not reconstructable after the action.

When both hold, capture the volatile evidence first, most-volatile-first, then mitigate. When either fails — the fix is evidence-neutral (shedding load, scaling out and adding capacity destroy nothing), or the evidence already lives in durable telemetry — there is no tension: just mitigate. Either way the routing only orders the stabilize step; it never blocks the run. What to capture, and the cheap-versus-expensive call on each capture, are [preserve-the-evidence](../../../craft/evidence/preserve-the-evidence.md)'s.

The default bias flips by incident type. An **availability or reliability** incident, where evidence is usually already durable telemetry → mitigate-first (`(basis: Google SRE, "stop the bleeding, restore service, and preserve the evidence")`). A **security or forensic** incident, or one that may become legal or regulatory → preservation weighs heavily and can precede destructive containment: don't shut down until evidence collection is complete, weighing evidence-preservation against service availability and time-to-capture deliberately (`(basis: RFC 3227 / BCP 55 §2.1–2.2; NIST SP 800-61r2 §3.3.1)`). The routing rule above selects between the two biases per incident; the bias never overrides it.

`(basis: derived from Google SRE's mitigate-first and the preserve-first of RFC 3227 and NIST)`

## The tradeoff, in a line

Mitigating first can cost a still-live cause — but only when the mitigation is **provisional**: a stop-gap that leaves the cause able to recur carries that recurrence risk as a follow-up, whereas a **durable** mitigation (a rollback / revert / permanent-kill) removes the cause and carries no such risk. And any mitigation, durable or not, can cost the evidence that would explain the incident — that evidence risk is what *When the evidence comes first* routes, independent of the durable/provisional split.

`(basis: Google SRE, "Managing Incidents" and "Emergency Response")`
