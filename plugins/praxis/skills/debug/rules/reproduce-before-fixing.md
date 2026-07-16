# Reproduce before fixing

A fix you cannot make fail on demand is a fix you cannot verify — you change something, the failure doesn't appear, and you have no way to tell whether you fixed it or whether it simply didn't fire this time. Every confident "fixed" with no reproduction behind it is a coin flip reported as a result. This rule makes a reliable trigger a precondition for acting, not an afterthought.

## Build the trigger first

Before forming a fix, construct the smallest reliable way to make the failure happen: the input, state, and steps that produce it on demand. This trigger does triple duty — it is the thing your experiments toggle against ([confirm-root-cause](../phases/05-confirm-root-cause.md)'s controlled test needs it), the thing your fix has to switch off, and the seed of the regression test that keeps it dead ([guard-against-regression](guard-against-regression.md)). No trigger, no verifiable fix.

## When it won't reproduce deterministically

Non-determinism doesn't excuse skipping this — it changes the form of the trigger:

- **Intermittent (timing/concurrency/environment):** build a **statistical reproduction** — a harness that runs the trigger enough times to make the failure appear at a measurable rate, optionally *amplifying* the rate first (inject delays or scheduling jitter, add resource pressure, run under a sanitizer) so it's frequent enough to work with. Judge a fix by the **rate before vs. after**, not one run. Note the honesty limit: zero failures in N runs *bounds* the failure rate, it does not *prove* the fix — so pair a statistical fix with instrumentation that will catch the "impossible" state if it recurs.
- **Capturable but rare:** if you can catch the failure once, a record/replay capture lets you replay it deterministically as many times as the investigation needs — turning a one-in-a-thousand failure into a repeatable one without paying the reproduction cost each pass.

## The discriminator: reproduced enough to proceed?

You may proceed to localize and fix when the failure is **deterministic**, or **intermittent with a statistical harness that fires often enough to measure**. You may **not** proceed to a fix when it is **not-yet-reproduced** — there, reproduction *is* the task ([reproduce-and-frame](../phases/01-reproduce-and-frame.md)): gather more evidence to reconstruct the trigger, and if it truly can't be reached, report that with what's needed rather than guessing at a fix. Confidence in the eventual cause is capped by how well you can reproduce it (per [the root-cause-confidence scale](root-cause-confidence.md)).

`(basis: Agans' Rule 2, "Make It Fail" — Debugging: The 9 Indispensable Rules (2002): "stimulate the failure … find the uncontrolled condition that makes it intermittent." Reinforced by Zeller's scientific debugging, which needs a reproducible failure to run controlled experiments against. The statistical-reproduction form (amplify, measure rate before/after, "N clean runs bounds but doesn't prove"), and record/replay for rare-but-capturable failures, are the corroborated community practice for the non-deterministic case.)`
