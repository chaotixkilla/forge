A plugin's skill pool is its architecture, and it's decided once, mostly up front, when changing it is cheapest. Get the carve wrong and every later skill inherits the wrong seams: responsibilities overlap, a flag does the work a skill should, or the pool sprawls into a feature checklist no one can hold in their head. This rule is the craft of carving a domain into a pool that's coherent, lean, and grows on demand — the method phase 1 leans on, and the method the scaffolding-skeptic checks the result against.

## Carve by responsibility, not by feature

A skill owns a *responsibility* — a coherent slice of the domain with a single reason to exist — not a feature. The difference is the failure mode: carve by feature and you get one skill per button the user might press, a pool that balloons past comprehension and duplicates logic across near-identical skills. Carve by responsibility and a handful of skills each cover a whole sub-domain, with variation handled *inside* a skill (an a-la-carte rule for craft, a flag-activated module for optional behavior) rather than as another skill.

The test for a single responsibility is the "and" test: state the skill's job in one sentence. If you need an "and" to join two unrelated jobs, it's two skills. If the "and" joins two facets of *one* job, it's one skill with internal structure. *"Open and track a change request"* is one responsibility (the change-request lifecycle); *"open a change request and send a chat message"* is two.

## Skill, module, flag, or phase — the placement ladder

Not every capability the interrogation surfaces deserves to be a pool entry. Run each candidate down this ladder, top to bottom, and place it at the first rung it matches:

- **Skill** — it's invoked for its own sake: someone asks for this outcome directly, and it produces its own output. Test: you could write its "when to use" without mentioning another skill's run. If describing when you'd reach for it always starts "while running X…", it's not a skill.
- **Module on an existing skill** — it's an optional extension of another skill's run: off by default, the base procedure completes without it, and a maintainer opts in *while* invoking that skill (an extra lens, an extra pass, a wider scope). Test: delete it and the parent still finishes its job.
- **Flag (a phase input)** — it merely selects among branches, windows, or defaults of behavior that runs regardless; the base procedure needs *some* choice here and the flag names which. A flag that names the default branch is a phase input, not a module — the classic trap is a selector that looks optional because it has a flag, but whose "off" state is just the same choice made implicitly.
- **Phase** — it only ever runs as a step inside one skill's sequence; no one asks for it alone. Test: if every realistic invocation is immediately preceded or followed by the same sibling capability, it's a step of that sibling's skill, not a peer.

The ladder is what keeps the pool from ballooning: most feature-shaped candidates land on the bottom three rungs. Counts alone never settle placement — the tests do.

## Split by altitude

Altitude is how broad a slice of the domain a skill governs, and a good pool has a deliberate spread of it rather than a flat list of same-size skills. Assign each surviving skill one of two bands: an **orchestrator** sequences other capabilities and owns a whole workflow's outcome; an **operation** does one concrete thing and owns one artifact or change. A healthy pool is mostly operations with a few orchestrators — the kit itself models the spread: a couple of marketplace-wide acts (publication, whole-catalog audit) over a floor of single-plugin operations.

Each band has its failure test. **Too high:** if the skill's one-line responsibility needs a follow-up question answered ("which part? on what input?") before an executor could start, it's a catch-all — split it until every line is startable as written. **Too low:** apply the phase rung of the placement ladder — a "skill" that only ever runs as someone else's step is noise in the pool. Altitude also fixes the parameter surface, so name it deliberately: a skill that governs one plugin takes its target as a parameter; a domain-wide skill takes none — that split is load-bearing, not cosmetic.

## Aim for roughly 8–12, and treat it as a seed

Roughly 8–12 capability skills is the target for an initial pool, and the band is a *symptom check*, not a quota. The real bar is twofold: the pool must be **reviewable as one page** — a maintainer holds the full list of names and one-line responsibilities in a single read — and it must **cover the domain's spine** — every recurring job in the domain routes to exactly one skill. Under ~8, suspect catch-alls: apply the too-high test to each entry. Over ~12, suspect feature-carving or a hidden second domain: apply the "and" test at the plugin level and the placement ladder to the excess. The kit's own pool of nine is the anchor: it covers author-audit-release end to end and reads in one screen. Critically, the pool is a *seed, not a spec* — a starter set grown via scaffold-skill and codify and pruned by dogfooding, never a frozen contract. Name the deferred skills in the design but don't scaffold them until they're earned; a lean pool you grow beats a wide one you prune.

## Name capabilities, never tools

Every skill in the pool is named and described as a *capability* — what it accomplishes — never a concrete tool, vendor, CLI, or transport. This is the hard rule the whole kit defends, applied at the moment of birth. *"Publish the artifact"* is a capability; the same skill named after a specific artifact backend is a leak that pins the plugin to one tool and breaks the moment a second consumer wants a different one. The concrete tool lives later, and only ever, in an adapter beneath the skill — the pool design must not anticipate it. A skill name that reads like a product name is the surest sign the carve has leaked.

## Defer pluggable backends to adapters and config, not the pool

When a capability routes to a backend a consumer chooses — a place to store artifacts, a provider for changes — that pluggability is *not* a skill in the pool and *not* a reason to multiply skills per provider. One capability skill names the need; the per-provider concrete work lives in adapters beneath it, and the consumer's choice lives in config. Designing one skill per backend ("publish-to-X", "publish-to-Y") is the classic carve error: it duplicates a single responsibility across tools and drags tool names into the pool. Keep the pool at the capability altitude and let the config layer and adapters absorb the variation.

## Run it past the skeptic before it's real

The pool design is finished only when each skill can defend its place against the scaffolding-skeptic's challenge: is this a genuine, present responsibility, or speculative structure for a need that hasn't arrived? The defense bar is concrete: a skill holds its place by naming a **specific first invocation** — who would run it, on what input, for what output, within the plugin's first real use. "We'll need it eventually" fails; "it completes the set" fails too — symmetry with the other skills is not a need. Cut anything that can't answer; cut means moved to the named-deferred list, not erased from the design. The cost of cutting here — deleting a line from a list — is the lowest it will ever be; every file, frontmatter field, and wire you'd add for a doomed skill is debt you avoid by killing it before it exists.
