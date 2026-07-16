The catalog is the marketplace's index — the one file that tells the harness which plugins exist and where to load each one from. A plugin can be perfectly built, versioned, and audited, but until it has an entry in the catalog it is invisible to consumers: nothing can resolve it, nothing can install it. This phase is the publication act itself. It splits cleanly by whether the plugin is already listed.

## First publish — add the entry

If the plugin has no catalog entry yet, add one. An entry carries three things, and all three must be right:

- **name** — matches the plugin's own `plugin.json` name exactly. A mismatch here means the catalog advertises one name and the plugin identifies as another, which breaks resolution.
- **source** — the path to the plugin's subdirectory under `plugins/`. Install copies that whole subtree, so the source must point at the plugin root and nothing above or beside it.
- **description** — the consumer-facing one-liner. Take it from the plugin's own description rather than composing a fresh one, so the catalog and the plugin agree on what the plugin is.

Add the entry without disturbing the others — the catalog lists every published plugin, and a release of one must leave the rest byte-for-byte untouched.

## Re-release — update the existing entry

If the plugin is already listed, update its entry in place rather than adding a duplicate. The version moved this release, so the entry's version (where the catalog carries one) follows `plugin.json` — the manifest is the source of truth, the catalog mirrors it. Refresh the description if the plugin's own description changed; leave name and source alone unless the plugin genuinely moved or was renamed (a rare, deliberate event worth calling out, not a silent edit). Never create a second entry for a plugin that already has one — a catalog with two entries for the same plugin is a defect the next packaging audit will flag.

## Confirm it resolves

Before declaring the catalog done, verify the entry is well-formed and actually resolves: name + source + description all present, and the source path points at a real plugin root that contains the manifest you just bumped. The check that the catalog *parses* and that every source resolves belongs to the packaging audit's domain — but a release that writes an entry it never confirms is one typo away from a catalog that loads nothing. Confirm the seam you just wrote.

## Under --dry-run

Show the exact entry that would be added or the precise field-level diff that would be applied to an existing entry, and write nothing. "Would add plugin X" is not enough — render the literal name/source/description so the maintainer can catch a wrong source path or a stale description before it's the published record.
