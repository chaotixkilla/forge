# Preserve the evidence

An action that changes the conditions destroys the evidence of how they were: a probe that rewrites the failing state, or a rollback, restart, failover or re-image that wipes the heap, the in-flight requests, the process state and the in-memory data that would have explained the failure. A failure you can reproduce only once is gone the moment your first change disturbs it, a rare or production-only one may not come back for days, and once the evidence is gone the explanation is reconstructed from memory instead of fact.

## Snapshot before you mutate

Before the first action that would change them, capture what the failure needs to be re-examined: the **inputs** that triggered it, the **state** at the point of failure (variables, data, the relevant store contents, process and thread state, open connections, in-flight requests), the **stack** or trace, and the **environment** (versions, config, timing conditions). Capture **most-volatile-first**: what the next moment erases goes before what will keep. The rarer and less reproducible the failure, the more this matters — for a one-shot production failure the capture may be the only witness you ever get, and an action that clears it can't be undone.

## The discriminators: capture first, or act now?

Not everything needs preserving — capturing isn't free, and over-capturing buries the signal. The test: **would losing this state cost you the failure or a hard-won observation?** Three questions decide it:

- **Does the action destroy it?** A probe that rewrites the failing state, and a rollback, restart, failover, re-image or terminate, wipe volatile state; shedding load, scaling out and adding capacity destroy nothing. An evidence-neutral action needs no capture first.
- **Is it gone forever, or durable?** Memory, process tables, open connections, the heap and in-flight requests die with the action; metrics, logs and traces already shipped to a store survive it, and a deterministic local failure you can re-trigger in seconds regenerates on demand — re-run it instead of snapshotting it. Capture only what the action would erase and nothing else can recover: a rare trigger, a production-only condition, a timing window, a corrupted store you're about to overwrite.
- **Is the capture cheap or expensive?** A thread dump, a metrics snapshot or a log tail costs seconds and destroys nothing — **grab them first, always; they are free insurance**. An expensive capture that itself deepens the damage (a full heap dump on a large heap at peak is a stop-the-world pause) is conditional: take it only on a confirmed need, such as a memory fault or evidence a security investigation must keep, and when the pause is tolerable — never reflexively. What counts as cheap enough to grab first is left to the responder's read of the outage's cost, deliberately open: it varies with the cost of each minute in ways no fixed number captures.

**Isolate instead of terminate** when you need both containment and evidence: quarantine the bad instance, cut off from the network, rather than killing it, so its state survives to be captured in parallel — "contain now, capture next" instead of either-or.

`(basis: Agans 2002, rule 6; Google SRE, Managing Incidents; RFC 3227 / BCP 55 §2.1–2.2; NIST SP 800-61r2 §3.3.1; the discriminators are the maintainer's)`

## Keep an audit trail as you go

Record each change you make and what happened after it — the experiments run, the values observed, the branches eliminated, the mitigations applied. This is what makes an elimination auditable, keeps one-change-at-a-time honest (you can see what's been varied and reverted), lets whoever explains the failure later tell your changes apart from the failure's own effects, and stops you re-running a test whose answer you already have.
