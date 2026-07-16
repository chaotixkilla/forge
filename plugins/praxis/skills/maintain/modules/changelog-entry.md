# changelog-entry (`--changelog`)

Activated by `--changelog`, referenced from [review-and-record](../phases/05-review-and-record.md).

The base run leaves a clean diff and the record the project expects (a commit, a ticket update). This module adds one more deliverable: a **user-facing changelog / release-note entry** for the change, matching the project's existing changelog format and categorization. **Deletion test:** remove it and maintain still leaves the diff and the base record; the release-note entry is the added, flag-gated artifact.

## The delta

- **Match the project's existing changelog.** Detect how the project already keeps its changelog — the file and its location, the section/version structure, and the categorization it uses (e.g. added/changed/fixed/security-style groupings, or whatever the project's own history shows). Mirror that structure ([match-the-surrounding-code](../rules/match-the-surrounding-code.md) applied to the changelog); do not impose a format the project doesn't use.
- **Derive the entry from the diff and the intent, not the commit subject.** The commit subject is written for maintainers; the changelog entry is written for users of the software. State what changed *from the user's vantage* — the observable effect, the upgrade note, the fixed symptom — not the internal mechanics of how it was done.
- **When the project has no existing changelog,** don't invent house structure silently: propose a minimal entry and flag that the project has no established format for the maintainer to confirm, rather than picking one by fiat.

## Standard-point — the entry is a clean export

The changelog entry is a clean export for a human audience: it carries the change and its rationale and **nothing of the machinery** — no skill/phase/tool mechanics, no mention of maintain's process, no internal risk-tier or delegation vocabulary. A user reads what changed and why it matters to them; the fact that a maintenance skill produced it, and how, is stripped. `(basis: the ratified praxis clean-export standard for anything written for a human audience — the content and the decisions, never the process that produced them.)`
