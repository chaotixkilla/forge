# from-telemetry (`--from-telemetry`)

Activated by `--from-telemetry=<ref>`, referenced from [assess-and-triage](../phases/01-assess-and-triage.md) (the intake site).

Base behavior: triage runs from a declared incident or a user report. This module makes a telemetry artifact the entry point. Deletion test: remove it and triage still runs from a report or a declared incident; seeding from a telemetry signal is optional intake a flag turns on — so it is a module.

## The delta — anchor triage on the firing signal

Read the telemetry artifact (an alert, dashboard, metric, or trace by reference) through the [telemetry](../../telemetry/SKILL.md) port and pull the firing metric, its onset, affected scope, and correlated signals to anchor [assess-and-triage](../phases/01-assess-and-triage.md). The signal feeds directly into the [real-signal-vs-flapping](../rules/real-signal-vs-flapping.md) check — a firing alert is the *input* to that judgment, not a confirmed incident: the module supplies the signal, triage decides whether it is real.

## Prerequisite and degrade

The read goes through the telemetry port (doer-owns-prerequisites; operate declares none). This module's degrade is the sharp one: if telemetry is unavailable and this was the only entry point, triage has no signal to read and **cannot run blind** — halt and guide the user to `init:telemetry` (the block posture triage owns). If another seed is also present (`--from-incident`), degrade to that instead and note the live signal could not be read.
