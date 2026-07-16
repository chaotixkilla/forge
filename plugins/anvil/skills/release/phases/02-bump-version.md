The version is the contract a plugin makes with the people who install it: it tells them, at a glance, whether an upgrade is safe or breaking. Get the bump wrong and you either scare consumers off a harmless patch or silently break them on what looked like a minor update. The gate already proved the plugin is shippable; this phase decides *what number* the world sees it as, and writes that number to the single place that owns it — the plugin's `plugin.json`.

## Read the current version

Read the plugin's `plugin.json` and take its current version as the baseline. This file is the source of truth for the version; the catalog entry (next phase) mirrors it, never the reverse. If the version is missing or malformed, treat it as a contract defect, not something to paper over — surface it and stop, because you cannot bump a version you can't parse, and a release skill that invents a starting point hides a real problem.

## Decide the bump

Apply the semver step the maintainer asked for via `--bump` (`major` | `minor` | `patch`). The mechanics of choosing — the consumer-surface discriminators for breaking/additive/fix, and the special handling of pre-1.0 — are craft, and they live in [versioning-and-catalog](../rules/versioning-and-catalog.md); apply that rule here rather than re-deriving the conventions inline.

If `--bump` is absent, derive the level from the change set: the plugin's changes since its last release. Resolve "since its last release" in this order: **(1)** the version tag matching the manifest's current version — the tag names the exact released tree, so the change set is everything under `plugins/<name>/` since it; **(2)** failing a tag, the commit that last set the manifest's version field — the release commit, a weaker but usable baseline; **(3)** if the workshop has no history at all, derivation is impossible — stop and require an explicit `--bump` rather than classifying a change set you cannot see. Guessing a level over an unknowable diff is worse than asking. With a baseline in hand, walk the change set and classify it by the derivation method in [versioning-and-catalog](../rules/versioning-and-catalog.md), then propose the resulting level. Derivation is a *proposal*, not a silent decision: state the level you'd apply and what in the change set drove it, so the maintainer can correct a misjudged bump before it's written. When a change is ambiguous — the edit that might or might not be observable to consumers — round toward the more conservative (higher) bump and say why; under-bumping a breaking change is the costlier error.

## Write the new version back

Compute the new version from baseline + level and write it back to `plugin.json`, touching only the version field. Don't reformat the rest of the manifest — a release diff should show the version change and nothing else, so the maintainer can review it at a glance and so the commit in the final phase stays legible.

## Under --dry-run

Show the transition — `current → proposed`, with the level and (when derived) the evidence behind it — and write nothing. The dry run's job here is to let the maintainer veto a wrong bump before it touches the file; a faithful preview names the exact version that *would* be written, never a vague "will bump."
