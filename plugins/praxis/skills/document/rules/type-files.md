# Type files

A type that says only where it files leaves its content to each run's average practice. One run's threat model then analyses flows and stops, and another's ranks nothing. A type file says what its pages hold, for whom, and how a page is known to be good enough.

## What is a type

A type is a document the [documentation-plan](../../../craft/writing/documentation-plan.md) names as owed, such as a threat model or a cutover plan, or one a kit row or an act names, such as a review record. Within a type, a piece that passes [items-and-agreements](items-and-agreements.md)'s granularity test is an item of one of its kinds: a threat, a go/no-go card, an acceptance criterion. Anything else is a section.

## What a type file holds

In this order, each present unless marked optional:

1. **One sentence** on what the type is.
2. **Reader and question.** Every page has the reader [shape-the-document](../phases/02-shape-the-document.md) names. This line names the roles that reader takes here, from a fixed set: new engineer, reviewer, decider, support, on-call, auditor, maintainer. It also names the one question the type answers for them, in their words. A page whose line names several roles is listed under each. (basis: maintainer, 2026-11-11, the paths per role)
3. **Page.** One of:
   - `own page`;
   - `on the <type> page`;
   - `on the <type> page at task scale, own page at an epic`.

   A host is always an own-page type, and lists the section a guest fills in its own Sections. A guest whose host isn't owed, or whose host's page this round didn't file, takes its own page. Its headings become subsections of the host's section. Which types share a page follows from the types the plan owes and these lines. (basis: maintainer, 2026-11-11, the plan deciding page sharing through the types it owes)
4. **Membership.** What belongs on a page of this type and what doesn't. What makes two filings the same document, which is its subject. And when it is filed again. A type that files more than one page per task names the field on its kinds that holds a page's subject, and every view and computed check on its pages filters on it with `is page subject`.
5. **Items.** The type's item kinds, each declared as [items-and-agreements](items-and-agreements.md)'s "What a type declares" lists. Only the kind's own fields are listed; the fields every item carries are implied. A kind is declared by exactly one type file, its home. Another type that shows items of that kind names the kind and its home, and declares nothing. When the home isn't owed, the kind's items stand on the first owed type that shows them, in the order this catalogue lists types. A type with no part a reader would cite on its own declares one kind for the whole page.
6. **Sections.** In reading order, the conclusion first. For each:
   - its heading, as written on every page: a question its reader asks, never the type's name;
   - whether it is always present, or present when a condition holds, naming the condition;
   - what it shows: the item kinds it carries and in what form (a view's presentation from [portable-tree-shape](portable-tree-shape.md), a list, or prose), or the prose it holds. A section that shows one item without naming a view writes it as prose from the item's body and fields.
7. **Checks.**
   - *Computed:* facts a script can establish from the items and the tree, which block publishing. Each is particular to the type, since the findings [items-and-agreements](items-and-agreements.md) lists apply to every type already. Each must be satisfiable at the type's due point: a spec due before the build can't require that each requirement is verified by a test.
   - *Judgment:* ways a page of this type could fail, phrased as the failure, such as "a threat with no response" or "a requirement no one could test". They prompt a review of the page and never block.
   - Each check names its source when one exists. Their number is open by design: as many as the genre's canon checks for.
8. **Views** (optional, since a prose type has none). The view blocks a page of this type carries by default, each with its presentation and what it shows.
9. **Minimum form.** What a page holds when an always-present section has nothing to say yet: every such section stays, with one line saying what isn't known, and the page still passes the computed checks.

## Plumbing types

A type that records how the work was done rather than what it established is plumbing: the task history, a round record and the scratchpad. Its file says "Plumbing" under its sentence and holds only its Page, Membership and Sections. A plumbing section's heading names its span, such as a round or a date, rather than a question, unless its type file names another heading. Plumbing pages are facts about the work, kept to the same plain terms as any page. [publish-and-link](../phases/03-publish-and-link.md) places them in a group titled `Work history`, out of the reader's path. The task log belongs to no task and keeps its own place. (basis: maintainer, 2026-11-11)

## Where the catalogue lives

Every type file sits in [types/](types/), named for what the type is: `threat-model.md`, not `stride.md`. A heading the maintainer fixed before this shape, such as the task record's family sections, keeps its name.

Read a type's file only when the documentation plan owes the type, a kit row or the act names it, or a page shows one of its kinds; the rest stay unread. The catalogue: [accessibility-check](types/accessibility-check.md), [audit-report](types/audit-report.md), [backup-restore-plan](types/backup-restore-plan.md), [breaking-change-notice](types/breaking-change-notice.md), [close-out-record](types/close-out-record.md), [communications-plan](types/communications-plan.md), [concept](types/concept.md), [cutover-plan](types/cutover-plan.md), [decision-brief](types/decision-brief.md), [decision-record](types/decision-record.md), [decision-register](types/decision-register.md), [design-document](types/design-document.md), [explanation](types/explanation.md), [faq](types/faq.md), [glossary](types/glossary.md), [how-to](types/how-to.md), [incident-record](types/incident-record.md), [plan](types/plan.md), [privacy-screening](types/privacy-screening.md), [privacy-threat-model](types/privacy-threat-model.md), [raid-log](types/raid-log.md), [readiness-review](types/readiness-review.md), [reference](types/reference.md), [research-report](types/research-report.md), [review-record](types/review-record.md), [round-record](types/round-record.md), [runbook](types/runbook.md), [scratchpad](types/scratchpad.md), [ship-notes](types/ship-notes.md), [slo-document](types/slo-document.md), [spec](types/spec.md), [spike-findings](types/spike-findings.md), [task-history](types/task-history.md), [task-log](types/task-log.md), [task-record](types/task-record.md), [test-plan](types/test-plan.md), [threat-model](types/threat-model.md), [traceability](types/traceability.md), [vendor-review](types/vendor-review.md).
