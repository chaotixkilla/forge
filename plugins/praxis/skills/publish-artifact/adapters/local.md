# local — artifacts adapter

Implements the **artifacts** capability against the local filesystem, writing the page tree as Markdown files under the destination the skill resolved (SKILL step 1 — the type's key entry, `destinations.default`, or a user-supplied target; the adapter does not key off the raw type itself). The [publish-artifact](../SKILL.md) skill resolves and maps the tree and dispatches here; this adapter owns the concrete file layout, filename derivation, and error mapping.

## Publish

1. Ensure the destination directory exists (create it and any missing parents).
2. Write the main page as `index.md` at the destination root; write each subpage as `NN-<slug>.md` alongside it, where `NN` is a two-digit position in tree order (`01`, `02`, …) and `<slug>` is the normalized title (below).
3. Render each page's neutral sections to Markdown (the block kinds below); link the index to its subpages with relative paths.
4. Return the directory and the written file paths, main page first.

**Content support surface.** This adapter renders these neutral block kinds natively: heading, prose, list, table (Markdown table), code (fenced), quote (blockquote), link/reference. This list is the authoritative content-support surface the degradation ladder ([degrade-unsupported-content](../rules/degrade-unsupported-content.md)) keys off; a kind not on it degrades. In practice Markdown covers nearly all neutral kinds, so degradation is rare (a rich interactive embed → a link + caption).

## Filename normalization

Deterministic so the resolved path is a stable identity across cold runs: the `<slug>` is the title lowercased, ASCII-folded (transliterate accented/non-ASCII letters to their nearest ASCII form — `é`→`e`, `ü`→`u` — and drop any character with no ASCII fold), then every run of characters outside `[a-z0-9]` collapsed to a single hyphen and leading/trailing hyphens trimmed (e.g. `"API Design (v2)"` → `api-design-v2`; `"Café Menu"` → `cafe-menu`). The main page is always `index.md`; subpages are always `NN-<slug>.md` in tree order. Two executors publishing the same tree write the same filenames.

## Capability matrix

What this backend can honor for the write-mode flags — the skill reads this to decide whether a flag applies or must degrade:

- **`--draft`** — *supported* via location: write the tree under a `drafts/` subdirectory of the destination, keeping it out of the published set until promoted. (A directory, not a per-file state — `drafts/` is the pinned placement, not a `.draft` suffix.)
- **`--version`** — *supported*: write the tree into a `v<n>/` subdirectory alongside prior versions, where `<n>` is one greater than the highest existing `v<k>/` at the resolved identity (`v1` if none). Reproducible and monotonic — no clock dependence.
- **`--idempotent`** — *supported*: the resolved destination directory path is the identity (below); re-publishing to the same path overwrites its files in place.

## Identity key

The **resolved destination directory path is the durable id** — the tree at a path is the same artifact across runs as long as it stays at that path (level 2 of the skill's identity precedence; the `<slug>` normalization above is the level-3 fallback). On `--idempotent` republish, rewrite the files at the resolved path; for a subpage present last run but absent now, delete its stale `NN-<slug>.md` so the on-disk tree matches the published tree. A rename/move of the destination is a new identity — an explicit `--to` path pins identity, otherwise a moved artifact resolves to its new path.

## Failure surface

Map filesystem errors to the capability outcomes in [failure-taxonomy](../rules/failure-taxonomy.md) — the caller hears an outcome, never an errno. The boundary between the first two is *storage reachability* vs *a named target's existence*:

- **The storage itself is unusable** — destination root not configured, the volume is not mounted, or the filesystem is read-only/offline → `unavailable` (retryable). This is infrastructure, not a missing directory: a missing destination directory is *created* (Publish step 1), not an error.
- **Write permission denied** on a reachable path → `unauthorized`.
- **An explicit `--to` target names a location that does not exist** (the caller pointed at a specific existing file/dir that is absent) → `target-not-found`. (A missing `--dest-dir` path is created, so it is not this case.)
- **An existing tree at the target with no `--idempotent`/`--version`**, or an `--idempotent` slug matching several candidates → `conflict`.
- **A neutral block no Markdown form can express even degraded** (rare — see the content support surface) → `unsupported-content`; degrade first per [degrade-unsupported-content](../rules/degrade-unsupported-content.md).
