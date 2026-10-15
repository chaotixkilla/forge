# Diagram as mermaid

A diagram block carries its form and its elements, never a notation ([portable-tree-shape](../../document/rules/portable-tree-shape.md)), so each destination can draw it in its best way. Several destinations draw mermaid: a file, a page that renders mermaid code blocks, a hosted review request. The conversation shows mermaid too. If each writer improvised the mapping, one diagram would come out as different pictures, and the marks that show what changed would be lost on the way. This rule is the one mapping, both ways. `(basis: maintainer, 2026-10-14)`

## Writing it

**Lines around the block.** The caption goes above the block as text. Below it, in this order, are up to three lines, each with a fixed lead that Fetch matches on:

- `Marks:` — what each mark looks like, when the diagram has marks;
- `Elided:` — the elision line;
- `Source:` — the provenance.

**The first line of the source** is `%% form: <form>`.

**Ids** are written `n_` followed by the element's id with hyphens made underscores, so no id collides with a mermaid keyword such as `end`.

| form | mermaid type | elements as |
|---|---|---|
| flow, structure, data-flow | `flowchart LR` | a group as `subgraph <id>["<label>"]`, nested by `parent`; a node as `<id>["<label>"]`, its `lines` joined under the label with `<br/>`. Shape by kind: decision `{"…"}`, start `(["…"])`, end `((("…")))`, store `[("…")]`, external `[/"…"/]`. An edge as `<from> -->\|"<label>"\| <to>` |
| state | `stateDiagram-v2` | a group as a composite state `state "<label>" as <id> { … }`; a state as `<id> : <label>`, its `lines` joined under it with `<br/>`; initial and final as `[*]`; a transition as `<from> --> <to> : <label>` |
| sequence | `sequenceDiagram` | a participant as `participant <id> as <label>`, in order; call `->>`, reply `-->>`, async `-)`, a note as `Note over <ids>: <text>` |
| data-model | `erDiagram` | an entity with its fields as `<type> <name>`, plus `PK` or `FK`; a relation as `<from> <left>--<right> <to> : "<verb>"`, where the left end is `\|\|` for one, `\|o` for zero or one, `}\|` for many and `}o` for zero or many, and the right end is `\|\|`, `o\|`, `\|{` or `o{` |
| timeline | `gantt`, `dateFormat YYYY-MM-DD`, or for offsets in seconds `dateFormat X` with `axisFormat %M:%S`, `%H:%M:%S` when the last offset is an hour or more | a span as `<label> : <id>, <start>, <end>`; a milestone as `<label> : milestone, <id>, <date>, 0d` |

**Labels.** In a flowchart's node, edge and subgraph labels and an erDiagram's relation labels, a label goes in double quotes, with `"` written as `#quot;`. Everywhere else it is written bare, with `:` as `#58;`, `;` as `#59;` and `#` as `#35;`, since quotes would show in the picture.

**Marks.** A mark — added, changed, removed — is drawn by type:

- **Flowchart nodes and groups, and states,** take a class, written with the lines below — only those whose class the diagram applies, the group-kind lines before the mark lines, so a marked group shows its mark:

  ```
  classDef added fill:#dafbe1,stroke:#1a7f37,stroke-width:2px
  classDef changed fill:#fff8c5,stroke:#9a6700,stroke-width:2px
  classDef removed fill:#ffebe9,stroke:#cf222e,stroke-dasharray:4 3
  ```

  applied with `class <ids> <mark>`.
- **Flowchart edges, state transitions, erDiagram relations and gantt rows** take the mark as a label suffix, ` · added`. A removed flowchart edge is also drawn as `-.->`.
- **An erDiagram entity** takes it as an extra attribute row, `mark <mark>`, which reads back as the mark, never a field.
- **In a sequence,** each marked message sits in a `rect` — `rgb(218, 251, 225)` for added, `rgb(255, 248, 197)` for changed, `rgb(255, 235, 233)` for removed — and the rect's last line is exactly `Note over <from>,<to>: <mark>` (`Note over <from>: <mark>` when they are one participant).

`(basis: derived — a mark that doesn't show is a before/after the reader can't see)`

**A group's kind** is a class on its subgraph, from these lines, only those it applies, so every kind reads back:

```
classDef container fill:none
classDef boundary fill:none,stroke-dasharray:6 4
classDef trust_boundary fill:none,stroke-dasharray:6 4,stroke-width:2px
classDef environment fill:none,stroke-dasharray:2 2
```

## Only the types the destination draws

Each destination's adapter says which mermaid types its renderer draws. A form whose type isn't among them is not written as mermaid. It degrades to its elements table, by [degrade-unsupported-content](degrade-unsupported-content.md). A type the renderer marks experimental counts only when the adapter lists it. The conversation shows the source as text, so any type will do there.

## Reading it back

Fetch reads a mermaid block by the same table, in reverse, into a diagram block:

- **The form** comes from the `%% form:` line. Without one — an older block — a `graph` or a `flowchart` in any direction is `structure`, and any other type is the form its row names.
- **Ids** lose their `n_` and have their underscores turned back into hyphens, a doubled one into the `--` that joins an edge's ends. An edge, transition, message or relation carries the id [portable-tree-shape](../../document/rules/portable-tree-shape.md) derives for it, so it is derived again, never invented; a `[*]` is the `initial` or `final` node its position gives, in its group.
- **Marks** come back from classes, label suffixes, an entity's `mark` row, and a sequence rect's colour; the rect's mark note is not an element.
- **The rest** — elements, marks, groups, the caption above, and the `Marks:`, `Elided:` and `Source:` lines below — comes back as written.

A block someone edited by hand into something the table doesn't produce comes back as a diagram with what it could read. A block it can't read at all comes back as code, saying it is a diagram's source.

Cited by [portable-tree-shape](../../document/rules/portable-tree-shape.md), [degrade-unsupported-content](degrade-unsupported-content.md), the artifacts adapters whose backend draws mermaid, and the version-control adapters that post descriptions and reviews.
