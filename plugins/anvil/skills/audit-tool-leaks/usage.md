# audit-tool-leaks — usage

Scan a target plugin's skill layer for concrete tool/provider names that escaped the adapters — enforcing the hard rule that skills name only capabilities, tools live only in adapters.

## When to use
- You suspect a skill's SKILL.md, usage doc, phase, rule, module, or agent file has hard-coded a vendor, CLI, SDK call, connector id, or borrowed jargon where it should name a capability.
- Before releasing a plugin — this is one of the three preflight gates release runs, and the one that keeps the skill layer swappable across tools.
- After codifying or hand-authoring procedure, to catch tool names that crept in while writing steps a cold executor would act on.
- Auditing the authoring kit itself: the kit must pass the rule it enforces, so pointing `--plugin` at the kit is a first-class path, not a special case.
- You want the leaks not just found but fixed in place — rephrased to a capability, or relocated down into an adapter.

## Not for / use instead
- Checking frontmatter shape, flag↔module wiring, config-key coverage, or slot placement — that is the internal-contract audit, a different lens on the same plugin → audit-contract
- Checking the ships-vs-authoring boundary across the marketplace (a published plugin ships only its consumer files, never its authoring-only material) → audit-packaging
- Running a plugin's skills end-to-end to surface behavioral friction a static scan can't see → dogfood
- Adding the adapter that a relocation needs when no home exists yet — this skill hands off, it does not scaffold → add-component
- Rephrasing a leaked step's *procedure* rather than its tool name, or authoring the procedure from scratch → codify
- The full release flow (version bump, catalog entry, notes, tag); this audit is only its leak-detection gate → release

## Examples
`--plugin=<plugin>` — audit every skill-layer file in the target plugin for tool leaks; report inline, worst-first, adapters excluded from scope.
`--plugin=<plugin> --fix` — same scan, then apply each fix top-down: rephrase careless tool words to capability nouns, relocate tool-intrinsic detail into the matching adapter, then re-scan until clean.
`--plugin=<plugin> --report=artifact` — emit the identical ranked findings as a structured page instead of inline prose; reach for it when the list is long or needs sharing.
`--plugin=<plugin> --fix --report=artifact` — repair in place and deliver the before/after findings as an artifact.
`--plugin=anvil` — audit the kit against its own rule (the self-hosting check).

## Gotchas
- `--plugin` is required. With it absent the skill stops and asks — it will not guess from the working directory or grab the first plugin it finds; auditing the wrong plugin gives a clean bill of health for code never looked at.
- `adapters/` is deliberately out of scope. A tool name there is the design working, not a leak; the exclusion is drawn structurally at collection, not left to the detection pass to "skip." Config-template provider lists are data, not skill-layer instruction, and aren't gathered either.
- The judgment is the swap test, not a banned-word list: could this token be swapped for a different tool of the same kind without changing the sentence? Yes → capability, pass. No → leak. Ambiguous → resolve toward leak and rephrase.
- Watch the disguised leaks a mechanical sweep waves through: a capability verb welded to a concrete object ("open a change request in <the named tracker>"), a tool-only parameter dressed as a setting, and borrowed vendor jargon for a generic concept. A fluent-reading example that a cold executor would *act on* is a leak, not a mention.
- `--fix` cannot silently invent an adapter. A relocation needs an adapter home; if none exists it hands off to add-component to scaffold one, and if the capability isn't in the plugin's config at all it flag-and-stops that finding rather than dangle a broken contract.
- Under `--fix` the exit condition is a clean re-scan, not one pass — edits beget new candidates (a rephrase reaching for a tool-flavored word, a dispatch line that names the adapter), so detection loops over the edited files until a pass comes back empty. A span still dirty after two repair attempts is flag-and-stopped to the maintainer, not guessed at a third time.
- A clean audit is a real result: it reports what was scoped (which skills, adapters excluded) so "clean" reads as "clean across this," not silence.
