# claude-docs — artifacts adapter

Implements the **artifacts** capability against Claude Docs, over the Claude Docs connector (a claude.ai connector, so it exists only where the user has it connected). The [artifacts](../SKILL.md) skill resolves and maps the tree and dispatches here. A doc holds tabs and each tab holds one prose body, so the portable tree maps onto one doc, with one tab per page. The connector authenticates through the user's own claude.ai connection, so the adapter needs no `secret_ref`; its transport is `mcp`. Docs live in the owner's artifact list, not under a parent, so this adapter takes no destination and artifacts skips the lookup for it. A destination resolved anyway (a configured `destination`, a path, a parent page) has nowhere to apply: report it as an ignored-destination advisory with the result rather than failing. The one target `--to` names here is an existing doc, by its id or link, and that is the doc's identity (below).

## Publish

1. **Birth the doc** with one `batch` call whose `container.create` carries the doc's name (the tree's title) and the main page as the first tab, named with the main page's title. The same batch adds each subpage as a further tab, in tree order, and writes every page's body, rendered by the content support surface below, so a mention of a tab this publish creates uses the batch's own id for it. Tabs on a doc are members the call spells, plus one member that names and orders them. A publish isn't watched, so the whole tree goes in the birth; when the caller says the user is watching the doc fill, follow the connector's outline-then-fill guidance instead, creating the tabs before the bodies that mention them.
2. **Return the doc's link**, with each tab's name and id in tree order. The birth's acknowledgement carries the link in its trailer and the ids the batch minted. Opening the doc on the user's screen is the caller's decision, not this adapter's.

**Content support surface.** This adapter renders these neutral block kinds natively: heading, prose, list, table (pipe table), code (fenced), quote (a `>` block), link/reference, diagram and chart. A kind not on it, or a block the connector refuses, degrades by [degrade-unsupported-content](../rules/degrade-unsupported-content.md).

- **An in-tree reference** to a page is its words as text, then a mention of that page's tab; the mention alone when the words are the page's title. A tab that already exists is mentioned by its id. A reference to a section in the same tab links its words to that heading. One to a section of another tab is its words, the tab's mention, then `›` and the heading's words, since the connector links headings only within a tab.
- **A diagram** is a fenced `mermaid` block, which the doc's viewer draws, with its caption above and its elision line below.
- **A chart** is the connector's chart widget, built from the block's rows with one series per series, embedded where the block sits. Its x-axis title carries the x axis's label and unit, its y-axis title the unit the series share, and its legend the series' labels; its kind follows the connector's chart guidance, and the embed's caption carries the claim and the number of observations. No table repeats the plotted figures.

**Reach.** Every doc is `private-until-shared`. Its share line: the owner opens **Share** at the top of the doc and adds people by name, to view, comment or edit. No connector operation shares a doc or shows who has access, so a doc shared after an earlier publish still reports `private-until-shared`: the adapter can't see that it was.

## Fetch

Read the doc by its id or link: the first tab is the main page and each further tab a subpage, in the doc's tab order, each with its body and its tab id as its location. Fetch inverts the surface. Words followed by a mention of another tab of the doc come back as an in-tree reference to that tab's page with those words, a bare mention with the page's title as its words, and a mention followed by `›` and words as a reference to the section those words begin with, the longest of that page's headings they start with. A link to a heading in the same tab comes back as a reference to that section. A `mermaid` block comes back as a diagram, with a caption only when a one-line caption sits directly above it. A chart widget comes back as a chart block: its claim and number of observations from the embed's caption, the x axis's label and unit and the series' unit from the axis titles, the series' labels from the legend, its rows from the widget's data. A chart or diagram the connector refused and that was shown degraded comes back as the table or the code it was shown as. A doc the connector refuses with an access error, where absence and no access look the same, is `unauthorized`.

## Capability matrix

- **`--draft`** — *unsupported*: a doc has no draft or unlisted state, and every doc is private to its owner until shared. Report `unsupported-content` ([failure-taxonomy](../rules/failure-taxonomy.md)); the caller decides whether a private doc is draft enough.
- **`--version`** — *supported*: birth a new doc titled `<title> v<n>`, where `<n>` is one greater than the highest version the caller records for this identity (`v1` if none). The prior doc stays as it is; the doc's own version history is the connector's, and this adapter doesn't rely on it.
- **`--idempotent`** — *supported* only with the doc's id passed as `--to` (below). Update the doc in place, so it matches the published tree. The main page matches the first tab. Each subpage matches the tab at the location it was handed with, or else the tab of its name. A matched tab is renamed when its page's title changed. A page is changed when its neutral content differs from the tab as Fetch reads it back, a reference counting as changed when it now resolves to a different tab. A changed tab is updated block by block. The tab's blocks and the page's are paired in order between the blocks that are unchanged, and a pair of the same kind is edited with the smallest edit the connector offers, so words that didn't change stay in place with the comments on them. A block left unpaired is inserted or deleted. A whole-tab rewrite re-creates every block and detaches the comments on them, so unchanged blocks are left as they stand. New pages get new tabs, written in the batch that creates them, and the tabs of pages the tree no longer has are removed. `(basis: derived — readers' comments hang on blocks, and a rewrite detaches them)`

## Retire

Delete the whole doc with the connector's doc-level delete, by the doc's id. It is owner-only (Failure surface), and no connector operation shows a doc's owner, so whether the user may delete it shows only in the delete's answer. Never retire tab by tab: a doc keeps at least one tab, so deleting its last is refused (`last_tab`), and emptying the tab instead leaves a blank doc at the same link. What retiring leaves behind: nothing at the link, which stops opening the doc for everyone.

## Identity key

The **doc id is the durable id**: the trailing id in the doc's link. Return it on every first publish, so the caller records it and passes it back as `--to` on every later publish of the same artifact, where it is the identity (level 1 of the skill's identity precedence). The connector has no lookup by name, so a doc can't be found from its title: an `--idempotent` publish whose `--to` names no doc fails `conflict` rather than birthing a duplicate, and never guesses an id.

## Failure surface

Map connector outcomes to the capability outcomes in [failure-taxonomy](../rules/failure-taxonomy.md). A refused call names a `code`, and nothing changed:

- **The connector isn't connected, isn't authorized, or is rate-limited or failing transiently** → `unavailable`, the retryable class.
- **A doc id the connector refuses with `access`**, where absence and no access look the same → `unauthorized`; never guess absence into a not-found.
- **No doc id as `--to` under `--idempotent`, or a guard mismatch during an in-place update** (someone edited the doc since it was read) → `conflict`. The edit someone else made wins: re-read and report it, and never resend with `force`.
- **An in-place change the connector refuses because it would remove words a comment hangs on** → the update is sent again without that tab's changes, again for each tab refused this way, and what then lands is the result: `partial`, naming the tab and the commented words. That tab stays as it was until a reader resolves the comment, which the caller tells the user. Nothing is forced. `(basis: maintainer, 2026-10-07, since refusing the whole update would hold every later filing on one comment)`
- **A doc-level delete the connector refuses because the user doesn't own the doc** → `unauthorized`. Nothing is removed; the result names the doc so its owner can delete it.
- **A block the connector refuses even degraded, or `--draft`** → `unsupported-content`.

## Call-time discovery

The connector's surface shifts, so this file names each operation and its purpose, and the exact call shapes are resolved when you call. Before the first docs call of a run, read the connector's own guide (`guide` with `topic.index`). Before adding, renaming or mentioning tabs, read `topic.tabs`. Before placing a chart, read `topic.charts`. Before changing content in place or linking a heading, read `topic.editing`. Resolve the doc-level delete's shape against the live operation before retiring. Each topic prints the member and op shapes this adapter relies on.
