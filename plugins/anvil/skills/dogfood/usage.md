# dogfood — usage

Run a target plugin's own skills against itself (or a chosen subject) to prove they work end-to-end and surface the friction static audits can't see.

## When to use
- You want the *behavioral* counterpart to the audits: not "is this plugin shaped right?" but "does it actually run without stalling, guessing, or drifting from what its frontmatter promised?"
- A skill's decision forks, flag combinations, or external-capability dispatches only fail when exercised — you want to run them, not just read them.
- You're proving the kit self-hosts: the kit running its own skills on its own tree (`--self`), because if the kit's own authoring/audit skills can't operate on the kit, self-hosting is a slogan.
- You want a ranked worklist of concrete defects — each graded (blocker / friction / nit), pinned to the phase/rule/frontmatter that owns it, and routed to the skill that repairs it — not a pass/fail verdict.

## Not for / use instead
- Checking frontmatter shape, slot placement, flag↔module wiring, adapter coverage — the *static* internal contract, read not run → `audit-contract`
- Catching concrete tool/provider names that leaked out of adapters into the skill layer → `audit-tool-leaks`
- Verifying the ships-vs-authoring boundary across the marketplace (authoring-only files staying out of shipping plugins, any unpublished plugin staying out of the catalog) → `audit-packaging`
- Actually shipping a plugin — version bump, catalog entry, notes, tag (release *runs* the audits as a preflight gate; dogfood only *diagnoses*) → `release`
- Fixing the defects dogfood finds: re-resolving a stalled step or rephrasing a phase → `codify`; wiring a missing flag/module/adapter/agent → `add-component`; laying out a slot or skill that should exist and doesn't → `scaffold-skill` / `new-plugin`
- Dogfood writes no fixes — it produces the worklist; the routed authoring skills apply it.

## Examples
`--plugin=<plugin>` — dogfood a plugin by running its own skills against itself; the plugin proves its skills work by turning them on itself.
`--self` — target the kit itself as both tool and subject; the self-hosting proof, aimed reflexively at the skills that operate on skills.
`--plugin=<plugin> --subject=<path>` — run the plugin's skills against a *different* subject; use when the plugin under test has no meaningful self to author against and needs a real external operand.
`--self --report=artifact` — self-run with the dogfood log rendered as a durable, scannable page via the configured artifacts backend instead of a wall of inline text.
`--plugin=<plugin> --report=inline` — findings returned as ranked prose to the caller (the default).

## Gotchas
- Requires `--plugin` or `--self`. If neither is given the skill **stops and asks** — it will not default the subject, because a run against the wrong tree produces findings that look real and aren't.
- `--subject` overrides only the operand, not the tool: it's still `--plugin`'s skills doing the running, just against another tree.
- Run every scenario as a *cold executor* — never reach into your own context to fill a gap the skill left open. The instinct to be helpful destroys findings: an assumption you smooth over is a stall the next executor still hits.
- A run that never stalls can still fail. Everywhere the skill demands a judgment without pinning the bar, two cold runs diverge — the challenge phase's standards-skeptic critic hunts these open standards alongside the cold-executor's stalls.
- Pick scenarios by likelihood of breakage, not setup cost. The easiest skill to invoke (one linear phase, no flags, no external touch) is the least worth a scenario — its audit already told you what a run would. Aim at forks, high flag/slot count, and external-capability dispatches — and name, in the scenario list, the defect each scenario hunts; if you can't, it's a demo, not a scenario.
- The scenario set is **closed before the run**. Under `--self` the run can recurse (a scenario that invokes dogfood itself); a fork the challenge phase surfaces is recorded as a "not yet exercised" coverage note, never folded into the live pass.
- A reasonable guess is still a gap: demote every "I assumed the obvious default" back to "the skill doesn't state a default here." Separate the skill bug from the thin scenario by reading the declared contract — an unstated precondition is the skill's fault, an ignored declared one is the scenario's.
- Every finding must resolve to a slot file (phase+step, rule, frontmatter flag, or a wiring gap surfaced as a *capability*, never a tool name). A finding with no file pointer is an opinion, not a work item.
- **Agent recruitment needs the target loaded as a plugin, not just present on disk.** When the target's own explorers/critics aren't registered as spawnable types in the running session — the common case when the kit is dev-loaded to *build* the target and dogfood it in the same session — a scenario that should recruit those agents can only exercise the skill's **inline-fallback** lens, not real fan-out. The skill stays correct (it cites the agents and provides the fallback the audits check), but **composition coverage is partial**: a clean run proves the fallback path, not that recruitment works. Say so — record it as a "not yet exercised" coverage note rather than letting a green run read as full coverage — and to exercise real recruitment, run dogfood with the target loaded as a plugin.
- `--report` changes delivery only; the ranked findings, pointers, and fix-routing are identical inline or as an artifact.
