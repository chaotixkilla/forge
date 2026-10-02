# Stable identity and override precedence

Two of this skill's decisions are silently open unless pinned, and both change *where content lands*. Left to taste, one run updates and the next duplicates, or two runs resolve different destinations from the same inputs.

## Classifying `--to`

`--to` names a target within the resolved space — the home, or the audience space `--space` selected ([SKILL.md](../SKILL.md) step 1): a path, page id, or other locator that the **adapter** interprets. The path-vs-id distinction is backend-specific and owned by the adapter, not decided here. Which space is chosen by `--space` alone, never by `--to`'s string, so a location in an audience space can be updated in place (`--space=<name> --to=<its id> --idempotent`). `(basis: maintainer, 2026-10-01)`

## Override precedence — where the artifact goes

Resolve the destination by this order; the first that applies wins:

1. **`--to` / `--dest-dir` explicit override** overrides the space's configured destination for this run.
2. **The configured destination** — the resolved space's `destination` — when no override is given.
3. **Neither resolves → ask, then degrade; never invent.** When that `destination` is empty and no override is given, ask the user where to publish (SKILL.md step 1); if that can't be answered, report `unavailable` (the destination is unconfigured — or `target-not-found` if the user's answer named a target that then proves absent) ([failure-taxonomy](failure-taxonomy.md)) and let the caller degrade — never invent or guess a destination, and never before any write.

The `--dest-dir` tie-break keys off the **resolved backend's kind**, not off parsing `--to`'s string:

- **Resolved backend is file-backed** → `--dest-dir` sets the base directory; if `--to` also named a within-backend path, that **whole** path nests under the base (`<dest-dir>/<full --to path>`), not just its terminal segment.
- **Resolved backend is not file-backed** → `--dest-dir` is inert (a file-base directory is meaningless there); ignore it and return the location with the ignored `--dest-dir` noted as an advisory (a successful-publish note, not a failure — see [SKILL.md](../SKILL.md) step 5).

`(basis: derived from per-run overrides outranking standing config, the config posture, and the maintainer's "ask on the spot" worst case)`

## Stable identity — recognizing the same artifact

Under `--idempotent`, resolve the identity of the already-published artifact by this order; the first reliable match wins:

1. **An explicit `--to` that the adapter resolves to a concrete existing location** (an id or path that already exists) **is** the identity — update exactly that. (If `--to` names no existing location, fall through.)
2. **The adapter's durable recorded key** — a written-back / manifest id where the backend supplies durable ids that survive renames; for a file-backed destination the resolved path itself is the durable id.
3. **A normalized destination path/slug** derived from the artifact's title + type + destination — the stateless fallback where no durable recorded id exists. The **normalization is backend-specific and each adapter declares it**, so two cold runs derive the same key.
4. **None resolves reliably** (an ambiguous slug matching several, or a required recorded id that is missing) → **fail `conflict`** ([failure-taxonomy](failure-taxonomy.md)). Do **not** mint a duplicate; hand the caller the ambiguity to resolve.

Each adapter **declares its identity key and its normalization** in its own file (a file-backed destination: the resolved path, and how a title becomes a filename; an id-based backend: the recorded/written-back id), because which key is *durable* — and how a name normalizes — is a property of the backend, not of this skill.

`(basis: maintainer, 2026-07-08)`

## How the two write-mode flags use identity

- **`--idempotent`** resolves the identity above and updates that location in place.
- **`--version`** resolves the same identity to find the prior output, then writes a **new labeled copy alongside** it, preserving history — it does not update in place. The label scheme is adapter-declared (see each adapter's Capability matrix) so the copy's location is reproducible.
- **Mutually exclusive.** `--idempotent` keeps one canonical, evolving location; `--version` fans out a new copy each run. Requesting both is a contradictory invocation — reject it up front and report the conflicting flags (not a publish outcome — see [failure-taxonomy](failure-taxonomy.md), "what this taxonomy does and does not cover"), rather than guess which the caller meant.
