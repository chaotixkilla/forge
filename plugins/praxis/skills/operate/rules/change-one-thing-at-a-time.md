# Change one thing at a time

During active diagnosis, the thing you are protecting is *attribution* — the ability to say "that change caused that effect." Batch three changes and watch the signal move and you have learned nothing: you cannot tell which one did it, and you may have introduced a second problem while chasing the first. So while diagnosing, vary a single factor per step, observe, and record before the next. This rule governs [diagnose-root-cause](../phases/03-diagnose-root-cause.md).

## The method

- **One variable per step.** Make one change — a probe, a toggle, a targeted revert — observe its effect, and record it before touching anything else. Revert it if it didn't help, keep it if it did, then move to the next.
- **Record the before and after.** Each experiment is only evidence if you captured the state before and after it; an undocumented change during an incident becomes noise nobody can attribute later.

## The tension with mitigate-first — name which phase you are in

This rule is in genuine tension with [mitigate-before-diagnose](mitigate-before-diagnose.md), and the resolution is to know which activity you are doing. **During stabilization, speed wins** — throw the reversible mitigation and stop the bleeding, even if it's several things at once, because restoring service outranks clean attribution. **During diagnosis, attribution wins** — the incident is no longer actively burning, so you can afford the discipline of one change at a time. The failure mode is running a stabilization change (batched, fast) and then trying to read it as a diagnosis experiment (needs isolation) — you get neither restored service you can trust nor a clean signal. State which phase you are in before you change anything.

`(basis: controlled-experiment / scientific-debugging discipline — one independent variable per trial so an observed effect is attributable; the same isolation principle test's control-nondeterminism and debug's hypothesis-testing rest on, applied under incident conditions where it competes with mitigation urgency.)`
