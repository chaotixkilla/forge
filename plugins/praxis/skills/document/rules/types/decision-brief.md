# Decision brief

The case put to the decider of a tier-1 question: what is being decided, by when, what waits on it, the options and what each costs, and what the work recommends. (basis: research, 2026-11-11, no standard sets a brief's format, so its parts are taken from DACI's contents, MADR's options and RAPID's roles)

## Reader and question

The decider: "What am I being asked to decide, by when, and which option should I pick?"

## Page

`own page`

## Membership

One brief per tier-1 question in the [decision-register](decision-register.md), the question's whole case and nothing about other questions. The decision, once taken, is the register's and its record's; the brief only links it. Its subject is its question, so a question has one brief. It is filed again when its question or the brief changes, and once more when the question is answered.

## Items

**Brief `BRF`.** The page's case as one item, since a decider weighs it whole.
- Fields:
  - `options`: list of text. Each option, with what it costs: effort, time, risk, and what it closes off.
  - `recommendation`: text. The option the work recommends, and why.
  - `if undecided`: text. What happens when the decide-by passes with no decision, and what the work does meanwhile.
- Granularity: one per tier-1 question.
- Links: it `serves` its question.
- Its owner is the recommender. (basis: RAPID, one recommender)
- Change regime: `baseline`.
- Agreement: `none`. The brief is a case put to the decider, not a commitment; what gets agreed is the decision that answers its question.
- Withdrawal condition: a brief is withdrawn when its question leaves tier 1, with that as its reason.

Shows its `Q` (home: [decision-register](decision-register.md)). The question's decider, decide-by, consulted and informed are shown from the question, never copied into the brief, so the two can't drift. (basis: prototype sweep, 2026-11-11, briefs drifted from the register unchecked)

## Sections

1. **What are you being asked to decide?** Always. The question card, then the recommendation in one line.
2. **What is true today?** Always. From the brief's body: each fact an option's cost or the recommendation turns on, with its source as a link. (basis: field prototype, a brief opens on today's facts and its evidence)
3. **What waits on it?** Always. The items the question `blocks`, as a list.
4. **What are the options?** Always. Each option with its cost as its `options` entry gives it, saying for each cost whether the people who use the product or the engineering work bear it, the recommended one marked, then why it is recommended.
5. **What happens if nobody decides?** Always. Its if-undecided. (basis: Rust RFC template, the impact of not doing it)
6. **Who has been asked?** Always. The question's consulted and informed. What each consulted person said, when a result holds it, goes in the brief's body, each attributed, with its evidence link.
7. **What was decided?** When the question is answered. The decision that `answers` it, linking its record.

## Checks

*Computed:* each skips `superseded` and `withdrawn` items.
- The brief serves exactly one question, and that question is tier 1.
- It has at least two options, a recommendation and its if-undecided. (basis: research, 2026-11-11, one decider, a deadline, at least two options and a recommendation)

*Judgment:*
- A fact in What is true today? with no source.
- A brief whose question names no decider, so the case is put to nobody. It is judged, not computed, since the register never picks one of several named people.
- An option set up to lose, or every option but the recommended one left without a real cost. (basis: Zimmermann, Dummy Alternative and Sales Pitch)
- A recommendation that isn't one of the options.
- Doing nothing made to sound worse, or safer, than it is.
- Nobody consulted among those the decision reaches beyond the change.
- A weighted score presented as more precise than the judgment behind it. (basis: Zimmermann, Pseudo-accuracy)

## Views

- **Question card:** `cards` of the `Q` with `served-by` `to` the brief's id: tier, reversibility, reach, decider, consulted, informed, decide-by, state, lean.
- **Waiting on it:** `list` of every kind the store declares, with `blocked-by` `to` the `Q`'s id: owner, decide-by.

## Minimum form

The options, the recommendation and the if-undecided make it a brief, so they are never left out. The other always-present sections can each be one line: no fact is established yet; nothing waits on it yet; no one has been consulted yet.
