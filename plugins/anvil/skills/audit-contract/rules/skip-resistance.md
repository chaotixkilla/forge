# Skip-resistance

The load-wiring check ([03-cross-reference](../phases/03-cross-reference.md)) confirms every phase is *referenced*, so it *can* load. This rule covers the next failure: the phase is referenced, but the running agent never *opens* it — because the spine gloss reads as a complete instruction, or a delegation reads as work to perform in place. The harness loads a phase or a sibling skill only when the agent opens or invokes it, so wiring runs the method only when it is **load-bearing**: the spine cannot be acted on without opening the phase, and a delegation cannot be satisfied without invoking the sibling. *Advisory* wiring — a self-sufficient gloss, a "delegates to X" that reads as "do X's job yourself" — lets the agent act on the summary, and the method never runs. Two statically-checkable properties keep wiring load-bearing.

## The spine gloss is a pointer, not an instruction

A numbered SKILL.md line names *what* the step achieves and points at its phase; it does not carry the method to *do* it. The test: **could a cold executor complete the step from the spine line alone?** If yes, the method has leaked up into the spine and the phase file will be skipped. Conformant — a capability plus a trailing pointer to the phase. Non-conformant — a runnable procedure sitting on the spine line. (Exempt: a thin/port skill whose spine *is* an inline procedure with no `phases/` — there is nothing to skip to; its spine is the method by design.)

## A delegation is a named invocation, not a description

A phase that hands a capability to a sibling skill or port names the sibling to **invoke** and consumes its returned result — it never describes the work as something to perform in place. The test: **does the step read as "invoke X and use what it returns," or as "do the thing X does"?** The latter licenses a raw, hand-rolled substitute — the delegation-bypass. A conformant delegation cites the sibling's `SKILL.md` (per the load-wiring citation form) and treats the returned result as the next step's input.

## What the check flags

Statically, off the files: the two findings above — a spine gloss that carries method (not a pointer), and a delegation phrased as work-to-do (not a named invocation). **Not** checked: whether a phase carries a *completion trace* (a named output a later step verifies) — not statically decidable, so it is codify's authoring discipline, not an audit join.

`(basis: derived — from the harness load model (a referenced file runs only when opened/invoked) and the dogfood record, where every phase-skip and delegation-bypass traced to a gloss or delegation that read as self-sufficient.)`
