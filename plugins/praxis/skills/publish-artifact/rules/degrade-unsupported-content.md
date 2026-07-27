# Degrading unsupported content

Backends differ in what they can represent — nesting depth, table richness, embeds, code blocks, callouts. When the neutral tree meets a backend that can't render a block, "degrade predictably to the nearest faithful form" is the instruction, but the bare verb converges on nothing: one executor drops the block, another errors the whole publish, a third flattens it beyond recognition, and the same artifact lands three different ways on the same backend. This rule pins *what faithful means* and *the order in which to try fallbacks*.

## What "faithful" means

**Faithful = the reader gets the same information and the same decisions, in the same order and grouping.** Fidelity is measured on the *substance*, not the *look* — a direct consequence of the clean-export contract (an artifact is the session's substance for a human audience). So the governing rule when a backend can keep a block's meaning **or** its exact formatting but not both:

**Preserve semantics (structure) over cosmetic formatting.** Keep headings, hierarchy, ordering, lists, table data, code-as-code, and links/references; let go of cosmetic form (exact styling, callout color, font, decorative layout) first. `(basis: ratified by the maintainer, 2026-07-08 — structure/semantics over cosmetic formatting; derived from the clean-export bar (substance for a human audience), round-trippability (structure round-trips across backends, formatting is backend-idiosyncratic), and semantic-over-presentational document-conversion practice.)`

## The ordered fallback

Which neutral block kinds a backend represents natively is declared by its adapter — each adapter's **content support surface** (its Publish block list) is the authoritative surface this ladder reads; a kind not on it is what triggers a fallback. Apply in order; stop at the first step that holds the block's meaning:

1. **Nearest native equivalent that preserves semantics.** Map to the backend's closest construct that keeps the block's role — a callout → the backend's aside/quote; a table → the backend's table; a code block → its code/monospace block; a labeled section → a heading. If the equivalent keeps the meaning, done.
2. **Flatten to a simpler neutral form that keeps the information and its role.** When no native equivalent preserves semantics: a rich embed → a link carrying its title/caption; nesting deeper than the backend allows → promote the inner content to the deepest supported level, preserving its order and leaving a visible marker of the collapsed depth; a complex table → a header row plus one grouped list per row. The information and its grouping survive; only the container simplifies.
3. **Visible placeholder — never a silent drop.** If a block cannot be represented even flattened, leave a short visible marker naming *what content was there* and pointing to its source form (`[diagram — see linked source]`, `[table rendered as list below]`). The marker names the **content** form, never the machinery — it must not leak tooling, process, or how the artifact was produced (the clean-export contract). Only when even a placeholder is impossible does the block become an `unsupported-content` failure ([failure-taxonomy](failure-taxonomy.md)) reported for the whole publish — a reported failure, still never a silent loss.

## Discriminators

- **Visible-degradation over silent-drop.** Any degradation a reader might not notice mattered gets a visible marker, so the reader knows the source carried a richer form and can reach it. A silent drop is the one outcome this rule exists to prevent.
- **Semantics over cosmetics** (the ratified policy above): when forced to choose, the meaning stays and the styling goes.
- **Anchors.** *Top (no degradation):* a heading + list maps one-to-one — leave it. *Bottom (must degrade):* a custom interactive embed on a backend without embeds → a link + caption placeholder naming it, never dropped; a five-level nested list on a backend supporting three → inner levels promoted to depth three with order preserved and the collapsed depth marked, never truncated.
