# Reader tabs

A task's documentation is laid out as a fixed set of tabs, each built around one reader's task. A type stays the unit of authoring and checking: its items, sections, computed checks and due points. A tab hosts one or more types, so things a reader uses together sit together, and the navigation stays the same size however many documents the work owes.

## The tabs

In this order. A tab appears once a type it hosts is in the documentation plan, whatever its due point; Map appears once the store holds a unit or a gate.

| Tab | Part | Hosts | Instrument | Instrument shows |
|---|---|---|---|---|
| Status | now | the task record (the main page) | status | unit, requirement, question, decision, gate |
| Map | now | none: a view across the plan | map | unit, gate, question, decision, dependency |
| Questions & decisions | now | decision register; decision briefs | register | question, decision, brief |
| RAID | now | RAID log | raid | risk, issue, assumption, dependency |
| Trace | now | traceability; test plan | trace | unit, requirement, gate |
| FAQ | now | FAQ | faq | answer, and the reviewer questions below |
| Design | plan | design document | design | slice, design section |
| Requirements | plan | spec | requirements | requirement, acceptance criterion |
| ADRs | plan | decision records | adrs | decision |
| Threats | plan | threat model; privacy threat model | threats | element, threat, privacy threat, mitigation |
| Data | plan | privacy screening; vendor review; backup and restore plan | data | screening criterion, vendor or dependency, restore path |
| Cutover | plan | cutover plan; readiness review; breaking-change notice; communications plan; accessibility check | cutover | gate, metric, risk |
| Runbook | plan | runbook; SLO document | runbook | objective, alert, procedure |
| Glossary | plan | glossary | glossary | term |

*Now* holds what changes while the work runs. *The plan* holds what is agreed before the work acts on it. A type the table doesn't name goes to the tab of the type its Page line puts it on; one with a page of its own takes a tab of its own under *the plan*, after Glossary in the order the types entered the plan, labelled with its type file's title. System documentation stays the group [publish-and-link](../phases/03-publish-and-link.md) names, under *the plan*. Work records (each round's plan, round records, review records, the task history, the scratchpad, and the group pages that list them) are **records**: their own area, reached by one link, never mixed into the reader's tabs. A records page carries its title and `part: records`, and no other head. (basis: maintainer, 2026-11-12, the epic's documents kept apart from the working rounds)

## What a tab carries

- **Its label**, the table's, used in the navigation.
- **No notes about the document** on the tab: no footer naming its type, key or date, and no review or check lines; those belong to the tab's page as filed and to the developer's report.
- **Its head:**
  - the kicker is the tab's label, but the main page's, which is its family's name, such as `The change`;
  - Map, which hosts no type, takes its headline and lead from the map's own findings: where to start, where the work converges, and the tier-1 question nobody is named to decide;
  - the headline is the claim [shape-the-document](../phases/02-shape-the-document.md) puts first, taken from the first hosted type in the table's order, unless another hosted type holds a blocking item still `open` or `lean`, whose title then is the headline;
  - the headline and lead never contradict a verdict the instrument computes, a computed check's result or a field it derives such as Data's verdict on whether an assessment is owed, and restate no count it computes but the lead's two below, which equal the instrument's (basis: benchmark, 2026-11-13, a headline said an assessment was presumed owed while the computed verdict said it may be);
  - the lead says, in two or three sentences, how many of the tab's items are `open` or `lean` and how many due points have passed, in that order, and names the first thing to act on;
  - the badge: a *now* tab shows `Live` when this filing observed a live field, else `As of <date>`; a *plan* tab shows `Agreed` when it hosts agreeable items, superseded and withdrawn ones left out, and every one is agreed, `Draft` when some are not, and no badge when it hosts none.

- **Its instrument**, first, where the backend renders instruments ([artifacts](../../artifacts/SKILL.md)), built to [design-reader-instruments](../../../craft/writing/design-reader-instruments.md). A tab is designed whole: its head, its instrument, and the hosted sections its design shows. Every hosted section is also filed unedited, with the type's computed checks and review lines, on a records page for the tab, `<tab>, as filed`, which the tab links to in one line at its end. (basis: maintainer, 2026-11-13, raw sections under each instrument judged messy and repeated; sections swept off the tab hid what no instrument showed)

  Three instruments answer more than their own items:
  - **FAQ** opens with the questions every reviewer asks, answered from the store, each linking the tab that holds the detail: how it ships; when; whether it can be rolled back, counting one-way gates and rehearsed rollbacks; what it depends on; what changes for callers; what is undecided, as the three open questions with the most items `blocked-by` them, ties by tier, then id, a question nothing is `blocked-by` left out. A question with nothing filed to answer it is left out. (basis: maintainer, 2026-11-13, the FAQ should answer the low-hanging questions)
  - **Cutover** follows its gates with every metric on a scale: baseline, target and latest reading, beside the go and stop lines of each gate that reads it. (basis: maintainer, 2026-11-13, a table isn't the view for metrics)
  - **Glossary** puts our words apart from the vendor's, a term whose `origin` is `both` with the vendor's, each term with the items that use it. (basis: maintainer, 2026-11-13, the prototype's glossary)
- **The sections it shows besides its instrument** are its tab design, in [tab-design](tab-design.md): each hosted section, by its heading in its type file's Sections list, goes under the head, into the instrument, which draws it from the items it rests on or from the section's own words, after the instrument as its own section, or only to the page as filed. A section goes into the instrument only when that adds what the instrument wouldn't otherwise show, the section's own words or items it doesn't draw; one whose items it already draws, saying nothing beyond them, goes only to the page as filed. A section the instrument's code takes in goes into it rather than after it, since after it the section only repeats as written; one it could draw but doesn't yet stays after it until the backend's renderer does. (basis: maintainer, 2026-11-13, rows of raw sections judged poor) A section goes only to the page as filed when an instrument on a tab this task's site has already shows what it says, or when it records how the work went rather than what the change is. (routed to maintainer: the per-tab design, 2026-11-13) A hosted item a tab's instrument doesn't draw is the backend's renderer's to draw, never held in a catch-all section on the tab. (basis: maintainer, 2026-11-13, a catch-all of leftover items judged poor) A section is headed as its type file's Sections list heads it, verbatim, or, for a decision record or a brief filed on a tab, its id or `Brief:` followed by its title; a section under any other heading has no place.
- On a backend that renders no instruments, the hosted types' sections and views, in their files' order, one type after another.
