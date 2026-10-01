Shipping and walking away is how a green-looking deploy becomes a 2 a.m. page: the rollout was accepted, the dashboard was calm for five minutes, and the leak that exhausts the connection pool surfaced an hour later under real load. This phase always runs: a run that promoted nothing still returns its outcome and why; only the health read waits on something having rolled out.

## Read the post-ship signals through telemetry

When the change rolled out ([promote](02-promote.md)), read the affected service's signals through the [telemetry](../../telemetry/SKILL.md) capability (a metric, error-aggregate, or log stream by reference) across a watch window. roll-out declares no telemetry prerequisite — the `telemetry` skill owns `tools.telemetry` (doer-owns-prerequisites). Watch the **golden signals**: latency, traffic, errors, and saturation of the service the change touched.

## The health verdict — the method

`(basis: Google SRE Book, ch. 3 and 6; SRE Workbook, canarying and "Alerting on SLOs"; Netflix Kayenta)`

- **Compare to a baseline, over the window**, by [confirm-the-signal-holds](../../../craft/evidence/confirm-the-signal-holds.md): each golden signal judged against its pre-ship baseline (or a control) as that standard defines it, held for the window it derives, with the traps that fake health avoided. Prefer a freshly comparable baseline over a long-running production cluster, whose warm caches confound the comparison; the error budget is the ship/halt rule.

## The verdict — a three-value partition

The run resolves the health judgment to **exactly one** of:

- **healthy** — every key golden signal stayed within its baseline band for the full window, with no sustained breach. The ship stands.
- **needs-rollback** — a key signal breached its threshold in a *sustained* way (not a lone spike). The change should be reversed per the rollout's reversibility strategy / the `--on-fail` policy.
- **indeterminate** — the signal is too thin to judge: traffic or window too small to distinguish a real regression from noise (SRE guidance is explicit that a too-small canary reads noise as signal). **Report indeterminate honestly — never round it to healthy**: hand off the watch with the last observed state and what would settle it, as the standard says, never declaring success.

**Partition proof:** the three are mutually exclusive and exhaustive over the signal state — either a sustained breach exists (needs-rollback), or none exists *and* there was enough signal to be sure (healthy), or there was not enough signal to be sure (indeterminate). The third value is the one a binary verdict drops: "no breach seen" collapses *healthy* and *indeterminate* together and ships a "looks fine" that was really "couldn't tell." Every run that rolled out lands in exactly one; a run that didn't roll out carries no health verdict.

The numbers — the burn-rate thresholds, the baseline band and the watch-window length — are house-specific: the maintainer sets them or wires them to the project's SLOs, since no numbers transfer across contexts (they depend on traffic volume, velocity and time of day). `(routed to maintainer: call healthy only after representative traffic across at least one full load cycle, below that indeterminate; the authorities set no numbers)`

## `--watch` and the fail policy

- **`--watch`** ([watch-the-pipeline](../modules/watch-the-pipeline.md)) keeps roll-out attached until the run and signals *settle* before returning — without it, roll-out reads the currently-available signals once and reports the verdict as of now (often *indeterminate* for a fresh ship, said honestly). A `--watch` timeout with signals unsettled reports *indeterminate*, not healthy.
- **needs-rollback triggers the fail policy.** A needs-rollback verdict is a rollout failure for `--on-fail` purposes ([failure-policy](../modules/failure-policy.md)): default abort (stop and report the verdict), `rollback` reverses the ship where a reverse exists, `ask` surfaces it for a human.

## The run's terminal outcome

Every executing, run-to-completion roll-out run resolves to **exactly one** outcome, read off one physical fact: *is a deploy of the change in place on the environment, not reversed?*

- **rolled-out** — yes, at whatever exposure this run reached: dark behind an off-switch, a partial canary, or full.
- **not-rolled-out** — no. The result names why: no environment named, the environment doesn't deploy from the change's branch, the environment couldn't be resolved to a deploy source, the pipeline was unavailable, the promotion failed before deploying, or a `rollback` reversed the deploy.

Two states are not members. A `--dry-run` reports its *would-be* outcome, evaluated as if the flag were unset and read-only. An `--on-fail=ask` pause has no outcome until it's answered, and where the run can't ask, `ask` acts as `abort` ([failure-policy](../modules/failure-policy.md)). Three axes are reported alongside and never move the outcome: the **exposure** reached, the **health verdict** (rolled-out runs only), and any **pending `--on-fail` action**. `(basis: derived from the one physical fact; the three axes, maintainer, 2026-07-11)`

## Close the phase

Return the outcome with what a caller needs to report it: the environment, the strategy and risk tier, the exposure reached and the stages that remain, the health verdict with the signals behind it and what a non-healthy verdict calls for, and, for *not-rolled-out*, why.

**Degrade, per capability:** no `tools.telemetry` → the rollout still stands but health can't be judged, so the verdict is **indeterminate**, with why. A missing watch backend narrows what can be *observed*; it never undoes the rollout. Under `--dry-run`, return the signals that *would* be watched, without reading them.
