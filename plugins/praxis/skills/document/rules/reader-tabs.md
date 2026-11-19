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
  - the headline follows [the words on a tab](#the-words-on-a-tab), but a title made the headline is quoted whole, never shortened;
  - the headline and lead never contradict a verdict the instrument computes, a computed check's result or a field it derives such as Data's verdict on whether an assessment is owed, and restate no count it computes but the lead's two below, which equal the instrument's (basis: benchmark, 2026-11-13, a headline said an assessment was presumed owed while the computed verdict said it may be);
  - the lead says, in two or three sentences, how many of the tab's items are `open` or `lean` and how many due points have passed, in that order, and names the first thing to act on;
  - the badge: a *now* tab shows `Live` when this filing observed a live field, else `As of <date>`; a *plan* tab shows `Agreed` when it hosts agreeable items, superseded and withdrawn ones left out, and every one is agreed, `Draft` when some are not, and no badge when it hosts none.

- **Its instrument**, first, where the backend renders instruments ([artifacts](../../artifacts/SKILL.md)), built to [design-reader-instruments](../../../craft/writing/design-reader-instruments.md). A tab is designed whole: its head, its instrument, and the hosted sections its design shows. Every hosted section is also filed unedited, with the type's computed checks and review lines, on a records page for the tab, `<tab>, as filed`, which the tab links to in one line at its end. (basis: maintainer, 2026-11-13, raw sections under each instrument judged messy and repeated; sections swept off the tab hid what no instrument showed)

  Three instruments answer more than their own items:
  - **FAQ** opens with the questions every reviewer asks, answered from the store, each linking the tab that holds the detail: how it ships; when; whether it can be rolled back, counting one-way gates and rehearsed rollbacks; what it depends on; what changes for callers; what is undecided, as the three open questions with the most items `blocked-by` them, ties by tier, then id, a question nothing is `blocked-by` left out. A question with nothing filed to answer it is left out. (basis: maintainer, 2026-11-13, the FAQ should answer the low-hanging questions)
  - **Cutover** follows its gates with every metric on a scale: baseline, target and latest reading, beside the go and stop lines of each gate that reads it. (basis: maintainer, 2026-11-13, a table isn't the view for metrics)
  - **Glossary** puts our words apart from the vendor's, a term whose `origin` is `both` with the vendor's, each term with the items that use it. (basis: maintainer, 2026-11-13, the prototype's glossary)
- **The sections it shows besides its instrument** are its tab design, in [tab-design](tab-design.md): each hosted section, by its heading in its type file's Sections list, goes under the head, into the instrument, which draws it from the items it rests on or from the section's own words, after the instrument as its own section, or only to the page as filed. A section goes into the instrument only when that adds what the instrument wouldn't otherwise show, the section's own words or items it doesn't draw; one whose items it already draws, saying nothing beyond them, goes only to the page as filed. A section the instrument's code takes in goes into it rather than after it, since after it the section only repeats as written; one it could draw but doesn't yet stays after it until the backend's renderer does. (basis: maintainer, 2026-11-13, rows of raw sections judged poor) A section goes only to the page as filed when an instrument on a tab this task's site has already shows what it says, or when it records how the work went rather than what the change is. (routed to maintainer: the per-tab design, 2026-11-13) A hosted item a tab's instrument doesn't draw is the backend's renderer's to draw or count, as [what a tab draws in full](#what-a-tab-draws-in-full) says, never held in a catch-all section on the tab. (basis: maintainer, 2026-11-13, a catch-all of leftover items judged poor) A section is headed as its type file's Sections list heads it, verbatim, or, for a decision record or a brief filed on a tab, its id or `Brief:` followed by its title; a section under any other heading has no place.
- On a backend that renders no instruments, the hosted types' sections and views, in their files' order, one type after another.

## What a tab draws in full

A tab is the reader's projection of the record, and its page as filed is the record, so the tab carries only what a reader must act on or know. (basis: field findings, 2026-11-19, a peer reviewer spent about four hours on a set where every decision was accounted for, but not for humans) Of the items an instrument gives as text, as a card, a row or a list entry, or inside another item's card, it draws in full those that pass at least one of these tests:

1. **An open ask:** a question `open` or `lean`, a decision `proposed`, a brief serving one of them, or any item not `agreed` whose decide-by is a date before the filing's. A decide-by naming a gate or a milestone never counts as passed. (basis: derived — only a date can be read against the store)
2. **A one-way or far-reaching call:** a question or decision of tier 1, or with `reach` `beyond the change`, in any state.
3. **Held up:** an item `blocked-by` an open ask.
4. **Missing or failing:** an item the instrument marks red, as [design-reader-instruments](../../../craft/writing/design-reader-instruments.md) point 2 defines it.
5. **The tab's subject:** an item of the first kind the table above lists under *Instrument shows* for the tab that the instrument gives as text, so Threats' subject is the threat, its parts being drawn as a picture.

Each item drawn in full links to its entry on the tab's page as filed. An item that passes no test isn't drawn, nested or not; it is counted in its kind's line, after the instrument's list, linking that page. The line reads `<n> more <kind>, none open`, which says why they were set aside: none passes a test, so none is open: `31 more acceptance criteria, none open`.

Every item that passes a test is drawn, however many pass; no fixed number caps a tab. (basis: maintainer, 2026-11-19, content is set aside by priority, never cut by a number) Within each list they rank by the lowest-numbered test each passes; then tier 1 before tier 2, items with no tier after; then decide-by: dates earliest first, then gates by their number, then any other value, and none last; then in the instrument's own order, such as the glossary's alphabetical one.

A mark in a picture, such as a node, a dot, a cell or a stop on a rail, takes no test; its label follows its visual's rule. (basis: derived — a picture is read as a whole, not item by item)

## The words on a tab

The words a tab writes itself, its head, its instrument's headlines and its count lines, aim at these. They are advice for the writer: nothing is cut or shortened to meet them, an item's own text is quoted as its type holds it, and a hosted section placed under the head or after the instrument stays exactly as filed. A section the instrument draws from its items is drawn by the tests above. (basis: maintainer, 2026-11-19, limits as advice, never a cut; reader-tab text had been written for completeness)

- A headline leads with one claim or one question, aiming at 14 words; what follows it is its detail, after the claim rather than in it. (basis: maintainer, 2026-11-19, the visual library's design rules)
- A sentence aims at 25 words at most. (basis: plain-language guidance, an average of 15 to 20 words a sentence)
- A sentence names at most two item codes; with more, it says how many and leaves them to the instrument. (basis: field findings, 2026-11-19, chains of codes made the tabs read as reference)
