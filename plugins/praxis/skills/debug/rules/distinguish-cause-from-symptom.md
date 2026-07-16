# Distinguish cause from symptom

The single most common way a debugging session ends wrong is stopping one level too early: fixing the place the failure *surfaced* instead of the place it was *caused*. The symptom fix passes the reproduction — that's what makes it seductive — but the mechanism is untouched, so the bug returns through another path, now masked by the patch that "fixed" it. This rule is the discipline of driving the explanation down to a mechanism before calling it the cause.

## The stop test: a mechanism, not another effect

Keep asking *why does that happen?* one level deeper, and read each answer against a single test: **does it bottom out in a mechanism, or does it point at a further effect?**

- A **mechanism** is a self-contained "this produces that" — a specific line, state, or interaction that, given its inputs, necessarily yields the next state. When the answer is a mechanism, asking "why" again would only ask why the *code is written that way* (a design question), not why the *failure occurs* (the bug question). That is the floor — stop there.
- An **effect** is another symptom wearing a cause's clothes: "the request fails because the cache is stale" — but *why* is the cache stale? If the answer names a further state that itself needs explaining, you are still on an effect, not the cause. Keep going.

The tell that you have stopped too early: the "cause" you name is itself something you'd have to debug. The tell that you have arrived: you can state the fix in terms of the mechanism, and you can explain every prior symptom as a consequence of it.

## Don't force a single linear chain

Asking "why" repeatedly biases toward a single line of causation and a single root cause — but real failures often have a *branching* chain (two conditions that had to co-occur) or more than one contributing cause. Follow every branch that the evidence supports, not just the first; a cause chain that felt too clean is often one where a co-cause was dropped. And the depth is set by reaching a mechanism, not by a fixed count of questions — the "five" in five-whys is illustrative, and stopping at an arbitrary depth is exactly how the method names a symptom as the root.

`(basis: the "ask why until you reach the root" method is Taiichi Ohno's five-whys (Toyota Production System, 1988); its documented failure modes — forcing a single linear path, assuming a single root cause, and stopping at an arbitrary depth that need not be the true cause — are from Alan Card, "The problem with '5 whys'," BMJ Quality & Safety 26(8), 2017. The "bottoms out in a mechanism, not another effect" stop test is the maintainer's house discriminator built on those, keyed to Zeller's cause-effect chain (Why Programs Fail) where the root is the transition from a correct to a faulty state.)`
