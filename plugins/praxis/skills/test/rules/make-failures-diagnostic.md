# Make failures diagnostic

Write cases and their messages so a red test debugs itself: from the failure alone, a reader should know *what was expected*, *what actually happened*, and *where*, without opening the code. A bare "assertion failed" forces the reader to reconstruct the whole scenario; "expected total 42 for a 3-item cart with a 10% discount, got 45" hands them the bug. Name cases for the behavior they pin, not the function they call, so a failure list reads as a list of broken behaviors.

This is what the reproduction attached to each genuine failure in [report-the-verdict](../phases/06-report-the-verdict.md) is built from — the input and conditions, the expected-vs-actual, and the location — enough that someone who wasn't at the run can reproduce it. A failure a reader cannot act on without re-deriving the scenario is a failure that costs more than it saves; the diagnostic quality of the red is part of the case's design, decided in [design-the-cases](../phases/03-design-the-cases.md), not an afterthought at report time.
</content>
