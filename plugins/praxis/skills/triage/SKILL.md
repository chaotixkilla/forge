---
name: triage
description: Decide whether a production signal is a real incident and how bad it is — check the signal against flapping, scope what it affects, and set its severity. Returns a real incident with its scope and severity, a lead to investigate, or a stood-down signal with the reason; responding to it is the caller's job.
metadata:
  flags:
    --from-incident=<ref>: seed triage from an existing incident record — its reported symptom, severity, timeline and prior actions — read via the project-management or communication capability (activates from-incident)
    --from-telemetry=<ref>: the telemetry signal to anchor on (an alert, dashboard, metric or trace) — an input to confirm-the-signal, not a module
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies. triage owns no backend of its own: it reads live signals through the [telemetry](../telemetry/SKILL.md) skill, the doer that owns its prerequisite.

1. Confirm the signal: read the firing signal and its context, reconcile any seed against it, and decide whether it is a real incident or flapping noise  — see [phases/01-confirm-the-signal.md](phases/01-confirm-the-signal.md)
2. Scope and grade it: establish what the real incident affects and how widely, set its severity, and return the result  — see [phases/02-scope-and-grade.md](phases/02-scope-and-grade.md)
