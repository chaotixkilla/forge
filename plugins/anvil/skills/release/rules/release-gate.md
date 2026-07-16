The release gate exists because publishing is the only act in the kit a consumer can be harmed by. Every other skill writes inside the workshop, where a mistake is a maintainer's problem to fix; release writes the catalog, where a mistake is an *installed* problem in someone else's project. So the gate's whole posture is conservative-by-construction: it would rather refuse a good release than allow a bad one, and it has no escape hatch by design.

## The hard block — no override

**Any plugin marked `--unpublished` must never enter the catalog.** That marking is a deliberate declaration that the plugin is *in-development* — a tool the maintainer is still building, not something meant for consumers yet. Publishing it would put half-finished machinery into a consumer's project — at best confusing, at worst a way for someone to install something that was never meant to ship. (Being an authoring kit or self-hosting is *not* itself a block reason — anvil is a published plugin; only the in-development marker gates.) Release recognizes the block the same way audit-packaging does — by an **explicit in-development marker** (for a plugin born by this kit, a README status line; or an equivalent unpublished flag on the plugin), not by absence from the manifest alone. A plugin present on disk but absent from the manifest with **no** such marker is a **first publish**, not an in-development block: the release proceeds and phase 03 adds its catalog entry (this is exactly audit-packaging's "wrongly *absent* → release it or mark it unpublished" case, not the "wrongly *present*" one). Only the explicit marker stops a release cold; do not infer a block from unlisted-ness, or the gate deadlocks every plugin's first release.

Honor the declaration. A plugin's publish posture is a property the plugin owns; if it's genuinely meant to become public, that's a change made to the plugin itself, somewhere upstream of this skill — never a flag that tells release to ignore the block.

There is intentionally **no `--force`**. The moment a gate has an override, the override becomes the path of least resistance under deadline pressure, and the gate stops gating. If you find yourself wanting to bypass a block, the answer is to change what's being released or change the plugin's posture deliberately — not to wave the gate through. Fail loud, name the block that fired, and stop.

## The three audits must all pass

A plugin earns the catalog only by passing the kit's full quality gate as preflight: the packaging-boundary audit (it ships only consumer-facing files), the contract audit (frontmatter, flags↔modules, config keys, slot placement are well-formed), and the tool-leak audit (the skill layer names only capabilities; tools stay in adapters). These run in **full**, not as a subset — the release gate is precisely the place that can't be partially satisfied, even if the maintainer ran a narrowed audit earlier in the session.

The gate is a conjunction: any one audit failing fails the whole gate. Don't proceed to bump or catalog on a partial pass, and don't try to "fix forward" inside release — surface the findings the audits return (anchored to file:line) and stop, so the failure is fixed in the right skill and re-gated cleanly.

## Why this is the real enforcement point

The audits can be run any time, on demand, on a subset, for exploration. That's useful but it's advisory. The release gate is where the same checks become *binding*: the one moment where failing them actually prevents something. The principle underneath every block here is simple — **a plugin that can't pass its own gate isn't ready to ship.** The gate doesn't add new rules; it refuses to let a plugin out the door until the rules the kit already enforces are satisfied for real.
