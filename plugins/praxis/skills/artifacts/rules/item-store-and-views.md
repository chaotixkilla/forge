# The item store and views

A caller that holds its content as items ([items-and-agreements](../../document/rules/items-and-agreements.md)) hands the port an item store and a live-state file beside the page tree. Its pages carry view blocks ([portable-tree-shape](../../document/rules/portable-tree-shape.md)), which the port resolves against both.

## The payload

- **Optional.** A tree handed with no item store publishes as it always has.
- **The item store** is one JSON document holding:
  - `kinds`: per item kind, its prefix, its fields and the live fields views may join, each with its type (`text`, `number`, `date`, `period`, `when`, `id`, `list of <type>`, or `enum`, written `{"enum": [values]}` in declared order), as the caller's types declare them. Every kind also has the fields every item carries: id, title, owner, state, decide-by, sensitivity, last reviewed and next review;
  - `items`;
  - `agreements`;
  - `dismissed`: the ids of feedback the developer already confirmed or dropped, never proposed again;
  - `restricted`: the store's first key, `true` when it was published with `--restricted` and `false` otherwise, set by the port;
  - `views`: each view block of the tree, keyed by its page (`null` for the main page, else the page's title) and its position among that page's view blocks, counting from 1. The port writes `views` from the tree's view blocks at each publish, replacing what was handed, so the two never disagree.

    A view is written in this JSON shape, which is the only one the port reads:
    - `caption`; `of`, a list of kinds by their `kind`, never a prefix; `as`, the presentation;
    - `where`: conditions, each `{"field": <key>, "is"|"in"|"not-in": <value or values>}` (a key is a field, a live field, `state` or `sensitivity`) or `{"link": <link or reverse>, "to"|"not-to": <id, kind or "none">}`;
    - `columns`, for a table, list or cards, each one of `{"field": <key>}`, `{"live": <key>}`, `{"body": true}`, `{"state": true}`, `{"link": <link or reverse, or a list of two>, "show": <key>, "kinds": [<kind>]}`, `{"agreement": "decider"|"consulted"|"informed"|"date"|"link"}` or `{"verification": "outcome"|"when"|"environment"|"commit"|"link"}`, each optionally with a `label` and an `empty` marker;
    - for a matrix, `rows` and `cols` (kinds), `cell` (a link or a list of two) and `empty`; for a graph, `edges` (links); for a chain, `start` (an id) and `follow` (a link or a list); for a timeline, `start_field`, `end_field` and any `columns`;
    - `sort`: keys in order, each `{"by": <key>, "desc": true|false, "empty": "first"|"last"}`; `group`: `{"field": <key>}` or `{"link": <link>}`.

    A type file's Views line maps onto this shape: its kinds by their `kind`, both of a matrix's included; its fields by their keys exactly as the kind declares them, spaces kept; id and title never as columns, since every form starts with them; anything a timeline also shows, as its `columns`.

    A filter using `page subject` takes the view block's `subject`, which the entry carries beside `page` and `position`; without one the view is rejected.

    An item's reason for its state, which `deferred` and `withdrawn` carry, is its `why`.

  Every published document has one store, bound to its main page's location.
  - `--idempotent` replaces it.
  - `--version` gives the new copy a store of its own.

  Its shape, with keys in snake case and the fields every item carries implied rather than listed in `kinds`. Views name those fields by their keys (`id`, `title`, `owner`, `state`, `decide_by`, `sensitivity`, `review.last`, `review.next`), and name kinds by their `kind`, not their prefix. A `number` is a JSON number and a `date` an ISO 8601 string. A missing owner, decider or field is JSON `null`, and an owner or decider is one name. A value that doesn't match its declared type is rejected up front, naming the item and field.

  ```json
  {"restricted": false, "kinds": {"REQ": {"kind": "requirement", "fields": {"keyword": "text", "priority": "number"}, "live": {"coverage": "number"}}},
   "items": [{"id": "REQ-1", "kind": "requirement", "title": "…", "body": [], "fields": {"keyword": "MUST"},
              "links": [{"link": "serves", "to": "GOAL-1"}], "evidence": [{"link": "…", "what": "…"}, {"who": ["…"], "when": "2026-11-12", "what": "…"}], "owner": "…",
              "state": "proposed", "first_state": "proposed", "first_filed": "2026-11-12", "decide_by": "GATE-2", "sensitivity": "team",
              "review": {"last": null, "next": "GATE-2", "notes": [{"date": "2026-11-12", "what": "…"}]}}],
   "agreements": [{"id": "AGR-1", "settled": [{"id": "REQ-1", "content": {}}, {"id": "REQ-2", "content": {"withdrawn": "…"}}], "decider": "…",
                   "consulted": [], "informed": [], "date": "2026-11-12", "link": "…"}],
   "views": [{"page": null, "position": 1, "view": {}}]}
  ```

  It lives wherever the adapter's **Item store** section says. It is written after the pages, even when they stopped partway, and a `partial` publish names it among what didn't land when it didn't. (basis: maintainer, 2026-11-11, the store lives on the backend)
- **The live-state file**, `{"observed": "2026-11-12T09:40:00+00:00", "items": {"REQ-1": {"coverage": 80}}}`, holds the time it was observed (ISO 8601, with its offset) and, per item id, the observed value of each live field. It is never published on its own; its values reach the backend only inside the rendered views. It feeds the views that join it, and through them their rendered data. It is never fetched back or read as an input to the next filing. (basis: derived — a generator never reads its own output)

## Up-front rejections

Each is the caller's defect, rejected before anything is written. Each names what it rejects ([failure-taxonomy](failure-taxonomy.md)):

- a view block with no item store;
- a view naming a kind, field or live field the store's `kinds` doesn't declare, or a link that is neither a link kind nor a reverse in [items-and-agreements](../../document/rules/items-and-agreements.md)'s table;
- a chain whose starting item isn't in the store;
- a filter on the state or the sensitivity with a value outside that field's set;
- without `--restricted`, a store marked `restricted: true`, a store holding an item marked `sensitivity: restricted`, or an agreement carrying agreed content for an id the store doesn't hold. An agreement may name such an id, but without its content.

The port checks only the store. Item content written into page bodies is the caller's to check before it hands the tree over. The port never filters restricted items itself, because filtering is authoring: a page would silently say less than its caller wrote. The caller publishes restricted items separately, with their own store, as [items-and-agreements](../../document/rules/items-and-agreements.md) says. (basis: maintainer, 2026-11-11, after a documentation site published an unreleased exploit path)

**`--restricted`** asks the adapter to restrict access to the publish, as its **Restricted** section says, so that only the publisher and the people the caller names can open it. Its reach must come back `private-until-shared` or `local-only`. A document published with `--restricted` is republished only with it. Before an `--idempotent` publish without the flag, the port reads the existing document's store mark through the adapter, and a store marked `restricted: true` is rejected, whatever the handed store says. Such a document is shared only with named people, never the organization. An adapter whose backend can't be shown to restrict access to the destination answers `unsupported-content` before writing. That refusal, like the no-store refusal below, is read from the adapter's declared sections in step 3, so `--dry-run` reports it.

## Resolving a view

In step 3, by running [resolve_views.py](../scripts/resolve_views.py) on the store and the live-state file. It makes the up-front rejections above for every view, then steps 1 to 4 below, and hands back each view's rows. Rows are never resolved by hand. A rejected view is fixed in its view block before publishing.

1. **Select** the store's items of the view's kinds that meet every condition of its filter. A condition is one of:
   - a field, the state or the sensitivity, with `is`, `in` or `not-in` and its value or values. A field's value may be `page subject`: the subject the page was filed for, such as its service. An `id` or `list of id` field is matched by id. An empty value, or a field the item's kind doesn't declare, fails `is` and `in` and meets `not-in`;
   - a link kind, or its reverse, with `to` or `not-to` an id or a kind, or `to` `none`.

   `superseded` and `withdrawn` items are left out unless a condition names their state. The selected items are everything the view shows: its rows, a matrix's columns, a graph's nodes, a chain's steps. A chain's starting item is shown and walked from even when the filter would leave it out. In a graph or chain, a target outside the documentation, or an id the store doesn't hold, is drawn as a node marked as the link rules below say. In a matrix, graph or chain, a link to an item in the store but outside the selection isn't drawn. A link column in a `table`, `list` or `cards` view lists every target.
2. **Join** each item's live fields from the live-state file by its id. Fill path, agreement and verification columns from the store: a path follows each link in turn, an agreement column reads the agreement that covers the item, a state column reads the item's state and the why it carries, and a verification column reads the latest verification in its evidence.
   - A value not observed leaves its cell empty, never filled. An empty cell shows its column's empty marker when the view declares one.
   - With no live-state file, every live cell is empty, and `live state not observed` takes the place of the observation time in the caption.
3. **Sort** the rows by the view's keys. A chain keeps chain order, and a graph's edges follow their source item's place. Ids compare by prefix, then number. Numbers, dates and periods compare as values, enums by their declared position, the first-declared value counting as the greatest, so a descending sort puts it first, and other fields as text. A `when` value puts dates first, then `build start`, then gates by id, then `end of round <n>` by n, then `close-out`. A `list` field sorts and groups by its first value. Empty cells sort last, unless the key says empty first. Ties, and a view with no sort, keep the store's order.
4. **Group** by one field or one link's target, an item with several targets grouped under the first in store order (a chain isn't grouped). Groups come in the order their first item appears, and items with no value in it come last, under "(none)".
5. **Render or degrade.** Hand the rows to the adapter, which renders the presentation at the level its **View surface** declares. A rendering the backend refuses falls back to the static table form, with an advisory. A view declared at `table` carries none.

**How links are read.** A link column, matrix cell or edge names a link kind or its derived reverse, read from the row's item.
- A cell lists its targets one per line in store order, each as id and title. A matrix cell lists the targets its link or path reaches between the row and column items, as ids, or holds the view's empty marker (default: empty). A graph's edges from one item come in the link table's order, then by target in store order.
- A target outside the documentation shows as its link.
- A target id the store doesn't hold, such as one published to the restricted destination, shows as its id followed by `[not in this document]`.
- A chain follows its link, or each link of its sequence in turn, from the starting item, depth first, taking branches in store order. An item met again ends its branch, with `(repeats)` in its link column.

**Captions.** A view's caption renders as the block's caption, then, after ` — `, anything the port adds:
- `as observed <the file's time, as the file gives it>`, for a view that joins live fields;
- the count of links left out.

A view that selects no items shows its caption, with "none" in place of its rows.

**Drawings.** A `native` graph, chain or timeline is drawn from a diagram block ([portable-tree-shape](../../document/rules/portable-tree-shape.md)) the port builds from the rows, which the adapter then draws as it draws any diagram:
- **Graph or chain:**
  - form `flow`, a chain running left to right;
  - one node per item, labelled `<id> · <title>`;
  - each edge labelled with its link's name;
  - a marked target as a node of kind `external`, labelled as the link rules above say.
- **Timeline:** form `timeline`, one row per item, labelled `<id> · <title>`, spanning its start to its end. It is a milestone when the view names no end field, its end is empty, or the end equals the start. An item whose start is empty, or whose start or end is a gate or a round, can't be placed. Such items are listed under the drawing in one line, `Not placed: <id> (<why>), …`, and stay in the table.
- **Groups:** a graph's groups are drawn as group containers. A timeline's are drawn as row groups.
- Its caption is the view's rendered caption, and its elision line names what was left out. Its provenance is `generated`: the item store as published.

## The view surface: what each adapter declares

Each adapter's **View surface** may give a level for each presentation. The first test that holds decides:

1. **Is the rendering the static table form itself, with no controls?** Then the level is `table`.
2. **Can the reader filter or re-sort it without a new publish?** Then it is `interactive`. It reads the resolved rows the adapter publishes with the page, as a data file, attributes in the page, or the backend's own database. Those rows are output, never fetched back. (basis: maintainer, 2026-11-11, views over the published data; rows written into the page keep it complete at rest)
3. **Otherwise** it is `native`: rendered in the backend's own form, fixed as of the publish.

A presentation the adapter doesn't name is `table`.

**`interactive` and `native` renderings keep the static table form beside them,** placed as the reader's alternative, collapsed or after the visual, as the adapter's View surface says. A rendering that is the static table enhanced in place, readable with scripts off, already is that alternative. A picture alone fails a reader who can't see it. Once a table carries the same values, the graphics are exempt from the non-text contrast criterion. (basis: maintainer, 2026-11-11; WCAG 2.2 SC 1.4.11)

## The static table form of each presentation

Every form starts with the item's id and title. Each keeps the view's caption and observation time. A grouped view is one table per group, each under a bold line holding the group's value, never a heading.

| Presentation | Rows | Columns after id and title |
|---|---|---|
| `table`, `list`, `cards` | One per item | The view's columns, in order |
| `matrix` | One per item of the row kind, columns in store order | The row item's live fields, then one per item of the column kind, each cell as the matrix cell above |
| `graph` | One per edge | The edge's link, then the target's id and title. An item with no edge follows all the edges, in store order, as a row of its own. |
| `chain` | One per step, in chain order | The step it came from, and the link from that step |
| `timeline` | One per item | Start, then end, or "milestone" when the view names no end field, the end is empty, or it equals the start |

## Fetch and the store

A fetch returns the store of the document at the location fetched. A document with no store, such as one published before stores existed, comes back as its tree with an advisory naming the store as not found. A view's region runs from its caption to the last line of its static table, or to its "none". On publish the adapter marks each region with the view's key, or, on a backend that can carry no hidden mark, renders the region so its **View surface** can find it again by its caption. A region is found when a line's text before its first ` — `, or the whole line when it has none, equals the stored caption exactly. Each search starts after the region before it. A caption containing ` — ` is rejected up front. A fetch replaces each region it finds with the view block from the store's `views`, so a fetched tree republishes unchanged. A region the store has no entry for comes back as ordinary content, and a stored view whose region isn't found is left out of the fetched tree. Both come with an advisory naming them. (basis: derived — some backends carry no hidden marks)

**An adapter that can't hold a store answers `unsupported-content` to a publish that carries one, before writing.** The store's home is the backend, so dropping it would leave the next filing with nothing. (basis: maintainer, 2026-11-11, the store lives on the backend)

## Feedback

An adapter's **Feedback** section declares, separately, whether it reads:
- **comments:** each thread with its page, its anchor, author, time, text and whether it is resolved. The anchor is the first 80 characters of the block's plain text, whitespace collapsed, or `page` for a comment on the page itself. A separate `item` field holds the row's item id when that block is a row of a view region. `resolved` is empty where the backend doesn't say;
- **approvals:** who approved, when, and which version of which page.

Each comment thread and approval comes back with an `id`: the backend's own id for it, or, where the backend gives none, its page, anchor and time joined. A read covers every page of the tree. When the adapter declares only one of the two, the other comes back empty, marked as not read by this backend. When it declares neither, the read answers `unsupported-content`. A read cut short is `partial`. What a comment or an approval means for an item is the caller's to propose and its developer's to confirm. (basis: maintainer, 2026-11-11, read back and propose, never apply)
