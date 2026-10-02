---
name: mitigate
description: Restore a degraded production service before its cause is understood — choose the fastest safe, reversible mitigation, capture the evidence it would erase, apply it through the path that owns it, and confirm the signal is back at baseline and holding. Returns mitigated, with the mitigation's kind and the signal's hold; indeterminate, when the signal can't yet say; or not-mitigated with the recommended action.
metadata:
  flags:
    --watch: hold the run open and re-read the signal until it stays at baseline for the signal's stability window, instead of reading it once (activates watch-until-stable)
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies. mitigate owns no backend of its own: it applies pipeline actions through the [ci](../ci/SKILL.md) skill and reads the signal through the [telemetry](../telemetry/SKILL.md) skill, each the doer that owns its own prerequisite.

1. Choose the mitigation: pick the fastest safe, reversible action that restores service, and name its kind — durable or provisional  — see [phases/01-choose-the-mitigation.md](phases/01-choose-the-mitigation.md)
2. Preserve the evidence: capture the volatile state the mitigation would erase, when it isn't already durable  — see [phases/02-preserve-the-evidence.md](phases/02-preserve-the-evidence.md)
3. Apply and confirm: apply the mitigation through its owning path, confirm the signal is back at baseline and holding, and return the outcome  — see [phases/03-apply-and-confirm.md](phases/03-apply-and-confirm.md)
