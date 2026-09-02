The written file is the source of truth every other praxis skill's config gate keys on. This phase commits the resolved values to disk in the template's exact shape, then validates that what it wrote is actually usable — because a config that *looks* filled but still holds a placeholder is worse than no config: the gate reads it as present and a downstream skill talks to a backend that isn't there. The phase has two jobs: write the right file the right way (a full write, or a surgical merge for a scoped run), and define precisely what "a valid config" means so the check can pass or fail without a judgment call.

## Write to the project config, preserving shape and version

Emit the config to `${CLAUDE_PROJECT_DIR}/.claude/praxis.json`, in the template's shape, carrying the `version` through unchanged. A full `init` run builds from the template shape filled with this run's resolved values.

**The `output` section is carried, not resolved.** `output` tells consuming skills how to shape their
reports; it is not a capability slot — no provider, no transport, no credential — and nothing in the
environment can infer a style preference. So the default posture does **not** ask about it: carry the
template's defaults through unchanged, exactly as `version` is carried (`--degrade` carries them too — there
is nothing to disable). `--guide` is the one posture that walks the four settings
([guided-walkthrough](../modules/guided-walkthrough.md)); otherwise a user wanting a non-default sets the
value in `.claude/praxis.json` directly, since each key is a plain scalar with a documented domain (below).
`output` is deliberately **not** a `--phase` target — it is not a phase, and putting four questions in front
of every run would spend the user's attention on settings that already carry working defaults. `(basis:
derived — the section ships pre-filled valid defaults rather than option-string menus precisely so that no
resolution step is owed; asking anyway would contradict that choice and buy no information, since no
environment signal exists to confirm against.)`

**An existing config's `output` values win over the template's defaults.** A full run must not reset style
the user already chose: read the existing `.claude/praxis.json` first, keep every `output` key it already
sets, and fill only the keys it lacks from the template — so re-running `init` never silently reverts a
hand-edited setting. A scoped run leaves the section exactly as it found it, **absent included**: `output` is
not a scoped target, so a scoped run neither backfills nor rewrites it. `(basis: derived — the section's whole
premise is that its values come from the user and not the environment, so a run that re-derived them from the
template would destroy the only signal that exists; this is the read-modify-write discipline the scoped-merge
rule below already applies to slots, extended to the one section no run resolves.)`

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

## The `output` section is validated by domain, not by slot shape

`output` is not a `tools.<cap>` slot (above), so neither the configured/disabled partition nor the
required-field rule reaches it. Validate it against its keys' value domains instead:

The four keys, the value domain of each, and which value is each one's default are defined in
[report-style-settings](../rules/report-style-settings.md) — validate a written value against
the domains that rule names. It is the single home for their meaning; do not restate the domains here, or the
validator and its consumers will drift apart on what a value licenses.

**Resolved (valid)** — everything the two defect cases below do not name. That includes the section
**absent entirely** (a config written before the section existed, valid because every consumer applies the
documented default for a key it cannot read), **default-filled**, an **empty object**, and **any key set to a
value inside its domain**. The defect list is the authoritative side of this partition; do not read the
examples here as its complement.

**A defect** in two cases: `output` present but **not an object** (a scalar or a list where the section
belongs), or a key set to a value **outside** its domain (`verbosity: "chatty"`, a string where `brief` takes
a boolean). An **unrecognized key** inside `output` is *not* a defect — report it as
ignored and carry it through the write untouched, so a config written by a newer praxis stays usable under an
older one.

`(basis: derived — the section ships valid defaults and consumers must tolerate its absence, so the only
state that can actually mislead a consumer is a value it cannot interpret; that is the whole defect line, and
it is the narrowest one that still holds the constraint that no existing config becomes invalid. The
capability-slot valid/defect line ratified 2026-07-05 is untouched by this — it governs `tools.<cap>`, and
this section is not one.)`

## The roster is validated leniently

`me`, `teams`, and `team[]` are **not** `tools.<cap>` slots the `config_requires` gate keys on — they are opportunistic context skills read to route reviews and address people, so a thin roster degrades a skill's routing, it doesn't block it. Validate them accordingly:

- **Resolved (valid):** an empty `me` (identity not yet established), an empty `team[]` (written `[]`), and `teams: {}` — the roster fills lazily via `--phase=team`. An empty roster is written as `team: []`; init does **not** persist the template's illustrative all-empty entry as if it were a member, so an all-blank entry never appears in a written config.
- **Defect:** internal inconsistency or a **partially-filled** member — `me` naming a `team[].id` no entry has, or a `team[]` entry with some **top-level** fields set and others empty (violating [resolve-team](03-resolve-team.md)'s fill-every-field rule). The fill-every-field test is on the entry's top-level fields (`id`, `name`, `role`, `owns`, `reviewer`, `timezone`, `handles`); an **empty `handles` sub-key** for a capability the person has no identity in is *resolved*, not a defect ([resolve-team](03-resolve-team.md)) — so do not fail a roster write because a non-engineer lacks a `handles.vcs`. Because an empty roster is `[]` and a real member has every top-level field filled, the only entry-level defect is a half-filled member — there is no option-string placeholder to look for in the roster, unlike a tools slot.

`(basis: derived — the roster is not a backend the gate blocks on; it is read opportunistically, so validating it as strictly as a tools slot would block init on information no environment holds and no downstream skill hard-requires. A missing owner degrades review routing; it does not stop the config from being usable.)`

## Offer to project the standing postures into the project's context file

The config is read by praxis skills when they run; it has no reach into the work the harness does *outside* a praxis run. One setting needs that reach: `output.comments` states a standing posture for code comments, and most comments are written during ordinary editing rather than inside a praxis skill, so a setting only praxis reads cannot govern them. After the config is written and valid, close that gap by **offering** to project the standing postures into the project's `CLAUDE.md`, the file the harness loads as standing context for every session here.

- **Offer it; never write it silently.** This edits a file the project owns and praxis does not, so it is proposed for confirmation like any inferred value, under the run's posture ([confirm-dont-assume-defaults](../rules/confirm-dont-assume-defaults.md)). `--degrade` **skips** it — there is nobody to ask, and an unrequested edit to a project's standing context is not a safe headless default. `--guide` explains what the stanza does before proposing it ([guided-walkthrough](../modules/guided-walkthrough.md)).
- **Project only what the config cannot reach.** The stanza carries the standing postures that govern work outside a praxis run — today that is `output.comments` alone — plus one line naming `.claude/praxis.json` as the source of truth. It does **not** restate the tools map, the roster, or the settings praxis reads for itself; a second copy of those drifts, and the config is already authoritative for every consumer able to read it.
- **Delimit it so a re-run replaces rather than appends.** Write the stanza between stable markers and, on any later run, replace what lies between them. Everything outside the markers belongs to the project and is never touched. The shape, so two runs produce the same file:

  ```
  <!-- praxis:begin -->
  ## praxis
  Code comments: why-only — write one only where the code cannot carry the meaning itself.
  Configured in `.claude/praxis.json`, which is the source of truth for this and every other praxis setting.
  <!-- praxis:end -->
  ```

- **Project scope only, never user scope.** The posture is a property of *this* project's config; writing it to a user-level context file would apply one project's choice to every other project that user touches.
- **No file, no assumption.** Where the project has no `CLAUDE.md`, offer to create one holding only the stanza, and treat a decline as a resolved answer — the config is valid and complete without it. The projection is a convenience, not a requirement, and never a defect — the validity check above does not consider it.

`(basis: ratified by the maintainer, 2026-09-01 — that init should write into the project's context file, at project scope, is the maintainer's request. What the stanza carries is derived from the settings-carrier decision made the same day: praxis.json was chosen as the single config home, whose accepted cost is that its values only bind inside a praxis run. Projecting exactly the postures that must outlive a run — and nothing the config already governs — closes that gap without creating the second home the decision was meant to avoid.)`

## Flag by kind — block on a defect, pass a disable

The validation pass sweeps for both placeholder kinds (un-replaced option-strings *and* empty required fields) and acts by kind:

- **A defect blocks the write** and is reported as such — do not persist a config that would mislead the gate into thinking an unresolved capability is configured. Report which slot and which field, so the fix is one targeted `--phase` away.
- **A deliberately-disabled slot passes** — `provider: null` is a resolved decision, written and reported as disabled, not flagged.
- **An out-of-domain `output` value blocks the write** exactly as a slot defect does, reported with the key and its allowed values — a consumer handed a value it cannot interpret has no defined behavior to fall back on. An absent or default-filled `output` passes silently.

Under `--degrade`, slots the run could not resolve without the user are written disabled (`provider: null`), so a headless run produces a *valid* config — narrower, never defective ([degrade-gracefully](../modules/degrade-gracefully.md)). Under `--dry-run`, run the full resolution and validation and render the would-be file with its validity verdict, but write nothing and trigger no secret side effect ([dry-run](../modules/dry-run.md)). Close the phase by reporting what was written (or would be), which slots are configured, which are disabled, and any defect that blocked the write.
