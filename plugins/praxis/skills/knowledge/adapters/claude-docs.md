# claude-docs — knowledge adapter

Implements the **knowledge** capability against Claude Docs, over the Claude Docs connector (a claude.ai connector, so it exists only where the user has it connected). The space is reached from the source's entry references — its `root` doc, or the docs the port names for a source without one — whose tabs and links lead to the rest of the owner's docs; the connector authenticates through the user's claude.ai connection, so the adapter needs no `secret_ref`, and its transport is `mcp`. The [knowledge](../SKILL.md) skill takes the caller's read and dispatches here. A doc holds tabs and each tab one prose body, so a doc reads as a document whose tabs are its sections.

## Supported reads

Fetch and children. **Search is unsupported**, scoped or not: the connector has no search across docs and no lookup by name — its `query` lists a doc's comment threads, and its text search runs inside one tab's body, matching words rather than a question. `(basis: maintainer, 2026-10-02)`

## Fetch a document

1. Fetch by reference: a doc's id, or its link, whose trailing id is the doc's. Read every tab's body, in the doc's tab order, as the document's sections, each under its tab's name.
2. A body links another doc by its link or by a doc mention. Keep each in the returned content as a link carrying the doc's id, so a caller can fetch it to walk on. A link of the doc-link form may be another artifact type, which the read refuses (failure surface).
3. Carry the provenance the connector exposes — the title, the doc id as the durable reference, and the author, created and last-edited times where the read returns them — into the port's provenance floor ([SKILL.md](../SKILL.md)). A field this connector doesn't return comes back *not-exposed*.

## List a document's children

A doc's children are its tabs: return each tab's name and reference, in the doc's own order, never their bodies. A tab has no children of its own. The docs a body links are not children; they come back in the fetched content.

## Content support surface

Returns as readable text: headings, prose, lists, pipe tables, code blocks, quotes and links. A chart or a diagram comes back as its source notation where the read carries one; an embedded block whose content the read doesn't carry is **reported** as a reference with the fact that its body wasn't inlined, never as an empty section.

## Failure surface

Map connector outcomes to the capability outcomes in [outcome-taxonomy](../rules/outcome-taxonomy.md):

- **The connector isn't connected, isn't authorized, or is rate-limited or failing transiently** → `unavailable`, the retryable class. A connector absent from the running context's tool pool is this same case: the read never reached a backend, so it is never an empty result.
- **A doc the connector refuses with an access error**, where absence and no access look the same, including a link that names another artifact type → `unauthorized`, per the taxonomy's masking default. Never guess absence into a not-found.
- **A doc whose content comes back cut short** → `partial`, returned with whatever was read.

## Call-time discovery

The connector's surface shifts, so this file names each operation and its purpose, and the exact call shapes are resolved when you call. Before the first docs call of a run, read the connector's own guide (`guide` with `topic.index`), which prints the read and tab shapes this adapter relies on. **Never pin a tool id**: the connector is exposed under different server prefixes depending on how a project connected it.
