# release — usage

Publish one plugin to the marketplace: gate it behind the three audits, bump its version, write its catalog entry, and cut release notes + a tag.

## When to use
- A plugin is built, wired, and you're ready to expose it to consumers for the first time — this is the publication act, the one skill that touches the catalog.
- You're shipping a new version of an already-listed plugin: bump the version, mirror it into the catalog, and tag the release.
- You want a faithful preview of exactly what a release would do — the bump, the catalog entry, the notes, the tag — without mutating the tree (use `--dry-run`).
- You need the binding quality gate enforced for real: release runs packaging + contract + tool-leak audits in full and refuses to publish a plugin that fails any of them.

## Not for / use instead
- Checking the audits without publishing — run them on demand; they're advisory and support subsets, release runs them in full as a hard gate → `audit-packaging`, `audit-contract`, `audit-tool-leaks`
- Proving a plugin's skills actually work end-to-end (a dynamic test, incl. `--self` self-hosting proof) — release only runs the static audits, never exercises the plugin → `dogfood`
- Creating a plugin (config posture, shell, initial skill pool) — that births it but deliberately stops short of publishing; release is where it enters the catalog → `new-plugin`
- Adding or authoring a skill/component inside a plugin — those change what ships; release ships what's already there → `scaffold-skill`, `add-component`, `codify`

## Examples
`--plugin=<plugin> --bump=minor` — full release: gate, bump 0.3.0→0.4.0 in plugin.json, mirror the entry in the catalog, write notes, commit + tag.
`--plugin=<plugin> --bump=patch` — ship a fix-only release; consumer upgrades without thinking.
`--plugin=<plugin> --bump=major` — breaking change; notes must lead with what breaks and the migration required.
`--plugin=<plugin>` — no `--bump`: derives the level from the change set since the last release (baseline: the prior version tag, else the last release commit) and *proposes* it (level + evidence) before writing.
`--plugin=<plugin> --bump=minor --dry-run` — preview only: shows current→proposed version, the literal catalog entry, the rendered notes, and the commit/tag plan; writes nothing, tags nothing.
`--plugin=<plugin> --bump=minor --report=artifact` — return the release notes as a rendered page/file instead of inline prose.
`--plugin=<plugin> --report=inline` — the default report mode, notes returned as inline prose.

## Gotchas
- `--plugin` is mandatory. Missing it stops the skill — it will not guess the publish target from the working directory or the most-recently-touched plugin.
- One hard block, **no `--force`**: any plugin marked `--unpublished` (in-development, built-but-unlisted) is refused with no override. Being an authoring kit or self-hosting is not itself a block — anvil ships. Flipping a plugin's publish posture is a deliberate change made to the plugin upstream, never a flag here.
- The gate is a conjunction: any one of the three audits failing fails the whole release. Release surfaces the findings (anchored to file:line) and stops — it does not fix-forward. Fix in the right skill, then re-gate.
- The gate runs the audits in **full** even if you ran a narrowed subset earlier in the session — the release gate is the one place that can't be partially satisfied.
- `--dry-run` still runs the gate for real (the audits are read-only, so the pass/fail is identical to a live release) — but creates no commit and no tag. Tagging under a dry run would be the worst possible bug in this skill.
- `plugin.json` is the source of truth for the version; the catalog entry mirrors it, never the reverse. They move together in one release commit — never bump one without the other.
- Pre-1.0 shifts the convention down a notch (breaking rides the minor position); reaching `1.0.0` is a deliberate maintainer decision, not a mechanical side effect of a breaking bump.
- If `--bump` contradicts the change set (a `patch` over a removed skill), release says so rather than silently obeying.
- No version control available? Release still writes the files, then degrades to a printed manual checklist (files changed, new version, tag to create) rather than silently skipping the history record. But bump *derivation* needs history: with no baseline to diff against, release stops and asks for an explicit `--bump`.
- Notes must pass the standalone test: a consumer on the previous version can decide upgrade-or-skip and perform any migration from the notes alone — entries in consumer terms (skills/flags/capabilities), never file paths.
