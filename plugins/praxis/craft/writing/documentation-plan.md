# Documentation plan

Without a plan, a piece of work gets whatever documentation someone thinks to ask for. A large, multi-domain change ends up with a traceability matrix because a developer demanded one, and with no threat model because nobody did. The plan decides, up front and in the open, which documents the work owes and when each is due. It sits above the [documentation-kit](documentation-kit.md), which says what evidence each kind of change owes. The plan says which documents hold that evidence and the analyses around it.

**Scope.** The plan belongs to work that builds a change: a feature, a fix, maintenance, a prototype, and every later round of that work, its ship round included. A review of someone else's change, an audit, an incident, research and learning owe only their kit rows. A workstream that spans several epics is out of scope.

## Scale picks the backbone

**The work is an epic** when any of these holds; otherwise it is a task:
- its tracked item has child items;
- its intent names phases, gates or streams;
- its decomposition yields more than one unit that ships as its own change request.

(basis: maintainer, 2026-11-11, a house rule; precedents: NASA's software classes, privacy-impact screening)

Scale is read again every round. A task that becomes an epic owes the epic's backbone from that round on. An epic that becomes a task drops the epic-only documents, as a re-screen does.

| Scale | Backbone |
|---|---|
| Task | the task record (its front page), the spec with its acceptance criteria, and the kit's pieces for the change's kinds |
| Epic | the task's backbone, plus a design document, a decision register (with a decision brief for each tier-1 question), traceability, a RAID log, a test plan and a close-out record |

A tier-1 question owes a decision brief at either scale. A **tier-1 question** is one whose answer is a one-way door, by [design-for-reversibility](../engineering/design-for-reversibility.md), and reaches beyond the task's own change, such as a schema others read or a contract others call. (basis: maintainer, 2026-11-11, a house rule)

A glossary joins either plan when the work first coins a term, or uses one in a sense particular to this project. An FAQ joins when someone outside the work first asks a question about it, a question such a person asked in the sources the work starts from counting as asked. Neither is predicted, and each is due from its trigger.

**A task owes no spec** when its change is one of:
- behaviour-preserving, a refactor that changes shape but not meaning;
- an objective numeric improvement, such as speed or size, with nothing else moving;
- invisible outside the change: no person and no code outside the diff observes a difference.

The plan names which. The kit's rows and the concerns still apply: the exemption governs the backbone only. (basis: Rust's RFC exemptions; maintainer, 2026-11-11, the exemption read as backbone-only)

## Concerns add analyses

Answer each question yes or no, with a one-line reason; a "no" keeps its reason too. A kit row of the change forces "yes" only where the row's trigger also meets the question, as the last column says.

| Concern | The question | "Yes" adds | Forced "yes" by |
|---|---|---|---|
| Personal data | Does the work collect, keep, move, expose or delete data about people? | a privacy screening and a privacy threat model | Security-relevant, when the data kept or sent outward is about people |
| Trust boundary | Does it change who can reach what: credentials, authentication or authorisation, a trust boundary, or an endpoint's access? | a threat model | Security-relevant, when it changes who can reach what |
| Shared contract | Does it change an interface, schema, event or file format that code outside the change consumes? | a breaking-change notice when the compatibility class is breaking or behavioural | API or tool contract |
| Production step | Does it reach production users in steps (a percentage, a cohort, a flag), or through a step that is a one-way door? | a cutover plan with a go/no-go card per gate; a readiness review | Rollout, flag or deploy order; Schema, when a step is destructive |
| Outside service | Does it start relying on a service another organisation runs, or move state into one? | a vendor review; a backup and restore plan for state that moves | Dependency added, when the dependency is a service rather than a library |
| Reliability | Does it run under a reliability target, or create one, or add a dependency, such as an outside service or a new job, whose failure stops a flow every user must complete before using the product at all, such as signing in? | an SLO document with its error budget policy; alerts and a runbook | — |
| People affected | Does what people see, or how they sign in or use the product, change? | a communications plan with support notes; an accessibility and localisation check | UI |
| Novelty | Does the brief name no **existing** code doing the same kind of thing as the change, while the intent names no approach? | spike findings, before the design is agreed | — |

The questions are the ratified questionnaire. Shared contract, production step, outside service and reliability follow anchored axes, and personal data does too within data-protection law's scope. Everything else is a house rule: personal data outside that scope, trust boundary, people affected, novelty's test, and reversibility. (basis: maintainer, 2026-11-11) Reliability's dependency clause is proposed and not yet ratified, and applies until the maintainer rules on it. (basis: benchmark, 2026-11-12, an outside service put on sign-in left on-call with no runbook)

## When each is due

| Due | Documents |
|---|---|
| **Before the build** | the spec; the design document, at least its minimum form; the decision register's tier-1 questions and their briefs; the threat models and the privacy screening; the test plan; the vendor review; the spike findings |
| **During the build** | decision records, as decisions are agreed; the register's other questions; the RAID log; traceability; the backup and restore plan |
| **Before the gate that needs it opens** | the cutover plan and its go/no-go cards; the readiness review; the runbook, alerts, SLO document and error budget policy; the breaking-change notice; the communications plan; the accessibility and localisation check |
| **From its trigger** | the glossary and the FAQ, from the filing whose result first meets the trigger |
| **After** | the close-out record, with what was built and who owns the outcome afterwards |
| **As the kit says** | the kit's pieces, each captured at the moment its row names |

- **Before a gate opens** means finished by the first filing of a build step, or by the first filing after the gate gets its `opens on` when that comes sooner, since a gate could open any day once the build starts: a gate's documents are what its decider and on-call read before calling go, not records of it. (basis: benchmark, 2026-11-12, runbook and cards owed at the gate itself reached on-call too late)
- **A gate** is a gate the intent names. Without one, it is the ship round of the change that needs the document, or that change's merge when it has no ship round. A gate the intent names whose step the sources the work starts from show already running in production at its full exposure has passed, so its documents are late from the first filing. A preparatory gate, one whose `users see it` is `no` ([cutover-plan](../../skills/document/rules/types/cutover-plan.md)), is not a gate here: it sets no due point and never passes, since nothing reaches users at it.
- **The task record** is kept current from the first filing.
- **A document owed late,** after its due point passed, or whose page still has a section in minimum form at it when the plan owes more than that form there, is owed now and marked late.
- **A due point is not a gate:** a missing document is listed as owed, and the work goes on.
- **Detail that drifts,** such as runbook commands or a detailed design, is finished before the gate that needs it opens. (basis: Lethbridge, Singer & Forward 2003, drift hits detail first)

## Changing the plan

- **Adding** a document needs no reason.
- **Dropping** one the plan owes needs a reason, recorded, and no one's acceptance: a document no reader needs costs every reader who meets it. A drop carries into later rounds until the answer or scale that owed the document changes. (basis: field findings, 2026-11-25 — adding was free and dropping needed acceptance, so sets only grew)
- **Every round re-screens** the scale and every concern.
  - A question that turns "yes" adds its documents.
  - One that turns "no" drops them, with that as the reason.
  - Code from a probe or prototype that moves into production is screened again as new work. (basis: NASA NPR 7150.2D, a prototype adopted for operations is reclassified)

## Documents for an outside decider

An outside decider is a person outside the work whose approval a gate or the intent needs, and who reads the set to give it. Documents going to one follow these, in addition to the rest. (basis: field findings, 2026-11-25 — an outside approver stopped reviewing sets that were too big, carried scope beyond the approved source, and asked dozens of untriaged questions)

- **Sibling tasks.** A budget or a criterion stated for several sibling tasks together is counted and tested over this task's own set, and the message that sends it names the siblings it didn't cover; reading across siblings waits on a cross-task coordination mode not yet built.
- **What reaches them.** A document the plan writes for the decider, such as a decision brief or a summary page made for them, carries every open ask whose decider is them, whatever its tier, and of the rest only tier-1 decisions and those a reader would challenge — one that reverses something the decider said, or departs from the scope source — each cited by id. Every other decision stays in the decision register as filed, linked once. The set's reader tabs keep their own tests ([reader-tabs](../../skills/document/rules/reader-tabs.md)).
- **Their budget, when they set one.** When the decider, or the user for them, states a size budget, it is recorded among the brief's obligations in a unit that can be counted: words or questions. A budget stated otherwise, in pages, minutes or as "short", is turned into one of those with the user once. Before the set goes to them, its size is counted over the pages the share links, not what those link onward, and a set over it goes only with the user's go. Refused, the user says what to cut; the run never cuts by a number on its own. With none stated, there is no budget.
- **Their questions.** Each question going to them is `lean`, with its lean, or carries in its body the reason none can be given. A question the scope source answers is decided as [scope-source](../../skills/spec/modules/scope-source.md) enters the source's decisions. One the proposal's own defaults answer ([run-the-act](../../skills/work/phases/03-run-the-act.md)'s Propose, then run) is filed as a decision taken by default, `proposed` under the decider and listed for them, not asked. A question this task shares with a sibling task the user names is asked once, in the register of the first to file it, the other citing it as `<task key>:<id>` ([items-and-agreements](../../skills/document/rules/items-and-agreements.md)). Before sending, the run reports how many questions go, against the budget when it counts questions.
- **Their criteria.** When the decider has said what they will check, those criteria are recorded among the brief's obligations. Before the set is called ready for them, one pass tests each, pass or fail, with the item or page that shows it, run by the [reader-sweep](../../agents/critics/reader-sweep.md) critic handed the criteria, or, without fan-out, by the run in a pass of its own. A fail is fixed, or named in the message that sends the set; it is never sent as ready.
- **The version they read.** The share names the version sent: the version the artifacts port returned for it, else the time of the filing it shows. The task's memory entry records the share, with that version and date, until the decider answers ([keep-the-task-memory-entry](../../skills/work/rules/keep-the-task-memory-entry.md)). While it stands, each later filing that changes an item's content on a page the share linked lists those items in the task history's current round under *Changed after sharing* ([task-history](../../skills/document/rules/types/task-history.md)); the filing that records the share isn't one. The next message to the decider leads with that list, and pins the version it sends in place of the earlier one, the list starting again. Their answer, an agreement whose decider is them or the user's word that they answered, a question back being none, approves at the version pinned unless it names another, and the filing that carries it removes the record. Nothing is held back. (basis: maintainer, 2026-11-25 — pin and record, since a hold had to outlive the act and the session)

## What the plan records

- the scale, with the condition that set it;
- each owed document, with when it is due, and late when it is;
- each concern's answer, with its reason;
- each drop, with its reason.

> **Scale:** epic, as its tracked item has four child items.
>
> **Before the build:** spec; design document; decision register (3 tier-1 questions, each with a brief); trust-boundary threat model; privacy screening and privacy threat model; test plan; vendor review.
>
> **During:** decision records; RAID log; traceability; backup and restore plan.
>
> **Kept current, and as the kit says:** task record; the kit's pieces for the schema, contract, security-relevant and rollout rows.
>
> **Before its gate opens:** cutover plan with four go/no-go cards, its page filed with the plan's gates; readiness review; runbook, alerts, SLO document and error budget policy; breaking-change notice; communications plan; accessibility and localisation check.
>
> **After:** close-out record.
>
> **Concerns:**
> - personal data yes (membership leaves for an outside processor);
> - trust boundary yes (sign-in moves to an identity provider);
> - shared contract yes (tokens gain a required claim: breaking);
> - production step yes (four switches, one one-way);
> - outside service yes (membership moves into the provider);
> - reliability yes (sign-in can't complete while the identity provider is down);
> - people affected yes (sign-in pages change);
> - novelty no (the brief names the earlier migration of another service as existing).
>
> **Dropped:** none.
