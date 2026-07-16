# Stable identity and override precedence

Two of this skill's decisions are silently open unless pinned, and both change *where content lands*. First: when config, `--to`, and `--dest-dir` all speak to the destination, which wins — and what does `--to` even name? Second: under `--idempotent` (and `--version`), how is "the same artifact" recognized across runs, so a republish updates in place instead of minting a parallel copy? Left to taste, one run updates and the next duplicates, or two runs resolve different destinations from the same inputs. This rule pins both so two cold executors resolve the same target and the same identity.

## Classifying `--to`

`--to` can name a backend, a path, or a page id, so it is classified before it is applied — in one deterministic order:

1. **If `--to` exactly matches a configured backend name**, it selects that backend; the destination *within* that backend stays the config default (or is set by `--dest-dir`, below).
2. **Otherwise `--to` names a target within the resolved backend** — a path, page id, or other locator that the **adapter** interprets. The path-vs-id distinction is backend-specific and owned by the adapter, not decided here.

This keeps the skill-level test binary and reproducible ("names a configured backend, or not"); the backend-specific parsing lives below the seam.

## Override precedence — where the artifact goes

Resolve the destination by this order; the first that applies wins:

1. **`--to` / `--dest-dir` explicit override**, classified as above, overrides the config default for this run.
2. **The configured destination** — the `tools.artifacts` entry the artifact's type-key names, falling back to `destinations.default` when that entry is empty or the type names no key ([SKILL.md](../SKILL.md) step 1 owns the type→key lookup) — when no override is given.
3. **Neither resolves → ask, then degrade; never invent.** When no key entry and no `default` resolve and no override is given, ask the user where to publish (SKILL.md step 1); if that can't be answered, report `unavailable` (the destination is unconfigured — or `target-not-found` if the user's answer named a target that then proves absent) ([failure-taxonomy](failure-taxonomy.md)) and let the caller degrade — never invent or guess a destination, and never before any write.

The `--dest-dir` tie-break keys off the **resolved backend's kind**, not off parsing `--to`'s string:

- **Resolved backend is file-backed** → `--dest-dir` sets the base directory; if `--to` also named a within-backend path, that **whole** path nests under the base (`<dest-dir>/<full --to path>`), not just its terminal segment.
- **Resolved backend is not file-backed** → `--dest-dir` is inert (a file-base directory is meaningless there); ignore it and return the location with the ignored `--dest-dir` noted as an advisory (a successful-publish note, not a failure — see [SKILL.md](../SKILL.md) step 5).

`(basis: derived — an explicit per-run flag is a deliberate override of a standing config default, so overrides outrank config; --dest-dir is file-backend-specific, so its applicability keys off the resolved backend's kind rather than a fragile parse of the --to string. Ask-then-degrade rather than a bare fail follows the config posture (`tools.artifacts` → guide via `init:artifacts`, else block) and the maintainer's "ask on the spot" worst-case: when the destination is unresolvable the port asks the user, and failing that the caller degrades — it never invents one.)`

## Stable identity — recognizing the same artifact

Under `--idempotent`, resolve the identity of the already-published artifact by this order; the first reliable match wins:

1. **An explicit `--to` that the adapter resolves to a concrete existing location** (an id or path that already exists) **is** the identity — update exactly that. (If `--to` only selected a backend, not a concrete location, fall through.)
2. **The adapter's durable recorded key** — a written-back / manifest id where the backend supplies durable ids that survive renames; for a file-backed destination the resolved path itself is the durable id.
3. **A normalized destination path/slug** derived from the artifact's title + type + destination — the stateless fallback where no durable recorded id exists. The **normalization is backend-specific and each adapter declares it**, so two cold runs derive the same key.
4. **None resolves reliably** (an ambiguous slug matching several, or a required recorded id that is missing) → **fail `conflict`** ([failure-taxonomy](failure-taxonomy.md)). Do **not** mint a duplicate; hand the caller the ambiguity to resolve.

Each adapter **declares its identity key and its normalization** in its own file (a file-backed destination: the resolved path, and how a title becomes a filename; an id-based backend: the recorded/written-back id), because which key is *durable* — and how a name normalizes — is a property of the backend, not of this skill.

`(basis: ratified by the maintainer, 2026-07-08 — durable-id-first, path/slug fallback, fail-don't-duplicate. Derived from the reliability trade-off: a slug/title path is stateless but duplicates on rename; a recorded id is robust but needs stored state. Resolved by making the key adapter-declared and precedence-ordered, and by failing to `conflict` rather than duplicating when identity is unreliable.)`

## How the two write-mode flags use identity

- **`--idempotent`** resolves the identity above and updates that location in place.
- **`--version`** resolves the same identity to find the prior output, then writes a **new labeled copy alongside** it, preserving history — it does not update in place. The label scheme is adapter-declared (see each adapter's Capability matrix) so the copy's location is reproducible.
- **Mutually exclusive.** `--idempotent` keeps one canonical, evolving location; `--version` fans out a new copy each run. Requesting both is a contradictory invocation — reject it up front and report the conflicting flags (not a publish outcome — see [failure-taxonomy](failure-taxonomy.md), "what this taxonomy does and does not cover"), rather than guess which the caller meant.
