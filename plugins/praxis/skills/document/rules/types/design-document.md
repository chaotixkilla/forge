# Design document

The design an epic builds toward: its context, the qualities it must have, how it works, what else was weighed and why it might still be wrong, kept current until the epic closes.

## Reader and question

A reviewer or decider now, and a maintainer later: "Which trade-offs did we make, and why?" (basis: Ubl, "Design Docs at Google")

## Page

`own page`. The [glossary](glossary.md) joins it, its terms view filling What do these words mean here? under no heading of its own.

## Membership

One per task. It holds the design, the trade-offs and the reasoning behind them. It does not hold:
- requirements, which are the [spec](spec.md)'s and shown here;
- a decision's full context and options, which are its [decision record](decision-record.md)'s, linked here;
- threats, which are the [threat model](threat-model.md)'s.

Content of those kinds that grows here is split to its own page ([one-type-per-page](../one-type-per-page.md)).

It is filed again in every round that changes the design. (basis: maintainer, 2026-11-11, living until the epic ships, then amended)

## Items

**Design section `DES`.** One part of the design a reader cites on its own.
- Fields:
  - `aspect`: enum `context`, `goal`, `non-goal`, `structure`, `runtime`, `deployment`, `interface`, `data`, `security`, `privacy`, `observability`, `version skew`, `alternative`, `drawback`, `inconsistency`;
  - `why not`: text, for an `alternative`, why it lost;
  - `applies`: enum `yes`, `no`, `not known yet`, for a `security`, `privacy` or `observability` section.
- Granularity: one component, interface, store, flow, cross-cutting concern, alternative, drawback or inconsistency.
- Change regime: `living`.
- Links: a section `serves` the requirements and quality goals it meets; an alternative or a drawback `serves` the section it weighs against; a section `rests-on` each decision it builds on.

**Quality goal `QG`.** A quality the design is judged by and trades the others against, with a scenario that shows it.
- Fields:
  - `rank`: number, 1 the highest;
  - `stimulus`: text, what happens and to what;
  - `environment`: text, under which conditions;
  - `response`: text, what the system does;
  - `measure`: text, a number and a unit, or `TBR Q-<n>` while that question isn't `agreed`.
- Granularity: one quality with one scenario; three to five on a page. A quality requirement that is checked by a test is a spec requirement, which `serves` its goal. (basis: arc42 §1 and §10)

## Sections

1. **Why this, and what is out of scope?** — always. The `context`, `goal` and `non-goal` sections: the context and scope, the goals, and the non-goals, each a goal someone could plausibly want, excluded on purpose. (basis: Ubl)
2. **What must the design be good at?** — always. The quality goals view.
3. **How does it work?** — always. The `structure`, `runtime`, `deployment`, `interface` and `data` sections, opening on a system context diagram, then a container diagram where more than one container changes. Interfaces and stores are sketched, never pasted whole. (basis: C4; Ubl)
4. **Which requirement does each part meet?** — present when a spec is owed. The requirements matrix view.
5. **What about security, privacy and observability?** — always. One `DES` for each of security, privacy and observability, each with its `applies`; one whose `applies` is `no` says why in a line.
6. **What happens while old and new run side by side?** — present when the [documentation-plan](../../../../craft/writing/documentation-plan.md)'s Shared contract or Production step question is answered yes. The `version skew` sections: upgrade and downgrade, clients holding old state across the switch, and surfaces that switch at different times. (basis: KEP template)
7. **What else did we weigh, and why not?** — always. Each `alternative` with why it lost, doing nothing among them, and the decisions view: every decision record a section rests on. (basis: Ubl; Rust RFC template)
8. **Why might we not do this?** — always. Each `drawback`, and what happens if the work isn't done. (basis: Rust RFC template)
9. **What is still unresolved?** — always. The unresolved view.
10. **Where does this description disagree with itself or the code?** — always. Each `inconsistency`, or one line saying none is known. (basis: ISO/IEC/IEEE 42010, unverified at source)
11. **What do these words mean here?** — present when the glossary joins this page.

## Checks

*Computed:*
- Section 1 holds at least one `goal` and one `non-goal` section, or in minimum form a line saying the non-goals aren't known yet. (basis: Ubl)
- Every `DES` has a body, or one line saying what isn't known yet; an `interface` section's content is its `IFC`, and an `alternative`'s `why not` counts as its body. A body holding an item code and five words or fewer besides its codes, such as "IFC-2." or "See NS-1", is missing: it says where to look, not how the part works, and the section is filed as its one line saying what isn't known yet, naming those codes. (basis: benchmark, 2026-11-12, sections filed as titles alone; 2026-11-13, bodies filed as a bare code)
- At most five quality goals, each with its measure a number with a unit, or a `TBR` naming a question the goal is `blocked-by` that isn't `agreed`. (basis: arc42 §1)
- Each `alternative` has its `why not`. (basis: Ubl)
- Section 5 holds one `security`, one `privacy` and one `observability` section, each with its `applies`; one whose `applies` is `no` gives a reason. `not known yet` passes in minimum form.
- Every diagram block's caption names its form and its scope, every node has a kind, and every edge's label is non-empty and isn't "uses". The key is drawn by the adapter. (basis: C4 review checklist; maintainer, 2026-11-11)

*Judgment:*
- A requirement neither a part of the design nor a quality goal meets: its row in Which requirement does each part meet? is empty and it `serves` no `QG`. Judged, not computed, since the minimum form owed before the build may not reach every requirement, and one met outside the design, such as by configuration, says so. (basis: field prototype, cross-document coverage)
- Fewer than three quality goals, a scenario that couldn't happen, or one missing its stimulus, environment or response. (basis: arc42)
- A non-goal nobody would want, listed to look thorough. (basis: Ubl)
- An implementation manual: detail the code would state better, or a pasted schema that will drift. (basis: Ubl; Lethbridge, Singer & Forward 2003)
- No alternative, or a straw man beside the chosen one. (basis: Zimmermann, Dummy Alternative)
- Drawbacks that are only praise in disguise. (basis: Zimmermann, Fairy Tale)
- A design not argued against its quality goals.
- Clients that hold old tokens or schemas across a switch, with no version-skew section.
- A security section that defers to a lower layer, or names no residual risk. (basis: RFC 3552 §5)

## Views

- **Quality goals**, in What must the design be good at?: `table` of every `QG`: rank, title, stimulus, environment, response and measure, sorted by rank.
- **Requirements met**, in Which requirement does each part meet?: `matrix` of every `REQ` not `superseded` or `withdrawn` against every `DES` whose aspect is `not-in` `context`, `goal`, `non-goal`, `version skew`, `alternative`, `drawback` and `inconsistency`, each cell its `served-by`.
- **Decisions**, in What else did we weigh, and why not?: `table` of every `DEC` that `supports` a `DES`: title, state and `supports`.
- **Unresolved**, in What is still unresolved?: `table` of every `Q` in `open`, `lean` or `proposed` that `blocks` a `DES` or `QG`: title, owner, decide-by and `blocks`, sorted by decide-by.

## Minimum form

The form owed before the build at the least ([documentation-plan](../../../../craft/writing/documentation-plan.md)): the context names the goal the intent states; the non-goals, when none is known, say so in a line; and each concern in section 5 may be `not known yet`.
