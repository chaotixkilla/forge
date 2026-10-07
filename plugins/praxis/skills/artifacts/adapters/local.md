# local — artifacts adapter

Implements the **artifacts** capability against the local filesystem, writing the page tree as Markdown files under the destination the skill resolved (SKILL step 1). The [artifacts](../SKILL.md) skill resolves and maps the tree and dispatches here.

## Publish

1. Ensure the destination directory exists (create it and any missing parents).
2. Write the main page as `index.md` at the destination root; write each subpage as `NN-<slug>.md` alongside it, where `NN` is a two-digit position in tree order (`01`, `02`, …) and `<slug>` is the normalized title (below). Each file opens with its page's title as its first heading.
3. Render each page's neutral sections to Markdown (the block kinds below).
4. Return the directory and the written file paths, main page first, with reach `local-only`.

**Content support surface.** This adapter renders these neutral block kinds natively: heading, prose, list, table (Markdown table), code (fenced), quote (blockquote), link/reference (an in-tree reference is its words as the text of a relative link to its page's file, with `#<anchor>` for a section; the anchor is the heading lowercased, with characters other than letters, digits, spaces and hyphens dropped and spaces turned to hyphens, as common Markdown hosts build it, and `-1`, `-2` added for a repeated heading), and diagram (a fenced `mermaid` block, which common Markdown hosts draw, with its caption above and its elision line below). A chart isn't on it. A kind not on it degrades by [degrade-unsupported-content](../rules/degrade-unsupported-content.md).

## Fetch

Read `index.md` at the location and each `NN-<slug>.md` beside it, in `NN` order, as the main page and its subpages. Each file's first heading is its page's title; a file that doesn't open with a level-1 heading, written before titles were, takes its title from its footer's type and the round the footer names (round 1 where it names none), or with no footer from its file name's slug, adding its `NN` where two would still repeat, and keeps every heading in its body. Fetch inverts the surface: a relative link to one of those files comes back as an in-tree reference to its page with the link's text as its words, its `#<anchor>` matched against that page's headings as the section, and a fenced `mermaid` block as a diagram, with a caption only when a one-line caption sits directly above it. A chart shown as its figures table comes back as that table, since the table doesn't say it was a chart. A location with no `index.md` is `target-not-found`.

## Retire

A location with no `index.md` is `target-not-found`. Otherwise remove the tree at it: its `index.md` and `NN-<slug>.md` files, then the directory, now empty. When the directory holds anything else (a `v<n>/` or `drafts/` subdirectory, a file this adapter didn't write), remove nothing and fail `conflict`, naming those entries, since the directory can't go without them. `(basis: derived from the conflict class: the write can't proceed as asked without loss)` A versioned copy is retired by its own location first. What retiring leaves behind: nothing on disk. Where the files were committed, the repository's history keeps them, and the removal is a working-tree change for the caller's next commit.

## Filename normalization

Deterministic so the resolved path is a stable identity across cold runs: the `<slug>` is the title lowercased, ASCII-folded (transliterate accented/non-ASCII letters to their nearest ASCII form — `é`→`e`, `ü`→`u` — and drop any character with no ASCII fold), then every run of characters outside `[a-z0-9]` collapsed to a single hyphen and leading/trailing hyphens trimmed (e.g. `"API Design (v2)"` → `api-design-v2`; `"Café Menu"` → `cafe-menu`). The main page is always `index.md`; subpages are always `NN-<slug>.md` in tree order.

## Capability matrix

What this backend can honor for the write-mode flags — the skill reads this to decide whether a flag applies or must degrade:

- **`--draft`** — *supported* via location: write the tree under a `drafts/` subdirectory of the destination, keeping it out of the published set until promoted. (A directory, not a per-file state — `drafts/` is the pinned placement, not a `.draft` suffix.)
- **`--version`** — *supported*: write the tree into a `v<n>/` subdirectory alongside prior versions, where `<n>` is one greater than the highest existing `v<k>/` at the resolved identity (`v1` if none). Reproducible and monotonic — no clock dependence.
- **`--idempotent`** — *supported*: the resolved destination directory path is the identity (below); re-publishing to the same path overwrites its files in place. A page's file isn't its identity here: each page is written at the `NN-<slug>.md` its position and title now give, and a location handed with a page only names its earlier file, which is removed when the name differs.

## Identity key

The **resolved destination directory path is the durable id** — the tree at a path is the same artifact across runs as long as it stays at that path (level 2 of the skill's identity precedence; the `<slug>` normalization above is the level-3 fallback). On `--idempotent` republish, rewrite the files at the resolved path; for a subpage present last run but absent now, delete its stale `NN-<slug>.md` so the on-disk tree matches the published tree. A rename/move of the destination is a new identity — an explicit `--to` path pins identity, otherwise a moved artifact resolves to its new path.

## Failure surface

Map filesystem errors to the capability outcomes in [failure-taxonomy](../rules/failure-taxonomy.md). The boundary between the first two is *storage reachability* vs *a named target's existence*:

- **The storage itself is unusable** — destination root not configured, the volume is not mounted, or the filesystem is read-only/offline → `unavailable` (retryable). This is infrastructure, not a missing directory: a missing destination directory is *created* (Publish step 1), not an error.
- **Write permission denied** on a reachable path, a removal's included → `unauthorized`; a retire that stops after removing some files → `partial`, naming the files removed.
- **An explicit `--to` target names a location that does not exist** (the caller pointed at a specific existing file/dir that is absent) → `target-not-found`. (A missing `--dest-dir` path is created, so it is not this case.)
- **An existing tree at the target with no `--idempotent`/`--version`**, or an `--idempotent` slug matching several candidates → `conflict`.
- **A neutral block no Markdown form can express even degraded** (rare — see the content support surface) → `unsupported-content`; degrade first per [degrade-unsupported-content](../rules/degrade-unsupported-content.md).
