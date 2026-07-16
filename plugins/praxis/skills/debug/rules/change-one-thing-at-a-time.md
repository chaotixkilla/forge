# Change one thing at a time

When you change three things and the failure goes away, you have learned almost nothing: you don't know which change mattered, whether two of them cancel, or whether the fix is real or coincidence. An experiment that varies one factor has exactly one possible explanation for its result; an experiment that varies several is not an experiment, it's a new configuration you now also have to debug. This rule keeps each probe interpretable.

## Vary one factor; revert before the next

Hold everything fixed but the single factor under test, run the experiment, and read the result against that one change. Then **revert the probe before the next one** — instrumentation, a toggled flag, a swapped value left in place becomes an uncontrolled variable in every later experiment, and a stack of un-reverted probes is how a session accumulates a fog of changes no one can account for. Keep a record of what you changed and what happened ([preserve-the-evidence](preserve-the-evidence.md)) so the elimination is auditable and you never re-run a test you already have the answer to.

## What counts as "one thing"

"One thing" is one *independent cause you could vary alone*, not one line of text — changing a value and the guard that reads it together is two things, and their result is ambiguous. If a change forces a second change to even run, they are coupled; find a smaller experiment that isolates one, or accept that this probe tests the pair and design the next to separate them.

## Under non-determinism, one trial is not an experiment

When the failure is intermittent, a single run proves nothing — the change may look effective because the bug simply didn't fire this time. "Change one thing" then means **repeated trials per change**: run the same single-factor experiment enough times to tell a real shift in the failure rate from noise, and compare rates before and after rather than one outcome to another (per [reproduce-before-fixing](reproduce-before-fixing.md)'s statistical reproduction).

`(basis: Agans' Rule 5, "Change One Thing at a Time" — Debugging: The 9 Indispensable Rules (2002): "use a rifle, not a shotgun … change one thing, see if the symptom changes," and change back what didn't help. The "one independent cause, not one line" clarification and the repeated-trials-under-non-determinism requirement are the maintainer's house extension for the statistical-reproduction case.)`
