# Confirm the signal holds

A change to a running service — a mitigation, a rollout — isn't confirmed when it's applied, and not when the first read looks calm. A dashboard quiet for five minutes says nothing about the leak that exhausts the connection pool an hour later under real load, and an alert that cleared is the start of confirming, not the end. What confirms the change is the signal holding at its baseline for as long as the signal itself takes to settle.

## Baseline is defined, not eyeballed

The signal is at **baseline** when the user-facing measure — the SLI, the symptom metric, each golden signal of the service the change touched (latency, traffic, errors, saturation) — is back within, or stays within, its range from before the change, or a control's. Where the signal is SLO-based, the burn rate is below threshold on **all** its configured windows, the paired long and short ones, not the instantaneous rate dipping under the paging line once. A single spike that recovers is not a breach; sustained consumption is.

`(basis: Google SRE, "Alerting on SLOs"; SRE Workbook, canarying; Netflix Kayenta)`

## How long it must hold, and how often to look

- **The hold** is derived from the signal's own evaluation window — its configured hold-for duration (the soak the signal itself requires before firing), the burn-rate long window, or the recheck count that defines it — so the hold matches what the signal itself considers settled. Where no window can be derived from the signal, a fallback window applies: the one the work pins for its kind of change — how long a fix must hold isn't how long a ship must prove itself — and, where none is pinned, one representative traffic cycle. A signal that defines its own window always overrides a fallback. `(basis: Prometheus for and keep_firing_for; SRE burn-rate windows; Nagios max_check_attempts)`
- **The reads** come at least once per the signal's refresh interval — its scrape or update cadence. Reading faster than the signal refreshes only re-reads jitter; reading slower can miss a regression mid-watch.

## The traps that fake health

`(basis: corroborated community canary-analysis lore)`

- **An aggregate that masks a spike** — slice by endpoint, region or tenant.
- **A success status over a failed outcome** — an HTTP 200 whose body is an error or a fallback; measure the outcome, not the status, since a success surface is not the effect ([observation-over-inference](observation-over-inference.md)).
- **A healthy median over a failing tail** — watch p99, not only p95.
- **An unrepresentative sample** — internal users, a warm cache, one geography.
- **A level that hides a slope** — for leak and saturation classes, watch connections or memory trending up, not the instantaneous level; the leak is invisible at low load and exhausts later.

## Three states, and the thin one is never rounded up

A watch ends in exactly one of: the signal **held** at baseline through the window; it **regressed** — a sustained breach during the watch, so the change didn't hold; or it's **too thin to judge** — too little traffic, or too short a window, to tell a real regression from noise. The third is the one a two-value read drops: "no breach seen" collapses *held* and *too thin* together and reports a "looks fine" that was really "couldn't tell". So a thin signal is reported as unsettled, never rounded up to held. Hand the watch off instead: report the last observed state and what would settle it. A run doesn't extend its own window, since nobody is there to choose a longer one; and when the signal becomes unreadable mid-watch, report the last observed state as unsettled and say the watch couldn't continue.

`(basis: derived — a watch that extended itself would have no end, and a watch run doesn't ask)`
