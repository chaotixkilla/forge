# render-diagram (`--diagram`)

Activated by `--diagram`, referenced from [synthesize-the-answer](../phases/05-synthesize-the-answer.md).

Adds a diagram of the traced structure or flow to the map. Deletion test: remove it and understand still returns the prose map; the diagram is an optional rendering of what the trace already found, for a question whose answer is easier to see than to read. The diagram is a diagram block — its form and elements ([portable-tree-shape](../../document/rules/portable-tree-shape.md)) — shown in the conversation as a fenced mermaid block ([diagram-as-mermaid](../../artifacts/rules/diagram-as-mermaid.md)), so it needs no drawing backend, and handed on as the block, so a published map draws it at its destination's best.

## Choosing the diagram kind
The kind is not a default: it's chosen by the axis the framed question's answer turns on, by [when-a-visual-is-owed](../../../craft/writing/when-a-visual-is-owed.md)'s *Which diagram* — structure, data-flow (the [follow-the-data](../../../craft/engineering/follow-the-data.md) lens made visual), sequence or state — and drawn to [diagram-legibility](../../../craft/writing/diagram-legibility.md). Only claims already in the map appear in the diagram, a node's certainty grade as one of its `lines`, and an element without lines carrying it at the end of its label.

When [when-a-visual-is-owed](../../../craft/writing/when-a-visual-is-owed.md) says no diagram is owed for what the trace found, draw none and say so in the map, in one line, so a flag an act passes never forces a picture of a single fact. (basis: derived — the flag asks for a diagram where one is owed)
