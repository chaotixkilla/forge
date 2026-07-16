# Follow the data

Tracing control flow tells you which code runs; it does not tell you what happens to the values moving through it — and a whole class of behavior lives in the data, not the control. A field silently coerced, a validation that runs on one path but not another, a shape that changes as it crosses a serialization or persistence boundary: these are invisible if you only follow which function calls which. This rule is the data-flow lens, distinct from and complementary to the execution trace.

## Trace the value, not just the call
For the data the question turns on, follow it across its lifecycle:
- **Shape at origin** — where the value is created or enters the system, and what shape/type it starts as.
- **Validation and coercion points** — where it is checked, transformed, defaulted, or silently coerced; note especially the paths where a check is *skipped*, because that is where malformed data survives.
- **Mutation and transformation** — where the value is changed, and whether callers up- or downstream still assume the old shape.
- **Boundary crossings** — where it is serialized, persisted, sent over a wire, or read back; shape and invariants are most often lost exactly at these seams (a nullable column, a JSON round-trip that drops a type, an encoding change).

## When data flow is the answer
Reach for this lens when the question is about *what the data becomes* rather than *which code runs* — a value arriving wrong, a field that should be set and isn't, a transformation that loses information. Control flow and data flow are two reads of the same code; a question about the correctness of *values* is answered by this one. It is also the axis a data-flow diagram draws ([render-diagram](../modules/render-diagram.md)).

Cited from [trace-the-behavior](../phases/03-trace-the-behavior.md) (and [render-diagram](../modules/render-diagram.md) for the data-flow diagram kind).
