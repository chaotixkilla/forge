# apply-fixes (`--fix`)

Activated by `--fix`, referenced from [deliver-findings](../phases/06-deliver-findings.md).

The base review reports findings and stops; the author applies them. This module extends the run past reporting: apply the accepted findings to the working tree as edits. Deletion test: remove it and review still produces its findings; applying them is optional behavior a flag turns on, which is why it is a module.

## The delta

- **Apply only the auto-applicable findings.** A finding is auto-applicable when it carries a concrete, least-invasive fix ([prefer-the-smaller-suggestion](../rules/prefer-the-smaller-suggestion.md)) and is confident enough to apply without the author's judgment (confirmed, or probable with an unambiguous fix — per [calibrate-confidence-to-effort](../rules/calibrate-confidence-to-effort.md)). A design-level finding, or one whose fix is a real decision the author owns, is **not** auto-applied — it is reported for the author to act on, exactly as in the base. Applying a sprawling or speculative fix is how `--fix` introduces a new bug; hold the line at small, certain edits.

  `(basis: ratified by the maintainer, 2026-07-02. The auto-apply cutoff = confirmed, or probable with an unambiguous fix; speculative and design-level findings are never auto-applied. Editing the tree unattended is consequential, so the cutoff is the maintainer's ratified house standard.)`
- **Report what was applied and what was left.** The run's record distinguishes the findings it edited from the findings it left for the author, so the outcome is auditable and nothing is silently "fixed."

## Re-check each fix at its site

After each edit, re-check it *at the site*: re-read the edited region and confirm the finding's failing scenario is now resolved and the edit introduced no obvious new local break (a dangling reference, a now-unreachable branch, a changed signature whose callers you must revisit).

`(basis: ratified by the maintainer, 2026-07-02. The re-check depth — this module re-checks each fix at its edit site (scenario resolved + no new local break) but does not run the test suite or drive the app; deeper end-to-end confirmation hands off to a separate verify pass. The site-level line is the maintainer's ratified house standard.)`

The boundary is deliberate: review reads and edits; it does not build or run. A fix that needs the app exercised to be trusted is a hand-off, not a step review absorbs.
