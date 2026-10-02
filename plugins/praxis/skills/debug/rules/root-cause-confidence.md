# The root-cause certainty

Every cause debug claims carries a certainty, and the certainty is what the diagnosis's recipient reads to decide the next move: fix it now, fix it provisionally, or gather more evidence. The claim "I found the root cause" hides a range — from "I can switch the failure on and off by toggling this line" to "the errors started around when this shipped, so it's probably this." Those are not the same finding, and a skill that treats them alike fixes on a guess: it patches a coincidental trigger, ships, and the bug returns because the real cause was never touched.

The words are the shared certainty scale, defined with its discriminators in [results-and-certainty](../../../craft/evidence/results-and-certainty.md): observed, traced, inferred, unverified. This rule holds what debug adds: how a *causal* claim places on that scale, and the floor a cause must reach to be a diagnosis. The certainty is assigned in [confirm-root-cause](../phases/05-confirm-root-cause.md) and consumed by [report-the-diagnosis](../phases/06-report-the-diagnosis.md), which routes on it, and by whoever applies the fix it recommends. It is distinct from *severity* (how bad the failure is) — a trivial bug can have an observed mechanism; a catastrophic one can sit at unverified. Grade the two apart.

## Placing a cause

The claim graded is *this cause produces this failure*. For that claim, "seen happening" is the **controlled toggle**: change only the claimed cause and the failure goes; revert it and the failure returns. A reproduction watched failing shows the failure, not its cause. `(basis: maintainer, 2026-07-10; after Zeller, Why Programs Fail)`

- **observed** — you can make the failure appear and disappear on demand by toggling **only** the claimed cause, **and** you can name every link in the chain from that cause to the symptom.
  - *Anchor (top):* re-introducing the off-by-one makes the reproduction fail; reverting exactly that line makes it pass, repeatably; and you can trace the dropped index → the truncated slice → the missing last record in the observed output.
- **traced** — every link from cause to symptom was read or watched, but the toggle wasn't run: the failure is intermittent, environment-bound, or the toggle is impractical.
- **inferred** — at least one link is reasoned rather than read or watched: an interleaving assumed, a caller left unopened.
  - *Anchor:* under load the request intermittently reads a stale cache entry; you have logged the stale read at the boundary and it lines up with every failure, but the interleaving that makes the entry stale is reasoned, and you cannot force the timing on demand.
- **unverified** — the cause rests on correlation, a name, a stack frame passing through, or a hypothesis not yet tested, with nothing of the chain worked through.
  - *Anchor (bottom):* the errors began around the caching-layer deploy and the stack trace passes through the cache, so the cache is probably at fault — no toggle, no link read or watched, just co-occurrence.

Between two levels, the standard's tie-break decides, with the toggle as the evidence observed needs; on a drop, re-check the cause against [fix-the-cause-not-the-symptom](../../../craft/evidence/fix-the-cause-not-the-symptom.md).

## The diagnosis floor

A cause is a diagnosis when both hold:

1. a single mechanism explains all the observed evidence, with nothing contradicting it; and
2. the cause is **observed**, or it is **traced** or **inferred** with at least one link watched on the running system — an instrumented value crossing a boundary, the bad state caught at its origin, or a bisection to the change that introduced it ([observation-over-inference](../../../craft/evidence/observation-over-inference.md)).

A cause below the floor is unverified, or a chain worked through by reading alone. The floor is the watched-link test, not a cut on the scale, so a chain read end to end but never run stays below it: with a reproduction in hand one watched link is cheap, and a misread path hides in reading alone. `(basis: maintainer, 2026-10-02)`

## What the certainty decides

debug fixes nothing. Its own outcome reads off the floor, by [report-the-diagnosis](../phases/06-report-the-diagnosis.md): a cause at the floor is a diagnosis that holds; a run that reproduced but ends below the floor is unsettled. Whether a fix may then be made, and when a cause below observed may be fixed provisionally, is the fixing act's call ([fixing-a-bug](../../work/acts/fixing-a-bug.md)). An intermittent bug whose trigger you cannot force caps below **observed** until you can — statistical reproduction (the failure rate drops to zero across many runs after the fix) is how a fix is judged there, in place of a clean deterministic toggle.
