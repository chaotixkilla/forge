# Documentation kit

A task's documentation tends to describe a change in prose and skip what a reviewer or a later maintainer reaches for first: the picture of what changed, and the few documents practice expects of that kind of change — a migration plan, a compatibility call, a rollback criterion. Each kind of change has its own kit, and assembling it is part of making the documentation ready. `(basis: maintainer, 2026-10-14)`

## The task's kinds

- **The change** is the diff from the merge base with the integration line to the task's heads, whoever wrote the commits. A task that changed nothing — an investigation that found no defect, research, learning — owes the research row alone.
- **The act gives its own row:** reviewing the review, responding-to-an-incident the incident, researching, learning and prototyping the research row; other acts give none. A change that fixes a defect its results state takes the bug-fix row, whatever its act.
- **What the change does to a surface gives the subject rows** — what moves that someone outside the diff relies on, read from its files, its intent, and the surface its symptom shows on. A fix whose failure a user sees is a UI change too. **Behaviour or flow** applies, beside any other row, whenever the change alters a sequence, a decision path or a lifecycle.

The task owes every one of its rows.

| Kind | Documents it owes | Generated | Observed | Drawn |
|---|---|---|---|---|
| Schema or data model | Migration plan; expand → migrate → contract when a step is destructive | Data model of the touched tables, base vs head; destructive-change check | The migration run, timed, when a step rewrites or locks existing rows | Data flow when data moves between stores |
| API or tool contract | Compatibility class (breaking, behavioural — same shape, different effect — additive, internal); deprecation, when something is removed; changelog entry, where the project keeps one | Contract diff, breaking first; map of routes or tools, new, changed and removed marked, when one is added, renamed or removed | Request and response examples | Sequence of the changed call path |
| Behaviour or flow | A few schematic scenarios | — | Sequence from a real trace, base vs head | State diagram for a lifecycle; before/after flow or sequence of the decision path |
| Bug fix | Reproduction, cause, fix | Coverage of changed lines | The failure, and the test that failed without the fix and passes with it | Cause-to-symptom chain |
| Limit, timeout or default — an expiry or lifetime included; a limit a contract declares takes the contract row too | What bounds the value, inside and outside, per consumer | — | A call near the limit, timed | Timeline to scale of the nested limits |
| Architecture or refactor | Why this decomposition; a decision record | Module graph of the affected area, before/after | — | Structure view of the area |
| UI | Setup steps for a reviewer | Visual-regression diffs | Before/after screenshots; a short recording | Flow between screens, when the change crosses screens |
| Performance | Benchmark method and the limiting factor | Benchmark and size deltas | Differential profile | — |
| Security-relevant: who can reach what — credentials or secrets, authentication or authorisation, an endpoint without it, auditing, what data is kept or sent outward, a trust boundary | Threat-model update; who owns an accepted risk | — | — | Data flow with trust boundaries |
| Infrastructure, deployment or config: what runs where, or what reaches it — a new secret or setting each environment must hold included | Which services run where, per environment | Graph from the infrastructure code or stack definition | — | Deployment view |
| Dependency added or upgraded | The upstream changes that matter here; for one added, why this one and its licence | Graph of the affected usage; lockfile summary | Test and benchmark deltas | — |
| Rollout, flag or deploy order | Rollback criteria; a flag's removal date, or for a flag or setting the change ships off behind, the condition that turns it on and who decides; the deploy order, when out of order breaks something | — | Metrics around each rollout step, against a control when there is one | Rollout timeline, or a sequence of the deploy order |
| Incident | Timeline, impact in numbers, causes, actions, where we got lucky | — | Metric charts around it | Timeline to scale; cause chain |
| Review of a change | The same kit for the request's kinds, base vs head | as its kinds | as its kinds | Standing findings and decisions drawn where they rest on structure |
| Research or learning | How the area works | Module graph of the area | Experiment or probe results, as a chart or table | Context and structure views |

**Reading the table.**

- **Owed cells.** Each filled cell of a change's rows is a visual its row owes, when the change moves what it shows. When the change doesn't move it, the cell is one line in its section: unchanged. The research row's cells are owed whenever the task studied the area.
- **Sources.** A cell's column is its most trusted source. When that source can't make it, draw it if a drawing can carry it; otherwise note it where it would stand, with why. A visual can take a source per part, each with its own provenance: a route map's API half generated, its UI half drawn.
- **Sharing a visual.** One visual discharges every cell whose form and elements it carries: one data flow with trust boundaries serves both Schema and Security.
- **Short chains.** A drawn chain or flow of three links or fewer may be a sentence.
- **Drawn sequences.** A drawn sequence is read from the call sites it names, which counts as its kind's read ([when-a-visual-is-owed](when-a-visual-is-owed.md)).

`(basis: maintainer, 2026-10-14 — most trusted first, since a generated picture can't misremember the code; the owed-only-when-moved, shared-visual and short-chain rules from the release check over past task records, 2026-10-15)`

## Where each piece lands

In the task record ([task-record](../../skills/document/rules/types/task-record.md)), by subject. The kit's visuals stand in these sections; a visual drawn on a working page moves into its section rather than being linked from it.

- **What changes and why:** a compatibility class, deprecation and changelog entry; the upstream changes that matter; a contract diff and route or tool map; a threat-model update.
- **What was wrong:** reproduction and cause, and the cause chain.
- **How it works:** structure, flow, sequence, state, data model and data-flow visuals; the scenarios; why this decomposition; what bounds a limit, and its timeline.
- **Depends on:** which services run where, per environment, and the deployment view.
- **Verification:** setup steps, as a list above its table; then screenshots, recordings, request and response examples, a call near a limit, visual-regression diffs, the destructive-change check, coverage, the test that failed then passed, and benchmark and size deltas with their method.
- **Rollout and rollback:** a migration plan and expand → migrate → contract, rollback criteria, a flag's removal date or turn-on condition, the deploy order, the migration run's timing, rollout timelines and metric charts.
- **Open:** who owns an accepted risk, until someone does.

For an incident:

- **Timeline:** the timeline.
- **Impact:** its numbers and metric charts.
- **Cause:** causes, the cause chain, and where we got lucky.
- **Follow-ups:** actions.

Elsewhere:

- a finding's drawing stands with its finding, on the review record and in the posted review;
- research's kit goes on its explanation page, or, in a change's task record, How it works;
- a decision gets its own decision record.

**Owed documents.** Close-out writes an owed document only from what the steps' results and the generated visuals establish, such as a compatibility class read from the contract diff. What they don't establish goes to Open, or to an incident's Follow-ups, as owed, with why.

In a review, the reviewer writes what its own results establish. One with no case is noted `none:` and why, such as a deprecation where nothing is removed. Only one that needs the author's knowledge, or a decision owner, becomes a question for the author, anchored at the file that raises it.

**What wasn't made.** Close-out writes, in each section, one line naming the owed cells it didn't fill, each with why. Nothing owed goes unmentioned.

## Three sources

1. **Generated** from the code by a tool the project already has — its scripts, development dependencies or CI, a tool CI fetches pinned counting, fetched the same way — learned by init as a workspace recipe, by purpose:
   - `schema` — data model, destructive-change check;
   - `contract` — contract diff, route or tool map;
   - `graph` — module, usage and infrastructure graphs, and a lockfile summary;
   - `coverage`;
   - `bench` — benchmark and size deltas;
   - `visual` — visual-regression diffs.

   It runs through the [workspace](../../skills/workspace/SKILL.md) at the head, with a fresh namespace, and at the change's base — the merge base with the integration line, or a reviewed request's base — as [run-code-in-the-task-workspace](../engineering/run-code-in-the-task-workspace.md) runs a baseline. No tool the project lacks is added. The project's own dependencies build at each commit as any run builds them.

   Its output is parsed into its form's neutral block, with marks from comparing base and head ([portable-tree-shape](../../skills/document/rules/portable-tree-shape.md)). It is attached as an image only when the tool's own output is one.

   In a review, a generator whose run executes the head's code, its namespace's setup included — `schema` with its migrations, `contract` when it boots the app, `coverage`, `bench`, `visual` — runs only when the review itself ran the head's code; otherwise its visual is drawn or noted. One that reads committed outputs, such as a contract file the project keeps current, runs in any review. A tool that compares by itself runs once, at the head, against the base.

   **In host mode nothing is generated.** No recipe exists there, and a generator that reads data would read the shared default. Those visuals are drawn, and their provenance says why.
2. **Observed** from the running change, by the step that runs it, as it runs — never staged afterwards:
   - verify captures screenshots and recordings, and request and response examples, from the surfaces it drives;
   - test captures the test that failed without the fix and passes with it;
   - debug captures the failure as it ran, and a trace where the stack emits one;
   - a migration run's timing is the duration the workspace returned for the task's latest `migrate-` run, kept by the step that ran it;
   - an incident's and a rollout's charts come from the telemetry those steps read for the window.

   A cell no step of the run captured is drawn or noted.
3. **Drawn** from understanding: every element traces to a claim the task's results hold, at its certainty ([diagram-legibility](diagram-legibility.md)).

Every visual records its provenance.

## The visuals' standard

The standard is [diagram-legibility](diagram-legibility.md) and [when-a-visual-is-owed](when-a-visual-is-owed.md), with these additions:

- a key explains every mark and colour;
- a visual of a change is shown against its base;
- detail a reader looks up — each element's values — goes in a table beside it, never into the picture;
- a visual over a size cap splits; it is never dropped.

**What the kit owes wins over the general rules.**

- The shape test's size bar and the override for a relation the reader never acts on don't drop a visual the kit owes.
- Prose that restates it is cut to a pointer.
- A diagrams setting of `never` governs reports in the conversation, not the task's documentation.

`(basis: maintainer, 2026-10-14 — the per-kind table governs)`

## Nothing leaks through a picture

- **Screenshots and recordings** mask secret fields before capture.
- **Traces, and request and response examples,** are stripped of credentials and personal data before they are kept.
- **Rendering** happens at the destination or in the task's environment, never by a third-party rendering service.

`(basis: maintainer, 2026-10-14)`

## Ready, never a gate

The documentation is ready when each owed document is present or listed as owed with why, and each owed visual is drawn or noted with why it couldn't be made. A description or review goes out once the documentation is ready, so it carries the visuals. A visual that can't be made never holds anything back. A screenshot the request's host can't show stands as its placeholder, and the documentation holds it. `(basis: maintainer, 2026-10-14)`

**Why praxis draws these at all**: data models for migrations, before/after for refactors, visuals in descriptions and reviews. No authority prescribes them. An always-current central source of the picture can't be assumed, so each task carries the picture its reader needs. `(basis: maintainer, 2026-10-14)`

Cited by [close-out](../../skills/work/phases/04-close-out.md), [open-the-review-request](../../skills/work/rules/open-the-review-request.md), review's [deliver-findings](../../skills/review/phases/06-deliver-findings.md), verify's [exercise-the-flows](../../skills/verify/phases/03-exercise-the-flows.md), test's [run-and-observe](../../skills/test/phases/05-run-and-observe.md), debug's [reproduce-and-frame](../../skills/debug/phases/01-reproduce-and-frame.md), [shape-the-document](../../skills/document/phases/02-shape-the-document.md), [init](../../skills/init/phases/02-resolve-tools.md), [task-record](../../skills/document/rules/types/task-record.md) and [when-a-visual-is-owed](when-a-visual-is-owed.md).
