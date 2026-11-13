# Privacy threat model

What a change could reveal about people, or do to them without their knowing, analysed by LINDDUN's seven threat types over the elements that carry personal data.

**Reader and question.** Reviewer (privacy), or decider (the data protection officer): "what could this change reveal about people, or do to them unawares, and is each handled?"

**Page.** `on the threat-model page`

## Membership

The analysis the plan's personal-data concern owes beside the [privacy screening](privacy-screening.md). It covers each element the [threat model](threat-model.md) marks with `personal data`, against the seven types. (basis: LINDDUN, KU Leuven; LINDDUN PRO not read) Security threats stay in the threat model. Whether a DPIA is owed, and the record of processing, stay in the screening.

Elements and mitigations are the threat model's kinds, shown here. An element's `scope` covers both analyses: it is `analysed` only when both STRIDE and LINDDUN are done on it.

A task has one, filed again in each round whose result adds or changes an element carrying personal data, a privacy threat or a response.

A privacy threat is restricted when filed with its exposure unfixed or not known to be fixed; only the developer changes it ([items-and-agreements](../items-and-agreements.md)). Its page handles it as the threat model's page handles a threat.

## Items

**Privacy threat `PTH`.**
- Fields:
  - `category` enum `linking`, `identifying`, `non-repudiation`, `detecting`, `data disclosure`, `unawareness and intervenability`, `non-compliance`. "Linkability" and its siblings are the older names of the same types;
  - `elements` list of id, the elements it affects;
  - `data` list of text, the categories of personal data it touches, and `people` text, whose;
  - `likelihood`, `impact`, `rank`, `response`, `rationale`, `remainder owner` and `residual`, as the threat model's threat declares them. `impact` is on the people, not the organisation.
- Granularity: one way people's data can be exposed or used against them, with one type and one response.
- Change regime: `baseline`.
- Agreement: `needed`. As with a threat, one whose `response` isn't chosen is `open`, and `proposed` once a response is written. No field is a `when`, so its decide-by is the plan's fallback for this type's due point ([items-and-agreements](../items-and-agreements.md)).

## Sections

1. **What's left for the people affected?** Always. The residual view.
2. **What are we working on?** When this page stands on its own. The elements carrying personal data, drawn as the threat model draws them, and as a table with their `personal data`.
3. **What could it reveal, element by element?** Always. A table the page writes, not a view, with a row per analysed element carrying personal data and a column per type. Each cell holds that element's privacy threats of that type, or "n/a" and its reason. Then the category view.
4. **Where do security and privacy pull apart?** When a mitigation covers both a repudiation threat and a non-repudiation privacy threat, or both sit on one element. Each pair side by side: an audit log that answers repudiation creates non-repudiation for the people it records. The page shows the pull and doesn't resolve it. A choice between the two is a decision in the decision register. (basis: the research's fork between STRIDE and LINDDUN, shown rather than resolved)
5. **What are we doing about each?** When this page stands on its own. The mitigation view. On the threat model's page this section is left out, since the threat model's mitigation view lists every mitigation.
6. **What didn't this cover?** When this page stands on its own. As the threat model's section 8, for these elements.

## Checks

- *Computed:*
  - every analysed element with `personal data` is covered for all seven types, by a privacy threat on it or a `not applicable` entry (derived from LINDDUN);
  - every privacy threat's `elements` carry `personal data`;
  - every privacy threat passes the threat model's response checks.
- *Judgment:*
  - detecting, linking or unawareness dismissed: a security analysis never raises them;
  - impact stated for the organisation rather than for the people;
  - a privacy threat answered by a security control alone, such as encryption against linking;
  - no way for people to learn of, see or correct the processing, and no threat filed on it;
  - a non-repudiation threat dropped to keep an audit log, with no decision recorded;
  - a pair that meets section 4's condition missing from it.

## Views

- Residual: `PTH` as a `table`, sorted by `residual`, descending, then `rank`, descending: title, category, elements, data, people, response, residual, state, owner.
- Categories: `PTH` as a `table`, grouped by `category`: title, elements, rank, response, state.
- Mitigations: `MIT` with `covers` `to` `PTH`, as a `table`: title, covers, served-by, verified-by, tracked in, state, owner.

## Minimum form

Every element carrying personal data `not yet analysed`, "no privacy threats identified yet", and "no mitigations yet".
