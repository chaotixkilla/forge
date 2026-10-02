# claude-docs — knowledge adapter

Implements the **knowledge** capability against Claude Docs, over the Claude Docs connector (a claude.ai connector, so it exists only where the user has it connected). The space starts from the resolved source's `root`, a doc whose tabs and links lead to the rest of the owner's docs; the connector authenticates through the user's claude.ai connection, so the adapter needs no `secret_ref`, and its transport is `mcp`. The [knowledge](../SKILL.md) skill takes the caller's read and dispatches here. A doc holds tabs and each tab one prose body, so a doc reads as a document whose tabs are its sections.

## Search the space

1. Query the owner's docs for the caller's query through the connector's search. The owner's docs are one space: a search reaches all of them, and the root only anchors a walk, so one claude-docs source covers them — say so with the results, as an unconfined search. A scope the caller names (a doc) narrows the read to that doc's tabs.
2. Return **ranked references only** — each a doc's id and link with its title and any snippet the search surfaces. Fetching every hit is this port's most expensive mistake.
3. Bound the result set by the page size the search exposes. When the backend cuts it short, that is `partial`.

## Fetch a document

1. Fetch by reference: a doc's id, or its link, whose trailing id is the doc's. Read every tab's body, in the doc's tab order, as the document's sections, each under its tab's name.
2. Carry the provenance the connector exposes — the title, the doc id as the durable reference, and the author, created and last-edited times where the read returns them — into the port's provenance floor ([SKILL.md](../SKILL.md)). A field this connector doesn't return comes back *not-exposed*.

## List a document's children

A doc's children are its tabs: return each tab's name and reference, in the doc's own order, never their bodies. A tab has no children of its own.

## Content support surface

Returns as readable text: headings, prose, lists, pipe tables, code blocks, quotes and links. A chart or a diagram comes back as its source notation where the read carries one; an embedded block whose content the read doesn't carry is **reported** as a reference with the fact that its body wasn't inlined, never as an empty section.

## Failure surface

Map connector outcomes to the capability outcomes in [outcome-taxonomy](../rules/outcome-taxonomy.md):

- **The connector isn't connected, isn't authorized, or is rate-limited or failing transiently** → `unavailable`, the retryable class. A connector absent from the running context's tool pool is this same case: the read never reached a backend, so it is never an empty result.
- **A doc the connector refuses with an access error**, where absence and no access look the same → `unauthorized`, per the taxonomy's masking default. Never guess absence into a not-found.
- **A search that completed and matched nothing** → `ok` with zero references.
- **A result set truncated by a page limit, or a doc whose content comes back cut short** → `partial`, returned with whatever was read.

## Call-time discovery

The connector's surface shifts, so this file names each operation and its purpose, and the exact call shapes are resolved when you call. Before the first docs call of a run, read the connector's own guide (`guide` with `topic.index`), which prints the read, query and tab shapes this adapter relies on. **Never pin a tool id**: the connector is exposed under different server prefixes depending on how a project connected it.
