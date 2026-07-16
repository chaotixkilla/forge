# from-incident (`--from-incident`)

Activated by `--from-incident=<ref>`, referenced from [reproduce-and-frame](../phases/01-reproduce-and-frame.md) (the intake site).

Deletion test: remove it and debug still frames the failure from the user's direct report; seeding from an incident record is optional intake a flag turns on.

## The delta

Instead of framing from a fresh report, seed the investigation from an existing incident/postmortem record: pull its **symptoms**, **timeline** (especially onset — the seam a regression crossed), **affected scope**, and **prior responder notes** (what was already tried, and any mitigation already in place). The record is read through a capability debug does not otherwise use:

- a **tracked incident reference** (an incident or ticket id) → the [project-mgmt](../../project-mgmt/SKILL.md) port's *fetch a work-item*;
- a **discussion-style incident thread** → the [communication](../../communication/SKILL.md) port's *read a thread*.

Which port is set by the reference's shape; debug sheds these prerequisites to the ports (doer-owns-prerequisites) and needs no adapter of its own. If the port reports the record unavailable, degrade: proceed from whatever the user gave directly, noting the record couldn't be read.

## Reconcile the report against what you can reproduce

An incident record is a *claim*, often written under pressure and broader than the truth ("all exports failing" when only large ones do). Treat the reported blast radius as a hypothesis to check, not ground truth: reconcile it against what you can actually reproduce, and treat the gap between reported and reproduced as evidence in its own right.

## Incident context legitimizes mitigate-then-diagnose

`--from-incident` is a signal that this is production-pressure context, which activates the incident branch of the mitigation-vs-root-cause fork in [report-or-resolve](../phases/06-report-or-resolve.md): stopping the bleeding first is legitimate here, with the mitigation recorded as provisional and the root-cause fix still owed. Absent that pressure, debug's cause-only default holds.
