# When a visual is owed

Whether an artifact gets a picture is usually decided by habit — some writers diagram everything, most diagram nothing — and both are wrong for the same reason: the decision belongs to the *content shape of the requirement*, not to the writer's taste. A relation rendered as prose makes the reader rebuild a graph in their head, and most will not bother; a single fact rendered as a diagram is decoration that costs a read.

## The shape test

A requirement is visual-shaped when **both** hold:

1. **Its content is not a single fact** — it is a relation between elements, a comparison of items across shared attributes, or a quantity varying over a continuum.
2. **It exceeds what linear text carries** — more than about four elements, or any branching or interleaving the reader must hold in mind simultaneously.

Fail either and the requirement is prose. Both must hold: three services in a chain are a relation and still a sentence; forty independent facts are many and still a list.

`(basis: house cap, by analogy from Cowan's ~4-chunk working-memory limit)`

**A changed relation is owed one by default.** A result that changes a flow, a state set, a data shape or a structure, a structure being the containment and dependency between components that *Which diagram* names, owes a diagram of the change: the before and after when the reader must compare them to act, as in judging the change, migrating to it or rolling it back, else the after alone. Clause 2's size bar and the short-walk anchor below don't apply to it; legibility and the two overrides still do, and a setting of `never` still wins. `(basis: maintainer, 2026-10-07)` `(routed to maintainer: before and after when the reader acts on the difference, matching the reader-action fork above.)`

## The form fork

Three shapes, three forms — and the three are exactly the content shapes clause 1 of the shape test admits, so every requirement that reaches this fork lands on one of them, and a requirement that fits none never passed the test and stays prose:

| the requirement's content | form |
|---|---|
| items compared across shared attributes | **table** |
| connection, ordering, containment, or topology | **diagram** |
| a quantity over a continuum — time, magnitude, distribution | **chart** |

**When two fit, decide by what the reader does with it:** if they must *trace a connection*, diagram; if they must *look up a value*, table. Five services with their latencies and their call graph is a table when the reader needs one service's number and a diagram when they need to know what breaks downstream.

`(basis: derived from the reader-action frame: an artifact serves what its reader does next)`

## Which diagram

The kind follows the axis the relation runs on:

- **Sequence** — ordering of interactions over time across participants.
- **Structure** — containment, dependency, or composition; what contains or calls what.
- **Data-flow** — how a value is shaped, validated, or transformed as it crosses boundaries.
- **State** — discrete states and the transitions between them, with their triggers. A state machine drawn as structure loses the triggers, which are the content.

When a requirement spans axes, **draw the one it most turns on and note the others in prose** rather than crowding one picture with all of them.

**When the dominant axis cannot be read but a secondary one can**, the diagram does not quietly fall back to the secondary — a picture drawn on the wrong axis answers a question the reader did not ask, and looks authoritative doing it. Declare the dominant relation blocked per [source-or-declare](source-or-declare.md), and draw the secondary axis only if it discharges a requirement of its own. `(basis: derived from source-or-declare's blocked disposition)`

`(basis: the standard decomposition of program behavior, plus state)`

## Each kind names its own read

A diagram is a claim about the system, and it is sourced under the same discipline as any other requirement ([source-or-declare](source-or-declare.md)). The kind determines what must be read:

| kind | sourced from |
|---|---|
| sequence | a trace of the actual call or message order — not the order the code reads in |
| structure | the real dependency or containment graph, as imported or wired — not the intended architecture |
| data-flow | the actual points where the value changes shape, including the ones that discard information |
| state | the enumerated states and the conditions that really fire each transition |

**A diagram drawn from an impression of the system is the invented sentence in visual form** — more authoritative-looking than prose and just as unsourced. Where the read cannot be performed, the diagram is blocked and is declared, not sketched from memory.

## Charts: the claim is owned here, the rendering is not

A chart still owes what any requirement owes — the claim it supports, its axes and units, and the number of observations behind it.

**The rendering belongs to whatever draws it**: a documentation backend that draws charts natively is the charting capability, and praxis carries no rendering craft of its own (encoding choice, palette, accessibility). Output published as a document hands the chart over as a chart block carrying those three and its rows, and the backend draws it or shows its figures table. Output read where it's produced, such as a report in the conversation, **emits the underlying figures as a table** carrying the same three. A table of real numbers is honest and readable; an improvised chart is neither. `(basis: maintainer, 2026-10-07)`

## Two overrides, applied after the fork

These run **last**, on a requirement that already passed the shape test and been assigned a form. Either one firing sends it to **prose**, regardless of what the test and the fork concluded — they are overrides, not a recap of the test, and they are the only two things that reverse a form already assigned:

- **The reader never acts on the relation.** It exists, it is real, and nothing the reader does depends on holding it. Interesting structure is not owed structure.
- **The visual would restate adjacent prose.** One home per requirement: either the picture carries it and the prose points at it, or the prose carries it and there is no picture. Two homes drift, and the reader reads both to find they said the same thing. Rows that hold each claim with its evidence aren't that prose, unless the rows themselves state the connections: a diagram of how the claims connect sits beside them as the relation's home. `(basis: maintainer, 2026-10-07)`

For contrast, and so the two are not confused: a **single fact**, or a **linear walk of four steps or fewer**, never reaches this point at all — both fail the shape test's clauses above, and a short ordered walk is carried better by a numbered list than by any picture. Those are calibration anchors for the test, not overrides of it.

`(basis: observed in three house dogfood runs that produced three different visual sets)`
