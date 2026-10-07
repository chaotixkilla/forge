# Degrading unsupported content

Backends differ in what they can represent — nesting depth, table richness, embeds, code blocks, callouts. When the neutral tree meets a backend that can't render a block, "degrade predictably to the nearest faithful form" is the instruction, but the bare verb converges on nothing: one executor drops the block, another errors the whole publish, a third flattens it beyond recognition, and the same artifact lands three different ways on the same backend.

## What "faithful" means

**Faithful = the reader gets the same information and the same decisions, in the same order and grouping.** Fidelity is measured on the *substance*, not the *look* — a direct consequence of the clean-export contract (an artifact is the session's substance for a human audience). So the governing rule when a backend can keep a block's meaning **or** its exact formatting but not both:

**Preserve semantics (structure) over cosmetic formatting.** Keep headings, hierarchy, ordering, lists, table data, code-as-code, and links/references; let go of cosmetic form (exact styling, callout color, font, decorative layout) first. `(basis: maintainer, 2026-07-08; after round-trippability and semantic-over-presentational conversion practice)`

## The ordered fallback

Which neutral block kinds a backend represents natively is declared by its adapter — each adapter's **content support surface** (its Publish block list) is the authoritative surface this ladder reads; a kind not on it is what triggers a fallback. Apply in order; stop at the first step that holds the block's meaning:

1. **Nearest native equivalent that preserves semantics.** Map to the backend's closest construct that keeps the block's role — a callout → the backend's aside/quote; a table → the backend's table; a code block → its code/monospace block; a labeled section → a heading. If the equivalent keeps the meaning, done.
2. **Flatten to a simpler neutral form that keeps the information and its role.** When no native equivalent preserves semantics: a rich embed → a link carrying its title/caption; nesting deeper than the backend allows → promote the inner content to the deepest supported level, preserving its order and leaving a visible marker of the collapsed depth; a complex table → a header row plus one grouped list per row. The information and its grouping survive; only the container simplifies.
3. **Visible placeholder — never a silent drop.** If a block cannot be represented even flattened, leave a short visible marker naming *what content was there* and pointing to its source form (`[interactive embed — see linked source]`, `[table rendered as list below]`). The marker names the **content** form, never the machinery — it must not leak tooling, process, or how the artifact was produced (the clean-export contract). Only when even a placeholder is impossible does the block become an `unsupported-content` failure ([failure-taxonomy](failure-taxonomy.md)) reported for the whole publish — a reported failure, still never a silent loss.

## Diagrams, charts and in-tree references

Where the surface doesn't list one of the first two kinds, or the backend refuses the block, the ladder lands as below. The third lands as below on every backend:

- **A diagram** becomes its notation as a code block, its caption extended to say it is a diagram's source, its elision line kept below.
- **A chart** becomes the figures table: one column for the x axis and one per series, each headed by its label and unit, under its claim, with the number of observations.
- **An in-tree reference** whose page isn't in the tree becomes its words followed by a visible marker naming the page, `[not in this document: Round 2 · Plan]`, and one whose page is there but whose section isn't keeps its page link, with the marker naming the section, `[not in this document: Round 1 · Plan › Rollout order]`.

`(basis: maintainer, 2026-10-07; the figures table as the chart's fallback, from when-a-visual-is-owed; the missing section, derived from the nearest faithful form)`

## Discriminators

- **Visible-degradation over silent-drop.** Any degradation a reader might not notice mattered gets a visible marker, so the reader knows the source carried a richer form and can reach it.
- **Semantics over cosmetics** (the ratified policy above): when forced to choose, the meaning stays and the styling goes.
- **Anchors.** *Top (no degradation):* a heading + list maps one-to-one — leave it. *Bottom (must degrade):* a custom interactive embed on a backend without embeds → a link + caption placeholder naming it, never dropped; a five-level nested list on a backend supporting three → inner levels promoted to depth three with order preserved and the collapsed depth marked, never truncated.
