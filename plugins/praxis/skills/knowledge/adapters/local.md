# local — knowledge adapter

Implements the **knowledge** capability against a local docs tree, reading text documents beneath the resolved source's `root` (SKILL step 1). The [knowledge](../SKILL.md) skill takes the caller's read and dispatches here.

**The configured root is the space, and it is not the working tree.** This adapter serves a docs tree a project *configured* as its knowledge backend. Reading a file that merely happens to sit in the repo is ambient and needs no port at all — a caller doing that reads it directly.

## The tree mapping

A filesystem has no page→subpage concept, so the mapping is pinned here rather than left to the executor:

- A **document** is a single file (`.md`, `.markdown`, `.txt`) beneath the root. Its **reference** is its path relative to the root — stable across runs and re-openable, which is what the provenance floor requires.
- A document's **children** resolve by the *directory-companion* rule: for `<name>.md`, the children are the document files directly inside a sibling directory named `<name>/`. A directory with no companion file is itself a document whose content is its `index.md` (or `README.md`) where one exists, and which is otherwise a title-only container — fetched as its title with an empty body. That index **stands for its directory**: a reference to `<dir>/index.md` and a reference to `<dir>` name the same document, and this adapter always returns it as `<dir>/index.md` (`<dir>` only for a directory with no index), so a search hit and a walk never name it two ways. A directory document's children are the documents directly inside it, in name order: its files other than the index, and its subdirectories other than a companion directory, which belongs to its file. That is the layout the artifacts port writes a page tree in — `index.md` as the main page, `NN-<slug>.md` beside it in tree order.
- Only the immediate level is a child; nesting is walked by the caller, one level per call.

`(basis: derived from round-tripping a hosted page tree through disk)`

## Search the space

1. Search file contents and filenames beneath the root, restricted to the document extensions above.
2. Return **ranked references** — the relative path, the document's title (its first heading, else its filename stem), and the matching line's context. Never return file bodies from a search.
3. Rank by match density, then by path depth, shallower first, so a top-level document outranks a deeply nested incidental mention. `(basis: derived from depth being the one prominence signal a filesystem exposes)`

## Fetch a document

1. Read the file at the reference and return its content as-is — it is already text, so there is no rendering step.
2. Provenance is **thinner here than on a hosted backend, and the gaps are declared rather than filled.** Title and reference are always available. `last-edited` is filled from the file's modification time, with the caveat that mtime records the last *write* — a checkout, a format pass, or a bulk move rewrites it without anyone editing the document — so it is a weak upper bound on staleness, not an authored date. `created` and `author` have no filesystem equivalent and are returned **not-exposed** per the port's provenance floor: never inferred from mtime, and never read out of version control, which is a different lane's evidence.

## List a document's children

Resolve the reference's children by the tree mapping above — a file's companion directory, or a directory document's own contents — and return them in name order. A document with neither has **no children — an `ok` with zero references, not a not-found.**

## Failure surface

Map filesystem conditions to the capability outcomes in [outcome-taxonomy](../rules/outcome-taxonomy.md). Three conditions look alike here and are three different answers:

- **The root itself is unusable** — not configured, absent, not a directory, or on a volume that is not mounted → `unavailable` (retryable/infrastructural). The space could not be reached at all.
- **The root is readable but a requested path inside it is permission-denied** → `unauthorized`.
- **The root is readable and the requested path simply is not there** → `target-not-found`. A filesystem distinguishes absence from refusal unambiguously, so unlike a hosted backend this adapter never falls back on the taxonomy's masking default.
- **A directory that exists and holds no matching documents, or a search that matched nothing** → `ok` with zero references. An empty directory is the space answering.
- **A file not decodable as text** — a binary carrying a document extension, or an undecodable encoding → `unreadable-content`.
- **A subtree skipped mid-walk for permissions, or a read cut short** → `partial`, returned with whatever was read. A search that silently skipped an unreadable directory must not report `ok`.
