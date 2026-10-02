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

**A key init doesn't recognize is carried and reported, never dropped.** A key is unrecognized when it is in
neither the template's shape nor an older shape the ports read (below). Any write over an existing file, full
or scoped, carries each one into the written file unchanged and in the same place: at the top level, in
`tools`, in a slot, in `output`, or in a knowledge source, audience space or roster member the run keeps
(matched by `name`, or by `id` for a member). An entry that leaves the config, removed or renamed, takes its
keys with it, and the report names them as dropped with it. List each carried key in the closing report as
unread by this praxis. It is never a defect, so a config written by a newer praxis, or extended by hand,
stays usable under this one. `(basis: maintainer, 2026-10-02)`

**A scoped run merges, it does not overwrite.** When the run is scoped to one section (`--phase=<name>` or `init:<cap>`), the write is a read-modify-write against the *existing* file, not a fresh emit from the template — load the existing `praxis.json` as the base, replace only the resolved section, and write it back with every other slot and the version untouched. The mechanics and why the base must be the existing file (never the empty template) are in [single-phase](../modules/single-phase.md).

## Validate — what makes a config valid

A config is **valid** when every slot is *resolved* and the shape matches the template. A slot is resolved in exactly one of two ways:

- **configured** — a provider and transport are set (for knowledge, on each source), the capability's per-category fields are filled (or legitimately empty for an optional field), and `secret_ref` is set or empty per the transport.
- **deliberately disabled** — `provider: null`, marking a capability the project doesn't use ([resolve-tools](02-resolve-tools.md)). Valid, and legible to the downstream gate.

A slot is a **defect** when it is neither — specifically:

- it still holds an **un-replaced option-string placeholder** (a value still carrying the template's `provider-a | provider-b | …` menu that init never resolved to one choice), or
- a **required field is empty** on a configured (non-disabled) slot — its provider or transport is empty, or a *required-when-configured* per-category field is empty, per the classification in [resolve-tools](02-resolve-tools.md). An *optional-when-configured* field left empty is **not** a defect, or
- two knowledge sources, or two audience spaces, **share a name**, or a source takes the name `artifacts-home`, which the knowledge port gives the home — a read or a publish that names one could reach either. `(basis: maintainer, 2026-10-01)`

`(basis: maintainer, 2026-07-05)`

A slot in an **older shape** — knowledge as a single provider/transport/root, artifacts with a per-type `destinations` map — is **valid**, because the ports read it as its current equivalent. A run that resolves such a slot writes it in the current shape, carrying its values over — the old `root` into the one source, `destinations.default` into `destination` — and reports any per-type entry it drops. `(basis: maintainer, 2026-10-01)`

The `teams: {}` empty map ([resolve-team](03-resolve-team.md)), `audiences: []`, and an optional per-category field left empty on a configured slot are **resolved, not defects** — the check must not flag them. init never persists the template's illustrative source or audience entry.

## The `output` section is validated by domain, not by slot shape

`output` is not a `tools.<cap>` slot (above), so neither the configured/disabled partition nor the
required-field rule reaches it. Validate it against its keys' value domains instead:

The four keys, the value domain of each, and which value is each one's default are defined in
[report-style-settings](../../../craft/writing/report-style-settings.md) — validate a written value against
the domains that rule names.

**Resolved (valid)** — everything the two defect cases below do not name. That includes the section
**absent entirely** (a config written before the section existed, valid because every consumer applies the
documented default for a key it cannot read), **default-filled**, an **empty object**, and **any key set to a
value inside its domain**. The defect list is the authoritative side of this partition; do not read the
examples here as its complement.

**A defect** in one case: `output` present but **not an object** (a scalar or a list where the section
belongs). A key set to a value **outside** its domain (`verbosity: "chatty"`, a string where `brief` takes
a boolean) is *not* a defect: report it with its allowed values, since every consumer applies the documented
default to a value it doesn't define and never halts on a style setting ([report-style-settings](../../../craft/writing/report-style-settings.md)). An **unrecognized key** inside `output` is carried and
reported like any other (above).

`(basis: derived from consumers' tolerance of an absent section)`

## The roster is validated leniently

`me`, `teams`, and `team[]` are **not** `tools.<cap>` slots the `config_requires` gate keys on — they are opportunistic context skills read to route reviews and address people, so a thin roster degrades a skill's routing, it doesn't block it. Validate them accordingly:

- **Resolved (valid):** an empty `me` (identity not yet established), an empty `team[]` (written `[]`), and `teams: {}` — the roster fills lazily via `--phase=team`. An empty roster is written as `team: []`; init does **not** persist the template's illustrative all-empty entry as if it were a member, so an all-blank entry never appears in a written config.
- **Defect:** internal inconsistency or a **partially-filled** member — `me` naming a `team[].id` no entry has, or a `team[]` entry with some **top-level** fields set and others empty (violating [resolve-team](03-resolve-team.md)'s fill-every-field rule). The fill-every-field test is on the entry's top-level fields (`id`, `name`, `role`, `owns`, `reviewer`, `timezone`, `handles`); an **empty `handles` sub-key** for a capability the person has no identity in is *resolved*, not a defect ([resolve-team](03-resolve-team.md)) — so do not fail a roster write because a non-engineer lacks a `handles.vcs`. Because an empty roster is `[]` and a real member has every top-level field filled, the only entry-level defect is a half-filled member — there is no option-string placeholder to look for in the roster, unlike a tools slot.

`(basis: derived from how the roster is read: opportunistically, never gated on)`

## The standing postures reach every session without the project's instruction files

One setting governs work done outside a praxis run: `output.comments`, the standing posture for code comments, since most comments are written during ordinary editing. praxis's session-start guidance reads that posture from the config and states it in every session of the project, so init adds nothing to the project's instruction files and never offers to. `(basis: maintainer, 2026-09-30)` Removing stale praxis lines from them (next section) is a cleanup, not a way to carry a posture: it only takes text out, and only on the user's yes. `(basis: maintainer, 2026-10-02)`

## Offer to remove the stale instruction lines

When [detect-environment](01-detect-environment.md) staged stale instruction lines, list them grouped by file, each with its line number, its text and its class. A line goes whole, except that where it also carries text no class reaches, only the smallest whole clause or list item that carries the stale name or direction goes, shown in the list as the line before and after. An earlier init's block goes with its markers. What init does with the list turns on whether `.claude/praxis.json` existed when the run started, because once it exists praxis's edit guard refuses edits to project files outside `.claude/` while no act runs, and init runs none. `(basis: maintainer, 2026-10-02)`

- **First run (no config yet).** Before writing the config, ask once whether to remove them; the user may take all, none or some. Edit only on a yes, and only what was taken. Nothing else in the file changes, and no file is deleted. A decline, or no answer, leaves the files as they are.
- **Re-run (the config exists).** For a file outside `.claude/`, attempt no edit: hand the user its listed lines to remove themselves. A file inside `.claude/` is offered and edited as on a first run.

## Flag by kind — block on a defect, pass a disable

The validation pass sweeps for both placeholder kinds (un-replaced option-strings *and* empty required fields) and acts by kind:

- **A defect blocks the write** and is reported as such — a roster defect as much as a slot one — so no config persists that would mislead the gate into thinking an unresolved capability is configured, or route to a half-filled member. Report which slot or member and which field, so the fix is one targeted `--phase` away. `(basis: derived from the defect partition above)`
- **A deliberately-disabled slot passes** — `provider: null` is a resolved decision, written and reported as disabled, not flagged.
- **A non-object `output` section blocks the write** exactly as a slot defect does, reported with what was found; its fix is an edit to that section, since `output` isn't a `--phase` target. An out-of-domain value is reported, not blocked, and an absent or default-filled `output` passes silently.

Under `--degrade`, slots the run could not resolve without the user are written disabled (`provider: null`), so a headless run produces a *valid* config — narrower, never defective ([degrade-gracefully](../modules/degrade-gracefully.md)). Under `--dry-run`, run the full resolution and validation and render the would-be file with its validity verdict, but write nothing and trigger no secret side effect ([dry-run](../modules/dry-run.md)). Close the phase by reporting what was written (or would be), which slots are configured, which are disabled, any defect that blocked the write, the unrecognized keys carried, and the stale instruction lines removed, declined, left to the user, or only listed.
