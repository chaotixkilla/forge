## Form hypotheses that could be proven wrong

A usable hypothesis states a specific mechanism *and predicts an observation that would be different if the mechanism were false*. "Something's wrong with the cache" predicts nothing and forbids nothing — it cannot be tested. "The cache returns a stale entry because the write invalidates key A while reads use key B" predicts a concrete, checkable fact: instrument both sites and the keys differ on the failing path. The bar for a hypothesis to enter testing: **you can name the observation that would disprove it.**

`(basis: Zeller, Why Programs Fail; Popper's falsifiability criterion)`

Where several mechanisms fit the evidence, hold them as a ranked set of candidates rather than committing to the first — and prefer the experiment that discriminates *between* candidates, killing the most theories per run.

## Run the cheapest disproving experiment

For each hypothesis, design the experiment that could disprove it for the least effort, and prefer disproof to confirmation ([guard-against-confirmation](../../../craft/evidence/guard-against-confirmation.md)). Two disciplines govern the experiment:

- **Change one thing at a time** ([change-one-thing-at-a-time](../../../craft/evidence/change-one-thing-at-a-time.md)) — vary a single factor so the observed change has exactly one possible cause, and revert each probe before the next. On an intermittent bug, "one run" is not an experiment: repeat trials per change, on the statistical reproduction's harness ([reproduce-before-fixing](../rules/reproduce-before-fixing.md)), until the result is statistically meaningful.
- **Make the invisible observable** ([make-the-invisible-observable](../rules/make-the-invisible-observable.md)) — where the deciding state is unseen, instrument the boundary and read the value crossing it rather than reasoning about what it "must" be. Believe the instrument over the model ([observation-over-inference](../../../craft/evidence/observation-over-inference.md)).

Record each experiment and its result as it runs, so the elimination is auditable and you do not re-run a test you already have the answer to. A hypothesis whose disproving experiment *fails to disprove it* is strengthened, not proven — it advances toward confirmation, where the controlled toggle settles it.

## Attack the surviving candidates

Before carrying a surviving hypothesis into confirmation, stress it. Recruit the [adversary critic](../../../agents/critics/adversary.md) to construct the case the hypothesis does not explain — an input that should fail by the theory but doesn't, or one that fails without the hypothesized condition — and the [assumption-hunter critic](../../../agents/critics/assumption-hunter.md) to surface the premise the hypothesis quietly rests on. Without fan-out, apply both lenses yourself: for each surviving hypothesis, actively try to construct the observation that breaks it before you let it stand.

The output is the surviving mechanism (or a short ranked set), each with the experiments that eliminated its rivals — handed to [confirm-root-cause](05-confirm-root-cause.md) for the end-to-end proof, or back into [localize-the-fault](03-localize-the-fault.md) if every candidate died and the search space needs narrowing again.
