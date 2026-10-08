# Task record

The task's front page: the first page a reader opens, saying what the work is and where it stands now, in the terms of the people it affects. (basis: maintainer, 2026-10-08)

## Its family

The task's act decides its family, and the family decides the sections and the page's title, the task's own title naming the whole documentation:

| Family | Acts | Name |
|---|---|---|
| A change | developing, fixing a bug, maintaining, reviewing, shipping | The change |
| An incident | responding to an incident | The incident |
| A question | researching, learning, prototyping | The answer |
| An audit | auditing | The verdict |

(basis: maintainer, 2026-10-08; shipping's place, derived — it acts on a change)

## Sections

Under its title, the page opens with a pin line: the family's name and what the page describes. A change names the head commit of each review request it describes and says the page is out of date once a head moves: `The change, as of 60f9a60, the head of review request 3468. If its head is newer, this page is out of date.` Before a request opens it names its branch's head, and before the task has a branch, the time of the filing. An audit names the commit it read; an incident and a question, the time of the latest filing, and a question adds whether the task is open and its next step, since it has no Status. Then come the family's sections in order, each present even when empty, but for What was wrong, which only a change that fixes a bug has; an empty section says so in a line. (basis: maintainer, 2026-10-08)

**Status** opens a change and an incident, and an audit calls it **Verdict**. Its first sentence, in bold, says where the task stands:
- a change: no review request yet, or each review request waiting, with changes requested, approved, merged or shipped;
- a review: per request, the latest round's stance posted on it (request changes, approve or comment-only), or the stance proposed while not yet posted, with the count by severity of the findings still standing, a withdrawn one left out;
- an incident: the outcome it rests at, or no outcome yet and what is running;
- an audit: the posture.

Then, in two sentences at most: what it waits on and on whom, the next step or "Nothing: closed", and the date and commit it reflects. For a change that shipped, add when and where, with links to the system documentation of the parts it touched. It is restated on every filing from the memory entry, the delivery recorded and the latest results, never added to. (basis: maintainer, 2026-10-08, for a review's stance and for restating on every filing; the state vocabularies, relayed from the vcs port's states and stances, the incident act's outcomes and security review's posture line; two sentences at most, derived from the page leading with where the work stands rather than how it got there)

**A change** then has:

1. **What changes and why** — first each outcome someone using the product meets, by the test of who bears it in review's brief ([deliver-findings](../../../review/phases/06-deliver-findings.md)): before → after, who is affected and what stays the same, each led by one bold sentence. Then each change another developer meets, each led by one bold sentence and followed by why it was done that way. A change no user can observe says so.
2. **What was wrong** — when the task's act or any of its rounds' acts is fixing a bug, and for a review when its brief states the defect the change fixes: the symptom as it was seen, and its cause, at the commit and line it was found at.
3. **How it works** — the mechanism behind the outcomes above, drawn where [when-a-visual-is-owed](../../../../craft/writing/when-a-visual-is-owed.md) owes a diagram, each with one line under it saying what to read from it.
4. **Depends on** — what has to be in place before the change works and lands: other review requests and the order they land in, migrations, settings, services, data, and changes other teams make.
5. **Verification** — a table, one row per requirement or acceptance criterion: the requirement, its result on [results-and-certainty](../../../../craft/evidence/results-and-certainty.md)'s scale, and the evidence, each at the commit it ran at. A result short of `holds` says what would settle it.
6. **Rollout and rollback** — how it reaches users: deploy order, how the merge strategy changes what lands, flags and exposure; how to undo it, as steps, and what can't be undone once it has run; what to watch after it ships. Once a ship round has run, what happened, with its health verdict.
7. **Open** — what is still owed before or after it lands: findings and questions still standing, follow-ups others asked for, decisions waiting on an owner, and claims not yet proven.
8. **Iterations** — one entry per round, newest first, a task of one round included, headed `Round <n> · <kind> · <date it opened>` with the compare link of the commits it covers once its peer review hands it, a review round's kind being `review`. Its fields:
   - **What changed:** the round record's Changes, else what its task history section says was done;
   - **Decided:** its Decisions, else its comment dispositions, else "nothing";
   - **Evidence:** its Evidence, else the results it filed;
   - **Outcome:** its reviewers' verdicts or how it closed, `open` while it runs;
   - **Detail:** its pages as in-tree references ([portable-tree-shape](../portable-tree-shape.md)).

**An incident** then has **Impact** (who and what, since when), **Where it stands** (the mitigation and health now), **Cause**, **What was changed**, **Follow-ups**, and **Timeline**.

**A question** has **The answer** (one paragraph, with its result on the results scale), **What it means for us**, **How we know** (the evidence and how hard it was tested), and **Still open**.

**An audit** then has **Findings by severity** (a table with one row per finding, highest severity first: severity, the finding in one line, where it is), **Fix first** (every finding at the highest severity present, in the report's own priority order, each with its fix), and **Not covered**.

(basis: maintainer, 2026-10-08, for the headings and the page names; each section's content, derived from the maintainer's reference page; Iterations for a task of one round, derived from the fixed headings, narrowing the 2026-10-07 default that a change done in one round carries no round machinery; Fix first's cut, derived from a highest-severity finding being the one a reader acts on first)

## Where each section comes from

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
- **A question** takes them from the research report, the explanation or the spike findings, What it means for us from what the result says its answer means for the purpose the question was asked for.
- **An audit** takes them from the audit report.
- **Each iteration** takes its fields from its round's record, or from its round's section in the [task history](task-history.md) when it has none, and its dispositions from its round's scratchpad section on them.

Shipping a change built outside this task fills what its own results carry, Status and Rollout and rollback, and says of the rest where the change was built. (basis: maintainer, 2026-10-08, for a review's page drawing on the reviewer's own read; the rest, derived from each act's own results)

## Below it

The record links to the task's other pages, which [publish-and-link](../../phases/03-publish-and-link.md) groups beneath it, rather than summarizing them, but for its current state and Iterations ([one-type-per-page](../one-type-per-page.md)). A record written before front pages, with Status, What's next, Current state, The task and Rounds as its sections, is reshaped on its next filing. Its sections above are restated from the pages filed so far, with an Iterations entry for each closed round written once by the sources above, its Rounds section standing in for its task history section, and frozen. Its The task and Rounds become the task history. A folded task's record is carried as it stands. (basis: maintainer, 2026-10-08)
