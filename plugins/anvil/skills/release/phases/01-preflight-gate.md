Releasing is the one act in the kit that exposes a plugin to consumers, and it's irreversible in the way that matters: once an entry lands in the catalog, someone can install whatever you pointed it at. So the first phase isn't release work at all — it's a refusal gate. Nothing here mutates the tree; everything here decides whether the rest of the skill is even allowed to run. A release that skips the gate to "save a step" is the failure mode this phase exists to prevent.

## Require a target

The skill is marketplace-level but it publishes *one* plugin, so `--plugin=<name>` is mandatory. If it's missing, stop and ask — do not guess from the working directory or the most-recently-touched plugin, because guessing the publish target is exactly the kind of silent assumption that ships the wrong thing. With the target named, resolve its plugin root under `plugins/<name>/` and confirm it exists; a `--plugin` that points at no such tree is a typo, not a release.

## Hard-block what must never ship

**Any plugin marked `--unpublished` is blocked from the catalog with no override** (the full reasoning lives in [release-gate](../rules/release-gate.md)). That marking is a declaration that the plugin is *in-development* — built but not yet meant for consumers; honor it. (An authoring kit or self-hosting plugin is not blocked on that basis — anvil ships; only the in-development marker gates.)

Detect the block *before* running anything expensive, and when you hit it, fail loud: name which rule fired and stop. There is no `--force`. If the maintainer genuinely means to publish a formerly-unpublished plugin, that's a deliberate change to the plugin's own posture made elsewhere — not a flag on this skill that waves the gate through.

## Run the three-audit quality gate

A plugin only earns the catalog by passing the kit's own quality gate — the three audits, run as preflight:

- the **packaging-boundary audit**, that the plugin ships only consumer-facing files and no authoring-only material has crept in;
- the **contract audit**, that frontmatter, flags↔modules, config keys, and slot placement are well-formed;
- the **tool-leak audit**, that the skill layer names only capabilities and every concrete tool stays in an adapter.

Delegate to each audit skill rather than re-implementing its checks — the audits own those checks, and this gate is just their conjunction. Any failure in any audit fails the gate: report the findings (anchored to file:line, as the audits return them) and stop. Do not proceed to bump or catalog on a partial pass. A plugin that can't pass its own gate isn't ready to ship — that's the whole principle, and the release skill is where it's enforced for real rather than on demand.

Edge case: if the maintainer narrowed the audits earlier in their session (e.g. ran a subset of contract checks), don't trust that as the release gate — the release gate runs the audits in full. The point of the gate is to be the one place that can't be partially satisfied.

## Under --dry-run

Still run the gate for real — the audits are read-only, so a dry run reports exactly the same pass/fail a live release would hit. Reporting "would release" while skipping the gate would make the dry run a lie about the most important decision in the skill. Run it, report the gate result, and only then continue into the dry-run previews of the later phases.
