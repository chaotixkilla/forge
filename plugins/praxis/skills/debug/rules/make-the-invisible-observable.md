# Make the invisible observable

Reasoning about state you cannot see is guessing with extra steps. The value crossing a boundary, the branch actually taken, the order two events actually occurred in — when these are invisible, the mind fills them with what it expects, and what it expects is the model that already failed to predict the bug. The remedy is not harder thinking; it is instrumentation: make the hidden state emit a fact you can read. This rule is the discipline of turning an assumption into an observation.

## Instrument the boundary you suspect

Rather than deduce what a value "must be" at a suspected point, put an observation there — log or assert the value crossing the boundary, the branch entered, the state on entry and exit — and read what it actually is. A single logged value at the right boundary settles a question that an hour of reasoning about the surrounding code cannot, because it replaces inference with fact ([trust-observations-over-assumptions](trust-observations-over-assumptions.md)).

## The discriminator: where to instrument

Do not instrument everywhere — that buries the signal. Instrument at the **suspected boundary**: the point between the last state you have confirmed correct and the symptom, ideally the midpoint so the reading also halves the search ([bisect-aggressively](bisect-aggressively.md)). The reading you want is the one that will send you to one side of that boundary or the other; if a probe's result wouldn't change where you look next, it's the wrong probe.

## Beware the probe that moves the bug

Observation can perturb the system it observes — a log statement, a lock, or added latency can change the timing that a concurrency or ordering bug depends on, so the bug hides when watched and returns when you stop (the classic heisenbug). When a probe changes the outcome, that is itself evidence (the bug is timing-sensitive), and it argues for lower-perturbation observation — capture that survives replay, sampling that doesn't serialize, or a record/replay approach — over heavier instrumentation that changes the very interleaving you're chasing.

`(basis: Agans' Rule 3, "Quit Thinking and Look," and Rule 2, "Make It Fail" — Debugging: The 9 Indispensable Rules (2002): instrument and observe the failure directly. The where-to-instrument discriminator ties to bisection (probe the boundary that halves the space); the observer-effect caution reflects the well-documented heisenbug hazard in community practice, where instrumentation perturbs timing-sensitive failures.)`
