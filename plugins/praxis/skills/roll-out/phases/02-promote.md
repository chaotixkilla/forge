## Promote, at a pace sized to risk

The environment and the risk tier come from [assess-the-rollout](01-assess-the-rollout.md).

- **Promote through the ci capability.** Promote the change's ref to the environment through [ci](../../ci/SKILL.md)'s *promote to an environment*. Honor the environment's gating: a required approval or an enforced delay comes back as a *pending* promotion, never forced past. Without `--watch` the run returns at once, reporting it pending with what it awaits; with `--watch` the watch waits for it within its window ([watch-the-pipeline](../modules/watch-the-pipeline.md)). `(basis: derived from the base run returning the immediate result)`
- **Choose the strategy by risk tier, not by target.** The *how* — all-at-once / small increment / staged exposure / behind a switch — comes from [make-rollout-reversible](../rules/make-rollout-reversible.md), keyed to the risk tier assigned in [assess-the-rollout](01-assess-the-rollout.md) (raised, never lowered, for a hotfix). ci promotes a ref to a named environment, so a stage is promoted as its own named environment; a switch is flipped by whoever owns the flag, since no port flips one — roll-out reports the flip the strategy needs as a step for the caller. `(basis: derived from ci's promote operation)`
- **For an irreversible-if-wrong change, verify the switch actually reverses without a redeploy.** A rollout is only "behind a switch" if turning it off is a config flip — a flag that still needs a redeploy to disable does not give fast rollback, and a flag/kill-switch identifier must never be one repurposed from older behavior. That is the Knight Capital failure class (~$460M): a deploy that missed one server flipped on repurposed dead code. `(basis: community incident lore and postmortems; Knight Capital, 2012)` A switch this rollout installs owes its removal ([retire-the-switches](../../../craft/engineering/retire-the-switches.md)).

## Confirm the rollout reached the target

A promotion that was *accepted* is not a promotion that *arrived*: confirm the change actually rolled out to **the scope this run promotes to** — for an all-at-once strategy the full environment; for a staged/canary or behind-a-switch strategy **the stage this run reaches** — once the promotion's state has come back *succeeded* for that scope, before handing to [confirm-healthy](03-confirm-healthy.md). A promotion accepted but not actually in place is reported as such (no deploy in place → *not-rolled-out*), never assumed to have arrived or its health to hold.

**A run rests at the deploy state its strategy reached.** roll-out is a single pass, not a long-running ramp driver: for a staged/canary or behind-a-switch strategy it promotes to the stage its strategy — and its `--watch` window — reaches, and rests there as *rolled-out*, reporting the exposure reached and the stages or flag flip that remain for a follow-up. It doesn't block to drive a multi-stage ramp to full exposure, since a progressive ramp's bake times outlast a single invocation. `(basis: maintainer, 2026-07-11)`

## Degrade and fail-policy

- **No pipeline backend:** promotion goes through the [ci](../../ci/SKILL.md) capability. If it is unavailable (`tools.ci` unconfigured), **degrade**: the promotion is skipped, not the run — hand to [confirm-healthy](03-confirm-healthy.md) as the success path does, carrying the *not-rolled-out* outcome and noting that the promotion couldn't run (the `ci` skill owns guiding through `init:ci`). Never undo the merge. `(basis: per-capability degrade)`
- **Rollout failure:** apply `--on-fail` ([failure-policy](../modules/failure-policy.md)) — default abort (stop and report, leave recoverable); `rollback` undoes the *deployment* and never the merge, and where nothing deployed it is a no-op; `ask` waits for a human where one can answer. A failed rollout never silently proceeds, and like the degrade branch above it still hands to [confirm-healthy](03-confirm-healthy.md), with the resting-state outcome.

## Close the phase

Under `--dry-run`, report the environment, the chosen strategy (and the risk tier that set it), and the promotion that *would* run — without promoting. On success, hand to [confirm-healthy](03-confirm-healthy.md) with the rollout result and the risk tier, so the health read knows what rolled out and how.
