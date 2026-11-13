# Items and agreements

When a type holds only prose, nobody can tell whether a requirement has a test, or whether a question has a decider. This rule applies to every type whose file declares item kinds, and where older text in that file or elsewhere in this skill says otherwise for such a type, this rule decides. An agreement is not a document type: a review record or a task record is a page, and it holds items like any other page.

## What a type declares

For each item kind it holds, a type file declares:

- **Prefix.**
- **Fields**, each with its type: `text`, `number`, `date`, `period` (an ISO 8601 duration, such as `P14D`), `when` (a date, the id of the gate it must come before, or a due point written `build start`, `end of round <n>` or `close-out`), `id`, `list of <type>`, or `enum` with its values in order, highest first when the field ranks.
- **Granularity.**
- **Change regime.** One of `freeze`, `baseline` or `living` (see Agreements below). Unless the type says otherwise:
  - decisions take `freeze`;
  - a design document's sections take `living`;
  - every other kind takes `baseline`.
- **Agreement:** `needed`, or `none` for a kind that records what happened or was found rather than something to agree: a finding, a timeline event, a page's overview. A `none` kind's items are `recorded` (or `superseded` or `withdrawn`), never owe a decide-by, and never block on one. Its change regime governs only how its content is carried: a changed item stays `recorded`. By default a kind needs agreement, but the kinds of a type an act or a kit row names, such as a review, an audit, research, a spike, an incident or ship notes, default to `none`.
- **Live fields** views may join, each with its type, the capability it is observed through, and what is observed, such as `ci: the latest run on the change's head`. They are observed at publish and never enter the item.

A type also says whether it is **operational** (runbooks, alerts, SLOs), once for all its kinds. By default it isn't.


## Items

An item is one addressable piece of a type's content: a requirement, a decision, a question, a risk, a threat, a gate, a metric, a term, an FAQ answer, a design section. A type with no part a reader would cite on its own, such as an overview, is a single item.

**Granularity.** By default a piece is its own item when it can be verified, settled or tracked on its own: something is blocked by it, serves it, rests on it, verifies it, covers it, or asks whether it is done. Anything else stays prose in its item's body. An acceptance criterion the result says is verified separately from its requirement is its own item. Otherwise it stays in the requirement's body. A north-star clause that requirements serve is its own item.

Every item carries the following. A property the result doesn't hold is shown as missing, never filled from average practice or defaulted to the person running praxis. (basis: derived — laying a result out adds no claim) Two texts are drafted instead, since a reader needs a starting point to agree or change: a requirement's acceptance criterion, when the spec is filed, and a notice's copy, when the communications plan is shaped. Each is drafted only from filed items and the result. A part none of them gives stays in the text as a marked gap, `[<the part>: not known yet]`, and a threshold none gives is a `TBR` naming a question the item is `blocked-by`: `reversibility` `two-way`, its `reach` by the register's test, its decider the item's owner, else missing, and its decide-by `build start`. A drafted text's body says it was drafted, and its item stays `proposed` until an agreement settles it. (basis: benchmark, 2026-11-13, most requirements and every notice filed empty)

- **`id`**
  - The kind's prefix, a hyphen and a number: `REQ-12`, `DEC-3`, `Q-7`, `RISK-4`.
  - Each prefix belongs to one kind. A shared prefix makes two kinds of thing indistinguishable in a trace. (basis: maintainer, 2026-11-11)
  - Each prefix counts on its own, across the task's whole documentation.
  - **Matching a piece to an existing item.**
    - A piece the result ties to an id is that item. A piece that carries only part of it, such as one added link, changes only what it carries.
    - A result names a piece it means as new by a handle: its prefix, `new-` and a number of the result's own, `REQ-new-1`, and its links to that piece use the handle. Numbering the piece rewrites each use of the handle, in links and in text such as a `TBR`. A handle that matches an existing item by subject takes that item's id instead.
    - A piece with no id is the existing item that is about the same subject, even when its content changed: the same obligation tightened, the same question rephrased, the same risk re-rated. It is a new item only when no existing item is about its subject. When the existing item is a `freeze` item and the content changed, the piece is a new item that `supersedes` it.
    - A piece that splits one item into several, or merges several into one, is a new item for each piece. Each `supersedes` what it replaces.
    - An item the result doesn't mention is carried forward as it stands, unless its type files a page per round and says its items aren't carried, as a review record's findings belong to the round that found them. Only a result that says to drop an item starts its withdrawal, or a condition its type file names, such as a decision brief whose question leaves tier 1.
  - The next number is one above the highest that prefix has ever used. Items are never deleted, only `superseded` or `withdrawn`, so every number used stays visible.
  - A type that numbers its pages, such as decision records, numbers them by their item's id.
- **`kind`, `title`, `body`.** The body is neutral blocks ([portable-tree-shape](portable-tree-shape.md)).
- **`fields`.** The fields the type declares for the kind.
- **`links`.** Each link is a statement "this item *link* that id", stored on this item:

  | Link | Meaning | Reverse |
  |---|---|---|
  | `serves` | It exists for that need or goal. | `served-by` |
  | `blocked-by` | It can't be settled or done before that one. | `blocks` |
  | `covers` | It mitigates that risk or threat. | `covered-by` |
  | `verifies` | It is how that requirement is shown to hold. | `verified-by` |
  | `supersedes` | It replaces that item. | `superseded-by` |
  | `amends` | It changes that shipped item without replacing it. | `amended-by` |
  | `answers` | It settles that question. | `answered-by` |
  | `opened-by` | That gate or item made it due. | `opens` |
  | `rests-on` | It assumes that one holds. | `supports` |
  | `breaks` | It shows that requirement or criterion doesn't hold. | `broken-by` |

  - The reverse of each link is derived, never stored, so the two directions can't disagree. (basis: NASA SWE-052 bidirectional traceability)
  - A target is an id in the task's documentation, restricted and held-back items included, or a link to something outside it, such as a need in the ticket, by its URL or by a key whose prefix no item kind declares.
  - A target that resolves to neither is a finding.
- **`evidence`.** What the item's claims rest on: the sources [shape-the-document](../phases/02-shape-the-document.md) lists.
  - Each piece is a link, or, for a conversation that has none, who took part and when.
  - A verification is evidence: one finished check, by a person or a run, with when, what was checked, its outcome, and the run or review it rests on. Its `outcome` is `holds` or `fails` and its `when` a date, so views and status read it; evidence without an outcome is a source, not a check.
  - A link that doesn't resolve is a finding.
- **`owner`.** Exactly one person, the one who answers for the item being right. When the result names several, the owner is missing. One is never picked.
- **`sensitivity`**
  - `team` or `restricted`. Restricted by default:
    - a threat whose exploit path is unfixed when it's filed, or not known to be fixed;
    - an incident's details;
    - where and how secrets are stored or rotated;
    - personal data, or a finding that personal data is exposed.

    An item is restricted when any part of it shows one of these.

    Everything else is `team`.
  - Only the developer changes an item's sensitivity, with a one-line reason recorded on the item. A fix landing later doesn't change it, since that would read live state into an item.
  - A restricted item goes only to the restricted destination named for the task. The developer is asked for it once, the first time the task has restricted content, and it is remembered for the task.
  - Until a destination is named, restricted items are held back while everything else publishes.
  - Every other page shows how many restricted items it leaves out and names their owners to ask.

  (basis: maintainer, 2026-11-11, after a documentation site published an unreleased exploit path)
- **`state`.** Where the item stands in being agreed, never in being built.

  | State | Meaning |
  |---|---|
  | `open` | Nobody has chosen an answer. |
  | `lean` | One answer is favoured but not agreed. |
  | `proposed` | Content is written but no agreement covers it yet. |
  | `deferred` | Paused. Carries why, and what brings it back. |
  | `agreed` | An agreement covers it. A question's `agreed` reads "answered", a decision's "accepted", and a risk's or threat's "accepted" when its response is to accept it. |
  | `superseded` | Replaced by the item that supersedes it. |
  | `withdrawn` | Dropped. Carries why. |
  | `recorded` | Filed as found, for a kind whose agreement is `none`. |

  - **`open` / `lean` vs `proposed`.** `open` and `lean` are for an item whose content is still a choice among answers: a question, or a decision whose options are still being weighed. A decision the result records as chosen is `proposed`.
  - **Who sets it.** Only an agreement sets `agreed` or `superseded`, or moves an `agreed` item anywhere else. Two exceptions return an `agreed` item to `proposed`: a `baseline` item whose content changes, and an item a result drops, whose proposed content is then its withdrawal, written `{"withdrawn": "<why>"}`. The agreement that settles a proposed withdrawal withdraws the item. An item becomes `superseded` when an agreement settles an item that `supersedes` it. The result sets every other state as it says, with the why that `deferred` and `withdrawn` carry.
  - **When a result reopens an `agreed` item.** The item keeps its state, the developer is told, and an `open` question `opened-by` the item is filed. A drop returns the item to `proposed`, as above.
  - **The state is never inferred.** A requirement the spec states but nobody has agreed is `proposed`, however settled it reads. (basis: maintainer, 2026-11-11)
  - **A decide-by.** An `open`, `lean` or `proposed` item carries one: a date, or the gate it must be settled before. A gate counts as a date because the work is anchored to gates. A type may name one of a kind's own `when` fields as its decide-by, such as a risk's proximity; the item's decide-by is then that field. An item that has neither takes its type's due point in the documentation plan, written into its decide-by when it is shaped: before the build, `build start`; during the build, `end of round <n>` for the round that files it; at the gate that needs it, that gate; from its trigger, `end of round <n>` for the round that files it; after, `close-out`. An anchor a result gives in another form, for a decide-by or any `when` field, is mapped: a round to `end of round <n>`; a milestone, a slice or anything else stays in the item's body, and the value takes this fallback. (basis: maintainer, 2026-11-11)
  - **Where state shows.** A changed state is not a content edit. An item's current state shows on the current round's pages and in views. A closed round's page keeps the state the item had when that page was filed ([pages-belong-to-their-task](pages-belong-to-their-task.md)). A type filed again in a new round carries all its items that aren't `superseded` or `withdrawn`, mentioned by the result or not, so the current page is complete. When an item's state changes and the current round hasn't filed its type, the type is filed again.
- **`first_state` and `first_filed`.** The state and date of the item's first filing, set then and carried unchanged when it is filed again.
- **`review`.** Every item still open to change carries one: an item that isn't frozen (a `freeze` item once agreed, or a `living` item once its task closes out), `superseded` or `withdrawn`. After close-out, only an operational type's items keep one.
  - **Last reviewed.** Set only when a result says the whole item was checked: a review or verification step, or the developer saying so. Never set by a rebuild, or because a round touched the item.
  - **Next review.**
    - While the work runs: the next gate's id, or `end of round <n>` when no gate falls in the current round.
    - After close-out: three months after the last review, or after close-out if the item was never reviewed. (basis: maintainer, 2026-11-11; the interval, Google's freshness reminders)
  - **Change notes.** One per change a reader must act on or know: what to do or know differently, a deadline, a correction of something wrong. Never one for wording or layout. Each says what changed, never just "updated", and carries its date: `{"date": "…", "what": "…"}`. (basis: NHS "page last reviewed"; GOV.UK change notes)

## Live state stays out

Current build and run state is never written into an item or an agreement:
- a change request's status;
- a pipeline's latest result;
- a ticket's status;
- whether a gate currently passes;
- coverage;
- how many requirements are built or met.

It is observed from the systems when the documentation is published and joined in when a page is rendered.

**The discriminator:** would this value change without anyone deciding or checking anything? If so, it's live state.

A system's current status is live state, dated or not, unlike a verification. When a result carries one, it is left out while shaping, and the developer is told. The blocking finding below catches one that reaches an item anyway. A "holds" with no verification behind it is a claim, marked `(unsourced)` like any other. (basis: maintainer, 2026-11-11)

## Agreements

An agreement is one agreement event the result carries: an approval, a decision made in a thread or a meeting, a sign-off. Filing documentation never creates one, and neither does shipping. The developer confirming a choice during the run is one, with the developer as decider. It is shown beside each item it settled, and it shows a restricted item's agreed content only where that item may appear. It holds:

- **`id`.** Prefix `AGR`, counted like any item.
- **The items it settled**, each with its content as agreed. An event settles only `proposed` items directly. A question an item it settles `answers` becomes `agreed` with it. An event that names items settles those. A result that decides an `open` question files the decision as an item that `answers` it, and the same event settles that item. An `open` or `lean` decision a result names as chosen becomes `proposed` first, then is settled. An approval of a page names no items, so it settles the `proposed` items written in that page's body at the version approved, whichever round first wrote them. An approval of a revision of the documentation settles the `proposed` items whose content it changed. Approving a code change settles no item. It is evidence on the items the change serves. Items shown on a page only through a view, and items in other states, are untouched. An approval read back from a documentation backend settles nothing until the developer confirms it.
- **The approval trail**
  - **decider:** exactly one person: the one the result names as deciding, or the sole approver of an approval;
  - **consulted** and **informed;**
  - **the date;**
  - **a link** to where it happened.

  A part of the trail other than the decider that the result doesn't hold is shown as not recorded.

**No decider, no agreement.** An event with no decider isn't an agreement, such as several approvals with none named the decider. Its items stay `proposed`, and the approvals are kept as evidence on them. One of several approvers is never picked as decider. (basis: PMI and DACI single decider)

**How agreed content changes follows the kind's regime:**

- **`freeze`**
  - Changing it means a new item with a new id that `supersedes` the old one.
  - The new item is `proposed`, and the old one stays as it is until an agreement covers the new one.
  - Its content is never edited in place.
- **`baseline`**
  - The item keeps its id as it changes.
  - Changed content is `proposed` again until an agreement covers it. Content changes when what the item says changes: what it requires, a value, its scope. Rewording that says the same thing isn't a change, and the item keeps its agreed content.
  - The task has one baseline: the latest agreed content of every `baseline` item, named by the id of the last agreement that touched one.
  - An item whose content differs from its baseline content shows that it changed, and since which agreement.
- **`living`**
  - Corrections land on the current round's page, carrying the content forward under the same ids, each with a change note.
  - A correction keeps the item's state. An `agreed` item shows that its content changed since its agreement, and the change notes say how. It needs no new agreement. (basis: maintainer, 2026-11-11)
  - It freezes when its task closes out (for an epic, the epic's close-out, not its first ship round; basis: maintainer, 2026-11-11, "until its epic ships" read as the whole epic). Anything later is an amendment: a new item that `amends` it.

(basis: maintainer, 2026-11-11, between the freeze-and-supersede and keep-living traditions)

**A gate records what it ran under.** A gate is an item kind. Each of its runs is a verification on it, which also lists:
- the agreements whose event date is on or before the run's date, other than those whose items had all been superseded;
- for each `living` item the gate `rests-on`, its latest change note, or its filing date when it has none.

So "was this agreed, and in what form, before it ran?" can be answered afterwards.

**Two patterns are flagged, not blocked.** Each shows as a note beside the agreement, naming the pattern.

- **Accepted at creation:** an item whose first filed state, kept in the store as `first_state` beside its date as `first_filed`, is `agreed`, under an agreement that records nobody as consulted. A consulted list that wasn't recorded counts as nobody consulted.
- **Self-acceptance:** a risk or threat whose response is to accept it, agreed under an agreement whose decider is the item's own owner.

Both can be legitimate. (basis: a 2026 study of open-source decision records found most were opened already accepted; maintainer, 2026-11-11)

## Shared checks

Every type's store gets these checks, which [check_store.py](../scripts/check_store.py) runs over the merged store, restricted items included, so links between the two resolve. It blocks on the store integrity the publish needs:
- ids well formed, unique, and of a declared kind;
- known states and link kinds;
- field values of their declared types, each element of a list included;
- each declared field type one the store allows, `enum` written `{"enum": [values]}`;
- every agreement with exactly one decider;
- every evidence entry with a link, or who took part and when;
- every recorded agreement date, `first_filed` and evidence `when` written as a date;
- every change note with a date and what changed.

A finding on an agreement stops every copy that holds it.

It also blocks on the findings below, and raises the two flags above without blocking.

**What the filing step does itself.**
- **Outside links and evidence links.** The script lists them, and the filing step resolves them: a code citation against the repository at its commit, a web link by fetching it.
- **Diagram geometry and colour.** These are checked by each adapter as it draws.
- **Live state in prose.** The script catches a declared live field written into an item. A live value in an item's body or a text field is caught by the shaping step, by the live-state discriminator above.

(basis: maintainer, 2026-11-11, computed checks as shipped scripts)

## Findings that block publishing

Each finding is reported to the developer, naming the item and what's wrong:

- an unresolved link, `id` field or evidence link;
- an `id` field naming no item in the task's documentation;
- a missing owner, or more than one;
- a missing decide-by on an `open`, `lean` or `proposed` item, or one that isn't a date, a gate or a due point;
- a live-state value written into an item or an agreement.

The developer supplies the missing value or changes the item, and the documentation publishes. Flagged patterns and held-back restricted items never block. (basis: maintainer, 2026-11-11, computed checks gate publishing)
