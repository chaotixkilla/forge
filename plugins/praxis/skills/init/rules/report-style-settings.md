# The report-style settings

A project can tune the shape of what praxis reports back to it — whether a report opens with an orienting
brief, whether a visual accompanies a structural change, how tightly each field is written, and when a code
comment earns its place. Those four settings live in the project config's `output` section, and they are read
by every skill whose output shape depends on one, plus the setup skill that validates them. That is the
problem this rule exists for: a setting whose meaning is defined in each reader separately drifts, so the same
value licenses a dense report in one skill and a sparse one in another, and a *missing* value gets filled from
whatever each reader guesses. Both failures are invisible in a single run and obvious across two. This rule is
the one home for what each value means and what to do when it cannot be read; it does not decide what acting
on a value looks like, which stays with the skill that owns the output.

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

`(basis: ratified by the maintainer, 2026-09-01 — the section, its four keys, and their defaults are the
maintainer's choice of a machine-readable style surface over prose preference or per-run flags. The
value-level definitions are the narrowest phrasing that makes each value's effect decidable without
prescribing the output it applies to; the no-dropping constraint on `verbosity` is the maintainer's
comparability requirement for pinned shapes, carried here so every consumer inherits it rather than
re-deriving it.)`

## An unreadable setting is not a decision to invent

Two cases, one posture: **apply the documented default, and never halt on a style setting.**

- **Absent** — the key is missing, the whole `output` section is (a config written before the section
  existed), or the section is present but not readable as a set of keys at all. Apply the default silently; this is the ordinary case, not a degradation, and a project that never
  touched the section is fully configured.
- **Out of domain** — the value is not one this rule defines. Apply the default *and say so* in the output,
  naming the key and the value found, so the project can correct it. Do not guess at what a near-miss meant,
  and do not fail the run: the work the skill was invoked for does not depend on the setting, and refusing to
  report because a style preference was misspelled trades the whole result for a typo.

`(basis: derived — the settings ship valid defaults precisely so that absence is a working state, which makes
silence correct for the absent case and wrong for the out-of-domain one: the first carries no information, the
second is a project trying to say something the reader could not parse. Surfacing rather than halting follows
from the settings being orthogonal to correctness — none of them changes what a skill concludes, only how it
says it.)`

## What this rule does not decide

It defines what the values mean, not what honoring them looks like. What a brief *contains*, the judgment of
when a visual is genuinely owed ([when-a-visual-is-owed](../../communicate/rules/when-a-visual-is-owed.md)), how tightly a
surviving sentence is written ([respect-the-readers-time](../../communicate/rules/respect-the-readers-time.md)), and the comment craft itself
each stay with their existing owner. A consumer reads its setting here and then applies its own craft; if this
rule ever seems to prescribe the output, the prescription belongs in the consuming skill instead.
