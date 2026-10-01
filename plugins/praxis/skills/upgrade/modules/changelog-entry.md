# changelog-entry (`--changelog`)

Activated by `--changelog`, referenced from [commit-and-hand-off](../phases/05-commit-and-hand-off.md).

The base run leaves a clean, committed diff. This module adds one more deliverable: a **user-facing changelog / release-note entry** for the change, matching the project's existing changelog format and categorization. **Deletion test:** remove it and upgrade still leaves the diff and the base record; the release-note entry is the added, flag-gated artifact.

## The delta

- **Match the project's existing changelog.** Detect how the project already keeps its changelog — the file and its location, the section/version structure, and the categorization it uses (e.g. added/changed/fixed/security-style groupings, or whatever the project's own history shows). Mirror that structure ([match-the-surrounding-code](../../../craft/engineering/match-the-surrounding-code.md) applied to the changelog); do not impose a format the project doesn't use.
- **Derive the entry from the diff and the intent, not the commit subject.** The commit subject is written for maintainers; the changelog entry is written for users of the software. State what changed *from the user's vantage* — the observable effect, the upgrade note, the fixed symptom — not the internal mechanics of how it was done.
- **When the project has no existing changelog,** don't invent house structure silently: propose a minimal entry and flag that the project has no established format for the maintainer to confirm, rather than picking one by fiat.

## Standard-point — the entry is a clean export

The changelog entry is a clean export for a human audience: it carries the change and its rationale and **nothing of the machinery** — no skill/phase/tool mechanics, no mention of the upgrade's process, no internal risk-tier or delegation vocabulary. `(basis: praxis's ratified clean-export standard)`
