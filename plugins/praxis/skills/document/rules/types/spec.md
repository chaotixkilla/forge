# Spec

The specification a task builds against: what must be true when the work is done, so the plan, the code and the tests can each be checked against it.

## Reader and question

A reviewer checking the change, and a maintainer building against it now or changing it later: "What must be true when this is done, and how will we know?"

## Page

`own page`.

## Membership

The spec step's result: its requirements, each with acceptance criteria and its source (a ticket, an RFC, a conversation), the constraints and non-goals, and what is still unsettled. A changed requirement reopens the spec: within its round, the page is updated with the change, its date and its source marked, not filed again, and its traceability row reopens with it. (basis: maintainer, 2026-09-30) A later round that changes a requirement files its own spec, restated whole. (basis: maintainer, 2026-10-07)

A requirement states *what* must hold, never how it is built; the how belongs to the [plan](plan.md) or the [design document](design-document.md).

## Items

**North-star clause `NS`.** One clause of the intent's goal that requirements serve.
- Granularity: one clause a requirement can serve on its own: the goal splits only where one outcome could hold while another fails.
- Links: it `serves` the need outside the documentation it comes from, such as the ticket, when there is one.

**Requirement `REQ`.** One obligation the change must meet.
- Fields:
  - `priority`: enum `must`, `should`, `could`, the release-scoped rung, missing on a `deferred` requirement;
  - `obligation`: enum, the declared convention's keywords, highest first: `MUST`, `SHOULD`, `MAY` by default, or `shall`, `should`, `may` under a convention that declares those;
  - `type`: enum `functional`, `quality`, `interface`, `constraint`:
    - `functional`: what the system does;
    - `quality`: how well a behaviour performs, measurably;
    - `interface`: what another party relies on;
    - `constraint`: a limit the solution must respect;
  - `verification`: enum `test`, `demonstration`, `analysis`, `inspection` (basis: ISO/IEC/IEEE 29148, unverified at source);
  - `stream`: text, optional, the stream of an epic the requirement belongs to, as the intent names its streams;
  - `rationale`: text.
- Granularity: one obligation, so one keyword. Two joined by "and" are two requirements. (basis: 29148's *singular*; EARS)
- Links: it `serves` an `NS`, or a need outside the documentation such as the ticket. A value not yet settled is written `TBR Q-<n>`, and the requirement is `blocked-by` that question, which carries the owner and decide-by a bare "TBD" lacks. A question is filed in the [decision register](decision-register.md), which it makes owed when the plan doesn't owe it yet ([documentation-plan](../../../../craft/writing/documentation-plan.md)). (basis: maintainer, 2026-11-11; NASA SE Handbook App. C, TBR with owner and date)

**Slice `SLC`.** One increment that ships on its own and delivers user-observable value. Once the plan has gates, its title opens with the code of the earliest gate that exposes its units, `<code> · <name>`, which the plan hands back.
- Fields:
  - `priority`: enum `must`, `should`, `could`, the highest `priority` among the requirements it delivers;
  - `spike`: text, optional, the unknown a time-boxed investigation must settle before the slice is committed.
- Links: it `serves` each `REQ` it delivers, and is `blocked-by` each slice it can't be built before and each question it waits on.
- Change regime: `baseline`.

**Acceptance criterion `AC`.** One observable check that its requirement holds.
- Fields: `verification`: enum, the same values as a requirement's `verification`, any of them.
- Granularity: as [items-and-agreements](../items-and-agreements.md)'s granularity rule decides for an acceptance criterion.
- Links: it `serves` exactly one `REQ`.

## Sections

1. **What is this for?** — always. The north-star clauses as a list, and the need outside the documentation each one comes from.
2. **How binding is each requirement?** — always. The keyword convention, declared once: "The key words MUST, SHOULD and MAY are to be read as in BCP 14 (RFC 2119, RFC 8174) when, and only when, they appear in capitals." A spec that adopts another convention, such as *shall* for a requirement and *should* for an unverified goal, declares that one instead. (basis: RFC 7322 §4; maintainer, 2026-11-11, declare the convention)
3. **What must be true?** — always. The requirements view.
4. **How will we know each holds?** — present when any acceptance criterion is its own item. The criteria view, each criterion's title being its given, when and then: a known state, a trigger, an observable output, three to five steps. (basis: Cucumber reference)
5. **What is out of scope?** — always. The non-goals as prose, each a goal someone could plausibly want; the constraints are requirements of type `constraint`, shown in section 3.
6. **In what slices does it ship?** — present when the spec carries slices. The slices view, then each slice's spike, when it has one, in prose.
7. **What is still unsettled?** — always. The unsettled view: each question in `open`, `lean` or `proposed` that a requirement is `blocked-by`, with its owner and decide-by; then the assumptions view.
8. **Which decisions shape these requirements?** — present when decision records join this page, at task scale. The decision records fill it.

## Checks

*Computed:*
- The page declares its keyword convention. (basis: RFC 7322 §4)
- Each requirement's body holds exactly one keyword of the declared convention, spelled as the convention spells it, and that keyword is the requirement's `obligation`. (basis: RFC 2119; NASA App. C, one thought per requirement)
- Each requirement `serves` an `NS` or a need outside the documentation. (basis: NASA SWE-052; maintainer, 2026-11-11)
- No requirement or criterion holds "TBD", and each `TBR` names a question the requirement is `blocked-by`. (basis: NASA App. C)
- A `quality` requirement states a number with a unit, a percentile or a percentage, or a `TBR` whose question isn't `agreed`; once it is, the number is written in. (basis: 29148; arc42 §10)
- Each acceptance criterion `serves` exactly one requirement.
- Every requirement not `superseded` or `withdrawn` is served by at least one acceptance criterion. (basis: benchmark, 2026-11-13, most requirements filed without one, so a reviewer couldn't tell when they held)

*Judgment:*
- A requirement that hits one of the smells: subjective language, ambiguous adverbs or adjectives, loopholes, open-ended terms, superlatives, comparatives, negatives, vague pronouns, incomplete references. A hit prompts a reread, never a rewrite on its own. (basis: Femmer et al. 2017, about 59% precise)
- A requirement that says how rather than what. (basis: NASA App. C)
- A requirement that joins two triggers either of which sets it off alone, or two outcomes, so it could hold in part. (basis: NASA App. C, one thought per requirement)
- A requirement no one could check by its named method.
- A requirement whose omission would harm nothing, the sign of over-engineering. (basis: NASA SWE-052, worst outcome if omitted)
- A north-star clause no requirement serves.
- A non-goal no one would plausibly want, listed to look thorough. (basis: Ubl, "Design Docs at Google")
- A negative that leaves the behaviour unspecified.
- A criterion coupled to the screen layout or the database. (basis: Cucumber reference)
- A requirement resting on an assumption nobody confirmed before it was agreed. (basis: NASA App. C)
- A term used in a sense the [glossary](glossary.md) doesn't give it.

## Views

- **Requirements**, in What must be true?: `table` of every `REQ` not `superseded` or `withdrawn`: title, obligation, priority, type, verification, `serves` and state, sorted by type in its declared order, then by id.
- **Criteria**, in How will we know each holds?: `table` of every `AC` not `superseded` or `withdrawn`, grouped by the `REQ` it `serves` and sorted by id: title and verification. One chain per requirement would draw a small fan for each, which a grouped table says better ([when-a-visual-is-owed](../../../../craft/writing/when-a-visual-is-owed.md)).
- **Slices**, in In what slices does it ship?: `table` of every `SLC` not `superseded` or `withdrawn`, sorted by priority in its declared order, then by id: title, priority, what it `serves`, what it is `blocked-by`, empty marker `none`. The order to build in follows `blocked-by`, which the column shows.
- **Assumptions**, in What is still unsettled?: `table` of every `ASM` (home: [raid-log](raid-log.md)) whose `status` is `open` that a `REQ` `rests-on`: title, `if false`, `validation`, `validate by` and `supports`.
- **Unsettled**, in What is still unsettled?: `table` of every `Q` in `open`, `lean` or `proposed` that `blocks` a `REQ`: title, owner, decide-by and `blocks`, sorted by decide-by, earliest first.

## Minimum form

What is this for? names the need the intent states, or says the intent states none; the keyword convention is declared.
