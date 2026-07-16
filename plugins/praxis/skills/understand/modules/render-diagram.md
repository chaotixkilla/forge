# render-diagram (`--diagram`)

Activated by `--diagram`, referenced from [synthesize-the-answer](../phases/05-synthesize-the-answer.md).

Adds a diagram of the traced structure or flow to the map. Deletion test: remove it and understand still returns the prose map; the diagram is an optional rendering of what the trace already found, for a question whose answer is easier to see than to read. The diagram is emitted as **inline text** — a fenced diagram block the reader's tooling can render — so it needs no drawing backend, consistent with understand declaring no `config_requires`.

## Choosing the diagram kind
The kind is not a default; it is chosen by what the framed question is about:

`(basis: control/data/sequence is the standard decomposition of program behavior — [follow-the-data](../rules/follow-the-data.md) owns the data axis, [trace-the-behavior](../phases/03-trace-the-behavior.md) the control and temporal axes; matching the diagram to the question's dominant axis is derived from that split.)`

- **Control-flow / structure** when the question is about *how components relate or how control moves* — what calls what, module boundaries, the shape of the system.
- **Data-flow** when the question is about *how data is shaped, validated, and transformed as it crosses boundaries* — the [follow-the-data](../rules/follow-the-data.md) lens made visual.
- **Sequence** when the question is about *the ordering of interactions over time across participants* — a request lifecycle, a protocol, who-calls-whom-when.

The criterion: **match the diagram kind to the question's dominant axis** — structure→control, transformation→data, temporal-ordering→sequence. When a question genuinely spans axes, draw the one the *answer* most turns on and note the others in prose, rather than crowding one diagram with all three. Only claims already in the map (at their certainty grades) appear in the diagram — it renders the understanding, it does not add to it.
