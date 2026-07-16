A plugin is born from a decision about *what it owns*, not from a folder. The most expensive mistakes in a plugin's life are made here, before a single file exists: a domain drawn too wide so the plugin sprawls into everything, a skill pool that's really a feature list, a config posture bolted on after skills already assume it. This phase is design, deliberately ahead of scaffolding — get the shape right while it's still free to change, then let later phases commit it to disk. Nothing is written here.

## Require the name first

`--name` is mandatory: it becomes the directory `plugins/<name>/` and the `plugin.json` name, and it threads into every downstream step (`scaffold-skill --plugin=<name>`, the eventual catalog entry). If it's missing, stop and ask — don't invent one. A good plugin name is a domain noun, plugin-agnostic and tool-agnostic, the way the kit's own skills are named verb-first and vendor-free; resist a name that bakes in a single tool or workflow the plugin will outgrow.

## Interrogate the purpose — the one domain it owns

Before any capabilities, pin the plugin's *single responsibility* at the plugin altitude: the one domain it owns, stated in a sentence, and — just as load-bearing — what it deliberately **won't** do. A plugin that can't name its boundary will accrete unrelated skills until it's a junk drawer. The kit itself models this: it owns *authoring other plugins* and explicitly excludes being a consumer-facing tool. Write down both halves; the exclusion is what you'll measure scope creep against for the plugin's whole life.

Watch for the tell that you have *two* plugins, not one: if the purpose needs an "and" between two unrelated domains, split it. Two coherent plugins beat one incoherent one — and they stay mutually independent, which the marketplace requires.

## Design the capability set and altitude split

Now carve the domain into its initial skill pool: roughly 8–12 capability skills, each owning one responsibility, split by **altitude** (how broad a slice of the domain each governs) — not an exhaustive enumeration of every feature a user might want. This is the craft this skill exists for; the full method — the placement ladder that decides skill vs module vs flag vs phase, the altitude bands with their too-high/too-low tests, and the sizing bar behind the 8–12 band — lives in [designing-a-skill-pool](../rules/designing-a-skill-pool.md). Pull prior art from *external* plugins via the plugin explorer to see how others carved a comparable domain — but never read sibling plugins in this marketplace as a source, which would breed the cross-plugin awareness the marketplace forbids. The output is a list of named capabilities with a one-line responsibility each, ordered roughly by altitude, with the deferred-to-later set called out — a seed, not a frozen contract.

Name every skill as a capability, never a tool. *"manage the changeset"* is a capability; the same skill phrased around a specific version-control product is a leak you'd have to undo the moment the plugin meets a second backend.

## Decide the config posture — the fork that shapes the shell

This is the single most consequential decision of the phase, because the next phase scaffolds differently depending on it. Config is **per-plugin**: every plugin owns (or forgoes) its own config, and *this* is where a new plugin's posture is set.

The discriminator is a single question, asked of each capability in the pool: **would two different consuming projects legitimately answer "which backend serves this?" differently, AND is the answer something the plugin cannot derive by reading the project itself?** Both halves must hold. If any one capability passes, the plugin is config-bearing; if none does, it's config-less. The second half is what filters the false positives: a value the plugin can discover from the tree is a lookup, not config; a choice that varies per *run* rather than per *project* is a flag, not config; a value the plugin can fix for everyone is a shipped default, not config.

- **Config-bearing** — some capability routes to a *pluggable backend the consuming project must choose*: a place to put artifacts, a version-control provider, a knowledge or project-management destination whose identity differs per consumer. A config-bearing plugin earns a config schema and a config-setup skill, and its skills carry typed prerequisites that point at that setup. The decision rule for *what* becomes config stays strict — a value qualifies only if it's project-specific, stable, non-derivable, and actually consumed — but at this phase you only need the binary the discriminator gives you.

- **Config-less** — the default, and the right answer for a plugin that operates purely on the repo/files via primitives, the way the kit itself does. A config-less plugin ships *no* config machinery: no schema, no config-setup skill, no prerequisites on its skills. Don't manufacture config a plugin doesn't need — empty is a feature, and you can always add config later when a skill earns it.

State the posture explicitly in the design output; phase 2 reads it as a switch. When genuinely uncertain, default to config-less: it's cheap to add a schema later, expensive to strip a config layer skills have come to assume.

## Recruit the scaffolding-skeptic before anything is committed

The skeptic's whole job is to attack speculative structure: for *each* proposed skill, can it justify its place, or is it premature scaffolding for a need that hasn't arrived? The pass bar is the defense test in [designing-a-skill-pool](../rules/designing-a-skill-pool.md): each skill names a specific first invocation — who runs it, on what, for what output. Run the pool past the skeptic now, while the cost of cutting a skill is deleting a line from a list — not unwinding files, frontmatter, and wiring. Cut anything that can't defend itself (cut = moved to the named-deferred list); a lean pool you grow on demand beats a wide one you prune later. Only once the surviving pool, its altitude split, and the config posture all hold do you proceed to scaffold the shell.
