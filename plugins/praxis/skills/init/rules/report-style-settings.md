# The report-style settings

Four settings in the project config's `output` section tune the shape of what praxis reports back, and they
are read by every skill whose output shape depends on one, plus the setup skill that validates them. A setting
whose meaning is defined in each reader separately drifts, so the same value licenses a dense report in one
skill and a sparse one in another, and a *missing* value gets filled from whatever each reader guesses. This
rule is the one home for what each value means and what to do when it cannot be read.

## The four settings

Each setting's **first-listed value is its default** — the value that applies when the key, or the whole
section, is absent.

- **`brief`** — whether a report opens with an orienting brief before its substance.
  - `true` — the report leads with the brief.
  - `false` — it does not. A report's own record of what it covered is **never dropped** to honor this; a
    skill that folded such a record into its brief relocates it rather than losing it.
- **`diagrams`** — when a visual accompanies the prose.
  - `when-structural` — a visual is included where the change alters structure (a shape, a flow, a set of
    relationships) and prose alone would carry it worse.
  - `always` — include one wherever the subject admits a legible visual.
  - `never` — prose only.
- **`verbosity`** — how tightly each field of a pinned output shape is written.
  - `terse` — one line per field: the pinned minimum that still carries the decision.
  - `normal` — a field may run to a short paragraph where it genuinely carries more than one item.
  - Neither value may **drop** a field from a pinned shape. Verbosity tunes how much a field says, never which
    fields exist — a setting that could delete fields would make two runs' output incomparable, which is the
    property a pinned shape exists to provide.
- **`comments`** — the standing posture for code comments in authored or edited code.
  - `why-only` — a comment is written only where the code cannot carry the meaning itself.
  - `match-codebase` — comment density follows the surrounding file.

`(basis: maintainer, 2026-09-01)`

## An unreadable setting is not a decision to invent

Two cases, one posture: **apply the documented default, and never halt on a style setting.**

- **Absent** — the key is missing, the whole `output` section is (a config written before the section
  existed), or the section is present but not readable as a set of keys at all. Apply the default silently; this is the ordinary case, not a degradation, and a project that never
  touched the section is fully configured.
- **Out of domain** — the value is not one this rule defines. Apply the default *and say so* in the output,
  naming the key and the value found, so the project can correct it. Do not guess at what a near-miss meant,
  and do not fail the run: the work the skill was invoked for does not depend on the setting.

`(basis: derived from the shipped defaults)`

## What this rule does not decide

It defines what the values mean, not what honoring them looks like. What a brief *contains*, the judgment of
when a visual is genuinely owed ([when-a-visual-is-owed](../../../craft/writing/when-a-visual-is-owed.md)), how tightly a
surviving sentence is written ([respect-the-readers-time](../../../craft/writing/respect-the-readers-time.md)), and the comment craft itself
each stay with their existing owner. A consumer reads its setting here and then applies its own craft; if this
rule ever seems to prescribe the output, the prescription belongs in the consuming skill instead.
