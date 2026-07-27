# Shaping a portable page tree

The caller hands over a *finished artifact* — authored content organized into sections, not a pre-carved tree. Turning that content into a page tree means deciding where a section becomes its own subpage versus stays inline, and if that is left to taste, two runs of the same artifact carve two different trees: one makes every heading a subpage, another keeps it all on one page, and the published shape (and every deep-link into it) changes run to run. This skill owns that carve — it shapes the *structure*, it does not author or edit the *content*. This rule pins the carve and shapes it so the tree survives mapping onto any backend without loss.

## What a page tree is

- **Exactly one main page** — the artifact's root: its title, and a landing summary (see below).
- **Ordered subpages beneath it** — each a top-level section that earns its own page, in the artifact's authored order.
- **Content as backend-neutral sections** — a page's body is a sequence of neutral blocks: heading, prose, list, table-as-data, code, quote, link/reference. No backend-specific construct enters the neutral tree; that is what lets the map step (step 3 of [SKILL.md](../SKILL.md)) render it onto either a nested-page model or an index-plus-section-files model without rework.

## The landing summary and table of contents — what the main page carries

The main page always carries the artifact's **title**. Two further pieces are decided independently:

- **Landing summary.** If the artifact's first top-level section is introductory — its role is to overview, summarize, or frame the whole, not to be one topic among peers — it is **consumed onto the main page** as the landing summary and does **not** also become a subpage. Discriminator: it introduces or summarizes the rest; a section titled to that effect (Overview / Summary / Abstract / Introduction) or positioned first and framing the others is introductory, a section that is one subject among sibling subjects is not. If there is no introductory section, the main page carries no summary — this skill authors no content, so it never synthesizes one.
- **Table of contents.** In the **carve** case (subpages exist — see the count gate below), the main page carries an ordered list of links to the subpages, **regardless of whether an introductory section was consumed**; when both are present, the table of contents follows the consumed summary. In the **single-page** case (all sections inline, no subpages), there is no table of contents — there are no subpages to list. A links-only table of contents is structural, not authored prose.

## The boundary decision — subpage vs. inline

Everything below is decided on the artifact's **top-level outline sections** (the highest heading level the producing skill used to divide the document), minus any consumed introductory section. The carve is two levels deep at most — main page → subpages; content below a subpage's own top level stays as inline headings **within** that subpage, never a third level.

Apply these in order; the first that decides, decides:

1. **Standalone-topic override (highest precedence).** If any top-level section is a *standalone topic* — it carries its own nested outline (multiple sub-sections of its own) **or** it **dominates** — then carve: that section (and each other top-level section) becomes a subpage. Dominance is pinned on all three of its parameters so it converges: a section dominates when its **source content** is at least half (**≥ 50%**, the threshold) of the **combined source content of the top-level sections under consideration** — i.e. excluding any consumed introductory section, the same scope set above (the base) — **counted in characters of the authored text across all block kinds** (the unit: a width-independent measure available before any backend is chosen; not rendered lines, which depend on a display width the carve step does not yet have). This override wins even when the count rule below would keep a single page. *(This is the tie the guards otherwise leave open — a short artifact with one large, self-structured section still carves.)*
2. **Section-count gate.** Otherwise, count the top-level sections beyond any consumed introductory section: **4 or more → carve** (each becomes a subpage, in order); **3 or fewer → a single main page** with those sections inline, no subpages. `(routed to maintainer: both cuts here are a derived proposal awaiting confirmation — the 4-section carve threshold (≤3 peer sections read as one page, 4+ warrant navigation) and the ≥50% dominance cut in the override above (its threshold, its base — the non-intro sections under consideration — and its unit — source-character count — are all pinned for convergence; only the threshold values are the maintainer's to confirm). Neither has an external authority, so each is pinned precisely enough to converge two cold runs but flagged for the maintainer to confirm or adjust.)`

The carve is reproducible because the primary gate is a **count** and the override keys off **structural signals** (a section's own nested outline; dominant length), not a quality adjective. `(basis: derived from the round-trippable-tree goal — a count-plus-structural-signal gate is what makes the carve reproducible across cold runs, the defect a bare "stands alone as its own topic" left open.)`

- *Anchor (carve):* a spec outlined Overview / Requirements / Design / Open Questions → Overview is introductory, consumed as the landing summary; the remaining 3 would fall under the count gate, but Design carries its own Data-model/API sub-sections (standalone-topic override) → carve; subpages = Requirements, Design, Open Questions in order; the Design subpage keeps Data model and API as inline headings, not further subpages.
- *Anchor (single page):* a status update outlined Summary / Next steps — 2 peer sections, neither self-structured nor dominant → one main page, both inline, no subpages.
- *Gray zone resolved:* Context / Approach / Risks / Timeline, four short peer sections → count gate fires at 4 → carve into 4 subpages (both cold runs converge on the count, not on "readable in one sitting").

## Ordering and round-trippability

- **Preserve authored order.** Subpages and sections keep the producing skill's order; never re-sort by title, alphabetically, or by length. Order carries meaning the reader relies on.
- **Stay backend-neutral.** Shape only in the neutral section kinds above; a tree that encodes one backend's construct (a specific embed, a backend-only layout) no longer round-trips to a different adapter. If the source content needs a construct no neutral kind covers, carry it as the nearest neutral kind and let [degrade-unsupported-content](degrade-unsupported-content.md) handle the per-backend rendering — the neutral tree stays clean.

## Fork — an artifact's own shape vs. an existing destination's conventions

When publishing **into an existing destination** that already has conventions (an area with a page-naming scheme, a docs location with an established section order or placement), two authorities conflict: mirror the destination's conventions, or impose the artifact's own shape. Encode the fork rather than pick a winner — split it by *what each authority owns*:

- **The destination owns placement and naming** — where the tree is rooted, the title/label form, and the ordering position among existing siblings. When the destination has a convention here, mirror it.
- **The artifact owns its own internal shape** — the subpage carve, the section order *within* the artifact, and its content structure. The destination does not reshape the artifact's internals.

Where that split still leaves a genuine conflict (the destination's convention would force a different internal carve), it is **non-gating** and routed: **surrounding convention → house rule → maintainer**. Mirror the surrounding convention by default; escalate only if it would violate a house rule. `(basis: fork-don't-side per the standard-closure depth bar; the placement-vs-internal-shape split and the surrounding-convention-first routing are the closure, so this needs no per-run maintainer call.)`
