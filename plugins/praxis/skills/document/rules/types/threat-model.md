# Threat model

What can go wrong where a change moves who can reach what, analysed element by element over a data-flow diagram, and what will be done about each threat.

**Reader and question.** Reviewer (of the change, best one from outside the team): "what can an attacker do through this change, and is each threat handled?"

**Page.** `own page`

## Membership

The analysis the plan's trust-boundary concern owes. It answers four questions: what are we working on, what can go wrong, what are we going to do about it, and did we do a good enough job. (basis: the Threat Modeling Manifesto, adopted by OWASP) It holds:
- the model of the part of the system the change touches: its elements, trust boundaries, entry and exit points, assets, trust levels, and the services others run;
- the threats against each element and the response to each;
- the analysis's limits.

Risks no attacker drives belong to the RAID log. What a provider's plan and terms commit us to belongs to the [vendor review](vendor-review.md), though the provider's service is an element here. Privacy threats belong to the [privacy threat model](privacy-threat-model.md), which fills this page's section on people.

A task has one threat model, about the trust boundaries its change touches. It is filed again in each round whose result adds or changes an element, a threat or a response.

A threat is restricted when filed with its exploit path unfixed or not known to be fixed; only the developer changes it ([items-and-agreements](../items-and-agreements.md)). So is a mitigation whose body describes the exploit it closes. So the full page, every item in place, goes to the task's restricted destination, and the model itself is access-controlled. The team page shows the model and the team items. In the coverage grid, a cell whose threats are all restricted reads "analysed". An element's `personal data` names categories, never anyone's records, so it is `team`. Its `holds` and `access` name kinds of asset and trust levels, never where a secret lives, so they are `team` too. (basis: OWASP, restricting access to the threat model itself; maintainer, 2026-11-11, after a documentation site published an unreleased exploit path)

## Items

**Element `ELM`.** One part of the data-flow diagram.
- Fields:
  - `element` enum `external entity`, `process`, `data store`, `log store`, `data flow`, `trust boundary`;
  - `scope` enum `analysed`, `not yet analysed`, `out of scope`, and `scope reason` text, required out of scope (basis: Microsoft Threat Modeling Tool, an out-of-scope element needs a written reason);
  - `within` id, the trust boundary it sits inside;
  - for a flow, `from` and `to` id, and `crosses` list of id, the trust boundaries it crosses;
  - `point` enum `entry`, `exit`, `both`, `none`, for a flow that crosses a boundary. An exit point is where data leaves, including an error message or page that reveals whether an account or membership exists (basis: OWASP Threat Modeling Process);
  - `trust level` text, who may use an entry point;
  - `holds` list of text, the assets it holds or carries, and `access` list of text, the trust levels that may reach them;
  - `personal data` list of text, the categories of data about people it holds or carries;
  - `operated by` enum `us`, `another team`, `another organisation`;
  - `not applicable` list of text, each `<threat category>: <reason>`, for a category that applies to its type but can't arise here.
- Granularity: one element per thing deployed separately, per data store, per external entity, and per trust level a process runs at. This is deliberately coarse: finer splits are the author's call when a threat needs them. A service another organisation runs `rests-on` its entry in the vendor review.
- Change regime: `baseline`.
- Agreement: `needed`.

**Threat `THR`.**
- Fields:
  - `category` enum `spoofing`, `tampering`, `repudiation`, `information disclosure`, `denial of service`, `elevation of privilege` (basis: STRIDE, Microsoft);
  - `elements` list of id, the elements it affects;
  - `likelihood` and `impact` enum `high`, `medium`, `low`, `not estimated`, anchored as the [RAID log](raid-log.md)'s probability and impact, with likelihood measured over the system's next year of use rather than a risk's proximity. The value or range behind each, with its unit, such as "1–4 a year" or "up to 40,000 accounts", is in the body;
  - `rank` enum `high`, `medium`, `low`, `not ranked`, looked up from likelihood and impact, never computed by multiplying scores (basis: OWASP prefers a qualitative rank; Cox, in the maintainer's visual rules, 2026-11-11):
    - `not ranked` when either is `not estimated`;
    - `high` when either is `high` and the other at least `medium`;
    - `low` when both are `low`;
    - `medium` otherwise;
  - `response` enum `mitigate`, `eliminate`, `transfer`, `accept` (basis: OWASP Threat Modeling Cheat Sheet);
  - `rationale` text, why it was accepted or transferred;
  - `remainder owner` text, for a transferred threat, who owns the remaining controls and the residual risk, since transfer doesn't reduce it;
  - `residual likelihood` and `residual impact`, as `likelihood` and `impact` once the response is in place;
  - `residual` enum `high`, `medium`, `low`, `not ranked`, looked up from them as `rank` is.
- Granularity: one way of attacking, with one category and one response. The same attack on several elements is one threat. Parts of it that need different responses are separate threats.
- Change regime: `baseline`.
- Agreement: `needed`. A threat whose `response` isn't chosen is `open`; once a response is written it is `proposed`.

**Mitigation `MIT`.**
- Fields: `tracked in` text, the work item that carries it, when no requirement serves it and no test verifies it.
- Granularity: one control. A control that covers several threats is one mitigation with several `covers` links. A requirement that `serves` it makes it a security requirement.
- Change regime: `baseline`.
- Agreement: `needed`.

No kind has a `when` field, so each item's decide-by is the plan's fallback for this type's due point ([items-and-agreements](../items-and-agreements.md)).

## Sections

1. **What's left after our responses?** Always. The residual view. Below it, each accepted or transferred threat with its rationale, its remainder owner, and the agreement that accepted it.
2. **What are we working on?** Always. The data-flow diagram (`data-flow` form), with a key: trust boundaries as groups, elements as nodes, each flow labelled with its id. Then the element view.
3. **What can reach what?** Always. The asset view.
4. **What do we rely on that others run?** When an element is operated by another team or organisation. The dependency view.
5. **What can go wrong, element by element?** Always. A table the page writes, not a view, since the categories are enum values rather than items. It has a row per analysed element other than a trust boundary, and a column per category. Each cell holds that element's threats in that category, or "n/a" and its reason, and is blank where the category doesn't apply to the element's type: an external entity takes spoofing and repudiation; a process all six; a flow and a data store tampering, information disclosure and denial of service; a log store those and repudiation (basis: STRIDE per element, a practitioner convention, unverified at source). Then the category view.
6. **What are we doing about each?** Always. The mitigation view.
7. **What could it reveal about people?** When the privacy threat model is owed and shares this page. Its sections.
8. **What didn't this cover, and who checked it?** Always. Elements not yet analysed or out of scope, with reasons. What STRIDE over this diagram can't see, and techniques left out on purpose, such as attack trees for goals that take several steps or misuse cases for business flows. Who took part, and who reviewed it from outside the team.

## Checks

- *Computed.* `point`, `trust level` and `access` may be `unknown`, which a judgment check catches at the build:
  - every analysed element is covered for each category its type takes, by a threat on it or a `not applicable` entry (derived from STRIDE per element);
  - every flow that crosses a boundary has `point`, and every entry point has `trust level` (derived from OWASP's process);
  - every element with `holds` has `access` (derived from OWASP's assets by trust level);
  - every element out of scope has `scope reason`;
  - `within` and `crosses` name trust boundaries, `from`, `to` and a threat's `elements` name other elements;
  - every threat that isn't `open` has `response`. An accepted or transferred one has `rationale`, a transferred one `remainder owner`, and a mitigated or eliminated one is `covered-by` a mitigation (basis: OWASP Threat Modeling Cheat Sheet);
  - every mitigation `covers` a threat or privacy threat, and is `served-by` a requirement, `verified-by` a test, or has `tracked in` (derived from OWASP's "can mitigations be tested");
  - every element operated by another organisation `rests-on` a vendor, when the vendor review is owed (derived).
- *Judgment:*
  - a diagram that doesn't match the system as designed (basis: OWASP);
  - a category marked not applicable for a reason that doesn't hold;
  - an assumption, or a decision's drawback, whose failure would give someone access the trust model's `access` doesn't grant them, with no threat whose body names it (basis: field prototype, a decision's bad consequence turned into a threat);
  - a missed exit point: an error message, redirect or sign-in page that reveals whether an account, tenant or membership exists;
  - a log typed as a plain data store, so repudiation is never asked;
  - a likelihood or impact that doesn't fit its anchor, or a rank or residual that doesn't follow the lookup under Threat;
  - a transferred threat treated as reduced (basis: the Manifesto's anti-patterns, as the next two);
  - techniques added to look thorough, or analysis that stops at the diagram;
  - one person modelling alone, or nobody outside the team reviewing it;
  - a mitigation that defers to a lower layer, such as "the platform handles it", with nothing showing it does;
  - a service others run trusted with no reason given;
  - a `point`, `trust level` or `access` still `unknown` when the build starts.

## Views

- Residual: `THR` as a `table`, sorted by `residual`, descending, then `rank`, descending: title, category, elements, rank, response, residual, state, owner, and the covering agreement's decider, date and link.
- Elements: `ELM` as a `table`, grouped by `element`: title, within, from, to, crosses, point, trust level, scope.
- Assets: `ELM` with `element` not in `trust boundary`, as a `table`: title, holds, access.
- Dependencies: `ELM` with `operated by` in `another team`, `another organisation`, as a `table`: title, operated by, rests-on.
- Categories: `THR` as a `table`, grouped by `category`: title, elements, rank, response, state.
- Mitigations: `MIT` as a `table`: title, covers, served-by, verified-by, tracked in, state, owner.

## Minimum form

The model as far as it's known, with any `point`, `trust level` or `access` not yet known as `unknown`, every element `not yet analysed` and listed under what this didn't cover, "no threats identified yet", "no mitigations yet", and "not yet reviewed".
