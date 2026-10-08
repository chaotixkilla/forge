# notion — artifacts adapter

Implements the **artifacts** capability against Notion, over the Notion MCP. The destination (a parent page or database) is the one the skill resolved (SKILL step 1); auth from that space's `secret_ref`, or over a connection — with several connections to Notion, the one whose workspace holds the destination, found by trying each until it resolves. The [artifacts](../SKILL.md) skill resolves and maps the tree and dispatches here.

## Publish

1. Create the main page under the configured parent (a page, or a row if the parent is a database), titled with the tree's title.
2. Create each subpage as a child of its parent, in tree order: the main page, or the group page that holds it — a parent must exist before its children, so create it first.
3. Map each page's neutral sections to Notion blocks (the block kinds below); record the created page id for each page (see identity). A page mention needs its target to exist, so a page whose body mentions one created after it gets that body once every page of the tree exists.
4. Return the created page URLs, main page first, with the main page's reach (below).

**Content support surface.** This adapter renders these neutral block kinds natively: heading, prose, list, table, code, quote (callout/quote block), link/reference (bookmark or inline link; an in-tree reference is its words as text, then a mention of the page, or the mention alone when the words are the page's title, and one to a section adds `›` and the heading's words after the mention), and diagram (a code block whose language is set to mermaid, which Notion draws, with its caption above and its elision line below). A chart isn't on it. A kind not on it, or nesting deeper than Notion allows, degrades by [degrade-unsupported-content](../rules/degrade-unsupported-content.md) (a rich embed → a bookmark/link with caption; over-deep nesting → flattened to the supported depth with order preserved).

**Reach.** A page takes its access from its parent, so the tree's reach is the main page's. Read the main page's location from the page fetch after publishing: under the publisher's private pages → `private-until-shared`; under a teamspace, or under a page shared with other members → `open`; a location the fetch doesn't settle → `private-until-shared`. Sharing goes by hand. The share line: the owner opens **Share** on the main page and invites people or a teamspace, and its subpages follow.

## Fetch

Fetch the main page by its id or link, then its child pages in the parent's order, each as a subpage with its content, and a subpage's own child pages as the pages it groups. Fetch inverts the surface: words followed by a mention of a page of the same tree come back as an in-tree reference with those words, a bare mention with the page's title as its words, a mention followed by `›` and words as a reference to the section those words begin with, the longest of that page's headings they start with, and a mermaid code block as a diagram, with a caption only when a one-line caption sits directly above it. A chart this backend showed as its figures table comes back as that table, since the table doesn't say it was a chart. A reference the integration may not read is `unauthorized`; one Notion reports genuinely absent is `target-not-found`.

## Capability matrix

What this backend can honor for the write-mode flags — the skill reads this to decide whether a flag applies or must degrade:

- **`--draft`** — *conditional*: Notion has no first-class page draft/unlisted state. If the destination is a database with a status property, set it to a draft value; if a drafts parent page is configured, create under it. If neither is configured, report `unsupported-content` ([failure-taxonomy](../rules/failure-taxonomy.md)) rather than silently publishing a live page.
- **`--version`** — *supported*: create a new `v<n>` child page alongside the prior one, where `<n>` is one greater than the highest existing `v<k>` at the resolved identity (`v1` if none) — the same reproducible, clock-free scheme the local adapter uses, so the label is consistent across backends.
- **`--idempotent`** — *supported*: match by the recorded page id (below) and update that page's blocks in place. A subpage matches the child page at the location it was handed with, or else the page of the same title beneath the main page, a group page's children included, and is renamed in place when its title changed, and moved under its new parent page when the tree now groups it elsewhere; its id is the one mentions of it use.

## Retire

Archive the main page, moving it to the workspace's trash; its subpages go with it. What retiring leaves behind: the page in trash, where members with access can restore it until the trash is emptied, and a link that opens it as deleted. A live surface with no way to archive or trash a page makes the retire `unsupported-content`: the page stands, and the result says its owner moves it to trash by hand.

## Identity key

The **recorded Notion page id is the durable id** — Notion titles and positions change, but a page id survives renames and moves (level 2 of the skill's identity precedence). On first publish, return each created page's id; the caller keeps the main page's as the artifact's location and hands each subpage's back with it as its recorded id. On `--idempotent` republish, resolve the stored id and update that page's content in place; for a subpage present last run but absent now, archive its page so the live tree matches the published tree. If no recorded id exists for the main page and only a title is available, matching by title is unreliable (titles collide and rename) — do **not** duplicate; report `conflict` and let the skill's identity precedence ([stable-identity-and-precedence](../rules/stable-identity-and-precedence.md)) decide. A subpage with no recorded id matches beneath the matched main page by its exact title, as the capability matrix says, and only several children sharing that title are a `conflict`.

## Failure surface

Map Notion/MCP errors to the capability outcomes in [failure-taxonomy](../rules/failure-taxonomy.md):

- **MCP unreachable, not authenticated, or rate-limited/transient** → `unavailable` (the retryable class).
- **Authenticated but the integration lacks access to the parent page/database, or edit access to a page it would archive** → `unauthorized`.
- **An unambiguous not-found** — the configured parent page or database id is reported as genuinely absent, distinct from a permission refusal → `target-not-found`. **An ambiguous not-found/forbidden** — Notion returns one indistinguishable response for "missing" and "no access" → `unauthorized` (the taxonomy's masking default; never guess absence into a not-found).
- **A page already exists with no `--idempotent`/`--version`, a concurrent edit, or an ambiguous identity match** → `conflict`.
- **A neutral block Notion can't represent even degraded, or `--draft` with no draft mechanism configured** → `unsupported-content`; degrade blocks first per [degrade-unsupported-content](../rules/degrade-unsupported-content.md).

## Call-time discovery

Notion's MCP surface shifts (tool names, block schemas, database property shapes), so name the operation and its purpose here and resolve the exact parameters when you call: confirm the current page-create, page-move and block-append tools (a surface that can't move a page leaves it under its old parent and reports it as an advisory, never re-creating it), the inline page-mention shape and the page-title update, the block shapes for tables/code/callouts, the database-vs-page parent distinction, how a page's location shows private versus shared, and whether a page can be archived, against the live MCP schema at call time.
