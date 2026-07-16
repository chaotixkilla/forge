A plugin's shell is the minimum that makes it a loadable, well-formed plugin — and the discipline is knowing exactly where that minimum stops. The recurring birth mistake is over-provisioning: scaffolding every folder, a config layer, and a fistful of speculative agents because they *might* be needed, leaving dead structure the contract and packaging audits will later flag. This rule draws the line between what every plugin needs at birth and what to leave empty until earned — *seeds, not specs*. Phase 2 applies it; this is the why behind each call.

## What every plugin needs at birth

Three things, and only three, are non-negotiable for a plugin to exist:

- **A manifest** — the plugin can't be loaded without one. It names the plugin, describes the domain it owns, carries the initial version `0.1.0` (semver's initial-development release — the leading zero *is* the honest compatibility statement at birth), and names the author. It starts pre-stable because birth is not publication; the version moves only when `release` says so.
- **A `skills/` folder** — a plugin with no skills does nothing. It may be empty for a heartbeat during scaffolding, but the pool is what the plugin *is*, so the folder is structural from the start.
- **A README** — the human entry point: what the plugin is, the one domain it owns and what it won't, and how to load it. Keep it to the plugin's durable shape, never a changelog (history lives in version control, not in docs).

That's the whole floor. Everything else is added when a concrete need arrives.

## What to leave empty until earned

- **`agents/`** — create the folder so the structure is visible, but leave it empty. An explorer or critic is added only when a skill actually recruits it; an agent no skill references is orphaned cruft the contract audit flags. Don't pre-stock agents you imagine the plugin will want.
- **`hooks/`** — same: the folder can exist, but a hook file is inert until a skill binds it to a lifecycle event, so don't seed hooks speculatively.
- **A config schema and config-setup skill** — added *only* for a config-bearing plugin (see below). For a config-less plugin these don't exist at all — not as empty stubs, not "to be safe."

The principle is uniform: an empty earned-later folder is correct and cheap; a folder pre-filled with speculative content is premature scaffolding that costs the plugin clarity now and an audit finding later. Empty is a feature.

## Config machinery is posture-gated, and comes as a pair

Config is per-plugin, and whether a plugin has any is decided once, at birth, by its posture:

- **A config-bearing plugin** — one whose skills route to a pluggable backend a consumer must choose — gets two pieces together: a **config schema with shippable defaults** (the declaration of which capabilities need a backend, plus any default convention values; the plugin ships the schema, never per-consumer values, which live in the consumer's own space) and a **config-setup skill** (the guided, on-demand target the pool's skills point their prerequisites at). They're a pair because a schema with no setup path leaves the consumer stranded, and a setup skill with no schema has nothing to set. The skills of a config-bearing plugin carry typed prerequisites naming the config keys they need with an `if_missing` posture; those prerequisites are part of the same earned machinery.
- **A config-less plugin** gets *none* of it — no schema, no setup skill, no prerequisites. The kit itself is the model: it runs on the repo via primitives and ships zero config. A value earns a place in config only if it's project-specific, stable, non-derivable, and actually consumed; a plugin none of whose capabilities meet that bar is config-less, and forcing an empty config layer onto it is exactly the dead structure to avoid.

When the posture is genuinely uncertain, default to config-less: a schema is cheap to add later when a skill earns it, and expensive to strip once skills assume it.

## The unpublished marking

A plugin born in-development is marked so it stays out of the catalog until it's built and released. The marker's pinned form is a status line in the plugin's README (*"Status: in-development — not in the catalog until released"*): the README already exists at birth, and the manifest schema is the harness's to define, not the kit's to extend. The marking is load-bearing downstream: it's what `release`'s gate and the packaging audit read to *refuse* publication while the plugin is unfinished — the explicit marker they lead with, backed by the durable built-but-unlisted signal. An unpublished plugin is built up over time but hard-blocked from `marketplace.json` by design, and loaded via the direct plugin-directory path rather than the catalog until it's ready. Birth never adds a plugin to the catalog regardless — publication is `release`'s sole act — but the unpublished marking is what guarantees the plugin can never be published by mistake before it's released.
