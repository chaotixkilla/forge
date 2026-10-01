# Follow the data

Control flow tells you which code runs; it doesn't tell you what happens to the values moving through it, and a whole class of behavior and failure lives in the data, not the control. A field silently coerced, a validation that runs on one path but not another, a shape that changes as it crosses a serialization or persistence boundary — these are invisible if you only follow which function calls which. And a design reasoned from the happy-path control flow buckles under the data's real shape, volume and lifecycle: the query that's fine at a thousand rows and dies at ten million, the value cached in two places that drift apart, the records nothing is ever allowed to delete. Read or written, the failure is treating the data as a detail of the logic.

## Characterize the data first

For the data the question or the change turns on, pin down:

- **Shape** — the entities and their relationships, what references what and which references must stay consistent; where a value is created or enters the system, and the shape and type it starts as.
- **Volume** — how much there is now and how fast it grows; the difference between a bounded set and an unbounded one is a difference in design, not a number to tune later.
- **Access** — the read/write ratio and the actual query patterns: which lookups are on the hot path, what's joined to what, what must be filtered or sorted.
- **Lifecycle** — how each datum is created, validated, mutated, retained and deleted. Note the **validation and coercion points**, where it's checked, transformed, defaulted or silently coerced, and especially the paths where a check is *skipped*, because that's where malformed data survives; the **mutations**, and whether callers up- or downstream still assume the old shape; and the **boundary crossings** — serialized, persisted, sent over a wire, read back — where shape and invariants are most often lost (a nullable column, a JSON round-trip that drops a type, an encoding change). Retention, auditability and deletion requirements shape storage as much as reads do.

## Reading: trace the value, not just the call

When the question is about *what the data becomes* rather than *which code runs* — a value arriving wrong, a field that should be set and isn't, a transformation that loses information — follow the value across that lifecycle. Control flow and data flow are two reads of the same code, and a question about the correctness of *values* is answered by this one. It's also the axis a data-flow diagram draws.

## Designing: let the data drive the structure

Before deciding where logic lives or what the interfaces are, characterize the data the change touches, then let it drive storage, indexing, denormalization and the placement of logic: the hot query names the store and index that serve it, and the consistency requirement names where a value may live. The tells of a design that ignored the data:

- **A value of record kept in two places** with no single owner — it will drift; give it one home. Data ownership is often the truest seam, since it's a real change and ownership boundary ([seam-along-change-boundaries](seam-along-change-boundaries.md)).
- **An unbounded collection** with no retention or archival story — the queue, cache or table that only grows.
- **A query pattern the chosen store can't serve** without a scan — the access pattern was designed after the storage, not before.

A volume or access assumption is load-bearing: state it, so it can be checked.

*Anchor:* a design that names its hottest query and the store and index that answer it, and states each dataset's growth and retention, versus one that's silent on volume and lifecycle and leaves them to be discovered in production.
