Localizing is search: the fault is somewhere in a space — of inputs, of code, of time — and this phase shrinks that space from "somewhere in the system" to "this span I can inspect directly." It is the first beat of the **localize → hypothesize-and-test → confirm loop**, and the loop matters: you do not finish localizing before you start testing. You narrow to a suspect span, form a hypothesis about it ([hypothesize-and-test](04-hypothesize-and-test.md)), and the experiment's result narrows the space again — each pass tightening the other. Treat this phase and the next as one cycle you re-enter until the mechanism is pinned, not two boxes to complete in order.

## Narrow by bisection, across all three axes

The move that beats reading linearly from the top is to **halve the search space** and ask which half holds the fault ([bisect-aggressively](../rules/bisect-aggressively.md) — which also pins *when* bisection beats a linear read, and when it doesn't). Bisect across whichever axes the failure offers:

- **The input** — reduce the failing input toward the smallest one that still triggers the failure, discarding what doesn't change the outcome. A minimal trigger is a smaller space to reason about and often names the cause by what it retains.
- **The code path** — binary-search the traced route from [gather-evidence](02-gather-evidence.md): probe a point midway between the last-known-good state and the symptom, and ask which side the state first goes wrong on. That halves the code under suspicion each probe.
- **The history** — when the failure is a regression that appeared at a known point, bisect the version-control history between a known-good and known-bad revision to find the change that introduced it. A first-bad change is often the cause handed to you directly.

## Trace to the first divergence, not the loudest symptom

The place a failure *surfaces* — the crash, the exception, the wrong value printed — is usually downstream of where it was *caused*. Follow the chain backward to the earliest point where actual state diverges from what it should be ([follow-the-first-divergence](../rules/follow-the-first-divergence.md)): the corrupted value was read here, but written wrong three frames earlier; the null was dereferenced here, but should have been non-null since its construction. Localizing to the surfacing site and fixing there is how a symptom patch gets mistaken for a cause fix — narrow to the *origin* of the bad state.

## The done-state for this pass

This pass of the loop is done when the fault sits in a span small enough to **inspect or instrument directly** — a function, a boundary, a single commit's diff — not when you have a theory of what's wrong (that is the next phase's job). If the span is still too large to reason about concretely, you have not narrowed enough: pick the next bisection and cut it again. If narrowing has bottomed out at a boundary you cannot see across, that is the signal to make it observable ([make-the-invisible-observable](../rules/make-the-invisible-observable.md)) in the hypothesize-and-test pass that follows, then narrow again with the value in hand.
