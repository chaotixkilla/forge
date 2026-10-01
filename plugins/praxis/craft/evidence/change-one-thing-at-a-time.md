# Change one thing at a time

When you change three things and the outcome changes, you have learned almost nothing: you don't know which change mattered, whether two of them cancel, or whether the result is real or coincidence. A probe that touches several unknowns at once gives a signal you can't attribute — if it fails, you don't know which part failed; if it passes, you don't know that luck elsewhere didn't mask a problem in the part you cared about.

## Vary one factor; hold the rest; revert before the next

Hold everything fixed but the single factor under test, run the experiment, and read the result against that one change. In a probe you build, holding the rest fixed means stubbing, mocking or hardcoding everything that isn't the question — and **never stubbing the factor under test itself**. Faking the database when the question is the API's throughput is isolation done right; faking the API layer when the question is the API's throughput leaves the probe unable to answer it. Then **revert the probe before the next one**: instrumentation, a toggled flag or a swapped value left in place becomes an uncontrolled variable in every later experiment. Keep a record of what you changed and what happened, so the elimination is auditable and you never re-run a test you already have the answer to.

## What counts as "one thing"

"One thing" is one *independent cause you could vary alone*, not one line of text — changing a value and the guard that reads it together is two things, and their result is ambiguous. If a change forces a second change to even run, they're coupled: find a smaller experiment that isolates one, or accept that this probe tests the pair and design the next to separate them. A question that genuinely spans two entangled unknowns is two questions: reframe it into two experiments rather than testing both at once.

## Under non-determinism, one trial is not an experiment

When the outcome is intermittent, a single run proves nothing — the change may look effective because the failure simply didn't fire this time. "Change one thing" then means **repeated trials per change**: run the same single-factor experiment enough times to tell a real shift in the failure rate from noise, and compare rates before and after rather than one outcome to another.

`(basis: Agans 2002, rule 5; the maintainer's one-independent-cause definition and repeated-trials rule)`
