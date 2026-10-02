# The incident-severity scale

Every incident carries a severity, and severity is the dial the rest of the response turns on: it sets how fast and how widely the response communicates, how aggressively it mitigates, and how high the bar sits for declaring the incident resolved.

Severity is assigned in [scope-and-grade](../phases/02-scope-and-grade.md), and only *after* [real-signal-vs-flapping](real-signal-vs-flapping.md) has confirmed there is a real incident to rate — a flapping alert is stood down, not assigned a severity. It answers one question: **how badly is the user's ability to use the product affected, and how widely?**

## The three levels

`(basis: maintainer, 2026-07-11; discriminators after the published incident-response guides of PagerDuty, Atlassian and incident.io, and ITIL)`

- **SEV1 — critical** — a core customer-facing capability is completely unavailable for all or most users, **or** confirmed data loss/corruption, **or** a security/privacy breach. No workaround; the product cannot be used for its primary purpose.
  - *Anchor (top of scale):* the primary API returns errors for every request — all users are locked out; or customer records have been irreversibly deleted; or an auth bypass is exposing one tenant's data to another.
- **SEV2 — major** — key functionality is broken or badly degraded, but the damage is bounded: a subset of users, or a non-core flow for everyone, with a painful-but-real workaround or partial availability. The product is impaired, not down.
  - *Anchor:* checkout succeeds but retries for ~10% of users on one payment method; or search returns results 5× slower than baseline for everyone while the rest of the app is fine.
- **SEV3 — minor** — minor or cosmetic impact with a ready workaround; users are largely unaffected and the fix can wait for business hours.
  - *Anchor (bottom of scale):* a secondary dashboard shows a stale timestamp; a layout glitch on a rarely-visited settings page.

## The adjacent-level discriminators

Assign by walking down from SEV1 until a level fits; the boundary tests are what stop an incident sliding between two rungs:

- **SEV1 vs SEV2** — is the impact *total and unworked-around* on a core capability (full outage of a primary flow, data loss, or a breach)? SEV1. Is it *bounded* — a subset of users, a non-core flow, or a real workaround exists — so the product stays usable? SEV2. (functional impact + blast radius + recoverability)
  - **Partial degradation of a core flow** (some requests fail, most succeed) is the case the round-up clause most often gets misapplied to, so pin it: the rung turns on **effective usability**, not the raw error fraction. If most affected users can still complete the action — a retry succeeds, a workaround exists — it is **SEV2** even on a revenue-critical flow. It rounds up to **SEV1** only when the failure rate is high enough that the capability is *effectively unusable* for **all or most users** — not merely a bounded subset, since a total failure confined to a small subset stays SEV2 by the blast-radius test above — or data-loss/breach is in play. An elevated error rate alone does not make a SEV1 — *effective unavailability* of a core capability, at scale, does. *Worked example:* checkout errors at ~12% with retries succeeding → SEV2 (most users still complete); checkout failing for most attempts → SEV1. `(basis: derived from the impact-keyed ladder and PagerDuty's published severity definition ("unable to use the product") as the top-rung gate)`
- **SEV2 vs SEV3** — does a *real user on a path they actually use* hit *broken or badly degraded* behavior? SEV2. Is the impact *cosmetic or trivially worked around*, with users largely unaffected? SEV3. (functional impact + user impact)

When two levels both seem to fit, **round up** — but only if you can name the affected capability, the scope, or the user impact that justifies the higher rung; absent that concrete impact, drop a level. `(basis: the published incident-response guides of PagerDuty and incident.io)`

## Duration is a secondary axis — re-assess as the incident ages

Severity is not fixed at declaration. A lower-severity incident that **persists** or is **actively worsening** escalates: a SEV2 degradation that is still spreading an hour in, or a SEV3 that has begun affecting a core flow, is re-rated up, and the re-rating tightens the communication cadence with it. `(basis: the duration boundary in Atlassian's published incident handbook; ITIL's urgency axis)` Treat the severity set in triage as the *current* rung, and re-open it whenever the blast radius or duration changes materially.

## When the runbook defines a different scale

This 3-level ladder is the house default, not a mandate. If the project's runbook already runs on a different vocabulary — a P1–P5 priority scheme, a 5-level SEV0–SEV4 with a public-comms-gated top rung, ITIL priority — **adopt the runbook's scale and its boundaries**, do not re-map it to SEV1–3 ([match-the-runbook-conventions](../../../craft/engineering/match-the-runbook-conventions.md)). The one genuine fork the authorities leave open is the **top rung**: whether SEV1 is earned by impact alone (this default, and the Atlassian and incident.io guides) or additionally requires a public-notification / executive-liaison trigger (the PagerDuty guide's SEV-1). This default keys the top rung to impact; a runbook that gates it on public comms is honored when present. Either way, the discriminators above — functional impact, blast radius, user impact — are what place the incident; only the labels and the top-rung gate change.
