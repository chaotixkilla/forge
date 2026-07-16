# Follow the first divergence

A failure is loudest where it surfaces — the crash, the exception, the wrong value on screen — and that is almost never where it was caused. The bad value was *read* here; it was *written wrong* somewhere earlier. Debugging the surfacing site fixes a symptom; the cause is upstream, at the first point where the program's actual state stopped matching what it should have been. This rule is the discipline of tracing back to that first point instead of stopping at the noise.

## Trace to the transition from correct to faulty

Walk backward along the causal chain from the observed failure: the failure was produced by some state, which was produced by an earlier state, and so on. At each step ask *was the state already wrong when it arrived here, or did this step corrupt it?* The point you are hunting is the **transition** — the earliest step where a correct state came in and a faulty state went out. Before that transition the state is sound; after it, the infection propagates until it surfaces. That transition is the cause's location; everything downstream of it is propagation, not cause.

## The discriminator: origin vs. propagation

For any suspect site, one question decides whether it is the cause or a waypoint: **is the state already wrong when it reaches this site?**

- Already wrong on arrival → this site is *propagation*; the cause is further back. Keep tracing.
- Correct on arrival, wrong on exit → this site is the *first divergence*; the fault is here.

This is what separates the crash site (where a null was dereferenced) from the fault (where the value should have been set non-null and wasn't). Fixing the dereference silences the crash; fixing the origin removes the bug.

`(basis: Zeller's cause-effect / infection model — Why Programs Fail (and The Debugging Book): a failure is the end of a chain of faulty states (infections), and the defect is found by tracing back the propagation to "a transition in which a correct state comes in and a faulty state comes out." The origin-vs-propagation discriminator is that transition test stated as a per-site check.)`
