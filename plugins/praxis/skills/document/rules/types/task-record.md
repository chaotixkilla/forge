# Task record

The task's front page: the first page a reader opens, saying what the work is and where it stands now, in the terms of the people it affects. (basis: maintainer, 2026-10-08)

## Reader and question

A teammate arriving cold, as a reviewer of the change, a decider or a maintainer later: "What is this, where does it stand, and what does it need from me?" (basis: maintainer, 2026-11-11)

## Page

`own page`. The task's other pages sit beneath it.

## Membership

One per task, the same document for the task's whole life, filed again on every filing from the first.

The task's act decides its family, and the family decides the sections and the page's title, the task's own title naming the whole documentation:

| Family | Acts | Name |
|---|---|---|
| A change | developing, fixing a bug, maintaining, reviewing, shipping | The change |
| An incident | responding to an incident | The incident |
| A question | researching, learning, prototyping | The answer |
| An audit | auditing | The verdict |

(basis: maintainer, 2026-10-08; shipping's place, derived — it acts on a change)

The record links to the task's other pages, which [publish-and-link](../../phases/03-publish-and-link.md) groups beneath it, rather than summarizing them, but for its current state and Iterations ([one-type-per-page](../one-type-per-page.md)). A record written before front pages, with Status, What's next, Current state, The task and Rounds as its sections, is reshaped on its next filing. Its sections below are restated from the pages filed so far, with an Iterations entry for each closed round written once by the sources below, its Rounds section standing in for its task history section, and frozen. Its The task and Rounds become the task history. A folded task's record is carried as it stands. (basis: maintainer, 2026-10-08)

## Items

**Overview `OVW`.** The page but its views, since a reader cites the front page whole.
- Fields: `family`: enum `change`, `incident`, `question`, `audit`.
- Granularity: one per task.
- Change regime: `living`, and it never freezes: it is restated whole from results on every filing, after close-out too, so it carries no change notes.
- Its owner is the task's owner, as the task history names it. Its agreement is `none`: a front page is restated, never agreed.
- Live field: `requests`, list of text, `vcs: each review request the page describes, with its state and its head`.

## Sections

Under its title, the page opens with a pin line: the family's name and what the page describes. A change names the head commit of each review request it describes and says the page is out of date once a head moves: `The change, as of 60f9a60, the head of review request 3468. If its head is newer, this page is out of date.` Before a request opens it names its branch's head, and before the task has a branch, the time of the filing. An audit names the commit it read; an incident and a question, the time of the latest filing, and a question adds whether the task is open and its next step, since it has no Status. Then come the family's sections in order, each present even when empty, but for What was wrong, which only a change that fixes a bug has, and What changed since you last looked? and What does each review request carry?, present only when their conditions hold; an empty section says so in a line. (basis: maintainer, 2026-10-08)

**Status** opens a change and an incident, and an audit calls it **Verdict**. Its first sentence, in bold, says where the task stands:
- a change: no review request yet, or each review request's state, joined at publish from the `requests` live field, or shipped;
- a review: per request, the latest round's stance posted on it (request changes, approve or comment-only), or the stance proposed while not yet posted, with the count by severity of the findings still standing, a withdrawn one left out;
- an incident: the outcome it rests at, or no outcome yet and what is running;
- an audit: the posture.

Then, in two sentences at most: what it waits on and on whom, the next step or "Nothing: closed", and the date and commit it reflects. Within those, an [epic](../../../../craft/writing/documentation-plan.md)'s names its next gate, the earliest by `opens on` whose step hasn't run, undated gates after dated ones in id order, with its `opens on` or `undated`; an epic with no gate names none. Within those, when commits made outside praxis follow the head praxis last checked, the entry's `at`, it names both, that head and the current one, not checked by praxis. (basis: maintainer, 2026-10-19) For a change that shipped, add when and where, with links to the system documentation of the parts it touched. It is restated on every filing from the memory entry, the delivery recorded and the latest results, never added to. A task with related tasks closes it with one line, `Related:` and each one's key, linked to its record, and why, from the entry's `related`. (basis: maintainer, 2026-10-08; the state vocabularies, the vcs port, the incident act and security review; two sentences at most, derived; request states joined live, maintainer, 2026-11-11)

**What changed since you last looked?** follows Status or Verdict, and opens a question's sections, once its list has two entries or more. It is a list the page writes, one entry per date found in these sources, as the store writes it, newest first, each headed with its date:
- each change note of that day: its item's id and title, and what changed;
- each agreement of that day: its id, and each item it settled, `agreed`, or `withdrawn` where the content it settled is `{"withdrawn": …}`; an agreement with no date is left out;
- the items first filed that day, counted by kind, with up to ten ids per kind and then "and n more".

A restricted item is named by its id alone, on a team copy.

A day with none of these has no entry. The list holds the five latest entries; earlier ones stay in the item store and the task history. (basis: maintainer, 2026-11-11; GOV.UK change notes; the cap of five, a house rule)

**A change** then has:

1. **What changes and why** — first each outcome someone using the product meets, by the test of who bears it in review's brief ([deliver-findings](../../../review/phases/06-deliver-findings.md)): before → after, who is affected and what stays the same, each led by one bold sentence. Then each change another developer meets, each led by one bold sentence and followed by why it was done that way. A change no user can observe says so.
2. **What was wrong** — when the task's act or any of its rounds' acts is fixing a bug, and for a review when its brief states the defect the change fixes, and when a task's results state a defect its change fixes, whatever its act: the symptom as it was seen, and its cause, at the commit and line it was found at.
3. **How it works** — the mechanism behind the outcomes above, drawn where [when-a-visual-is-owed](../../../../craft/writing/when-a-visual-is-owed.md) owes a diagram, each with its caption above it saying what to read from it, standing here rather than linked from a working page.
4. **Depends on** — what has to be in place before the change works and lands: other review requests and the order they land in, migrations, settings, services, data, and changes other teams make.
5. **Verification** — the Verification view below, one row per requirement or acceptance criterion: its result on [results-and-certainty](../../../../craft/evidence/results-and-certainty.md)'s scale and the evidence, each at the commit it ran at. Where the task files no requirement, the rows stand as prose in the same shape. A result short of `holds` says what would settle it. Then, when the spec has slices, the Slices view.
6. **Rollout and rollback** — how it reaches users: deploy order, how the merge strategy changes what lands, flags and exposure; how to undo it, as steps, and what can't be undone once it has run; what to watch after it ships. Once a ship round has run, what happened, with its health verdict.
7. **What does each review request carry?** — when the change's units name more than one review request in `ships in`: the review brief view below, one group per request, in landing order, the lowest `order` among each request's units first. Units with no `ships in` are grouped last, under the port's `(none)` and don't count toward the condition. (basis: maintainer, 2026-11-11)
8. **Open** — what is still owed before or after it lands, in this order: the Decisions waiting and Work waiting views below; the findings, questions for the author and review comments still standing, one line per page that holds them, linking it, with how many stand and that they wait on the change's author; the requirements and criteria whose latest result isn't `holds`, one never verified included, one line with their count, linking Verification; and the pages awaiting agreement.
9. **Iterations** — one entry per round, newest first, a task of one round included, headed `Round <n> · <kind> · <date it opened>`, `<n>.<m>` after a revision, with the compare link of the commits it covers once its peer review hands it, a review round's kind being `review`. Its fields:
   - **What changed:** the round record's Changes, else what its task history section says was done;
   - **Decided:** its Decisions, else its comment dispositions from its round's scratchpad section on them, else "nothing";
   - **Evidence:** its Evidence, else the results it filed;
   - **Outcome:** its reviewers' verdicts or how it closed, `open` while it runs;
   - **Detail:** its pages as in-tree references ([portable-tree-shape](../portable-tree-shape.md)).

**An incident** then has **Impact** (who and what, since when), **Where it stands** (the mitigation and health now), **Cause**, **What was changed**, **Follow-ups**, and **Timeline**.

**A question** has **The answer** (one paragraph, with its result on the results scale), **What it means for us**, **How we know** (the evidence and how hard it was tested), and **Still open**.

**An audit** then has **Findings by severity** (a table with one row per finding, highest severity first: severity, the finding in one line, where it is), **Fix first** (every finding at the highest severity present, in the report's own priority order, each with its fix), and **Not covered**.

(basis: maintainer, 2026-10-08; each section's content, Iterations for a task of one round and Fix first's cut, derived)

**Where do I read next?** closes every family's sections, before a change's Iterations, when the task has a page beneath other than its work history. It gives one line per page, grouped by role ([type-files](../type-files.md)), each line with that type's question and a link. (basis: maintainer, 2026-11-11, one path per role on the entry page)

### Where each section comes from

Every section but Status and the closed rounds' Iterations entries is the task's current state, restated on every filing from every result filed so far. A later result replaces an earlier one on each subject it covers, a subject being one requirement, one unit or one operational instruction, but a result that checked nothing on a subject, `not checked`, replaces nothing. It is never patched or marked as revised: earlier versions live in the rounds' pages. (basis: maintainer, 2026-10-07) A section takes only what results carry, each claim with its source, and a section no result covers says what wasn't looked at and what would settle it. (basis: derived from shaping adding no claim)

- **A change a task authors** takes:
  - outcomes and requirements from the latest spec;
  - what was wrong from the diagnosis;
  - the changes another developer meets from develop's landed result, its "What another developer must know", and why from the plan's decisions and the decision records;
  - the mechanism, dependencies and rollout from the latest plan and its units;
  - verification from the latest test, verify and review results;
  - what is open from the results' gaps, the open sign-offs and the review requests' unanswered comments.

  An act that files no spec or plan (a bug fix, maintenance, the small-change path) takes the outcomes from the diagnosis or the change's own result, the mechanism from the diagnosis's mechanism for a bug fix, from the change step's map of what it touches for maintenance and from nothing on the small-change path, dependencies and rollout from its review's brief, and verification rows from the acceptances the review judged and the guards the tests added. The small-change path, which runs neither test nor review, takes Verification from verify and says of Depends on and Rollout and rollback that the path doesn't check them; a refactor or upgrade round, which runs no develop step, takes the changes another developer meets from its change step's result.
- **A change a task reviews** takes what changes, what was wrong, how it works, its dependencies and its rollout from the reviewer's own work before the change's description was read: the review's brief and the map of the change. It takes Status's stance, Verification and Open from the review as posted: its fitness results, its standing findings and its questions for the author; until it is posted, from the latest review result filed, the stance marked proposed. A review whose brief was turned off fills the first group from its findings and scope, saying so. (basis: maintainer, 2026-10-08, the reviewer's own read; the posted review for the verdict, derived — the page states the stance the author received)
- **An incident** takes its sections from the incident record, and while the incident is live, from the timeline notes.
- **Every family** also takes the pieces of its [documentation-kit](../../../../craft/writing/documentation-kit.md), each in the section the kit places it in.
- **A question** takes them from the research report, the explanation or the spike findings, What it means for us from what the result says its answer means for the purpose the question was asked for.
- **An audit** takes them from the audit report.

Shipping a change built outside this task fills what its own results carry, Status and Rollout and rollback, and says of the rest where the change was built. (basis: maintainer, 2026-10-08, for a review's page drawing on the reviewer's own read; the rest, derived from each act's own results)

## Checks

*Computed:*
- The pin line names what its family's pin names: each review request's head, the branch head, the commit read, or the filing time.
- Status opens with one bold sentence and at most two more, before its shipped and Related lines.
- Every section the family owes, given its conditions, is present.
- Verification has one row per requirement and acceptance criterion that isn't `superseded` or `withdrawn`.
- Iterations has one entry per round, newest first.

*Judgment:*
- A Status that tells how the work got here rather than where it stands ([lead-with-the-takeaway](../../../../craft/writing/lead-with-the-takeaway.md)).
- An outcome written as a code change when a user meets a different one.
- A verification that ran before the pinned head, read as current.
- A What was wrong where its condition doesn't hold, or none where it does.
- A decision or question a page beneath names as waiting, missing from the family's open-items section: a change's Open, an incident's Follow-ups, a question's Still open or an audit's Not covered.
- A reader role a page beneath serves with no line in Where do I read next?. (basis: maintainer, 2026-11-11)

## Views

- **Verification**, in a change's Verification: `table` of every `REQ` and `AC` not `superseded` or `withdrawn`: title, and its latest verification's outcome, date, commit and evidence, sorted by id.
- **Review brief**, in What does each review request carry?: `table` of every `UNIT` (home: [plan](plan.md)), sorted by `order` and grouped by `ships in`, so the groups fall in landing order: title; what it `serves`, ids and titles; the mitigations it carries, the path `serves` then `serves`, targets of kind mitigation (`MIT`, home: [threat-model](threat-model.md)) only, empty marker `none`; the gates it `blocks`, targets of kind gate (`GATE`, home: [cutover-plan](cutover-plan.md)) only, ids and titles, empty marker `none`; those gates' `rollback`. A column whose kind no owed type declares is left out.
- **Slices**, in a change's Verification: `table` of every `SLC` not `superseded` or `withdrawn`, sorted by priority in its declared order, then by id: title, priority, state with its reason, the units that serve it with their `request state` (`served-by`, only `UNIT` targets), the requirements it `serves`, and the tests that verify those (path `serves` then `verified-by`, field `latest run`), empty marker `none`. (basis: maintainer, 2026-11-11, an epic's state aggregated from its rounds)
- **Decisions waiting**, in a change's Open, an incident's Follow-ups, a question's Still open and an audit's Not covered: `list` of every `Q` and `DEC` (home: [decision-register](decision-register.md)) in `open`, `lean` or `proposed`, grouped by decider, so one with no decider falls under the port's `(none)`, and sorted by decide-by, earliest first: id, title, tier, decide-by and what it `blocks`. Their kinds count as declared wherever a page shows them, the spec's included. (basis: maintainer, 2026-11-11, what needs whom, ranked)
- **Work waiting**, after it: `table` of every `RISK`, `ASM`, `ISS` and `DEP` (home: [raid-log](raid-log.md)) whose `status` is `open`, and every `ACT` (home: [incident-record](incident-record.md)) in `open` or `proposed`: title, kind and decide-by, grouped by owner and sorted by decide-by, earliest first. A kind no owed type declares is left out, and the view with it when none is left; Open then says in a line that no risk log or incident is kept.
- **The pages awaiting agreement**, after the views: a list the page writes, one line per page with items in `proposed` that the views above don't show, the page as an in-tree reference and how many of its items await its approval, which the task's owner seeks. Those items are never listed one by one: a page's content waits on its approval, not on a person per item. (basis: benchmark, 2026-11-12, every proposed item listed as waiting buried the decisions)

## Minimum form

The pin line names the filing time. Status, or Verdict for an audit, says no result is filed yet and names the next step; a question, which has no Status, says both in its pin line. A change's Iterations holds round 1, `open`.
