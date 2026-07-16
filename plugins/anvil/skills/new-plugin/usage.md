# new-plugin — usage

Birth a new plugin in the marketplace: decide its config posture, scaffold the loadable shell, and seed its initial skill pool — stopping short of publication.

## When to use
- You're starting a *new* plugin and need the whole birth in one move: name it, carve its domain into a skill pool, pick config-bearing vs config-less, and lay the shell.
- You want the pool designed *before* any files exist — the altitude split and the one-domain boundary pinned while they're still free to change.
- You're deciding, once and up front, whether the plugin owns config at all (a pluggable backend a consumer must choose) or ships zero config machinery.
- You're bootstrapping an in-development plugin that must stay out of the catalog until it's built and released (`--unpublished`).
- You want a faithful preview of the entire tree — manifest, folders, README, and any config machinery — before committing it (`--dry-run`).

## Not for / use instead
- Laying *one* skill's file skeleton (frontmatter + slots) in an already-born plugin → **scaffold-skill**. new-plugin delegates each seeded skill to it; reach for it directly to add a skill to an existing pool.
- Filling a skill's *procedure* — turning a human process into a runnable method → **codify**. new-plugin routes each fresh skeleton to codify; call it directly to author or refine a procedure.
- Adding a *non-skill* component — an adapter, explorer, critic, rule, module, or hook — to a plugin → **add-component**. That's where a concrete tool name is legitimately introduced, beneath a skill; new-plugin never names a tool.
- *Publishing* the plugin — preflight audits, version bump, catalog entry, release notes → **release**. new-plugin stops at birth on purpose; it never touches `marketplace.json`.
- Proving the seeded skills actually work end-to-end and surfacing runtime friction → **dogfood**. new-plugin only makes the pool real and runnable, not proven.
- Checking the built plugin's internal wiring — frontmatter shape, slot placement, flag/config wiring, adapter coverage → **audit-contract**.
- Scanning the skill layer for leaked tool/provider names → **audit-tool-leaks**; auditing the ships-vs-authoring boundary across the marketplace → **audit-packaging**. new-plugin designs to avoid these findings; the audits verify later.

## Examples
`--name=<plugin>` — birth a config-less plugin: design its pool, write `plugins/<plugin>/` with manifest, `skills/`/`agents/`/`hooks/`, and a README, then seed the earned skills. The default posture.
`--name=<plugin> --dry-run` — show the exact scaffold plan (every file/folder, manifest fields, README) and write nothing — a reviewable preview.
`--name=<plugin> --unpublished` — build a plugin fully but mark it in-development (a README status line) so `release`'s gate and the packaging audit refuse to publish it until it's ready; the handoff points at the direct plugin-directory load path, not at `release`.
`--name=<plugin> --unpublished --dry-run` — preview the birth of an unpublished plugin, including its out-of-catalog marking, without touching disk.

## Gotchas
- `--name` is mandatory. Missing it stops the run — new-plugin will not invent a name. Pick a domain noun, plugin- and tool-agnostic; a name that bakes in a single tool or workflow will be outgrown.
- Design comes before scaffolding: phase 1 pins the *single* domain the plugin owns AND what it deliberately won't do, carves ~8–12 capability skills split by altitude, and decides config posture — all before a file is written. Config posture is a switch phase 2 reads; state it explicitly.
- Config-less is the default and, when uncertain, the right call. The discriminator: config-bearing only if some capability's backend is one that two consuming projects would choose differently AND the plugin can't derive by reading the project — derivable is a lookup, per-run is a flag, fixable-for-everyone is a shipped default. A schema is cheap to add later, expensive to strip once skills assume it. Never manufacture an empty config layer "to be safe" — dead machinery the contract audit will flag.
- Config-bearing is a hard commitment to a *pair*: a config schema (with shippable defaults, never per-consumer values) AND a config-setup skill, plus typed `if_missing` prerequisites on the skills that route to a backend. Choose it only if some capability routes to a pluggable backend the consumer picks.
- Skills are named as capabilities, never tools — the hard rule, applied at birth. A skill named after a product is a leak; the concrete tool lives only in an adapter added later via add-component.
- One capability per pluggable backend, not one skill per provider. Let config + adapters absorb the variation; "publish-to-X" / "publish-to-Y" is the classic carve error.
- Pull prior art only from *external* plugins; never read sibling plugins in this marketplace as a source — that breeds the cross-plugin awareness the marketplace forbids.
- Seeds, not specs: scaffold only what the design earned and the skeptic passed (the pass bar: each skill names a concrete first invocation); name deferred skills but leave them unbuilt. Every seeded skill at least gets codify's goal/process split; the full drive to a validated procedure waits for skills whose process the maintainer can already narrate end-to-end.
- The plugin is born, NOT published: it never lands in `marketplace.json`, isn't installable, and the handoff says so plainly. Point at `release` only once the plugin is codified, adapter-backed, and passes the audits — and never for an `--unpublished` plugin.
- Regardless of `--unpublished`, new-plugin never touches the catalog. Publication is `release`'s sole act.
