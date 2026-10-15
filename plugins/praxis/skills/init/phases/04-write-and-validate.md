## Write to the project config, preserving shape and version

Emit the config — on a re-run, the existing config with the resolved slots over it ([detect-environment](01-detect-environment.md)'s review) — with `praxis_version` set to the installed praxis's version from `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`, to `.claude/praxis.json` in the repository's main checkout, even when init runs from a worktree, since praxis reads its state there for every worktree. The main checkout is the parent of the folder `git rev-parse --git-common-dir` prints, read relative to where git ran, when that folder is named `.git`. Outside a repository, and when git's folder has another name (as a bare repository's, a submodule's or a separate git dir's usually does), it is the session's project folder, which is where praxis's hooks look too. Every `.claude/praxis.json` this skill names is that file. `(basis: maintainer, 2026-10-14)` One exception: when the main checkout has no config and the session's project folder holds one, as an older praxis set up in a subfolder, that file is the existing config. Read it there, write the result to the main checkout, and tell the user the old file can be removed; the hooks read it only until the main checkout has one. `(basis: derived from the hooks' same fallback)` Write it in the template's shape, carrying the `version` through unchanged. A full `init` run builds from the template shape filled with this run's resolved values, carrying every workspace service and recipe a run has proven unchanged.

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
neither the template's shape nor an older shape the ports read (below); a workspace service's or recipe's keys are the ones the workspace port's slot section names. A slot's, a knowledge source's or an audience space's `adapter` is recognized, as [resolve-tools](02-resolve-tools.md) allows it; a value other than `learned` is reported as an advisory, and the built adapter governs. Any write over an existing file, full
or scoped, carries each one into the written file unchanged and in the same place: at the top level, in
`tools`, in a slot, in `output`, or in a knowledge source, audience space or roster member the run keeps
(matched by `name`, or by `id` for a member). An entry that leaves the config, removed or renamed, takes its
keys with it, and the report names them as dropped with it. List each carried key in the closing report as
unread by this praxis. It is never a defect, so a config written by a newer praxis, or extended by hand,
stays usable under this one. `(basis: maintainer, 2026-10-02)`

**A scoped run merges, it does not overwrite.** When the run is scoped to one section (`--phase=<name>` or `init:<cap>`), the write is a read-modify-write against the *existing* file, not a fresh emit from the template — load the existing `praxis.json` as the base, replace only the resolved section, and write it back with every other slot and the version untouched. The mechanics and why the base must be the existing file (never the empty template) are in [single-phase](../modules/single-phase.md).

## Validate — what makes a config valid

A config is **valid** when every slot is *resolved* and the shape matches the template. A slot is resolved in exactly one of two ways:

- **configured** — a provider and transport are set (for knowledge, on each source; for workspace, `files` and `commands`, with provider, transport and setup only under `commands: container`), the capability's per-category fields are filled (or legitimately empty for an optional field), and `secret_ref` is set or empty per the transport.
- **deliberately disabled** — `provider: null`, marking a capability the project doesn't use ([resolve-tools](02-resolve-tools.md)). Valid, and legible to the downstream gate.

A slot is a **defect** when it is neither — specifically:

- it still holds an **un-replaced option-string placeholder** (a value still carrying the template's `provider-a | provider-b | …` menu that init never resolved to one choice), or
- a **required field is empty** on a configured (non-disabled) slot — its provider or transport is empty (for workspace, only under `commands: container`), or a *required-when-configured* per-category field is empty, per the classification in [resolve-tools](02-resolve-tools.md). An *optional-when-configured* field left empty is **not** a defect, or
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

## Keep praxis's state out of version control

The config and `.claude/praxis/` are the developer's own, never the project's: praxis is one developer's tool, and a teammate may not use it. A full run checks this after a successful write; when a defect blocks the write, a dry run's included, it reports the check not run. A scoped run doesn't, since it is usually a port's gate calling mid-task and its scope is one slot ([single-phase](../modules/single-phase.md)), and neither does a run outside a repository. `(basis: derived from those scopes)`

git is praxis's declared local version-control substrate, so these steps name its commands. `(basis: maintainer, 2026-10-01, reaffirmed 2026-10-15)`

1. From the main checkout, ask git whether it ignores the config and a path inside `.claude/praxis/` (`git check-ignore` on `.claude/praxis.json` and `.claude/praxis/acts/check.json`; a folder that doesn't exist yet still matches its rule), and whether it tracks the config (`git ls-files --error-unmatch .claude/praxis.json`). When git can't answer there, as when that folder isn't a work tree, report the check not run and why.
2. A tracked config stays tracked under any ignore rule, so it gets no offer: say it is tracked, and that taking it out of the index (`git rm --cached .claude/praxis.json`) is the user's to run, since it deletes the file for everyone who pulls. Never run it. `(basis: derived — an ignore rule can't untrack a file, and removing it from the index is a change to the shared repository)`
3. For each path neither ignored nor tracked, ask to add its rule, `**/.claude/praxis.json` or `**/.claude/praxis/`, to the user's global git ignore file: `core.excludesFile` when set, else `$XDG_CONFIG_HOME/git/ignore`, else `~/.config/git/ignore`. Name only the missing rules, append only those, create the file when absent, and never edit the project's `.gitignore`. A decline, or no answer, leaves everything as it is; the next full run asks again, since nothing records a decline. `(basis: maintainer, 2026-10-14, after how the harness keeps its own local settings file out of version control)`

A file-backed docs home inside the repository but outside `.claude/praxis/`, as an older praxis set by default, is flagged too: task documentation is never versioned, so offer it here, once, whether the setup review listed it or not: on a yes, set the home to the default in this same write and copy its files there once the write lands, leaving the repository's copies for the user to remove in a commit of their own, since removing versioned files is theirs to decide. `(basis: maintainer, 2026-10-14)`

Under `--degrade` the check still runs, nothing is offered and the global file is never written, since it is the user's own config. `(basis: derived from --degrade asking nothing)` Under `--dry-run` nothing is written either, and the report says which rules would be offered and to which file; with both flags, none would be.

## The standing postures reach every session without the project's instruction files

One setting governs work done outside a praxis run: `output.comments`, the standing posture for code comments, since most comments are written during ordinary editing. praxis's session-start guidance reads that posture from the config and states it in every session of the project, so init adds nothing to the project's instruction files and never offers to. `(basis: maintainer, 2026-09-30)` Removing stale praxis lines from them (next section) is a cleanup, not a way to carry a posture: it only takes text out, and only on the user's yes. `(basis: maintainer, 2026-10-02)`

## Offer to remove the stale instruction lines

When [detect-environment](01-detect-environment.md) staged stale instruction lines, list them grouped by file, each with its line number, its text and its class. A line goes whole, except that where it also carries text no class reaches, only the smallest whole clause or list item that carries the stale name or direction goes, shown in the list as the line before and after. An earlier init's block goes with its markers. What init does with the list turns on whether `.claude/praxis.json` existed when the run started, because once it exists praxis's edit guard refuses edits to project files outside the checkout's own `.claude/` while no act runs, and init runs none. `(basis: maintainer, 2026-10-02)`

- **First run (no config yet).** Before writing the config, ask once whether to remove them; the user may take all, none or some. Edit only on a yes, and only what was taken. Nothing else in the file changes, and no file is deleted. A decline, or no answer, leaves the files as they are.
- **Re-run (the config exists).** For a file outside the checkout's own `.claude/`, attempt no edit: hand the user its listed lines to remove themselves. A file inside it is offered and edited as on a first run.
- **Memory lines**, on either run, are offered and edited as on a first run, since the memory folder sits outside every checkout; removing a memory note removes its index line and its file together.
- **A line that sets up by hand what a capability now covers** is offered remove, keep or fold on either run, after the write lands, and dropped when its capability ended disabled or, for a container command, with `commands: host`. A fold writes the config field first; the line is then removed, from memory directly, or, in a project file outside the checkout's own `.claude/`, handed to the user to remove.

## Flag by kind — block on a defect, pass a disable

The validation pass sweeps for both placeholder kinds (un-replaced option-strings *and* empty required fields) and acts by kind:

- **A defect blocks the write** and is reported as such — a roster defect as much as a slot one — so no config persists that would mislead the gate into thinking an unresolved capability is configured, or route to a half-filled member. Report which slot or member and which field, so the fix is one targeted `--phase` away. `(basis: derived from the defect partition above)`
- **A deliberately-disabled slot passes** — `provider: null` is a resolved decision, written and reported as disabled, not flagged.
- **A non-object `output` section blocks the write** exactly as a slot defect does, reported with what was found; its fix is an edit to that section, since `output` isn't a `--phase` target. An out-of-domain value is reported, not blocked, and an absent or default-filled `output` passes silently.

Under `--degrade`, slots the run could not resolve without the user are written disabled (`provider: null`), so a headless run produces a *valid* config — narrower, never defective ([degrade-gracefully](../modules/degrade-gracefully.md)). Under `--dry-run`, run the full resolution and validation and render the would-be file with its validity verdict, but write nothing and trigger no secret side effect ([dry-run](../modules/dry-run.md)). Close the phase by reporting what was written (or would be), which slots are configured, which are disabled, any defect that blocked the write, the unrecognized keys carried, the stale instruction lines removed, declined, left to the user, or only listed, the workspace values left `unproven` and why, and the ignore check's outcome: rules added, declined or missing and not offered, already ignored, the config tracked, or not checked and why. Name the config's full path, and that praxis keeps the project's state beside it, since a session that started before the config existed has had no other word of it.
