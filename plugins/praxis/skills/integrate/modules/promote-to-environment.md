# promote-to-environment (`--target=<env>`)

Activated by `--target=<env>`, referenced from [ship-to-target](../phases/05-ship-to-target.md).

Base behavior: a plain `integrate` run lands (merges) and stops — it ships nothing, because the config model carries no default deploy environment, and shipping to production on every land is exactly the surprise a safe default avoids. This module adds the ship behavior: promote the landed change to a named environment. Deletion test: remove this module and integrate still lands and reports; the promotion is opt-in behavior a flag turns on, so it is a module. `(basis: ratified by the maintainer, 2026-07-11 — with no --target and no configured default deploy environment, integrate terminates at "landed" and does not promote; a team wanting land-then-ship names the target. Auto-shipping an unnamed environment is the unsafe surprise.)`

## The delta — promote to the named environment

- **Resolve the environment's promotion path.** Take `<env>` (e.g. `staging`, `production`) and resolve its deploy/promotion path and any environment-specific gating through the [ci](../../ci/SKILL.md) capability's *promote to an environment* operation; the dispatch resolves to whichever provider is configured.
- **Choose the rollout strategy by risk, not by habit.** The *how* of the promotion — all-at-once, incremental, staged exposure, or behind a switch — comes from [make-rollout-reversible](../rules/make-rollout-reversible.md), sized to the change's risk tier assigned in [assess-the-change](../phases/01-assess-the-change.md). `--target` names *where*; the risk tier sets *how*. Do not default every promotion to all-at-once.
- **Honor environment gating.** If the environment has a protection rule (a required approval, a wait timer), the capability reports it as a *pending* promotion; surface that and wait for it rather than forcing past it. A pending approval is not a failure.
- **Confirm arrival.** After promoting, confirm the rollout actually reached the environment (the promotion's state came back success for the intended scope) before handing to [confirm-and-report](../phases/06-confirm-and-report.md); a promotion that was accepted but did not roll out is reported, not assumed healthy.

## Composition

- **With `--watch`** ([watch-the-pipeline](watch-the-pipeline.md)): stay attached through the rollout and the post-ship signal window rather than reporting the moment the promotion is accepted.
- **With `--on-fail`** ([failure-policy](failure-policy.md)): a failed rollout follows the policy — hold, ask, or roll back — instead of the default stop-and-report.
- **Refused with `--commit`**, which terminates before landing and so has nothing to promote.

## Prerequisite and degrade

Promotion goes through the [ci](../../ci/SKILL.md) capability (which owns `tools.ci` — doer-owns-prerequisites; integrate declares none). If it reports the backend unavailable (`tools.ci` unconfigured), **degrade**: the change is already landed, so report that it landed but could **not** be promoted to `<env>` (the `ci` skill owns guiding the user through `init:ci`), rather than losing the landing. Shipping is the one thing that genuinely needs the backend; landing already succeeded without it. `(basis: integrate's per-capability degrade — a missing ship backend narrows the run to land-only, it does not undo the land; doer-owns-prerequisites shed, USING-ANVIL §2.)`
