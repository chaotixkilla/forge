# Real signal vs flapping alert

The first judgment in triage is whether there is an incident at all. A firing alert is not proof of one: monitoring flaps, single probes blip, and a signal that oscillates and self-clears will burn a responder's night for nothing. Engage on noise and you train the team to ignore the pager (the alert-fatigue spiral); stand down on a real signal and you miss the incident. This rule is the bar that separates a genuine incident (**engage** — assign a severity and drive the response) from a flapping/transient alert (**stand down** — record it and route the noisy alert to be fixed, do not run the incident spine). It is applied in [confirm-the-signal](../phases/01-confirm-the-signal.md), and while narrowing a diagnosis it tells a causal signal from residual jitter.

## The four discriminators — engage when they converge

No single test is sufficient; combine them in this order, first match wins:

1. No user-facing symptom → a lead to **investigate**, not an incident.
2. Corroborated, or unmistakable by the hold test below → **engage**: an independent second signal outweighs oscillation and flappy history.
3. Oscillating past flap detection → noise, **stand down**.
4. Persisted past its hold → **engage** — unless the alert is known-flappy, which waits out one more hold first: still firing, engage; cleared, stand down with the alert flagged for fixing. (routed to maintainer: one extra hold for a known-flappy alert, since an alert that habitually clears in minutes and still fires after two holds is behaving unlike its history.)
5. Not yet past its hold → wait it out and judge again; cleared inside it → **stand down**.

`(basis: derived from symptom-based alerting, Ewaschuk)`

- **Persistence** — has the signal *stayed* firing past a metric-appropriate hold, or is it *oscillating* (ALERT↔OK repeatedly)? A real signal survives a hold timer; a transient blip clears inside it. A signal oscillating fast enough to trip flap detection (a high state-change ratio across its recent evaluations, at the threshold the alerting backend or the runbook sets) is noise, not an incident. `(basis: alerting practice of a hold duration before firing, and of flap detection over recent state changes)`
- **Symptom-mapping** — does the signal map to a **user-facing symptom** (errors users see, failing requests, latency they feel), or is it a **single internal probe** (one host's CPU, a queue depth) with no user-visible consequence? Engage on symptoms; a cause-metric with no symptom is a warning to investigate, not an incident to declare. `(basis: Ewaschuk, "My Philosophy on Alerting", Google SRE)`
- **Corroboration** — is the signal backed by an **independent or correlated** second signal, or is it alone? A user-facing error rate *and* a latency rise *and* support tickets is an incident; one metric with everything around it healthy is suspect. `(basis: Google SRE multi-window burn-rate alerting; alert correlation and suppression of dependent alerts)`
- **Known-flappy history** — does this alert have a track record of **auto-resolving within minutes** (about five) — at least three of its last five firings? (routed to maintainer: three of the last five, as the house default where the runbook sets none.) If it habitually clears itself, it waits out the extra hold in step 4 rather than engaging at once: it needs fixing, not paging. `(basis: incident-management practice of pausing notifications for alerts that habitually auto-resolve)`

## The tests, concretely

- **Wait out the hold, don't react to the edge.** A signal that just crossed threshold has not persisted — give it the signal's own hold window (its configured hold-for / evaluation window) before declaring, unless the impact is already **unmistakable**. *Unmistakable* means a user-facing SLI whose single reading already exceeds the burn rate its own fast-burn page fires at — where no SLO defines one, an error rate at least double its baseline and reaching users — **or** an already-corroborated signal; `(basis: SRE Workbook multi-window burn-rate alerting)` (routed to maintainer: double the baseline, for an SLI with no SLO.) either authorizes engaging immediately without waiting out the full soak, and it need not be a full outage. (Note "magnitude," not "sustained": persistence is exactly what the soak establishes, so it cannot also be the license to skip it — a single reading of sufficient magnitude, or corroboration, is what qualifies.) Soak only a marginal signal sitting near threshold from a single uncorroborated probe. A single sample across the line is the classic false positive.
- **Look for the symptom underneath the metric.** Before engaging on an internal-cause alert, check whether a user-facing SLI actually moved. If nothing users touch degraded, the signal is a lead for investigation, not a declared incident.
- **Check the neighbours.** One firing signal with all correlated signals healthy, and no support/user reports, is more likely instrumentation than incident.

## Anchors

- *Clearest REAL (engage now):* a user-facing error rate or latency SLI that has stayed above threshold past its hold window **and** is corroborated by a second correlated signal (or by both burn-rate windows) — a symptom, sustained, corroborated. Assign severity and drive the response.
- *Clearest FLAPPING (stand down):* a single internal probe oscillating OK↔ALERT within minutes, auto-resolving on its own, mapping to no user-visible symptom, with a known-flappy history. Record it, route the noisy alert to be tuned, and do not open the incident spine.

## The sanity bar

If triage is engaging on more than roughly **two actionable incidents per 12-hour on-call shift** as a steady state, the bar is set too loose, and it's the alerting, not the responder, that needs work. `(basis: Google SRE, "Being On-Call")` This is a calibration check on the rule itself, not a per-incident test.
