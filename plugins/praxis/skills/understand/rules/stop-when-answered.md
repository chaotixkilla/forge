# Stop when answered

An investigation with no stopping rule fails two ways: it quits early and the map is full of holes the question needed filled, or it never quits and tours the whole system, burning effort on paths the question never turned on.

## The stopping test

`(basis: derived from review's [read-the-diff-in-its-blast-radius](../../review/rules/read-the-diff-in-its-blast-radius.md) and the saturation stop in [know-when-to-stop](../../../craft/evidence/know-when-to-stop.md))`

The question is **answered** when both hold:
- **every claim the framed question requires is at or above its target certainty rung** (default target: *traced* for the claims the answer turns on; [certainty-scale](certainty-scale.md)), and
- **no open divergence or unresolved sub-question remains that would change the answer.**

The dig is **done** when the next read would neither raise a load-bearing claim's certainty rung nor change any part of the map. Past that point, stop and synthesize.

## Which paths matter — and when to widen
Scope the dig to the question, and judge each path by one test: **a path matters when a claim the framed question must answer depends on what that path does.** Trace those; a path the answer does not turn on is noted as existing and left unread — record "this exists, not traced" rather than tracing it.

Widen only when a finding *forces* it: a traced path reveals the answer actually depends on a path you'd scoped out (a caller that violates the assumption, a branch that changes the result). Then the new path is in scope because the question now turns on it — not because it was nearby.

## What --deep raises
[deep-dive](../modules/deep-dive.md) (`--deep`) raises the bar the test measures against — it does not remove the test.

Cited from [frame-the-question](../phases/01-frame-the-question.md) (set the initial scope/depth), [trace-the-behavior](../phases/03-trace-the-behavior.md) (which paths to follow), and [synthesize-the-answer](../phases/05-synthesize-the-answer.md) (declare the question answered).
