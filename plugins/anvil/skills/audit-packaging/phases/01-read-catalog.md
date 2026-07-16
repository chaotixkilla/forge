Every later phase is measured against the catalog, so the catalog is where the audit starts. The marketplace manifest is the single source of truth for what the world can install: it names each published plugin and the source path the installer copies from. Read it wrong and the whole audit is anchored to the wrong baseline — you'd check files against plugins that don't ship, or miss a plugin that does. Get the catalog right first, and the boundary question becomes mechanical: *is this file inside a published source path, and does it belong there?*

## Read the manifest

Read the marketplace manifest and pull out, for each listed plugin, two things: its **name** and its **source path** (the directory the installer treats as that plugin's shippable root). The source path is the load-bearing field — it defines the exact subtree that gets copied to a consumer on install. Record the set of published source paths; this is the audit's frontier. Everything under a published source path is in shipping scope; everything outside every published source path is, by definition, not shipped.

Do not infer publication from a directory merely *existing* under the plugins area. A plugin folder can sit in the repo fully built and deliberately unlisted — that is exactly how an unpublished plugin lives. Publication is defined by presence in the manifest, never by presence on disk. The manifest is the gate; the filesystem is just where the candidates live.

## Identify any unpublished plugins

A plugin can be built on disk yet deliberately kept out of the catalog — marked `--unpublished` / in-development, listed nowhere in the manifest until it is released. Collect the set of such plugins now, because phase 3 has to affirmatively confirm each stays absent from the manifest, not just fail to notice it.

Identify an unpublished plugin by the durable signal, not a baked-in name. It is the plugin that is (a) absent from the manifest yet (b) present on disk as a full plugin tree, and typically (c) carries an explicit unpublished marker if the maintainer set one. Lead with the marker if it exists, fall back to "built-but-unlisted" otherwise. A *full plugin tree* means a directory under the plugins area carrying a plugin manifest and at least one skill — a manifest-less directory is scrap or scaffolding debris, not an unpublished plugin. The marker's concrete shape is deliberately not pinned here: it belongs to the birth convention that sets it, and this audit reads whatever that convention wrote — pinning a filename would break the check on the next convention change. This set can be empty — a repo where every built plugin is published is a valid state, and it is fine for anvil itself to be published and catalogued alongside the plugins it authors.

## What you hand to the next phase

A two-part picture: the **published frontier** (each published plugin's name and source-path root) and the **unpublished set** (every built-but-unlisted plugin, which may be empty). Phase 2 walks the tree against this picture; phase 3 judges every file relative to which side of the frontier it sits on. If the manifest is malformed or a listed source path points at a directory that doesn't exist, that is itself a finding — surface it now rather than silently auditing against a broken baseline.
