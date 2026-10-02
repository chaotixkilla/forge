# notion — knowledge adapter

Implements the **knowledge** capability against Notion, over the Notion MCP. The space is the resolved source's (SKILL step 1); auth comes from the configured connection — with several connections to Notion, the one whose workspace holds the source's root, found by trying each until the root resolves. The [knowledge](../SKILL.md) skill takes the caller's read and dispatches here.

## Search the space

1. Before a scoped search, fetch the page it is confined to — the source's root, or the caller's subtree beneath it — once per run: a refused or missing scope makes the search `unauthorized` or `target-not-found` by the failure surface below, never an empty result; a scope that is a database searches within its data source, as below. Then run a search for the caller's query **confined to the source's root** — pass the root page as the search's scope, or the subtree the caller names beneath it; where the scope names a database's data source, search within that source. When the live search accepts no page scope, say so with the results, so the caller reads them as the workspace's rather than this source's.
2. Return **ranked references only** — each a page reference the caller can fetch, with its title and whatever snippet the search surfaces. Do not fetch page bodies here: search returns references, and fetching every hit is this port's most expensive mistake.
3. Bound the result set by the page size the search exposes. When the backend cuts it short, that is `partial` — not a complete answer (see the failure surface).

## Fetch a document

1. Fetch by reference (a page URL or id). Content returns as Notion-flavored markdown.
2. **Branch on what the reference resolves to.** A page returns document content. A **database or data source returns a schema and its rows' shape, not prose** — that is not a document, and it maps to `unreadable-content` rather than being handed back as though it were one. A caller that wanted the rows asks for the children instead.
3. Carry the provenance Notion exposes per page — title, the page id as the durable reference, author, created and last-edited timestamps — into the port's provenance floor ([SKILL.md](../SKILL.md)). Notion exposes all of them, so mark a field *not-exposed* only where a specific page genuinely lacks it, never as a blanket.

## List a document's children

1. Walk the page's child pages — **the immediate level only**, in the backend's own order.
2. A page's children are its subpages; a database's children are its rows. Return references, never bodies — the caller decides which to fetch.
3. Notion trees run deeper than they look. Return one level and let the caller walk; how deep to go is the caller's policy, not this adapter's.

## Content support surface

Returns as readable text: headings, prose, lists, tables, code, quotes and callouts, inline links and bookmarks. Two shapes do not survive as text and are **reported rather than silently flattened** — a synced or embedded block whose source lies outside the fetched page, and a linked database view whose rows live elsewhere. Both come back as a reference to the source, with the fact that the body was not inlined stated explicitly, so a caller never reads a placeholder as an empty section.

## Failure surface

Map Notion/MCP conditions to the capability outcomes in [outcome-taxonomy](../rules/outcome-taxonomy.md):

- **MCP unreachable, not connected, not authenticated, or rate-limited/transient** → `unavailable` (the retryable class). **A Notion MCP absent from the running context's tool pool is this same case** — the read never reached an authenticated backend, so it is `unavailable` and never an empty result.
- **Authenticated, but the integration lacks access to the page or space** → `unauthorized`.
- **An unambiguous not-found** — the reference is reported genuinely absent, distinct from a permission refusal → `target-not-found`. **An ambiguous not-found/forbidden** — Notion returns one indistinguishable response for "missing" and "no access" → `unauthorized`, per the taxonomy's masking default. Never guess absence into a not-found.
- **A search that completed and matched nothing** → `ok` with zero references. That is the space answering, not a failure.
- **A reference resolving to a database or data source rather than a document**, or content no text form can carry (above) → `unreadable-content`.
- **A result set truncated by a page limit, a page whose content is cut short, or a space where some subtree is silently skipped for access** → `partial`, returned with whatever was read.

## Call-time discovery

Notion's MCP surface shifts — tool names, block schemas, database property shapes, the page-vs-data-source distinction — so name the operation and its purpose here and resolve the arguments when you call: confirm the current search, fetch, and child-listing tools, the scoping parameters search accepts, and how a data source is distinguished from a page in the schema as it stands. **Never pin an MCP tool id.** The ids are install-specific — the same Notion connector is exposed under different server prefixes depending on how a project connected it — so an adapter that hardcodes one is wrong for every other install.
