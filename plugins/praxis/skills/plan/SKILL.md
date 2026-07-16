---
name: plan
description: Convert a spec into a buildable design — anchor it to the real system, deliberately close the solution space, specify concrete interfaces down to the field, pre-solve the flows most likely to bite, and plan a rollout that reaches production safely; optionally run at maximum rigor, seeded from a written spec or prior art, stress-tested by extra critics, resumed one phase at a time, or published as a clean team-facing design document.
metadata:
  flags:
    --deep: maximum-rigor mode — widen the approach search, dig into hard-part mechanics, and demand explicit trade-off scoring before committing — activates the deep-mode module
    --from-spec=<path>: treat a written spec at PATH as the locked, authoritative input; trace each design decision back to a spec clause — activates the from-spec module
    --prior-art=<ref>: anchor the approach search on an existing design/system REF — mine it for reusable shape and named divergences before enumerating fresh alternatives — activates the seed-prior-art module
    --critics=<n>: how many perspective-diverse critics stress-test the committed design — activates the adversarial-critics module
    --phase=<name|n>: run or resume a single phase in isolation, trusting the upstream phases' outputs (spine control, not a behavior module)
    --publish: hand the finished plan to the artifacts capability as a clean team-facing design document — activates the publish-handoff module
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies. plan owns no backend of its own: it delegates its evidence-gathering to the `gather` skill and the publish handoff to `publish-artifact` (each the doer that owns its own prerequisite), so it declares no `config_requires`.

`--deep` raises rigor across the whole run — wider approach search, deeper hard-part mechanics, explicit written trade-off scoring: see [modules/deep-mode.md](modules/deep-mode.md). `--critics=<n>` sets how many perspective-diverse critics stress-test the committed design: see [modules/adversarial-critics.md](modules/adversarial-critics.md). `--phase=<name|n>` runs or resumes one phase in isolation — it **selects which spine steps run** rather than adding behavior to any one phase, which is why it is taught here inline and carries no module. It **trusts the upstream phases' outputs rather than regenerating them**, so those outputs must already be present in the invocation context or supplied at a referenced path; if a required upstream output is absent, **halt and ask for it** — do not regenerate the upstream phases (that defeats the flag) or proceed on invented assumptions. Use it when one phase's input changed and you want to rework that slice without re-running the spine, having first made the upstream outputs current. `<name>` resolves against this fixed set: `1=mapping`, `2=approach`, `3=interfaces`, `4=hard-parts`, `5=rollout`, `6=validate`.

1. Map the spec onto the existing system: anchor the abstract spec to concrete code reality  — see [phases/01-mapping-to-system.md](phases/01-mapping-to-system.md)
2. Choose the approach: close the solution space deliberately  — see [phases/02-choosing-approach.md](phases/02-choosing-approach.md)
3. Specify the concrete interfaces: turn the chosen approach into exact contracts  — see [phases/03-specify-interfaces.md](phases/03-specify-interfaces.md)
4. Work the hard parts: pre-solve the flows most likely to bite mid-build  — see [phases/04-working-the-hard-parts.md](phases/04-working-the-hard-parts.md)
5. Plan the rollout: how it reaches production safely  — see [phases/05-planning-rollout.md](phases/05-planning-rollout.md)
6. Slice and validate: confirm the design is buildable and closed  — see [phases/06-slice-and-validate.md](phases/06-slice-and-validate.md)
