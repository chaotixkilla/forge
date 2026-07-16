With the pool designed and the config posture decided, this phase commits the *shell* — the minimum a plugin needs to exist and be loadable, and nothing more. The discipline here is restraint: a plugin is born almost empty, and stays that way until each part is earned. The full reasoning for what every plugin needs at birth versus what to defer lives in [plugin-shell-conventions](../rules/plugin-shell-conventions.md); this phase is the procedure that applies it.

The shell branches on the config posture from phase 1. The common shell is the same for every plugin; the config machinery is added *only* for a config-bearing plugin and *omitted entirely* otherwise.

## The common shell — every plugin gets this

Create the manifest and the structural skeleton that make the plugin a loadable plugin:

- **`.claude-plugin/plugin.json`** — the manifest: name (matching `--name`), a one-line description naming the domain the plugin owns, an initial version, and author. The initial version is `0.1.0` — semver's initial-development release, whose leading zero declares the compatibility promise still weak; `release` is what later moves it toward a published, stable version. Don't reach for a manifest field the plugin doesn't yet use; the manifest, like everything else, accretes on demand.
- **The slot folders** — `skills/`, `agents/`, and `hooks/`. Create the folders so the structure is visible and the next phase has somewhere to land each scaffolded skill, but leave `agents/` and `hooks/` empty: they're populated only when a skill actually recruits an agent or binds a hook. An empty earned-later folder is correct; a folder pre-filled with speculative agents is premature scaffolding the skeptic would cut.
- **A README** — what the plugin is (the one-domain purpose from phase 1, including what it deliberately won't do) and how to load it. This is the human entry point; keep it to the durable shape of the plugin, not a changelog.

## Config-bearing only — add the config machinery

Do this branch *only* if phase 1 marked the plugin config-bearing. Two pieces, and they come as a pair:

- **A config schema with shippable defaults** — the declaration of the pluggable backends the plugin's skills route to, plus any default convention values the plugin can ship. Crucially, the plugin ships only the *schema and defaults*; the actual per-consumer values live in the consuming project's space, never in the read-only plugin cache. The schema is the contract a consumer fills in; it enumerates the capabilities that need a backend, not concrete tools.
- **A config-setup skill** — the guided target that the pool's skills point their prerequisites at. When a config-bearing skill runs and finds its required config slice missing, the lazy gate guides the consumer through *this* skill to set just that slice. It exists so that setup is on-demand and scoped, never a wall of upfront configuration. Scaffold it as a skill like any other (it will be filled like the rest in phase 3).

In capability terms: a config-bearing plugin's schema might declare *"the artifacts backend"* and *"the changeset provider"* as keys a consumer must choose, and its skills declare a typed prerequisite naming those keys with an `if_missing` posture (guide, degrade, or block). The schema names capabilities and leaves the concrete provider to the consumer's config and the plugin's adapters — never a tool name in the schema's prose.

## Config-less — add none of it

If phase 1 marked the plugin config-less, this is a hard *skip*, not a lighter version: **no** config schema, **no** config-setup skill, and the pool's skills carry **no** config prerequisites. Manufacturing an empty config layer "to be safe" is exactly the speculative structure the kit refuses — it leaves dead machinery that the contract audit will later flag as config keys with no backing. The kit itself is the model: it operates on the repo via primitives and ships zero config.

## Honor `--unpublished`

If `--unpublished` is set, mark the plugin in-development so it stays out of the catalog until it's built and released — the posture any not-yet-releasable plugin starts in. The marking has a pinned form: a status line in the plugin's README — *"Status: in-development — not in the catalog until released."* The README is where it lives because the shell already owns that file and the manifest schema belongs to the harness (don't invent manifest fields the loader never specified); the line is the explicit marker the gate and audits lead with, while catalog absence stays the operative signal they fall back to. The marking is what `release`'s gate and the packaging audit read to *refuse* to publish the plugin while it's unfinished; an unpublished plugin is built up over time but is hard-blocked from the catalog by design until it's ready. Regardless of this flag, new-plugin never touches `marketplace.json` — publication is `release`'s job alone.

## Under `--dry-run`, write nothing

`--dry-run` produces the exact scaffold plan — every file and folder that *would* be created, the manifest fields, the README, and (only if config-bearing) the schema and config-setup skill — and writes none of it. A dry run is a faithful preview the maintainer can review before the tree is touched, never a half-applied scaffold.
