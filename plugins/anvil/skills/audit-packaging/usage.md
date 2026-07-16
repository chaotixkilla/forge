# audit-packaging — usage

Audit the ships-vs-authoring boundary across the whole marketplace: every published plugin ships only consumer-facing files, authoring-only material stays outside every source path, and any plugin marked unpublished stays absent from the catalog.

## When to use
- Before a release, to confirm nothing authoring-only will copy to consumers on the next install — install copies a plugin's source directory whole, with no per-file exclude, so a mislabeled file has no downstream filter to catch it.
- After adding design notes, maintainer scripts, tests, or fixtures anywhere near a plugin tree, to confirm they landed outside the shipping frontier and not inside a source path.
- After editing marketplace.json, to confirm any `--unpublished` plugin is still absent and every entry still resolves to a real, non-overlapping source path.
- Whenever you suspect a populated config, secret-bearing file, or maintainer tooling has drifted into shipping scope — the highest-stakes leak this skill exists to catch.
- As a periodic marketplace-wide packaging sweep, not tied to any one plugin — it walks the whole catalog, not a single target.

## Not for / use instead
- Checking ONE plugin's internal wiring — frontmatter shape, slot placement, flag-to-module and config-key coverage, adapter coverage → `audit-contract`. That audit asks "is this plugin correctly *built* inside its own tree"; packaging asks "does the right *set of files* cross the ship/authoring line marketplace-wide."
- Scanning a plugin's skill layer for concrete tool/provider names that escaped adapters → `audit-tool-leaks`. That is a content leak (a capability skill naming a vendor); packaging is a file-placement leak (an authoring file inside a source path). Different plane, different fix.
- Actually publishing a plugin — version bump, writing the catalog entry, release notes → `release`. audit-packaging only *inspects* the boundary and catalog read-only; it never adds an entry or tags a version. release runs this audit as a preflight, then ships.
- Proving skills work end-to-end by running them → `dogfood`. That is dynamic execution surfacing friction; packaging is a static file-classification pass that runs nothing.
- Creating a new plugin and deciding its publish posture (including `--unpublished`) → `new-plugin`. That *establishes* which side of the catalog a plugin sits on; packaging *verifies* an existing posture held.
- Generating a skill skeleton, adding a non-skill component, or filling a procedure → `scaffold-skill` / `add-component` / `codify`. Those author content; packaging judges where existing content sits.

## Examples
`` — audit the whole marketplace, report findings inline, most-dangerous-first, no changes proposed.
`--report=artifact` — same audit, rendered as a scannable/navigable page instead of inline prose; reach for this when the finding set is large or you want an artifact to keep alongside a release. Findings and their order are identical to inline — only presentation changes.
`--fix` — for each finding, propose the concrete correction: relocate the authoring-only file across the boundary (from-path → to-path), or remove the offending catalog entry for an unpublished plugin. Proposals only — the maintainer approves before any file moves.
`--fix --report=artifact` — proposed relocations rendered as a page rather than inline, for a large or release-adjacent finding set.

## Gotchas
- **Publication is presence in the manifest, never presence on disk.** A fully built plugin folder that isn't listed does not ship. Audit every file against the manifest's source paths, not against what happens to exist under the plugins area.
- **An unpublished plugin's absence is an affirmative check, not a default.** The audit must look at the catalog and assert "this `--unpublished` plugin is not listed" — "I didn't happen to see it" is not a confirmation. Identify unpublished plugins by durable signal (an unpublished marker, else built-but-unlisted), never by a hardcoded name. The unpublished set can be empty, and anvil's own presence in the catalog is correct — it is a published plugin, not a leak.
- **The only remedy is relocation across the boundary — there is no per-file exclude.** `--fix` never proposes "exclude this from the package," because the install model has no such mechanism; the fix is always to move the file physically outside the source path (or drop the catalog entry). Proposing an exclude teaches a mechanism that does not exist.
- **A widened source path is a leak even when every file is fine.** The leak can be the *path*, not the files: a source path that reaches past a plugin's root drags whatever else lives there (design notes, a sibling unpublished plugin) into shipping scope. Point at the narrower root that restores separation.
- **Classify by audience and runtime need, never by extension or name.** A README splits by *who reads it* (consumer usage ships; contributor/architecture docs are authoring-only); a config splits by *template-vs-populated* (empty template ships; a populated secret-bearing config is a hard flag). A misleading filename is exactly the trap.
- **A genuinely ambiguous file is marked *uncertain*, not force-verdicted** — it's carried to the boundary-keeper critic to promote or clear, because a wrong "ships" leaks tooling and a wrong "authoring-only" could strip something a consumer needs.
- **A clean boundary is a real, reportable result.** If both invariants hold and the catalog is integral, the report says so plainly and names what was checked — it does not invent borderline nits to look thorough.
- **`--fix` is a proposal, not a silent rewrite.** Moving files reshapes the repo; a misjudged relocation can move a file a consumer needed. Present the moves; the maintainer confirms.
