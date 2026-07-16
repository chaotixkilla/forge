# Follow the data

A design reasoned from the happy-path control flow looks clean and then buckles under the data's real shape, volume, and lifecycle — the query that is fine at a thousand rows and dies at ten million, the value cached in two places that drift apart, the records nothing is ever allowed to delete. The trap is designing the *logic* first and treating storage as a detail to fill in later. This rule reverses that: characterize the data first and let its realities drive the structure.

## Characterize the data before the logic

Before deciding where logic lives or what the interfaces are, pin down the data the change touches:

- **Shape** — the entities and their relationships; what references what, and which references must stay consistent.
- **Volume** — how much there is now and how fast it grows; the difference between a bounded set and an unbounded one is a difference in design, not a number to tune later.
- **Access** — the read/write ratio and the actual query patterns: which lookups are on the hot path, what is joined to what, what must be filtered or sorted.
- **Lifecycle** — how each datum is created, mutated, retained, and deleted; retention, auditability, and deletion requirements shape storage as much as reads do.

Then let those realities drive storage, indexing, denormalization, and the placement of logic — the hot query names the store and index that serve it; the consistency requirement names where a value may live.

## The tells of a design that ignored the data

- **A value of record kept in two places** with no single owner — it will drift; give it one home (this is often the truest [seam-along-change-boundaries](seam-along-change-boundaries.md), since data ownership is a real change/ownership boundary).
- **An unbounded collection** with no retention or archival story — the queue, cache, or table that only grows.
- **A query pattern the chosen store cannot serve** without a scan — the access pattern was designed after the storage, not before.

*Anchor:* a design that names its hottest query and the store/index that answers it, and states each dataset's growth and retention, versus one that is silent on volume and lifecycle and leaves them to be discovered in production.

Cited by [mapping-to-system](../phases/01-mapping-to-system.md) and [specify-interfaces](../phases/03-specify-interfaces.md). Related: [seam-along-change-boundaries](seam-along-change-boundaries.md), [surface-assumptions](surface-assumptions.md) (a volume or access assumption is load-bearing).
