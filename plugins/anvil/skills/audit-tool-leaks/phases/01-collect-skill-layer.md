The whole audit turns on one boundary: the skill layer names capabilities, the adapter layer names tools. So before you hunt for a single leak you have to know, file by file, which side of that line each file sits on — because a tool name inside an adapter is correct and a tool name anywhere above it is the bug. Get the collection wrong and the rest of the audit is wrong: miss a phase and a leak ships; sweep in an adapter and you flag the one place tools are *supposed* to live. This phase draws the line.

## Require a target

This is a plugin-level skill, so it needs a plugin to point at. If `--plugin` is absent, stop and ask — do not guess from the working directory or pick the first plugin you find. Auditing the wrong plugin produces a clean bill of health for code you never looked at, which is worse than no audit. The authoring kit is audited the same way: point `--plugin` at the kit like any other plugin. The kit must pass the rule it enforces, so auditing itself is a first-class path, not a special case.

## Enumerate the skill layer

The skill layer is everything in a skill that a maintainer reads as *instruction*: the `SKILL.md` (its description, its flag meanings, its phase spine), the `usage.md` — caller-facing docs are instruction too, and a tool name in a usage example pins the skill for every caller before a single phase runs — plus every body slot — `phases/`, `rules/`, and `modules/`. Walk every skill in the target plugin and gather all of these. Use the plugin explorer to enumerate and read them; it already knows a plugin's shape and returns findings anchored to file and line, which is exactly the anchoring later phases need to point a maintainer at an offending token.

Two slots beyond the skills also belong to the skill layer and are easy to forget:

- **Agent files** — explorers and critics. An explorer that says "read the change request from the tracker" has leaked just as surely as a phase that does; agents are instruction too. Scan the agent *body*, but **exclude the frontmatter `tools:` field** from the sweep the way `adapters/` is excluded: that field is the harness's mandated grant of platform primitives (`Read`, `Grep`, `WebSearch`, …), legitimate by location, and the swap test can't apply to a non-swappable primitive (the full account is in [legitimate-tool-mentions](../rules/legitimate-tool-mentions.md)).
- **Hook bodies**, where the plugin has them. A hook describes behavior at a lifecycle event in capability terms; a concrete tool baked into a hook is the same leak in a different file.

What you are building is a complete list of files where a tool name would be a violation. Completeness matters more than speed here — a leak in an un-read file is a leak that ships.

## Exclude the adapter layer — and only that

Deliberately exclude `adapters/` from the audit set. The adapter is the *single* place a concrete tool, transport, vendor, SDK call, or tool id is allowed to appear — that is its entire job. Flagging a tool name inside an adapter inverts the rule: it punishes the layer that exists precisely to absorb tool detail and keep it out of everything above. So `adapters/` is out of scope for leak detection, full stop.

Be precise about what "the adapter layer" means, though — exclude the adapter *files*, not every mention of the word. A phase that says "dispatch to the matching adapter" is skill-layer text about the seam and stays in scope; only the files under `adapters/` come out. One more legitimate-mention site is *not* an exclusion you make here: a provider name sitting in a config template's provider list is data, not instruction, and that file isn't part of the skill layer you're enumerating anyway. Don't add it to the audit set, and don't treat its absence as something to explain — it simply isn't skill-layer instruction. (The full account of where a tool name is legitimate lives in [legitimate-tool-mentions](../rules/legitimate-tool-mentions.md); this phase only needs to keep adapters out of the pile.)

Anti-pattern: scoping by file extension or a flat glob that rakes in `adapters/` and then leaning on the detection phase to "skip the adapter ones." That couples collection to detection, and the moment detection's judgment slips, an adapter gets flagged. Draw the boundary here, once, structurally — what you hand to the next phase should be *only* files where a tool name is a defect.

The output of this phase is that scoped set: every skill-layer file in the target, with adapters excluded, ready for the detection pass.
