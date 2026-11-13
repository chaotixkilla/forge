# Accessibility check

The evaluation, against WCAG 2.2, of the user-facing parts a change adds or alters, and whether they hold in every language they ship in.

## Reader and question

A reviewer of the change: "Can everyone use what changed, in every language it ships in?"

## Page

`on the communications-plan page`

## Membership

Each component, page and whole process the change adds or alters that people use, pages another organisation hosts that become part of the product's path included. Its subject is the task's user-facing change, so a task has one. It is filed again when an evaluated part changes or is evaluated again.

The page holds one target level, `AA` unless the decider names another, recorded on the page with who named it. Every finding is evaluated against it.

## Items

**Finding `A11Y`.** One evaluated component, page or process, with what its evaluation found.

- `scope`: enum `process`, `page`, `component`. A process conforms only when every step of it does. (basis: WCAG 2.2, conformance)
- `outcome`: enum `fail`, `pass`. `fail` when any criterion failed.
- `criteria`: list of text. Each success criterion evaluated at the page's target level, as `criterion: result (method)`. The result is `pass`, `fail` or `not applicable`; the method is `assistive technology`, `manual` or `automated`.
- `relies on`: list of text. The technologies the conformance relies on. (basis: WCAG 2.2, conformance claims)
- `locales`: list of text. The languages it was checked in: copy translated, nothing truncated or overlapping.
- `hosted by`: text. Who serves it, when not the project.

Agreement `none`, change regime `baseline`.

## Sections

1. **What fails?** Always. The failing list.
2. **What was checked, and how?** Always. The target level, then the evaluation table.

## Checks

*Computed:*
- The page records its target level.
- Every finding has its scope, outcome, at least one criterion with its result and method, what it relies on and its locales.
- A finding's outcome is `fail` exactly when one of its criteria failed.

*Judgment:*
- A page passed while a step of the process it belongs to fails. (basis: WCAG 2.2, whole processes)
- A pass resting only on automated checking for a criterion that needs a person or assistive technology.
- A user-facing page another organisation hosts left out.
- A locale the product ships in that wasn't checked.

## Views

- **Failing list:** `list` of `A11Y` whose outcome is `fail`, sorted by scope, processes first: criteria, locales, owner.
- **Evaluation table:** `table` of every `A11Y` grouped by scope: outcome, criteria, relies on, locales, hosted by.

## Minimum form

Each section keeps its heading with one line: nothing is evaluated yet, and who evaluates it.
