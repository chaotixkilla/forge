The packaging boundary has two sides. [ships-vs-authoring](ships-vs-authoring.md) governs the *filesystem* side — which files sit inside a published source path. This rule governs the *catalog* side — what the marketplace manifest is allowed to list, and which plugins must be kept out of it. The two are independent leaks: a plugin can have a spotless file tree and still be a packaging defect if it is wrongly listed (or wrongly absent) in the catalog. This rule is the craft for judging the manifest.

## What the manifest is

The marketplace manifest is the published catalog: the authoritative list of what a consumer can discover and install. Each entry names a plugin and a source path — the directory the installer copies as that plugin's shippable root. Listing in the manifest is the single act of publication. Nothing else makes a plugin public; building it on disk does not, and a plugin folder existing under the plugins area does not. **Publication is presence in the manifest, full stop.** That makes the manifest the one place to check whether a plugin is, or is not, shipped.

## What belongs in it

Only genuinely publishable plugins — those meant to be installed and used by consumers — and each must list a source path that is exactly the plugin's shippable root, no wider. A source path widened to swallow a parent directory drags whatever else lives there (design notes, a sibling unpublished plugin) into shipping scope; a source path narrower than the plugin's real root ships an incomplete plugin. The entry should resolve to a real plugin tree, and no two entries should claim overlapping paths. A dangling or overlapping entry is a catalog defect even when every individual file is correctly classified.

## What must stay out — and why it is a positive check

A plugin marked `--unpublished` / in-development must be **absent** from the manifest. Such a plugin is built, possibly fully working, but deliberately not listed — it opts out of the catalog until the maintainer releases it. This is the in-development contract: the plugin exists on disk and can be dev-loaded as a local directory, but it is not installable by consumers while the marker stands.

The crucial discipline: confirming a plugin's absence is an **affirmative check, not a default.** The audit must look at the manifest and *assert* every unpublished plugin is not listed — because the regression this guards against is precisely an in-development plugin quietly sliding into the catalog during some edit and shipping before it is ready. "I didn't happen to notice it" is not the same as "I confirmed it is not there." Make the negative explicit. This set can be empty — a repo where every built plugin is published is a valid state.

## How to recognize the plugin that must stay out

Identify it by its **explicit in-development marker**, never a baked-in name and never mere unlisted-ness:

- The explicit unpublished marker is what *declares* a plugin must-stay-out; lead with it and treat it as the only signal that keeps a plugin out.
- **Built-but-unlisted, with no marker, is not a must-stay-out signal.** A full plugin tree on disk with no manifest entry is equally the state of a plugin *awaiting its first publish*, so the audit cannot read it as in-development. Treat it as the *wrongly-absent* case below — route it to the maintainer (release it, or mark it unpublished) — never as a block. Only the marker separates "deliberately kept out" from "not yet shipped."

Resist hardcoding any plugin's current name into the audit. Names change across renames or restructurings; the durable method is the explicit marker. The marker's concrete shape is likewise left open on purpose — it belongs to the birth convention that sets it, and this audit reads whatever that convention wrote, so the check survives convention changes. Note in particular that anvil, the plugin that authors the others, is itself a normal published plugin catalogued alongside them — its presence in the manifest is correct, not a leak.

## The two catalog leaks

- **A plugin wrongly absent** — a publishable plugin built but never listed. **Low** severity: nothing wrong ships, it just isn't shipping. Surface it when both hold — no unpublished marker, and the tree is complete (a plugin manifest plus built skills). A marked plugin is exercising the in-development contract and is not a gap. The audit can't read intent, so this finding routes to the maintainer with both exits named: release it, or mark it unpublished. (Low is the report ladder's level for this case — [phases/04-report](../phases/04-report.md); this rule names the same level so the two never disagree.)
- **A plugin wrongly present** — an `--unpublished` / in-development plugin appearing in the manifest. **Critical** severity: it makes unreleased work installable by consumers — premature release, not recoverable once someone has installed it. This is the leak this rule exists to catch. (Severity is assigned by the report ladder in [phases/04-report](../phases/04-report.md), where premature-release-to-consumers is Critical alongside a secret reaching a source path; this rule names the same level so the two never disagree.)

## Anti-patterns

- **Treating disk presence as publication.** A plugin tree in the repo says nothing about whether it ships; only the manifest does. Audit against the manifest, not the filesystem.
- **Defaulting an unpublished plugin's absence instead of asserting it.** Not seeing it in a quick scan is not a confirmation. Look for each *marked* unpublished plugin by its marker and state the negative result.
- **Treating unlisted-ness as a keep-out signal.** A built-but-unlisted plugin with no marker is not in-development — it is either awaiting first publish or a wrongly-absent nudge; only the explicit marker keeps a plugin out. Inferring a block from absence alone deadlocks every plugin's first release.
- **Hardcoding a plugin's name into the check.** Encodes a fact that goes stale; encode the unpublished marker instead.
- **Treating anvil's manifest entry as a leak.** anvil is a published plugin like any other; its presence in the catalog is correct. The catalog leak is an `--unpublished` plugin appearing, not the authoring plugin being listed.
- **Letting a widened source path pass because every file in the plugin is fine.** The leak is the *path*, not the files: a source path that reaches past the plugin's root ships everything underneath it regardless of how those files are individually classified.
