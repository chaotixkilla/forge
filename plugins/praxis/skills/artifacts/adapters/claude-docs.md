# claude-docs — artifacts adapter

Implements the **artifacts** capability against Claude Docs, over the Claude Docs connector (a claude.ai connector, so it exists only where the user has it connected). The [artifacts](../SKILL.md) skill resolves and maps the tree and dispatches here. A doc holds tabs and each tab holds one prose body, so the portable tree maps onto one doc, with one tab per page. The connector authenticates through the user's own claude.ai connection, so the adapter needs no `secret_ref`; its transport is `mcp`. Docs live in the owner's artifact list, not under a parent, so this adapter takes no destination and artifacts skips the lookup for it. A destination resolved anyway (a configured `destination`, a path, a parent page) has nowhere to apply: report it as an ignored-destination advisory with the result rather than failing. The one target `--to` names here is an existing doc, by its id or link, and that is the doc's identity (below).

## Publish

1. **Birth the doc** with one `batch` call whose `container.create` carries the doc's name (the tree's title) and the main page's content as the first tab's markdown. A publish isn't watched, so the whole main page goes in the birth; when the caller says the user is watching the doc fill, follow the connector's outline-then-fill guidance instead.
2. **Add each subpage as a further tab**, in tree order. Tabs on a doc are members the call spells, plus one member that names and orders them; the main page's tab comes first.
3. **Render each page's neutral sections as markdown**: headings, prose, lists, pipe tables, fenced code and links are native, a quote is a `>` block, and a diagram is a fenced code block of its text notation. A block the connector refuses degrades by [degrade-unsupported-content](../rules/degrade-unsupported-content.md).
4. **Return the doc's link**, with each tab's name in tree order. The birth's acknowledgement carries the link in its trailer. Opening the doc on the user's screen is the caller's decision, not this adapter's.

**Reach.** Every doc is `private-until-shared`. Its share line: the owner opens **Share** at the top of the doc and adds people by name, to view, comment or edit. No connector operation shares a doc or shows who has access, so a doc shared after an earlier publish still reports `private-until-shared`: the adapter can't see that it was.

## Fetch

Read the doc by its id or link: the first tab is the main page and each further tab a subpage, in the doc's tab order, each with its body. A doc the connector refuses with an access error, where absence and no access look the same, is `unauthorized`.

## Capability matrix

- **`--draft`** — *unsupported*: a doc has no draft or unlisted state, and every doc is private to its owner until shared. Report `unsupported-content` ([failure-taxonomy](../rules/failure-taxonomy.md)); the caller decides whether a private doc is draft enough.
- **`--version`** — *supported*: birth a new doc titled `<title> v<n>`, where `<n>` is one greater than the highest version the caller records for this identity (`v1` if none). The prior doc stays as it is; the doc's own version history is the connector's, and this adapter doesn't rely on it.
- **`--idempotent`** — *supported* only with the doc's id passed as `--to` (below). Update the doc in place: rewrite each tab's body to the page's new content, add tabs for new pages, and remove the tabs of pages the tree no longer has, so the doc matches the published tree.

## Retire

Delete the whole doc with the connector's doc-level delete, by the doc's id. It is owner-only (Failure surface), and no connector operation shows a doc's owner, so whether the user may delete it shows only in the delete's answer. Never retire tab by tab: a doc keeps at least one tab, so deleting its last is refused (`last_tab`), and emptying the tab instead leaves a blank doc at the same link. What retiring leaves behind: nothing at the link, which stops opening the doc for everyone.

## Identity key

The **doc id is the durable id**: the trailing id in the doc's link. Return it on every first publish, so the caller records it and passes it back as `--to` on every later publish of the same artifact, where it is the identity (level 1 of the skill's identity precedence). The connector has no lookup by name, so a doc can't be found from its title: an `--idempotent` publish whose `--to` names no doc fails `conflict` rather than birthing a duplicate, and never guesses an id.

## Failure surface

Map connector outcomes to the capability outcomes in [failure-taxonomy](../rules/failure-taxonomy.md). A refused call names a `code`, and nothing changed:

- **The connector isn't connected, isn't authorized, or is rate-limited or failing transiently** → `unavailable`, the retryable class.
- **A doc id the connector refuses with `access`**, where absence and no access look the same → `unauthorized`; never guess absence into a not-found.
- **No doc id as `--to` under `--idempotent`, or a guard mismatch during an in-place update** (someone edited the doc since it was read) → `conflict`. The edit someone else made wins: re-read and report it, and never resend with `force`.
- **A doc-level delete the connector refuses because the user doesn't own the doc** → `unauthorized`. Nothing is removed; the result names the doc so its owner can delete it.
- **A block the connector refuses even degraded, or `--draft`** → `unsupported-content`.

## Call-time discovery

The connector's surface shifts, so this file names each operation and its purpose, and the exact call shapes are resolved when you call. Before the first docs call of a run, read the connector's own guide (`guide` with `topic.index`). Before adding tabs, read `topic.tabs`, and before rewriting or removing content in place, read `topic.editing`. Resolve the doc-level delete's shape against the live operation before retiring. Each topic prints the member and op shapes this adapter relies on.
