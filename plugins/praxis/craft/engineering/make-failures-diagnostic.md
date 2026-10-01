# Make failures diagnostic

Write cases and their messages so a red test debugs itself: from the failure alone, a reader should know *what was expected*, *what actually happened*, and *where*, without opening the code. A bare "assertion failed" forces the reader to reconstruct the whole scenario; "expected total 42 for a 3-item cart with a 10% discount, got 45" hands them the bug. Name cases for the behavior they pin, not the function they call, so a failure list reads as a list of broken behaviors.

The diagnostic quality of the red is part of the case's design, decided when the case is written, not an afterthought when a failure is reported — and it's what the reproduction attached to a reported failure is built from.
