# audit-contract — usage

Check one plugin's internal contract — frontmatter shape, slot placement, the cross-references that wire flags, config, adapters, and phases together, and whether its skills' judgment bars are closed — and report where it's broken.

## When to use
- You've edited a skill's frontmatter or slots and want to confirm the loader still sees a well-formed contract before moving on.
- A flag, config dependency, or provider was added and you need to know it's actually backed — that the switch fires a module, the `config_requires` key resolves to a real config slot, the enumerated provider has an adapter.
- You suspect a phase or rule silently never loads — an uncited phase file, an orphaned rule, a bare-path citation the loader can't follow — because the skill is running on its summary instead of its method.
- A skill grades, ranks, filters, or selects, and you want its bars checked for closure — pinned with a basis, or deliberately open with the reason recorded — before two cold runs get the chance to disagree.
- A pre-release or hand-off sanity pass on a single plugin's structural conformance, ideally as the diagnostic step before you fix anything.
- Re-checking one dimension (`--checks=flags-to-modules`) after a targeted fix, without re-running the whole audit.

## Not for / use instead
- Hunting concrete tool/vendor/CLI names that leaked into skill prose — that's a full-body scan, not the frontmatter description field this audit reads. → audit-tool-leaks
- The ships-vs-authoring boundary across the whole marketplace (what ships to consumers vs. what stays authoring-only, and that any in-development plugin is kept out of the catalog until released) — that's a cross-plugin packaging concern, not one plugin's internal wiring. → audit-packaging
- Proving skills actually work by running them end-to-end — this audit is static; it reads the contract, it never executes the plugin. → dogfood
- Creating the missing thing the audit flagged (a rule, module, adapter, explorer, critic, hook) — this reports the hole; it writes nothing back. → add-component
- Deciding what an open bar should be — the audit flags an open standard-point and never proposes its value; sourcing and pinning the bar is the maintainer's call, made against the plugin's design record. → codify (to write the pinned bar into the skill)
- Filling an empty or malformed procedure — authoring the runnable steps behind a skill is a different job from checking their wiring. → codify
- Seeding the file skeleton for a brand-new skill — audit checks an existing skeleton, it doesn't generate one. → scaffold-skill
- Standing up a whole new plugin shell and its skill pool. → new-plugin
- Shipping a plugin to the catalog (preflight, version bump, notes) — release runs its own preflight audits; this is one diagnostic you'd run beforehand, not the release itself. → release

## Examples
`--plugin=<plugin>` — full contract audit of one plugin: frontmatter shape, all cross-references (flags↔modules, config↔keys, adapters↔providers, spine↔phases, phases↔rules, the usage.md pointer), slot placement, and standard-point closure, reported inline severity-ranked.
`--plugin=<plugin> --checks=frontmatter` — run only the frontmatter-shape check; nothing else is pulled in.
`--plugin=<plugin> --checks=flags-to-modules,slot-placement` — re-check just those two dimensions after a fix; a subset run is honored exactly, and the report says which checks ran and which were skipped.
`--plugin=<plugin> --checks=config-keys,adapter-coverage` — the config-bearing checks only; on a config-less plugin these are correctly skipped and reported as a deliberate skip.
`--plugin=<plugin> --checks=standard-closure` — content bars only: every judgment a skill demands is pinned-with-basis or open-by-design-with-reason; open-by-omission points come back quoted, each with the two divergent readings that prove it open.
`--plugin=<plugin> --skill=<skill>` — audit just one skill after editing it, without judging the whole plugin; siblings and the config template are still read so cross-skill joins (a delegation citing a sibling, a `config_requires` key) resolve, but findings come back only for that skill. Composes with `--checks` (`--skill=<skill> --checks=standard-closure` re-checks one skill's bars).
`--plugin=<plugin> --report=artifact` — write the findings to the configured artifacts backend instead of inline, for a baseline or sign-off record someone else will read.
`--plugin=<plugin>` — required; without `--plugin` the audit stops and asks rather than guessing a target.

## Gotchas
- `--plugin` is mandatory. A contract audit pointed at the wrong plugin certifies the wrong thing, so a missing or typo'd target fails loud up front — it will not fall back to the working directory or "the obvious one."
- Diagnostic only — it reports what's wrong, where, and what the contract expects, and fixes nothing. Remediation is a separate, deliberate act (often add-component, codify, or a manual edit).
- Config-bearing vs. config-less is decided first, and the config checks (`config-keys`, `adapter-coverage`) apply only to config-bearing plugins. On a config-less plugin their absence is correct, not a gap; forcing them manufactures false findings.
- Not every flag needs a module. Selector/format/scope flags (like `--report`, `--checks`, `--skill`, a `--plugin` target) parameterize a phase rather than gating dormant behavior — demanding a module for them is over-reporting. Only behavior-gating flags oblige a `modules/` file.
- `--skill` is not a plugin-wide audit: a clean scoped run clears only that one skill, not its siblings, and the report says so. (It still reads the whole plugin as join context so a cross-skill reference resolves — see the Example.)
- Every cross-reference runs both directions. A one-way check catches the missing backing (dead flag) but misses the orphan (unreachable module, uncited rule) — half a contract check.
- Highest severity is a broken load reference: a `SKILL.md` spine that doesn't cite one of its phases means that phase never loads and the skill runs on its summary, not its method. It ranks above a dead flag or a missing config slot — those leave the method intact.
- A citation only counts if it resolves as a relative link from the citing file (`[name](../rules/name.md)` from inside `phases/`). A bare `rules/name` path is prose the loader never follows — a dangling reference in the same severity family as an orphaned rule.
- An open standard-point is a behavior-breaker, not a style nit: the skill still runs, but each executor fills the unpinned bar from its own priors, so runs diverge silently. The audit flags the openness — with the two divergent readings as evidence — and never proposes the bar's value.
- Slot placement is the judgment-heavy call and the one where a confident wrong verdict does the most damage (it tells a maintainer to move a file that was fine). Close calls go to the contract-skeptic critic before they reach the report.
- A clean audit still reports — "all checks passed" plus the checks that ran. Silence reads as a crash.
- A partial `--checks` run reports exactly its subset and says so; it never implies full coverage.
