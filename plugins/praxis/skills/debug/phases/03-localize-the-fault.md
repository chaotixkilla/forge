Shrink the search space — of inputs, of code, of time — from "somewhere in the system" to a span you can inspect directly. This is the first beat of the **localize → hypothesize-and-test → confirm loop**: you do not finish localizing before you start testing, because each experiment in [hypothesize-and-test](04-hypothesize-and-test.md) narrows the space again, and you re-enter the cycle until the mechanism is pinned.

## Narrow by bisection, across all three axes

**Halve the search space** and ask which half holds the fault, across whichever axes the failure offers: the **input**; the **code path** (the traced route from [gather-evidence](02-gather-evidence.md)); and, for a regression that appeared at a known point, the **history** — a first-bad change is often the cause handed to you directly. [bisect-aggressively](../rules/bisect-aggressively.md) holds the method for each axis and pins *when* bisection beats a linear read, and when it doesn't.

## Trace to the first divergence, not the loudest symptom

The place a failure *surfaces* — the crash, the exception, the wrong value printed — is usually downstream of where it was *caused*. Follow the chain backward to the earliest point where actual state diverges from what it should be ([follow-the-first-divergence](../rules/follow-the-first-divergence.md)): the corrupted value was read here, but written wrong three frames earlier; the null was dereferenced here, but should have been non-null since its construction.

## The done-state for this pass

This pass of the loop is done when the fault sits in a span small enough to **inspect or instrument directly** — a function, a boundary, a single commit's diff — not when you have a theory of what's wrong (that is the next phase's job). If the span is still too large to reason about concretely, you have not narrowed enough: pick the next bisection and cut it again. If narrowing has bottomed out at a boundary you cannot see across, that is the signal to make it observable ([make-the-invisible-observable](../rules/make-the-invisible-observable.md)) in the hypothesize-and-test pass that follows, then narrow again with the value in hand.
