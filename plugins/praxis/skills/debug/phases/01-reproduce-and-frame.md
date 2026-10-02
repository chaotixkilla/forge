Before touching any code or forming any theory, state exactly *what is wrong* and pin it to a way to *make it happen on demand*.

## Frame the expected-vs-actual gap precisely

State, concretely: on what input or in what state, what the system *should* do, and what it *actually* does — down to the specific value, error, or observable difference. "The export is wrong" becomes "exporting a list of 100 rows writes a file with 99 — the last row is dropped." That precise gap is the target the whole session aims at, and the assertion the fix will have to satisfy.

When a `--from-*` seed is in play, frame from it: the [from-incident](../modules/from-incident.md), [from-telemetry](../modules/from-telemetry.md), or [from-logs](../modules/from-logs.md) intake gives you the reported symptoms, onset, and scope — but treat the report as a *claim to reconcile*, not ground truth. Reconcile the reported blast radius against what you can actually reproduce: the report says "all exports fail," your reproduction shows only exports over 99 rows fail — the gap between reported and reproduced is itself evidence.

## Build a reproduction, and preserve the evidence first

Construct the smallest reliable trigger for the framed failure ([reproduce-before-fixing](../rules/reproduce-before-fixing.md)). Before you start poking — especially for a rare or production-only failure that your poking might destroy — capture the failing state, inputs, stack, and environment ([preserve-the-evidence](../../../craft/evidence/preserve-the-evidence.md)), so a failure you reproduce once is not lost to your own experiments. "Minimal" means reduced to the smallest input or step-sequence that *still triggers the failure* — cut what doesn't change the outcome — because a small trigger is a small space to reason about in the localize loop and often names the cause by what it retains.

## Classify the reproduction — and gate on it

How reliably the bug reproduces decides whether you may proceed, and it caps the certainty the cause can ever reach. Classify it:

- **deterministic** — the same inputs/steps fail every run. Proceed freely; this is the ideal, and the controlled toggle in [confirm-root-cause](05-confirm-root-cause.md) is directly available.
- **intermittent** — it fails only some fraction of runs (a timing, concurrency, ordering, or environment dependence). Build a **statistical reproduction**: a harness that runs the trigger enough times to make the failure appear at a measurable rate, so you can observe it and later measure a fix's effect (the failure rate falling toward zero). The failure rate a reproduction harness must reach is deliberately left open: it varies with the bug's base rate and cost in ways this phase cannot enumerate, and the executor at run time holds more of that context. You may proceed on a statistical reproduction — but the cause's certainty caps below *observed* until you can control the trigger enough to toggle the failure on demand ([root-cause certainty](../rules/root-cause-confidence.md)). Changing one thing at a time now means *repeated trials per change*, since a single run proves nothing when the outcome is probabilistic.
- **not-yet-reproduced** — you cannot make it fail at all. Do **not** proceed to a fix: a fix you cannot trigger is one you cannot verify. Reproduction becomes the active goal — pull more evidence ([gather-evidence](02-gather-evidence.md): telemetry onset, logs, the incident's conditions) to reconstruct the triggering conditions. If reproduction genuinely can't be reached, that is a terminal result: the diagnosis is **not checked**, because the failure couldn't be reproduced, reported with the conditions tried and the evidence that would let someone reproduce it, rather than guessing at a fix.

`(basis: maintainer's house rule, after Zeller, Why Programs Fail, and Agans 2002, rule 2)`

The phase is done when you hold a precise expected-vs-actual gap and a reproduction classified deterministic or intermittent-with-a-harness — or an explicit report that the failure couldn't be reproduced. That framed, reproducible failure is what [gather-evidence](02-gather-evidence.md) and the localize loop reason from.
