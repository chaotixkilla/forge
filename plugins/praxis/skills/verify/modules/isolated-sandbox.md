# isolated-sandbox (`--sandbox`)

Activated by `--sandbox`, referenced from [stand-the-app-up](../phases/02-stand-the-app-up.md).

The base run stands the instance up in the ambient environment. This module stands it up inside a disposable, isolated one, so a driven flow cannot reach real state — the posture for exactly the flows worth being careful with, the ones that charge, send, delete, or write somewhere a person will later read. It is resolved **locally** — verify provisions its own throwaway environment — and declares no backend; this is the same config-less local resolution the plugin's other `--sandbox` skills use, not a delegated remote-environment capability.

## The delta

Provision the throwaway environment before the instance goes up, stand the instance up inside it, and tear it down when the run ends. What "isolated" concretely guarantees, pinned so two cold runs provision the same thing:

- **No reach into real state** — the data the drive reads and writes lives in a throwaway store seeded for this run; no real record is created, changed, or removed.
- **No outward effect** — anything a flow would send past the instance (a message, a charge, a notification, a call to a service outside it) is blocked or lands in a local stand-in that records the attempt; nothing leaves.
- **A scratch workspace** — files the run writes land somewhere discarded at teardown, and the real working tree is untouched.
- **A known starting state** — the drive begins from fixtures provisioned into the environment rather than from whatever ambient state happens to be lying there, so a reproduction can name the state the flow started from.
- **Discardable in one move** — the environment is torn down wholesale, and nothing the run needs dies with it: the verdict, the findings, and every reproduction cross back out first.

**Deletion test:** without the flag, [stand-the-app-up](../phases/02-stand-the-app-up.md) stands the instance up in the ambient environment and records it; the throwaway environment, the substitutions it forces, and their entry in that record are the added behavior — remove the module and the same flows are driven against real state.

## The tension: isolation against fidelity

In most skills a sandbox trades only convenience for safety. Here it trades **evidence**, and that makes the tension verify-specific: this skill's whole claim rests on having observed a real application reached the way a user reaches it, so every substitution that isolation makes moves the instance one step further from the thing users will actually meet. Isolate carelessly and the run still produces a confident verdict — about a simulation. Two rules keep the drive worth its result.

**What must stay real, or the drive proves nothing:**

- **The entry point.** The flow is still reached through the path a user reaches it by, on the terms [stand-the-app-up](../phases/02-stand-the-app-up.md) established. An isolated instance is not licence to drive the flow through a harness or to invoke the handler directly — that is the one trade this skill cannot make, because it is the trade that would make the run a test.
- **The application under check.** What runs is the thing as built and configured for real use. A build or configuration path taken *only* because the sandbox needed it means the run observed a variant, not the change that is about to land.
- **The wiring between the change and the flow.** Routing and resolution, authorization, serialization, rendering, the connective steps between components: these are the layers verify exists to observe, and they are never stubbed out to make isolation easier.
- **Every framed step.** Isolation may change what a step *reaches*; it may not change whether the step happens. A step dropped because it was awkward to isolate is unobserved, and it stays unobserved in the record.

**What may be substituted, and at what cost:** the far side of a boundary the flow crosses outward — a service beyond the instance, a path that sends or charges — and the contents of the data store, seeded rather than real. Both are admissible; both narrow what the verdict covers. So the rule: **name every substitution, specifically, in the environment record [stand-the-app-up](../phases/02-stand-the-app-up.md) keeps**, since that record is what the verdict is scoped to. A verdict earned against a stand-in is a claim about the flow's behavior up to that boundary and no further, and where a framed step's claimed effect lay past it the unit cannot reach `works` at all. An unrecorded stand-in does more damage than the substitution itself: a reader takes the verdict as covering the real integration, and nothing in the report tells them it does not.

The test when it is unclear whether a particular substitution is admissible: **would a defect living in the thing you replaced have been invisible to this run?** If no, substitute freely. If yes and that layer sits inside the change's reach, you have replaced the thing you were sent to observe — keep it real, or drive the flow and record its scope as narrowed at that boundary, which caps the unit by [verdict-scale](../rules/verdict-scale.md)'s substitution-or-unknown cell wherever a framed step's claimed effect depends on the thing you replaced. If yes but the layer sits outside the change's reach, the substitution is admissible, and it is recorded like every other. `(basis: the skill contract, applied to the sandbox — its evidence rule is that a result is an observation of the real application reached the way a user reaches it, and its scoping rule is that a works verdict covers only the flows driven in the recorded environment. The first fixes what isolation may not replace; the second is why anything replaced has to appear in that record.)`

One thing this module does not do is second-guess the request. If the framed flows turn out to mutate nothing and send nothing, isolation is still provisioned as asked; deciding that a caller's safety request was unnecessary is not this module's call to make.

## Degraded case

If isolation cannot be provisioned — no way to create a throwaway environment, no way to stop the flows' outward effects from leaving — do not silently drive against real state. **Default: stop and report** that `--sandbox` was requested and isolation is unavailable, naming which guarantee could not be met, and drive nothing. The caller asked for isolation precisely because these are flows whose real effects matter, so driving them un-isolated risks the exact effect the flag existed to prevent. The caller can re-invoke without `--sandbox` to accept an ambient drive; and where the caller has already said an ambient drive is acceptable, drive ambient and record in the environment that isolation was requested and unavailable, so the verdict carries that fact instead of the caller having to remember it. Either way the loss of isolation is reported, never hidden. `(basis: fail-safe on an explicit safety request, mirroring the plugin's other --sandbox degraded posture — a requested isolation guarantee that cannot be met defaults to not running rather than to running without the guarantee, and the caller who asked for the sandbox owns the decision to proceed without it.)`

**Partial isolation** is the common shape and takes its own branch: a throwaway store is available but outward sends cannot be blocked, or the reverse. Treat partial isolation as unavailable **for the flows whose effects escape through the axis that failed** and available for the rest — drive the flows that are fully contained, stop on the ones that are not, and report the split with the failed axis named. A flow whose only uncontained effect is one the caller has already accepted may be driven under the ambient-acceptance branch above; a flow that would send, charge, or destroy something real through the missing axis is not driven on the strength of the axes that did work.

**If teardown fails**, the run's results still cross out — they were collected before teardown — and the environment is reported as **left behind, with where it is**, so it can be removed by hand. A sandbox that could not be discarded is a stated outcome of the run, not a detail to swallow, because the next run's "known starting state" guarantee depends on the last one actually having been thrown away.
