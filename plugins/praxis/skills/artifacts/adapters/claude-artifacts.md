# claude-artifacts — artifacts adapter

Implements the **artifacts** capability against Claude's published artifacts: HTML pages hosted on claude.ai, written with the harness's Artifact tool and read back with it and its ArtifactComments tool (Call-time discovery). The [artifacts](../SKILL.md) skill resolves and maps the tree and dispatches here. The transport is `harness`, a tool the harness provides with the user's own claude.ai access, so the adapter takes no `secret_ref`.

An artifact lives in its owner's gallery, not under a parent, so this adapter takes no destination, and artifacts skips the lookup for it. A destination or `--dest-dir` resolved anyway is reported as an ignored-destination advisory. The one target `--to` names is an existing artifact, by its link: its identity (below).

## Publish

1. **Under `--idempotent`, read the artifact first** (its pages and file list), then **build the site in a working folder**, `artifacts/<slug>/` under the session's scratchpad. The slug is the tree's title, normalized as the local adapter normalizes titles ([local](local.md)). Under `--dry-run` nothing is built.
   - The main page is `index.html`.
   - **A page keeps the path it already has**, so its comments stay on it. That is the location it was handed with, or else the path of the published page with its title. The navigation gives the order, not the path.
   - A reader tab is `pages/<instrument>.html`, named by its instrument in [reader-tabs](../../document/rules/reader-tabs.md); any other `now` or `plan` page is `pages/<slug>.html`, and a `records` page `records/<slug>.html`, the slug from its label, with `-2`, `-3` added for a repeat. A page with no `part` is a `plan` page. The renderer links tabs to each other by these names.
2. **Render the site with the shipped renderer, never by hand.** Write the tree as `site.json` in the working folder, in the shape below, and the store's resolved views by running [resolve_views.py](../scripts/resolve_views.py) on the store, then run [render_site.py](../scripts/render_site.py) on `site.json`, the resolved views and the store; it draws each reader tab from the document skill's [tab design](../../document/rules/tab-design.md), holding no copy of its own. A page it refuses is the caller's defect, fixed in the tree. Then run [check_site.py](../scripts/check_site.py) on the written site and the store, which holds it to what [design-reader-instruments](../../../craft/writing/design-reader-instruments.md) can compute. Then run [check_render.py](../scripts/check_render.py) on the written site, with `--shots` into a folder beside it, which loads every page in a headless browser and reports how it draws; with no browser it says the rendering went unchecked, and the publish says so too. A `link` or `read-back` finding is fixed in the tree before publishing, and so is an `unplaced` one, by heading the section as its type file's Sections list heads it, verbatim, and an `unlinked` one, by adding the id to `refs` or `ref_patterns`, by marking it `(no link)` right after the id when it has no address, or, when it names no source, as a standard such as `SHA-256` does, by writing it as code; and an `untitled` one by giving its `refs` entry a title. A `code reused`, `dangling code` or `same fact twice` finding is fixed in the store before publishing: a reused code renamed; a dangling code's step filed when the result carries it, else the citation removed and the step shown as missing; the two items linked, the one that settles them naming the other, such as a decision that `answers` the question, and made one only when both are the same kind on the same subject. A `leak`, `empty` or `anchor` finding, and every finding of check_render, is the renderer's, reported to the developer with the publish, which goes ahead with them listed. The check sees ids only, and not a source's ids that share this store's prefixes, which stay named with their source ([mine-the-sources](../../../craft/evidence/mine-the-sources.md)); a document or thread named in words is linked in the prose itself. An `unshown items` finding and a `headlines` finding only the renderer can fix: each is reported to the developer with the publish, which goes ahead with them listed.

   `site.json` holds `title`; `home`, the short name the navigation shows; `foot`, one line under every page; `refs`, each source the pages name by an id, as written, mapped to `{"url", "title"}`: its address and what it is ([shape-the-document](../../document/phases/02-shape-the-document.md)), `url` left out when a pattern gives it or there is none, `title` `null` when it isn't recorded, shown on hover and in each page's Sources key so the prose doesn't repeat it, and an id naming two sources keyed on the phrase that tells them apart; `ref_patterns`, `{"match", "url"}` pairs giving the address of a family of ids, such as a review request's number, the URL taking the match's groups as `{1}`…; and `pages`, in tree order, each holding its `path` (step 1's), `label`, `part`, `kicker`, `headline`, `badge`, `meta` (the as-of line), `lead` (or `{"auto": "status"}` to have the main page's lead computed), `sections` and `checks`. A section is a `heading` and `blocks`, each one of `{"p"}`, `{"ul"}`, `{"callout"}`, `{"tiles"}`, `{"table"}`, `{"code"}`, `{"quote"}`, `{"figure"}` (a drawn diagram: caption, SVG, its lines), `{"image"}` (src as published, from the artifact's root; alt; caption; provenance), `{"h"}` (a sub-heading inside a section), `{"view": {"page", "position"}}`, the key the port writes for that view on this page (the page's title, `null` for the main page, and its position among the views kept on it), or `{"instrument": <the tab's instrument>}`. A check is `{"state", "text"}`.
3. **Draw diagrams** as the content support surface below says, and hand each to the renderer as a `figure` block.
4. **Publish in one call.** `index.html` is the page and every other file the renderer wrote goes through `files`: the pages, images, and `items.json` last. Every publish sets the artifact's title to the tree's title, with its version suffix under `--version`. A first publish also sets `icon` to `document`. Under `--idempotent`, publish to the artifact's link and pass `null` for each file the tree no longer has. A `--to` link without `--idempotent` or `--version` is `conflict`, as for any existing target.
5. **Return the artifact's link**, and each page's path in tree order, with the written site's folder and the screenshots folder, the pages and screenshots a reader sweep reads.

**Content support surface.** The renderer writes headings, prose, lists, tables, code, quotes and links, an in-tree reference as a relative link to its page's file with `#<id>` for a section. This adapter supplies two block kinds itself:
- **diagram:** a `figure` block with the caption, the drawing and the `Marks:`, `Elided:` and `Source:` lines. The drawing is an inline SVG with `role="img"`, a `<title>` (the caption) and a `<desc>` (the finding), following the block's form:
  - groups as containers labelled with their kind;
  - nodes shaped by kind: decision a diamond, store a cylinder, start and end rounded, external a double border;
  - edges as one-way arrows labelled with their verb;
  - a key naming each shape and mark the drawing uses;
  - a sequence as lifelines with messages, replies dashed;
  - a data model as entity boxes with their fields, relations labelled with each end's cardinality in words;
  - a timeline on a date axis, spans as bars, milestones as diamonds.

  Never mermaid, which renders reliably only on an artifact's main page. Marks take the accent for added, a warning tone for changed, and dashed and quiet for removed, each also written as a word on the element.

  After drawing, check the geometry from the coordinates written, counting a label as 0.6 times its font size per character wide and 1.2 times it high:
  - no edge crosses a node it doesn't join;
  - no two labels overlap;
  - nothing runs outside the canvas.

  Correct it at most twice, changing layout only, then keep it and note what still reads poorly as an advisory.
- **image:** an `image` block with the file published at `assets/<page path without .html>/<file>`, its alt text, its caption and its provenance. An idempotent publish passes `null` for images no page shows.

A chart is not on it: it degrades to its figures table, by [degrade-unsupported-content](../rules/degrade-unsupported-content.md), as any other kind not on it does.

**Reach.** Every artifact starts private, so every publish is `private-until-shared`. The share line: the owner opens the artifact and shares it from its share control, with the people named.

## Item store

The store is `items.json` beside `index.html`, formatted as the local adapter formats it.

## View surface

| Presentation | Level |
|---|---|
| `table`, `list`, `cards`, `matrix`, `timeline` | `interactive`, as the renderer draws it: rows filterable and sortable where there are many, the static table form readable with scripts off, and kept under a native drawing as `Table form, for reading or printing` |
| `graph`, `chain` | `native`: the port's diagram block, drawn as a diagram is above |

Each view's region is a `<section data-view="<page> <position>">`, and each row a `data-item` with its item's id, which Feedback reads.

## Restricted

The artifact's sharing can't be read, so `--restricted` is honored only when this publish creates the artifact. The share line then names the people the caller gave. A publish into an existing artifact answers `unsupported-content`, and a restricted document is renewed with `--version`.

## Feedback

- **Comments:** each thread, with the port's fields, read with ArtifactComments. Its page is the path the thread is on. Its block is the nearest element, the thread's own or an ancestor, that renders a neutral block: a heading, paragraph, list, table, code, quote or figure. Its `item` is the `data-item` of the nearest ancestor carrying one, or none. A thread on no element has the anchor `page`.
- **Approvals:** not read. An artifact has no approval record.

## Fetch

Read the artifact by its link, then each page by path. Every page carries its own entry of the site tree in `<script type="application/json" id="praxis-page">`, which the renderer writes: that entry comes back as the page, its head, sections and blocks as written, diagrams and images included, in the order the main page's entry lists the pages. The tree's title is the artifact's, without a trailing ` v<n>`. A view block comes back as the store's `views` entry its `view` names, and an instrument as the instrument it names. `items.json` comes back as the item store and is never content.

## Share

The Artifact tool has no sharing operation: answer `unsupported-content` with the share line above, naming the people to add.

## Capability matrix

- **`--draft`**: *unsupported*. An artifact has no draft state: report `unsupported-content`.
- **`--version`**: *supported*. Publish a new artifact titled `<title> v<n>`, where `<n>` is one greater than the highest `<title> v<k>` among the owner's artifacts (`list`), or `v1` if none. The prior artifact stays.
- **`--idempotent`**: *supported* only with the artifact's link passed as `--to`, read in this session first as the tool requires. Without one, the identity can't be resolved: `conflict`.

## Retire

Delete the artifact by its link. The caller's consent is the confirmation, and the tool may also ask the person itself. Retiring leaves nothing at the link: it stops opening for everyone. A surface with no delete makes the retire `unsupported-content`: the owner deletes it by hand from the gallery.

## Identity key

A tree with no link is a new artifact. There is no title-based fallback, since a gallery can hold several artifacts with one title.

## Failure surface

- **The Artifact tool isn't available in this session**, or the claude.ai connection isn't signed in → `unavailable`.
- **A read or publish refused for access** → `unauthorized`. A read that doesn't say the person can edit (`writer`) is `unauthorized` for a publish, and is still read for a fetch.
- **A link that opens nothing** → `target-not-found`.
- **A publish refused because a newer version was saved since this session read it** → `conflict`. The caller re-reads and republishes; it never forces.
- **A page or file over the size limit, or a script source the page contract refuses** → `unsupported-content`.
- **A publish that landed some files and not others** → `partial`, naming what landed, `items.json` included.

## Call-time discovery

The tools' actions and limits change, so resolve them when you call:
- read the Artifact tool's description for its publish, read and delete shapes, the `files` map and the size limits;
- read the harness's design guidance for artifacts before writing the first page;
- read the ArtifactComments tool's shape before reading feedback.
