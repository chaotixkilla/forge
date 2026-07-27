---
name: benchmark
description: Prove whether a change to a target plugin's skill is a net improvement or a hidden regression — run the changed and pre-change versions over the same scenarios, several times each, and compare outcomes with variance. The heavyweight verification tier beneath dogfood; reach for it before a release or after a revise batch when regression risk is real.
allowed-tools: Read, Glob, Grep, Write
metadata:
  flags:
    --plugin=<name>: target plugin whose change is being evaluated (required — stop and ask if absent)
    --skill=<skill>: narrow to one skill; default is whatever the diff touches
    --baseline=<ref>: override the baseline; default is the pre-change tree / last release
    --repeats=<n>: runs per arm — the variance knob; default pinned in signal-vs-noise
    --scenarios=<ref>: reuse a curated scenario set instead of picking fresh
    --report=<fmt>: inline (default) or artifact
    --dry-run: frame the comparison and show the run plan, execute nothing
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies.

**A benchmark needs a resolvable baseline.** The whole method is a measured delta between the changed tree and the version before it, so the *before* is load-bearing: if the change has no pre-change version to compare against — a brand-new skill with no prior release, an untracked tree — there is no delta to take, and benchmark stops rather than fabricate a verdict against nothing. When there is no *before* to beat, prove the version runs with dogfood instead; come here once there is one.

1. Frame the comparison: resolve the baseline via the configured version-control capability, then fix the one scenario set and the repeat count both arms will share before anything executes  — see [phases/01-frame-the-comparison.md](phases/01-frame-the-comparison.md); leans on [scenario-corpus-discipline](rules/scenario-corpus-discipline.md)
2. Run both arms: delegate execution to dogfood — the two arms are the changed tree and the baseline, and each arm is run N times over the identical scenarios (N the repeat count signal-vs-noise pins, default 3), collecting a log per run; benchmark orchestrates the pairing and the repeats, it does not re-implement the runner  — see [phases/02-run-both-arms.md](phases/02-run-both-arms.md); leans on [signal-vs-noise](rules/signal-vs-noise.md)
3. Grade outcomes: recruit the critics as the assertion library (the full roster by default, dropped only where the change cannot reach a concern) against each arm's logs and the diff, and fall back to a blind reading only for the subjective residue no critic covers  — see [phases/03-grade-outcomes.md](phases/03-grade-outcomes.md); leans on [grading-the-ungradable](rules/grading-the-ungradable.md)
4. Aggregate and decide: compare per-scenario outcomes across the repeats with their variance, and classify each scenario as improvement / regression / within-noise against the pinned threshold  — see [phases/04-aggregate-and-decide.md](phases/04-aggregate-and-decide.md); leans on [signal-vs-noise](rules/signal-vs-noise.md)
5. Report and verdict: deliver the net verdict with regressions surfaced first — the one thing an A/B-with-repeats catches that a single pass cannot — backed by the per-scenario evidence  — see [phases/05-report-and-verdict.md](phases/05-report-and-verdict.md)
