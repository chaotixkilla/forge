# Observation over inference

This standard governs one thing: **what may be written down as having happened.** An **observation** is a specific thing the running system did — what was exercised, the action you took, and what came back — recorded in the form it arrived and at the point it arrived. An **inference** is anything you concluded *from* an observation, or without one: that the write landed because a confirmation appeared, that the steps after the one you watched behaved the same way, that the other inputs take the same path, that the cause is the change you're checking, that "this should work" because the library clearly supports it or the types line up. Both belong in a result and both are useful — an inference is what points the next probe and what a handoff needs to be actionable. The defect is the unlabeled promotion: an inference occupying an observation's slot, where a reader has no way left to tell which of your lines a run actually produced.

## Label every line, and check the inferences you lean on

The test on each line you are about to record: **can you name what was exercised, the action, and the result — from the run rather than from the code or from what you expected?** If any part has to be reconstructed, the line is an inference and carries that label. Record the result in the form it actually arrived, *before* normalizing it against what should have happened; normalizing first is where the discrepancy quietly disappears, because the mind supplies the expected shape and the record ends up describing the specification rather than the instance.

The same label runs through reasoning, link by link: is this fact **observed** (you saw the value, ran the path, watched the branch taken) or **inferred** (you concluded it from a name, a type, a comment, or "it must be")? An inferred fact is a hypothesis, not evidence, and it may be the very fault you're looking for. Check each load-bearing inference at least once before building on it: the one you were surest of is the one most likely to be false, precisely because you didn't check it. When the deciding state isn't visible, don't fall back to assuming it — make it visible, by instrumenting or exposing it, and observe it. A conclusion that rests on a run names that run — the input, the execution, the observed output; one that rests on reasoning, however confident, hasn't been shown.

`(basis: IEEE 829's test-incident report; Dijkstra 1972; Agans 2002, rule 3; Zeller, Why Programs Fail; Ries's validated learning, The Lean Startup; the XP spike solution)`

## An unobserved step is unobserved, not passing

Not seeing a failure is not observing a success, and the gap between those two is where most overstated results come from. A step is **unobserved** whenever any of these holds, and each one is recorded per step with its reason rather than smoothed over:

- you never reached it (the run ended earlier, or the path diverged);
- you passed through it without inspecting the result — the action was taken, nothing was read back;
- you read the result too early, before the effect it reports could have landed;
- you reconstructed it afterwards from a record the system emitted about itself rather than watching the step;
- you concluded it from a neighboring step's success — the strongest of these and still an inference, since steps fail *between* each other.

The consequence is not negotiable by how healthy everything around the gap looked: a run containing an unobserved step has not been shown to work, so it can't carry the top grade of whatever scale grades it — it carries a grade bounded by its gap, plus the gap named.

One edge case: **one run is one observation, not a property.** A step that worked on this run was observed working on this run; a step that behaved differently across two runs yields two observations, not a contradiction to resolve by picking the nicer one. How many clean repeats a behavior owes before it counts as stable is settled where failures get classified; this standard only insists that each run's result survive into the record instead of being averaged away.

## The success surface is not the effect

The commonest way a run reports a pass over something that did nothing: a confirmation appeared, and the confirmation was recorded as the effect it announces. A success surface — a confirmation message, a success status, a calm dashboard — is a claim the system makes about itself, and the claim and the effect are two separate observations that can come apart in every direction: the confirmation shown before the work is committed, shown after work that was rolled back, shown for a request that reached a different destination than intended, shown by a path that swallowed its own error.

So confirm the effect where the effect lives, reached the way its consumer would reach it: the record read back, the message actually delivered to its recipient, the state reflected on the next entry, the refusal actually refusing. Then the surface *and* the effect are both in the record, and if they disagree that disagreement is itself the finding.

A self-reported success surface counts as the observation only where the claim under check ends at what the user is *told*; never trusting one would leave a claim like "the user is told why it failed" unobservable. Where the claim is about a change in the world, the effect is observed where it lands, and the surface is a second, weaker observation alongside it. The discriminator between the two: **does the claim under check terminate at what the user perceives, or at a durable change beyond it?** `(basis: maintainer, 2026-07-27)`

Two residual cases. A step whose effect is genuinely not observable with the access the run holds is **unobserved with a stated reason**, the same disposition as a step that couldn't be driven: the record says what couldn't be seen, not that nothing was wrong. And a run that couldn't be started at all yields **zero observations**: the record carries no observed steps for it and says so plainly, rather than borrowing evidence from the runs that did go.
