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
of every run would spend the user's attention on settings that already carry working defaults.
`(basis: derived from the section's shipped defaults)`

**An existing config's `output` values win over the template's defaults.** A full run must not reset style
the user already chose: read the existing `.claude/praxis.json` first, keep every `output` key it already
sets, and fill only the keys it lacks from the template — so re-running `init` never silently reverts a
hand-edited setting. A scoped run leaves the section exactly as it found it, **absent included**: `output` is
not a scoped target, so a scoped run neither backfills nor rewrites it.
`(basis: derived from the scoped-merge rule's read-modify-write discipline)`

**A scoped run merges, it does not overwrite.** When the run is scoped to one section (`--phase=<name>` or `init:<cap>`), the write is a read-modify-write against the *existing* file, not a fresh emit from the template — load the existing `praxis.json` as the base, replace only the resolved section, and write it back with every other slot and the version untouched. The mechanics and why the base must be the existing file (never the empty template) are in [single-phase](../modules/single-phase.md).

## Validate — what makes a config valid

A config is **valid** when every slot is *resolved* and the shape matches the template. A slot is resolved in exactly one of two ways:

- **configured** — a provider and transport are set, the capability's per-category fields are filled (or legitimately empty for an optional field), and `secret_ref` is set or empty per the transport.
- **deliberately disabled** — `provider: null`, marking a capability the project doesn't use ([resolve-tools](02-resolve-tools.md)). Valid, and legible to the downstream gate.

A slot is a **defect** when it is neither — specifically:

- it still holds an **un-replaced option-string placeholder** (a value still carrying the template's `provider-a | provider-b | …` menu that init never resolved to one choice), or
- a **required field is empty** on a configured (non-disabled) slot — its provider or transport is empty, or a *required-when-configured* per-category field is empty (`knowledge.root`, `project_mgmt.project_key`), per the classification in [resolve-tools](02-resolve-tools.md). An *optional-when-configured* field left empty (an `artifacts.destinations` entry) is **not** a defect.

`(basis: maintainer, 2026-07-05)`

The `teams: {}` empty map and an optional per-category field left empty on a configured slot are **resolved, not defects** ([resolve-team](03-resolve-team.md)) — the check must not flag them.

## The `output` section is validated by domain, not by slot shape

`output` is not a `tools.<cap>` slot (above), so neither the configured/disabled partition nor the
required-field rule reaches it. Validate it against its keys' value domains instead:

The four keys, the value domain of each, and which value is each one's default are defined in
[report-style-settings](../rules/report-style-settings.md) — validate a written value against
the domains that rule names.

**Resolved (valid)** — everything the two defect cases below do not name. That includes the section
**absent entirely** (a config written before the section existed, valid because every consumer applies the
documented default for a key it cannot read), **default-filled**, an **empty object**, and **any key set to a
value inside its domain**. The defect list is the authoritative side of this partition; do not read the
examples here as its complement.

**A defect** in one case: `output` present but **not an object** (a scalar or a list where the section
belongs). A key set to a value **outside** its domain (`verbosity: "chatty"`, a string where `brief` takes
a boolean) is *not* a defect: report it with its allowed values, since every consumer applies the documented
default to a value it doesn't define and never halts on a style setting ([report-style-settings](../rules/report-style-settings.md)). An **unrecognized key** inside `output` is *not* a defect — report it as
ignored and carry it through the write untouched, so a config written by a newer praxis stays usable under an
older one.

`(basis: derived from consumers' tolerance of an absent section)`

## The roster is validated leniently

`me`, `teams`, and `team[]` are **not** `tools.<cap>` slots the `config_requires` gate keys on — they are opportunistic context skills read to route reviews and address people, so a thin roster degrades a skill's routing, it doesn't block it. Validate them accordingly:

- **Resolved (valid):** an empty `me` (identity not yet established), an empty `team[]` (written `[]`), and `teams: {}` — the roster fills lazily via `--phase=team`. An empty roster is written as `team: []`; init does **not** persist the template's illustrative all-empty entry as if it were a member, so an all-blank entry never appears in a written config.
- **Defect:** internal inconsistency or a **partially-filled** member — `me` naming a `team[].id` no entry has, or a `team[]` entry with some **top-level** fields set and others empty (violating [resolve-team](03-resolve-team.md)'s fill-every-field rule). The fill-every-field test is on the entry's top-level fields (`id`, `name`, `role`, `owns`, `reviewer`, `timezone`, `handles`); an **empty `handles` sub-key** for a capability the person has no identity in is *resolved*, not a defect ([resolve-team](03-resolve-team.md)) — so do not fail a roster write because a non-engineer lacks a `handles.vcs`. Because an empty roster is `[]` and a real member has every top-level field filled, the only entry-level defect is a half-filled member — there is no option-string placeholder to look for in the roster, unlike a tools slot.

`(basis: derived from how the roster is read: opportunistically, never gated on)`

## The standing postures reach every session without CLAUDE.md

One setting governs work done outside a praxis run: `output.comments`, the standing posture for code comments, since most comments are written during ordinary editing. praxis's session-start guidance reads that posture from the config and states it in every session of the project, so init writes nothing to `CLAUDE.md` and never offers to. `(basis: maintainer, 2026-09-30)`

## Flag by kind — block on a defect, pass a disable

The validation pass sweeps for both placeholder kinds (un-replaced option-strings *and* empty required fields) and acts by kind:

- **A defect blocks the write** and is reported as such — do not persist a config that would mislead the gate into thinking an unresolved capability is configured. Report which slot and which field, so the fix is one targeted `--phase` away.
- **A deliberately-disabled slot passes** — `provider: null` is a resolved decision, written and reported as disabled, not flagged.
- **A non-object `output` section blocks the write** exactly as a slot defect does, reported with what was found; its fix is an edit to that section, since `output` isn't a `--phase` target. An out-of-domain value is reported, not blocked, and an absent or default-filled `output` passes silently.

Under `--degrade`, slots the run could not resolve without the user are written disabled (`provider: null`), so a headless run produces a *valid* config — narrower, never defective ([degrade-gracefully](../modules/degrade-gracefully.md)). Under `--dry-run`, run the full resolution and validation and render the would-be file with its validity verdict, but write nothing and trigger no secret side effect ([dry-run](../modules/dry-run.md)). Close the phase by reporting what was written (or would be), which slots are configured, which are disabled, and any defect that blocked the write.
