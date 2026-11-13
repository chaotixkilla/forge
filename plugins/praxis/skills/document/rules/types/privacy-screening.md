# Privacy screening

Whether a change's processing of personal data owes a data protection impact assessment (DPIA), and what that processing is: its purposes, data, people, recipients and retention.

**Reader and question.** Decider (the data protection officer), or reviewer (privacy) where there is none: "does this change need a DPIA, and what does it change in what we hold about people?"

**Page.** `own page`

## Membership

The screening the plan's personal-data concern owes, before the processing starts, since an assessment is owed before processing likely to be high-risk (basis: GDPR Art 35(1)). It holds:
- every criterion, answered;
- the decision and its reasons;
- the processing, as the record of processing describes it;
- whether less data would do;
- when a DPIA is owed, the rest of the assessment's parts.

The screening records `law`: `EU GDPR`, `UK GDPR` or `none`, as the result or the developer states it, and missing otherwise. The deciding fact is the law that governs the processing, and it is never inferred. It sets the lists that apply:
- `EU GDPR`: the `mandatory` cases and the `EDPB` nine;
- `UK GDPR`: those, and the `ICO` list;
- `none`: no criteria are filed and no decision. The page records that no data-protection law requires a DPIA, and keeps "Could we use less?".

Threats to people's data belong to the [privacy threat model](privacy-threat-model.md), and this page links it for the assessment's risks and measures. What a provider keeps, and where, belongs to the [vendor review](vendor-review.md). The vendors it names are recipients here.

A task has one. It is filed again when an answer, a category of data or people, a purpose, a recipient, a transfer or a retention period changes. Each of those changes the record of processing (basis: GDPR Art 30) and the risk a DPIA was judged on (basis: GDPR Art 35(11)).

Its items describe categories of data and people, never anyone's records. They are `team` unless one says personal data is exposed.

## Items

**Screening criterion `SCR`.**
- Fields: `source` enum `mandatory`, `EDPB`, `ICO`; `met` enum `yes`, `unsure`, `no`; `reason` text, why it is or isn't met by this processing.
- Granularity: one criterion. Every criterion on the lists that apply is filed, met or not: the same items, answered again at each screening.
  - `mandatory` (GDPR Art 35(3)): systematic and extensive automated evaluation of people, profiling included, with legal or similarly significant effects; large-scale processing of special-category or criminal-offence data; large-scale systematic monitoring of a publicly accessible area;
  - `EDPB`, the nine: evaluation or scoring; automated decisions with legal or similar effect; systematic monitoring; sensitive or highly personal data; processing on a large scale; matching or combining datasets; data about vulnerable people; an innovative use of technology; processing that stops people exercising a right or using a service or contract;
  - `ICO`: biometric data; genetic data; data matching; invisible processing; tracking location or behaviour; children's data; processing whose breach could endanger someone's physical safety.

  (basis: GDPR Art 35(3); the ICO's screening guidance; EDPB WP248 rev.01 for the nine, as its main text words them; its Annex 2 wasn't read)
- Change regime: `baseline`.
- Agreement: `needed`. No field is a `when`, so a criterion's decide-by is the plan's fallback for this type's due point ([items-and-agreements](../items-and-agreements.md)).

Shows `DEC` (home: the [decision-register](decision-register.md) type). The decision on whether a DPIA is owed is one, answering the question "Does this change owe a DPIA?". The data protection officer's advice is evidence on it, and any departure from that advice is in its body with why. It is decided by these rules:
- a `mandatory` criterion met: owed;
- two or more `EDPB` criteria met: owed is presumed, and deciding against it takes reasons that rebut it. One can be enough;
- under the UK GDPR, any `ICO` criterion met: owed is presumed (basis: when unsure, a DPIA is done). The ICO says some are owed on their own and some only with an `EDPB` criterion; which is which wasn't read, so this list is to be checked at source;
- `unsure` counts as met, since when unsure, a DPIA is done;
- "not owed" always records its reasons.

(basis: EDPB WP248 via the ICO, two of nine presumes a DPIA, one can suffice, a decision against records its reasons)

Shows `PTH` (home: the [privacy-threat-model](privacy-threat-model.md) type), counted in section 6 and named in section 2.

## Sections

1. **Does this change need a DPIA?** Always. The `law` it was screened under. Under `none`, the line that no data-protection law requires a DPIA. Otherwise the decision, its state and its reasons; how many criteria are met or unsure, and any mandatory one met; the data protection officer's advice and any departure from it.
2. **Must the regulator be consulted first?** When a DPIA is owed and a privacy threat's `residual` is `high`. The processing waits for prior consultation with the supervisory authority. Those privacy threats, by id. (basis: the ICO, a high residual risk means consulting it before going ahead)
3. **Which criteria does it meet?** When `law` isn't `none`. The criteria view.
4. **What do we process, and why?** Always. The processing and its purposes in prose (basis: GDPR Art 35(7)(a)). Then a table with one row per category of personal data: the people it's about, its purpose, whether it is a special category, its recipients, transfers out of the jurisdiction with their evidence, its retention period, and whether it is new, changed or unchanged in the record of processing. A row whose retention, recipients or transfers' destination is written `unknown` files one question naming each unknown part, reused while it is open on later filings: `reversibility` and `reach` by the register's tests from what its answer settles, decider the one person the run names for the processing or else missing, owner the task's owner, decide-by `build start`. The data protection officer advises on it and never decides it. (basis: benchmark, 2026-11-12, every retention and region unknown, no question filed; GDPR Art 39, the officer advises)
5. **Could we use less?** Always. Each category set against what its purpose needs: what was dropped, narrowed, kept for less time or pseudonymised, and why the rest is needed. When a DPIA is owed, this is its necessity and proportionality (basis: GDPR Art 35(7)(b)).
6. **What could it do to people, and what will we do about it?** When a DPIA is owed. A link to the privacy threat model, with its privacy threats counted by `residual` (basis: GDPR Art 35(7)(c) and (d)).
7. **What did the people affected say?** When a DPIA is owed. Their views and how they were sought, or why seeking them wasn't appropriate (basis: GDPR Art 35(9)).

## Checks

- *Computed:*
  - `law` is stated;
  - every criterion on the lists that apply is filed, with `met` and `reason`;
  - a `mandatory` criterion met means the decision is "owed";
  - a presumption met means a "not owed" decision has reasons in its body;
  - when a DPIA is owed, the privacy threat model the page links is in the task's documentation;
- *Judgment:*
  - a retention that isn't a period: a duration, or an event and a duration, such as "90 days after the account closes". Another party's policy, such as "the vendor's retention", isn't one (basis: maintainer, 2026-11-11, from the prototype sweep);
  - a vendor whose `receives` names personal data missing from the recipients, or from the transfers when its `region` is outside the jurisdiction (derived);
  - a processing row without its people, purpose, recipients or retention (derived from GDPR Art 30);
  - a category in an element's `personal data` in the threat model with no row that matches it (derived, linking the data-flow stores to the record);
  - a screening done after the processing began;
  - `no` where `unsure` was the honest answer;
  - one criterion met, the risk to people plainly high, and no DPIA;
  - only security risks weighed, not people's rights;
  - "could we use less?" answered with nothing actually considered;
  - a new or changed row with no update to the record of processing by the first gate that puts that processing in production, a preparatory gate included, since copying data is processing (derived: Art 30 sets no deadline, and the record should describe processing that runs);
  - a transfer through a provider's regions or subprocessors taken on trust, with no evidence;
  - no advice sought from the data protection officer where the organisation has one;
  - a retention still `unknown` when the build starts;
  - a recipient that receives people's data with no way recorded for a person's erasure to reach it: for a processor, its contract's assistance clause and the deletion path it offers; for another controller, the notification. (basis: GDPR Art 17, 19 and 28(3)(e); field prototype, 2026-11-10)

## Views

- Criteria: `SCR` as a `table`, grouped by `source`, sorted by `met`, descending: title, met, reason.

## Minimum form

The law stated, or shown missing; under a law, every criterion filed `unsure`, with "not yet assessed" as its reason, and the decision `open` with `build start` as its decide-by, "processing not yet described", and "less data not yet considered".
