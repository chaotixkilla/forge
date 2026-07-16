The written file is the source of truth every other praxis skill's config gate keys on. This phase commits the resolved values to disk in the template's exact shape, then validates that what it wrote is actually usable — because a config that *looks* filled but still holds a placeholder is worse than no config: the gate reads it as present and a downstream skill talks to a backend that isn't there. The phase has two jobs: write the right file the right way (a full write, or a surgical merge for a scoped run), and define precisely what "a valid config" means so the check can pass or fail without a judgment call.

## Write to the project config, preserving shape and version

Emit the config to `${CLAUDE_PROJECT_DIR}/.claude/praxis.json`, in the template's shape, carrying the `version` through unchanged. A full `init` run builds from the template shape filled with this run's resolved values.

**A scoped run merges, it does not overwrite.** When the run is scoped to one section (`--phase=<name>` or `init:<cap>`), the write is a read-modify-write against the *existing* file, not a fresh emit from the template — load the existing `praxis.json` as the base, replace only the resolved section, and write it back with every other slot and the version untouched. The mechanics and why the base must be the existing file (never the empty template) are in [single-phase](../modules/single-phase.md); the hazard it prevents is a scoped run silently clobbering the six slots it wasn't asked about.

## Validate — what makes a config valid

A config is **valid** when every slot is *resolved* and the shape matches the template. A slot is resolved in exactly one of two ways:

- **configured** — a provider and transport are set, the capability's per-category fields are filled (or legitimately empty for an optional field), and `secret_ref` is set or empty per the transport.
- **deliberately disabled** — `provider: null`, marking a capability the project doesn't use ([resolve-tools](02-resolve-tools.md)). Valid, and legible to the downstream gate.

A slot is a **defect** when it is neither — specifically:

- it still holds an **un-replaced option-string placeholder** (a value still carrying the template's `provider-a | provider-b | …` menu that init never resolved to one choice), or
- a **required field is empty** on a configured (non-disabled) slot — its provider or transport is empty, or a *required-when-configured* per-category field is empty (`knowledge.root`, `project_mgmt.project_key`), per the classification in [resolve-tools](02-resolve-tools.md). An *optional-when-configured* field left empty (an `artifacts.destinations` entry) is **not** a defect.

`(basis: ratified by the maintainer, 2026-07-05. The valid/defect line — resolved (configured or provider:null) is valid; a leftover placeholder or an empty required field on a non-disabled slot is a defect — is the maintainer's ratified acceptance standard; it is the contract the config_requires gate depends on, so it is pinned here rather than left to the run. Which per-category fields count as required-when-configured is fixed in [resolve-tools](02-resolve-tools.md) by the discriminator "the consumer cannot use the capability at all without it.")`

The `teams: {}` empty map and an optional per-category field left empty on a configured slot are **resolved, not defects** ([resolve-team](03-resolve-team.md)) — the check must not flag them.

## The roster is validated leniently

`me`, `teams`, and `team[]` are **not** `tools.<cap>` slots the `config_requires` gate keys on — they are opportunistic context skills read to route reviews and address people, so a thin roster degrades a skill's routing, it doesn't block it. Validate them accordingly:

- **Resolved (valid):** an empty `me` (identity not yet established), an empty `team[]` (written `[]`), and `teams: {}` — the roster fills lazily via `--phase=team`. An empty roster is written as `team: []`; init does **not** persist the template's illustrative all-empty entry as if it were a member, so an all-blank entry never appears in a written config.
- **Defect:** internal inconsistency or a **partially-filled** member — `me` naming a `team[].id` no entry has, or a `team[]` entry with some **top-level** fields set and others empty (violating [resolve-team](03-resolve-team.md)'s fill-every-field rule). The fill-every-field test is on the entry's top-level fields (`id`, `name`, `role`, `owns`, `reviewer`, `timezone`, `handles`); an **empty `handles` sub-key** for a capability the person has no identity in is *resolved*, not a defect ([resolve-team](03-resolve-team.md)) — so do not fail a roster write because a non-engineer lacks a `handles.vcs`. Because an empty roster is `[]` and a real member has every top-level field filled, the only entry-level defect is a half-filled member — there is no option-string placeholder to look for in the roster, unlike a tools slot.

`(basis: derived — the roster is not a backend the gate blocks on; it is read opportunistically, so validating it as strictly as a tools slot would block init on information no environment holds and no downstream skill hard-requires. A missing owner degrades review routing; it does not stop the config from being usable.)`

## Flag by kind — block on a defect, pass a disable

The validation pass sweeps for both placeholder kinds (un-replaced option-strings *and* empty required fields) and acts by kind:

- **A defect blocks the write** and is reported as such — do not persist a config that would mislead the gate into thinking an unresolved capability is configured. Report which slot and which field, so the fix is one targeted `--phase` away.
- **A deliberately-disabled slot passes** — `provider: null` is a resolved decision, written and reported as disabled, not flagged.

Under `--degrade`, slots the run could not resolve without the user are written disabled (`provider: null`), so a headless run produces a *valid* config — narrower, never defective ([degrade-gracefully](../modules/degrade-gracefully.md)). Under `--dry-run`, run the full resolution and validation and render the would-be file with its validity verdict, but write nothing and trigger no secret side effect ([dry-run](../modules/dry-run.md)). Close the phase by reporting what was written (or would be), which slots are configured, which are disabled, and any defect that blocked the write.
