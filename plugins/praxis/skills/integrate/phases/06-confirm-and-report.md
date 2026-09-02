Shipping and walking away is how a green-looking deploy becomes a 2 a.m. page: the rollout was accepted, the dashboard was calm for five minutes, and the leak that exhausts the connection pool surfaced an hour later under real load. This phase closes the loop — it watches the post-ship signals, judges whether the change is actually healthy where it landed, and reports the outcome to whoever owns the affected area. It is the one phase that **always runs**: even a land-only run owes a report of its outcome; only the health *watch* is conditional on something having shipped.

## Read the post-ship signals through telemetry

When the run shipped ([ship-to-target](05-ship-to-target.md)), read the affected service's signals through the [telemetry](../../telemetry/SKILL.md) capability (a metric, error-aggregate, or log stream by reference) across a watch window. integrate declares no telemetry prerequisite — the `telemetry` skill owns `tools.telemetry` (doer-owns-prerequisites). Watch the **golden signals**: latency, traffic, errors, and saturation of the service the change touched.

## The health verdict — the method

`(basis: the health-judgment METHOD is authoritatively convergent — the four golden signals (latency, traffic, errors, saturation) as the minimal user-facing signal set (Google SRE Book, Ch.6); judge them relative to a baseline/control rather than an absolute, and prefer a freshly-comparable baseline over raw long-running production (Google SRE Workbook canarying; Netflix/Kayenta automated canary analysis — a long-lived prod cluster's warm caches confound the comparison); and require a SUSTAINED breach, not a transient spike, via error-budget burn-rate over paired long+short windows (SRE Workbook, "Alerting on SLOs"). The error budget is the ship/halt decision rule (SRE Book, Ch.3).)`

- **Compare to a baseline, over the window.** Judge each golden signal against its pre-ship baseline (or a control), not an absolute number, across the watch window — a single spike that recovers is not a breach; sustained consumption is.
- **Avoid the traps that fake health** `(basis: community canary-analysis lore, corroborated across independent practitioner accounts):` don't read an aggregate that masks a regional/endpoint spike — **slice** by endpoint/region/tenant; don't count HTTP-200 as success when the body is an error/fallback — measure the **outcome**; don't watch only p95 while p99 blows up — watch the **tail**; don't trust an unrepresentative canary slice (internal users, warm cache, one geo); and for leak/saturation classes, watch the **slope** (connections/memory trending up), not the instantaneous level — the leak is invisible at low load and exhausts later.

## The verdict — a three-value partition

The run resolves the health judgment to **exactly one** of:

- **healthy** — every key golden signal stayed within its baseline band for the full window, with no sustained breach. The ship stands.
- **needs-rollback** — a key signal breached its threshold in a *sustained* way (not a lone spike). The change should be reversed per the rollout's reversibility strategy / the `--on-fail` policy.
- **indeterminate** — the signal is too thin to judge: traffic or window too small to distinguish a real regression from noise (SRE guidance is explicit that a too-small canary reads noise as signal). **Report indeterminate honestly — never round it to healthy.** The correct response is to keep watching (with `--watch`), widen the window, or hand off the watch, not to declare success.

**Partition proof:** the three are mutually exclusive and exhaustive over the signal state — either a sustained breach exists (needs-rollback), or none exists *and* there was enough signal to be sure (healthy), or there was not enough signal to be sure (indeterminate). The third value is the one a binary verdict drops: "no breach seen" collapses *healthy* and *indeterminate* together and ships a "looks fine" that was really "couldn't tell." Every run that shipped lands in exactly one; a run that did not ship carries no health verdict (its terminal outcome is committed-only / opened-for-review / merged per [land-it](04-land-it.md)).

`(routed to maintainer: the numeric THRESHOLDS and the watch-window length are house-specific — the authorities are explicit that no numbers transfer across contexts (they depend on traffic volume, velocity, time of day). Method is pinned above; the burn-rate thresholds, the baseline band, and the window duration are the maintainer's to set (or wire to the project's SLOs). Proposed default: watch until the change has seen representative traffic across at least one full load cycle before calling healthy; below that, indeterminate.)`

## `--watch` and the fail policy

- **`--watch`** ([watch-the-pipeline](../modules/watch-the-pipeline.md)) keeps integrate attached until the run and signals *settle* before reporting — without it, integrate reads the currently-available signals once and reports the verdict as of now (often *indeterminate* for a fresh ship, said honestly). A `--watch` timeout with signals unsettled reports *indeterminate*, not healthy.
- **needs-rollback triggers the fail policy.** A needs-rollback verdict is a rollout failure for `--on-fail` purposes ([failure-policy](../modules/failure-policy.md)): default abort (stop and report the verdict), `rollback` reverses the ship where a reverse exists, `ask` surfaces it for a human.

## Before it goes out, read it as its reader

Put the finished report through [deliver-at-the-readers-register](../../communicate/rules/deliver-at-the-readers-register.md) before delivering it: take from that rule the obligations this phase has not already settled for itself, and apply its honesty floor to the result. A run with no register to write to falls back on the only vocabulary it has loaded — this procedure's own — which is how a report comes out accurate and unreadable. Read the floor from the rule item by item rather than from memory — the passages it protects are exactly the ones that read as padding to anyone not checking whether the claim is true — and let its carve-out for named levels and verdict values hold the graded rungs and status names this skill defines and reports on.

## Report to where it matters

Report the outcome — the terminal outcome from [land-it](04-land-it.md); the **gate status as a named field** (the hosted-CI verdict: `green` / `failed` / `degraded: hosted pipeline not consulted`) — required, so a run that never checked CI cannot report a clean "done" with the omission hidden; this named field is the completion trace for [run-the-gate](03-run-the-gate.md), which real runs skipped silently; and, if shipped, the health verdict and what's being done about a non-healthy one — through the [communication](../../communication/SKILL.md) capability, routed to whoever owns the affected area ([report-to-where-it-matters](../rules/report-to-where-it-matters.md)). The report is a clean, team-facing account of what shipped and whether it's healthy — never integrate's internal machinery.

**Degrade, per capability:** no `tools.telemetry` → the ship still stands but health can't be judged, so report **indeterminate** and say why; no `tools.communication` → return the outcome locally and note it couldn't be posted. A missing watch/report backend narrows what can be *observed or delivered*; it never undoes the land or ship. Under `--dry-run`, report the signals that *would* be watched and the channel that *would* be notified, without reading or posting.
