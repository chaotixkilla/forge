This is where debugging becomes science rather than guesswork. With the fault narrowed to a span, you explain it — but an explanation is only worth acting on if an experiment could have proven it *wrong*. This phase forms candidate mechanisms as falsifiable hypotheses and runs the cheapest experiment that could disprove each, letting observation — not the plausibility of the story — eliminate candidates. It is the middle beat of the localize→hypothesize→confirm loop: each experiment's result narrows the search space ([localize-the-fault](03-localize-the-fault.md)) and feeds the eventual proof ([confirm-root-cause](05-confirm-root-cause.md)).

## Form hypotheses that could be proven wrong

A usable hypothesis states a specific mechanism *and predicts an observation that would be different if the mechanism were false*. "Something's wrong with the cache" predicts nothing and forbids nothing — it cannot be tested. "The cache returns a stale entry because the write invalidates key A while reads use key B" predicts a concrete, checkable fact: instrument both sites and the keys differ on the failing path. The bar for a hypothesis to enter testing: **you can name the observation that would disprove it.** A theory that no observation could contradict is not a hypothesis — it is a belief, and it will survive any amount of testing while explaining nothing.

`(basis: the scientific method applied to debugging — Zeller, Why Programs Fail: form a hypothesis consistent with the observations, derive a prediction, run an experiment, and refine or reject the hypothesis by the result. Falsifiability (a hypothesis must forbid some observable outcome) is the Popperian criterion Zeller's loop rests on; it is the discriminator for "is this a testable hypothesis," not a house preference.)`

Where several mechanisms fit the evidence, hold them as a ranked set of candidates rather than committing to the first — and prefer the experiment that discriminates *between* candidates, killing the most theories per run.

## Run the cheapest disproving experiment

For each hypothesis, design the experiment that could disprove it for the least effort, and prefer disproof to confirmation — an experiment that only *could* confirm tells you far less than one that *could* refute. Two disciplines govern the experiment:

- **Change one thing at a time** ([change-one-thing-at-a-time](../rules/change-one-thing-at-a-time.md)) — vary a single factor so the observed change has exactly one possible cause, and revert each probe before the next. On an intermittent bug, "one run" is not an experiment: repeat trials per change until the result is statistically meaningful.
- **Make the invisible observable** ([make-the-invisible-observable](../rules/make-the-invisible-observable.md)) — where the deciding state is unseen, instrument the boundary and read the value crossing it rather than reasoning about what it "must" be. Believe the instrument over the model ([trust-observations-over-assumptions](../rules/trust-observations-over-assumptions.md)): the whole reason you are here is that the model already failed to predict the failure.

Record each experiment and its result as it runs, so the elimination is auditable and you do not re-run a test you already have the answer to. A hypothesis whose disproving experiment *fails to disprove it* is strengthened, not proven — it advances toward confirmation, where the controlled toggle settles it.

## Attack the surviving candidates

Before carrying a surviving hypothesis into confirmation, stress it. Recruit the [adversary critic](../../../agents/critics/adversary.md) to construct the case the hypothesis does not explain — an input that should fail by the theory but doesn't, or one that fails without the hypothesized condition — and the [assumption-hunter critic](../../../agents/critics/assumption-hunter.md) to surface the premise the hypothesis quietly rests on. Without fan-out, apply both lenses yourself: for each surviving hypothesis, actively try to construct the observation that breaks it before you let it stand. A hypothesis that survives a real attempt to break it is worth confirming; one that was only ever tested for confirmation is a candidate still.

The output is the surviving mechanism (or a short ranked set), each with the experiments that eliminated its rivals — handed to [confirm-root-cause](05-confirm-root-cause.md) for the end-to-end proof, or back into [localize-the-fault](03-localize-the-fault.md) if every candidate died and the search space needs narrowing again.
