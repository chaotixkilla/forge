---
name: operate
description: Run and respond to a production incident — confirm and triage a live signal, mitigate to restore service before root-causing, diagnose the true cause, remediate durably and verify the signal holds at baseline, keep stakeholders informed at a severity-right cadence, and turn the incident into prevention. Reach for it when production is degraded or a telemetry signal fires; distinct from debug (root-causes a defect that already bit, without incident authority to mitigate) and integrate (ships a change and watches its rollout).
metadata:
  flags:
    --from-incident=<ref>: seed triage from an existing incident record — its reported symptom, severity, timeline, and prior actions — read via the project-management or communication capability (activates from-incident)
    --from-telemetry=<ref>: seed from a telemetry signal (an alert, dashboard, metric, or trace) as the entry point — anchor triage on the firing signal and its surrounding context (activates from-telemetry)
    --watch: after remediation, hold the run open and re-read the signal until it stays at baseline for the signal's stability window before declaring resolved (activates watch-until-stable)
    --notify[=<target>]: push status transitions (acknowledged, mitigated, resolved) out over the communication capability at phase boundaries instead of only returning them; <target> is where they go, absent it the configured incident channel (activates notify-stakeholders)
    --background: detach the operate loop so watching and diagnosis continue across turns, re-engaging only on a state change or threshold breach (activates run-in-background)
    --publish: publish the incident record / postmortem as a durable team-facing document via the artifacts capability (activates publish-incident-record)
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies. operate owns no backend of its own: it delegates telemetry reads to the `telemetry` port, status posts and notifications to the `communication` port, incident-record reads to the `project-mgmt` / `communication` ports, and postmortem publishing to the `publish-artifact` port; it recruits explorers directly for its bounded evidence sweeps and hands the durable code fix to develop / debug — so it declares no `config_requires`. Its block/degrade posture is behavioral, written into the phases (telemetry unavailable with no seeded signal halts triage; communication unavailable degrades to returning the message to send by hand).

`--notify` pushes status transitions over the communication capability at phase boundaries: see [modules/notify-stakeholders.md](modules/notify-stakeholders.md). `--background` detaches the loop so watching and diagnosis continue across turns: see [modules/run-in-background.md](modules/run-in-background.md).

1. Assess and triage: establish what is actually happening and how bad it is — confirm the signal is real, scope the blast radius, set severity  — see [phases/01-assess-and-triage.md](phases/01-assess-and-triage.md)
2. Stabilize first: restore service before understanding root cause — reach for the fastest safe, reversible mitigation, stopping the bleeding without destroying the evidence  — see [phases/02-stabilize-first.md](phases/02-stabilize-first.md)
3. Diagnose the root cause: once it is no longer actively burning, form and test hypotheses against evidence and narrow to the true cause, not the nearest symptom  — see [phases/03-diagnose-root-cause.md](phases/03-diagnose-root-cause.md)
4. Remediate and verify: apply the durable fix (or hand it off), confirm the signal returns to baseline and holds, and resolve to exactly one terminal outcome  — see [phases/04-remediate-and-verify.md](phases/04-remediate-and-verify.md)
5. Communicate status: keep the right audience informed at a severity-right cadence throughout, and declare resolution explicitly  — see [phases/05-communicate-status.md](phases/05-communicate-status.md)
6. Learn and harden: turn the incident into prevention — a blameless retrospective, a captured timeline, and concrete follow-ups  — see [phases/06-learn-and-harden.md](phases/06-learn-and-harden.md)
