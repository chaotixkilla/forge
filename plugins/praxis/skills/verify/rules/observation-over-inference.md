# Observation over inference

This rule governs one thing: **what may be written down as having happened.** An **observation** is a specific thing the running system did — a named flow, a named step within it, the action you took, and what came back — recorded in the form it arrived and at the point in the run it arrived. An **inference** is anything you concluded *from* an observation: that the write landed because a confirmation appeared, that the steps after the one you watched would have behaved the same way, that the other inputs take the same path, that the cause is the change you're checking. Both belong in a verify report and both are useful — an inference is what points the next drive and what a handoff needs to be actionable. The defect is the unlabeled promotion: an inference occupying an observation's slot, where a reader has no way left to tell which of your lines a run actually produced.

The test on each line you are about to record: **can you name the flow, the step, the action, and the result — from the run rather than from the code or from what you expected?** If any of the four has to be reconstructed, the line is an inference and carries that label. Record the result in the form it actually arrived, *before* normalizing it against what should have happened; normalizing first is where the discrepancy quietly disappears, because the mind supplies the expected shape and the report ends up describing the specification rather than the instance.

`(basis: the actual-result-versus-expected-result split that standard defect reporting has carried since IEEE 829's test-incident report — what the system did is recorded distinctly from what it should have done, precisely because the two collapse under pressure; and Dijkstra's asymmetry, that a run can show the presence of a defect but never its absence, which is what makes an unwatched step a gap rather than a pass. praxis already pins the same fact-versus-inference separation for investigation claims; this is its running-behavior counterpart.)`

## An unobserved step is unobserved, not passing

Not seeing a failure is not observing a success, and the gap between those two is where most overstated verdicts come from. A step is **unobserved** whenever any of these holds, and each one is recorded per step with its reason rather than smoothed over:

- you never reached it (the flow ended earlier, or the path diverged);
- you passed through it without inspecting the result — the action was taken, nothing was read back;
- you read the result too early, before the effect it reports could have landed;
- you reconstructed it afterwards from a record the system emitted about itself rather than watching the step;
- you concluded it from a neighboring step's success — the strongest of these and still an inference, since the whole reason to drive a flow end-to-end is that steps fail *between* each other.

The consequence is load-bearing and it is not negotiable by how healthy everything around the gap looked: a flow containing an unobserved step has not been shown to work, so it cannot carry the top verdict — what it carries is a verdict bounded by its gap, plus the gap named. A flow driven with an unreachable step is a *partial* observation reported as one, which is a genuinely useful result; the same flow reported as a pass is a false one.

The edge case that catches people twice: **one drive is one observation, not a property.** A step that worked on this drive was observed working on this drive; a step that behaved differently across two drives yields two observations, not a contradiction to resolve by picking the nicer one. How many clean re-drives a behavior owes before it counts as stable is settled where failures get classified — this rule only insists that each drive's result survive into the record instead of being averaged away.

## The success surface is not the effect

The commonest way a verify run reports a pass over a flow that did nothing: a confirmation appeared, and the confirmation was recorded as the effect it announces. A success surface is a claim the application makes about itself, and the claim and the effect are two separate observations that can come apart in every direction — the confirmation shown before the work is committed, shown after work that was rolled back, shown for a request that reached a different destination than intended, shown by a path that swallowed its own error.

So confirm the effect where the effect lives, reached the way a user would reach it: the record read back, the message actually delivered to its recipient, the state reflected on the next entry into the flow, the refusal actually refusing. Then the surface *and* the effect are both in the record, and if they disagree that disagreement is itself the finding.

`(basis: ratified by the maintainer 2026-07-27, on the build's recommendation — the bar above — a self-reported success surface counts as the observation only where the framed claim ends at what the user is *told*; where the claim is about a change in the world, the effect is observed where it lands and the surface is a second, weaker observation alongside it. The discriminator between the two cases: does the claim under check terminate at what the user perceives, or at a durable change beyond it? Derived here rather than taken from a source. Why this over the alternatives: never trusting a surface would make a claim like "the user is told why it failed" structurally unobservable, while always trusting one licenses the exact false pass this section exists to stop.)`

Two residual cases. A step whose effect is genuinely not observable with the access this run holds is **unobserved with a stated reason**, which is the same disposition as a step that could not be driven — the record says what could not be seen, not that nothing was wrong. And a flow that could not be started at all yields **zero observations**: the report carries no observed steps for it and says so plainly, rather than borrowing evidence from the flows that did run.

For the same evidence discipline written for a throwaway probe rather than a shipped path, read [ground-claims-in-a-run](../../prototype/rules/ground-claims-in-a-run.md) — worth opening if you are calibrating how strict "it ran and showed it" has to be, and deliberately not restated here, since one instruction with two homes drifts.

Applied most directly in [exercise-the-flows](../phases/03-exercise-the-flows.md), where each step's result is recorded as it happens, and in [report-the-verdict](../phases/05-report-the-verdict.md), where every line of the report is either an observation or a labeled inference; [as-user](../modules/as-user.md) applies it to persona claims, where a user you did not simulate is an inference about that user.
