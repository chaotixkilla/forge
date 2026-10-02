# The root-cause-confidence scale

Every cause debug claims carries a confidence, and confidence is what the diagnosis's recipient reads to decide the next move: fix it now, fix it provisionally, or gather more evidence. The claim "I found the root cause" hides a range — from "I can switch the failure on and off by toggling this line" to "the errors started around when this shipped, so it's probably this." Those are not the same finding, and a skill that treats them alike fixes on a guess: it patches a coincidental trigger, ships, and the bug returns because the real cause was never touched.

Confidence answers one question: **how much of the chain from the claimed cause to the observed failure have you actually demonstrated?** It is assigned in [confirm-root-cause](../phases/05-confirm-root-cause.md) and consumed by [report-the-diagnosis](../phases/06-report-the-diagnosis.md), which routes on it, and by whoever applies the fix it recommends. It is distinct from *severity* (how bad the failure is) — a trivial bug can have a confirmed mechanism; a catastrophic one can sit at suspected. Grade the two apart.

## The three levels

`(basis: maintainer, 2026-07-10; after Zeller, Why Programs Fail)`

- **confirmed-mechanism** — you can make the failure appear and disappear on demand by toggling **only** the claimed cause (a controlled experiment — change one thing, the effect changes; revert it, the effect reverts), **and** you can name every link in the chain from that cause to the observed symptom. The mechanism is proven, so the fix is derived from it, not hoped at.
  - *Anchor (top of scale):* re-introducing the off-by-one makes the reproduction fail; reverting exactly that line makes it pass, repeatably; and you can trace the dropped index → the truncated slice → the missing last record in the observed output.
- **probable** — a single mechanism explains all the observed evidence with nothing contradicting it, **and** you have proven at least one link of the chain by direct observation (instrumented the boundary and watched the bad value cross it, caught it at its origin, or bisected to the change that introduced it) — but you have **not** shown full appear/disappear-on-demand control: the failure is intermittent, environment-bound, or the toggle is impractical to run. The mechanism fits best; a second one cannot be fully excluded.
  - *Anchor:* under load the request intermittently reads a stale cache entry; you have logged the stale read at the boundary and it lines up with every failure, but you cannot yet force the timing on demand, so you cannot toggle the failure at will.
- **suspected** — a candidate cause is consistent with the symptom, but the chain is mostly **inferred** — from correlation ("it started when X shipped"), from a code path you read but did not run, or from a hypothesis not yet tested against a live observation. It could still be a coincidental trigger or a downstream symptom.
  - *Anchor (bottom of scale):* the errors began around the caching-layer deploy and the stack trace passes through the cache, so the cache is probably at fault — no demonstrated toggle, no observed link, just co-occurrence.

## The adjacent-level discriminators

Assign by walking **up** from suspected until a rung's test fails; the boundary tests are what stop a finding sliding between rungs:

- **confirmed-mechanism vs probable** — can you toggle the failure on and off by changing *only* the claimed cause (a controlled experiment), *and* name every link cause→symptom? Confirmed-mechanism. Can you explain a mechanism that fits all the evidence but *cannot* demonstrate the on-demand toggle (intermittent, environment-bound, or impractical to toggle)? Probable. (demonstrated causal control + a complete chain)
- **probable vs suspected** — have you proven at least one link of the chain by *observing the running system* ([observation-over-inference](../../../craft/evidence/observation-over-inference.md)) — an instrumented value, a caught origin, a bisected commit? Probable. Is *every* link still inferred from correlation, names, or reading rather than a run you watched? Suspected. (one observed link vs an all-inferred chain)

When a finding seems to sit between two rungs, the higher wins only if you can point to the specific demonstration it requires — the controlled toggle for confirmed, the one observed link for probable; absent that demonstration, drop a rung, and re-check the finding against [fix-the-cause-not-the-symptom](../../../craft/evidence/fix-the-cause-not-the-symptom.md).

## What the rung decides

debug fixes nothing. Its own outcome reads off the rung, by [report-the-diagnosis](../phases/06-report-the-diagnosis.md): confirmed-mechanism and probable (with an observed link) report a confirmed diagnosis; suspected reports inconclusive. Whether a fix may then be made, and when a probable cause may be fixed provisionally, is the fixing act's call ([fixing-a-bug](../../work/acts/fixing-a-bug.md)). An intermittent bug whose trigger you cannot yet control caps at **probable** until you can force the timing — statistical reproduction (the failure rate drops to zero across many runs after the fix) is how a fix is judged there, in place of a clean deterministic toggle.
