# render-diagram (`--diagram`)

Activated by `--diagram`, referenced from [synthesize-the-answer](../phases/05-synthesize-the-answer.md).

Adds a diagram of the traced structure or flow to the map. Deletion test: remove it and understand still returns the prose map; the diagram is an optional rendering of what the trace already found, for a question whose answer is easier to see than to read. The diagram is emitted as **inline text** — a fenced diagram block the reader's tooling can render — so it needs no drawing backend.

## Choosing the diagram kind
The kind is not a default: it's chosen by the axis the framed question's answer turns on, by [when-a-visual-is-owed](../../../craft/writing/when-a-visual-is-owed.md)'s *Which diagram* — structure, data-flow (the [follow-the-data](../../../craft/engineering/follow-the-data.md) lens made visual), sequence or state — and drawn to [diagram-legibility](../../../craft/writing/diagram-legibility.md). Only claims already in the map, at their certainty grades, appear in the diagram.
