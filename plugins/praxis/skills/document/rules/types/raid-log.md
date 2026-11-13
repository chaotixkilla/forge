# RAID log

The work's risks, assumptions, issues and dependencies in one place, each with one owner and what is being done about it.

## Reader and question

A maintainer running the work, and a decider it reports to: "What could stop us, what already has, what are we taking for granted, and whom are we waiting on?"

## Page

`own page`

## Membership

Every risk, opportunity, assumption, issue and dependency of the work, in PMI's vocabulary throughout. (basis: PMI Lexicon v4.0; research, 2026-11-11, no standard defines a combined log, so it bundles PMI's risk register, issue log, assumption log and dependencies, one vocabulary per register) A threat to the system's security is the [threat-model](threat-model.md)'s, and a question to settle is the [decision-register](decision-register.md)'s. Its subject is the work's exposure, so a task has one. It is filed again when an entry is added, changes, or is reviewed.

The `owner` every item carries is the person who watches the entry and chooses its response. Who carries the response out is the actionee, who may be someone else. (basis: PMI, risk owner and risk action owner)

## Items

**Risk `RISK`.** One uncertain event that would affect the work if it happened, for worse or for better.
- Fields:
  - `direction`: enum `downside`, `upside`. An upside risk is an opportunity. (basis: PMI, a risk can be positive)
  - `if` and `then`: text. The cause and event, and its effect on the work.
  - `trigger`: text. The sign that it is happening.
  - `probability` and `impact`: enum `high`, `medium`, `low`, each kept apart and never multiplied. (basis: Cox 2008, risk matrices)
    - `probability`: `high` when it is more likely than not to happen before its proximity; `low` when it is unlikely, about one in five or less; `medium` between.
    - `impact`: `high` when a gate or a north-star clause would be missed; `medium` when a gate would slip or a requirement be degraded; `low` when the work would absorb it.
  - `proximity`: when. When it could happen.
  - `response`: enum `avoid`, `mitigate`, `transfer`, `escalate`, `accept` for a downside risk; `exploit`, `enhance`, `share`, `accept` for an upside one. (basis: PMI response types)
  - `actionee`: text. One person, for any response but `accept` and `escalate`.
  - `escalated to`: text. Who an escalated risk went to.
  - `contingency`: text. What is done if the trigger fires.
  - `residual`: text. What is left once the response has worked.
  - `status`: enum `open`, `occurred`, `closed`. `occurred` is a status, never a closure reason: an occurred risk closes when the issue it opened closes.
  - `closure reason`: text. Why it closed: it passed, it was avoided, or the issue it opened closed.
  - `key person` (optional): text. The one person whose loss the risk is about.
- Links: a risk the response creates, a secondary risk, is `opened-by` the risk.
- An agreement on a risk settles its response.

**Assumption `ASM`.** One thing the work holds true without proof.
- Fields:
  - `if false`: text. What breaks if it fails.
  - `validation`: text. How it will be checked.
  - `validate by`: when. When it must be checked by.
  - `status`: enum `open`, `verified`, `false`, `closed`. `verified` when a check finds it holds; `false` when it failed, which opens an issue; `closed` when the work no longer rests on it.
  - `closure reason`: text.
- A check of it is a verification on it. One that finds it false sets its status to `false`.

**Issue `ISS`.** One condition already affecting the work.
- Fields:
  - `impact`: enum `high`, `medium`, `low`, anchored as a risk's impact.
  - `target date`: when. When it is to be resolved by.
  - `workaround`: text. What the work does meanwhile.
  - `status`: enum `open`, `closed`.
  - `closure reason`: text.
- Links: it is `opened-by` the risk or assumption it came from.

**Dependency `DEP`.** One thing the work needs from a party it doesn't control. (basis: IPA, the dependencies indicator)
- Fields:
  - `needs`: text. Who on the work needs it.
  - `provides`: text. The party that delivers it, and the person there who answers for it.
  - `need by`: when. When the work needs it.
  - `status`: enum `open`, `met`, `closed`. `met` when it is delivered; `closed` when the work no longer needs it or it was dropped.
  - `closure reason`: text.
- Links: the items it holds up are `blocked-by` it.

Every kind takes `baseline`. Each kind's decide-by is its `when` field: a risk's proximity, an assumption's validate by, an issue's target date, a dependency's need by. `status` is decided by someone, not observed, so it is a field and not live state. `status` and `closure reason` are bookkeeping: changing them isn't a content change.

## Sections

1. **What is going wrong now?** Always. The issues table.
2. **What could stop us?** Always. The risks table, which keeps an `occurred` risk while the issue it opened is open.
3. **Whom are we waiting on?** Always. The dependencies table.
4. **What are we taking for granted?** Always. The assumptions table.
5. **What could go better than planned?** When an upside risk whose status is `open` exists. The opportunities table.
6. **What has closed?** When an entry's status is neither `open` nor `occurred`. A list of each, with its reason and what it opened.

## Checks

*Computed:* each skips `superseded` and `withdrawn` items.
- Every risk has its if and then, trigger, probability, impact, proximity and response, and a response drawn from its direction's set. (basis: PMI; prototype sweep, 2026-11-11, trigger and proximity missed)
- A risk whose response is neither `accept` nor `escalate` names an actionee.
- An escalated risk names who it was escalated to, and has opened a question in the register. (basis: PMI, escalate when outside the team's authority)
- An occurred risk has opened an issue. A closed entry of any kind has its closure reason.
- Every issue has its impact and target date. Every dependency has both parties and its need-by. Every assumption has its if-false, validation and validate-by.
- An assumption whose status is `false` has opened an issue.
- One person owns more than half of the task's open items, at least five open items are filed, at least two people own one, and no open risk names that person as its `key person`. Open items are the [decision-register](decision-register.md)'s items whose state is `open`, `lean`, `proposed` or `deferred`, and this log's risks, assumptions, issues and dependencies whose status is `open`. The finding drafts the risk with only its if, then and key person filled: if that person becomes unavailable, then the items they own stall; its key person is that person. Its other fields show as missing, for the developer to supply. (basis: maintainer, 2026-11-11)

*Judgment:*
- A risk that is really an issue already, or a worry with no event.
- Ratings nobody could defend, or every risk rated medium.
- A response out of proportion to the risk.
- Escalation of what the team could settle itself, or no escalation of what it can't.
- A mitigation that creates a risk nobody filed, or a residual risk left blank.
- An entry past its next review.
- An assumption that is really a risk, because it is already in doubt.

## Views

- **Issues:** `table` of every `ISS` whose status is `open`, sorted by target date: impact, owner, target date, workaround, what it is `opened-by`.
- **Risks:** `table` of every downside `RISK` whose status is in `open`, `occurred`, sorted by proximity, ascending, then impact, descending: if, then, trigger, probability, impact, proximity, response, owner, actionee, escalated to, residual, last reviewed, and the risks and questions it `opens`. No heat map is drawn without these values beside it. (basis: maintainer, 2026-11-11)
- **Dependencies:** `table` of every `DEP` whose status is `open`, sorted by need by: needs, provides, need by, what it `blocks`.
- **Assumptions:** `table` of every `ASM` whose status is `open`: if false, validation, validate by, its latest verification, what `rests-on` it.
- **Opportunities:** `table` of every upside `RISK` whose status is `open`: if, then, probability, impact, response, owner, actionee.

## Minimum form

Each always-present section keeps its heading with one line: none known yet. The key-person check still runs, so a log with no entries may still owe that one risk.
