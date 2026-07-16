---
name: debug
description: Find and fix the true root cause of a defect that has already bitten — reproduce it, localize the fault, form and test falsifiable hypotheses, confirm the mechanism rather than a coincidental trigger or downstream symptom, and (with --fix) resolve it at the cause with a guarding regression test. Reach for it when a specific failure needs root-causing; distinct from review (hunts latent defects in a change) and test/verify (confirm intended behavior).
metadata:
  flags:
    --from-incident=<ref>: seed the investigation from an incident/postmortem record — its symptoms, timeline, affected scope, and responder notes — read via the project-management or communication capability
    --from-telemetry=<ref>: seed from a telemetry signal (error-aggregate, trace, metric, dashboard) — anchor on the regression's onset and correlated signals, and turn the spike into a reproduction target
    --from-logs=<path|ref>: treat a log file (a local path) or a hosted log stream (a store reference) as the primary evidence to reconstruct the failure from
    --fix: extend past diagnosis — apply the smallest correct change at the confirmed root cause and add a regression test that fails before the fix and passes after
    --sandbox: run reproduction and experiments in an isolated throwaway environment (branch/worktree/container) so probes, instrumentation, and risky toggles never touch the working tree or shared state
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

debug owns no backend of its own: it delegates telemetry reads to the `telemetry` port, incident reads to the `project-mgmt` / `communication` ports, and recruits explorers directly for its bounded evidence sweep — so it declares no `config_requires`.

`--sandbox` routes all reproduction and experiments into an isolated throwaway environment so no probe touches the working tree or shared state: see [modules/sandbox-isolation.md](modules/sandbox-isolation.md).

Phases 3–5 (localize → hypothesize-and-test → confirm) run as an **iterate-until-pinned loop**, not a strict waterfall: cycle between narrowing and testing until the mechanism is confirmed, then confirm and resolve.

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies.

1. Reproduce and frame: pin the bug to a deterministic, minimal reproduction and state the expected-vs-actual gap precisely before touching anything — if it can't be reproduced, that is the first problem to solve  — see [phases/01-reproduce-and-frame.md](phases/01-reproduce-and-frame.md)
2. Gather evidence: collect the observable facts around the failure — code paths, recent changes near the symptom, telemetry/logs, and prior occurrences — recruiting explorers for the sweep  — see [phases/02-gather-evidence.md](phases/02-gather-evidence.md)
3. Localize the fault: narrow from whole-system to the smallest suspect span by bisecting the input, the code path, and the timeline  — see [phases/03-localize-the-fault.md](phases/03-localize-the-fault.md)
4. Hypothesize and test: form falsifiable hypotheses about the mechanism and run the cheapest experiment that could disprove each; let observation, not intuition, eliminate candidates  — see [phases/04-hypothesize-and-test.md](phases/04-hypothesize-and-test.md)
5. Confirm the root cause: prove the mechanism end to end — show the bug appears and disappears when the claimed cause is toggled — and grade the confidence, distinguishing the true cause from a coincidental trigger or symptom  — see [phases/05-confirm-root-cause.md](phases/05-confirm-root-cause.md)
6. Report or resolve: write up the mechanism, blast radius, and reproduction; hand off a precise diagnosis, or (with --fix) make the smallest correct change at the cause plus a guarding regression test  — see [phases/06-report-or-resolve.md](phases/06-report-or-resolve.md)
