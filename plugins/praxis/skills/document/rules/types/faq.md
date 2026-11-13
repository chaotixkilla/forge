# FAQ

The questions people outside the work have actually asked about it, each with its answer, who it is for, and what the answer rests on.

## Reader and question

Support, or a decider, outside the work: "Has someone already asked what I'm about to ask?"

## Page

`own page`.

## Membership

One per task. It joins the plan when someone outside the work first asks a question about it, and grows only from questions asked, never from questions predicted ([documentation-plan](../../../../craft/writing/documentation-plan.md)). (basis: maintainer, 2026-11-11) When the [RAID log](raid-log.md) is owed, it also carries the internal core: how the work could fail and what must hold for it to work, shown from the RAID log rather than restated. (basis: Working Backwards, the internal FAQ) An answer that a page of the task already gives links to that page. It is filed again when a question is asked or an answer changes.

## Items

**Answer `FAQ`.** One question as asked, with its answer. Its title is the question, in the asker's words. Its state is the answer's.
- Fields:
  - `answer`: text, in one to three sentences, the detail in the body;
  - `audience`: enum `external`, `internal` (basis: Working Backwards);
  - `asked by`: text, the role or team that asked;
  - `asked`: date, when it was first asked;
  - `answered`: date.
- Granularity: one question. The same question asked again is the same item.
- Links: it `rests-on` each decision, question or assumption its answer depends on.

## Sections

1. **What have people asked?** — always. The answers view, external first.
2. **Which answers wait on an open question?** — present when an answer `rests-on` a question in `open`, `lean` or `proposed`. The waiting view.
3. **How could this fail?** — present when the RAID log is owed. The risks view.
4. **What must hold for this to work?** — present when the RAID log is owed. The assumptions view.

## Checks

*Computed:*
- Every answer has an audience, who asked, and when. (basis: Working Backwards; maintainer, 2026-11-11)
- An answer that isn't `open` has its `answer` field and its answered date.
- An `agreed` answer doesn't `rests-on` a question or decision that is `superseded`, `withdrawn` or not `agreed`. (basis: maintainer, 2026-11-11, the drift check against the [decision register](decision-register.md))

*Judgment:*
- A question nobody asked, written to look complete. (basis: maintainer, 2026-11-11)
- An answer that restates a page instead of linking it.
- An internal answer marked external.
- An answer resting on a change's state or the code, with no commit or date to say when it held.
- An internal core that misses the likeliest way the work fails, or an assumption it can't do without. (basis: Working Backwards, the top reasons it could fail)

## Views

- **Answers:** `cards` of every `FAQ` not `superseded` or `withdrawn`: title, answer, state, asked by, asked, answered and `rests-on`, sorted and grouped by audience, so external comes first.
- **Waiting:** `table` of every `Q` in `open`, `lean` or `proposed` that `supports` an answer: title, owner, decide-by and `supports`.
- **Risks:** `table` of every `RISK` whose `direction` is `downside` and `status` is `open`, sorted by proximity in `when` order ([item-store-and-views](../../../artifacts/rules/item-store-and-views.md)), then impact, as the RAID log sorts them: if, then, probability, impact, proximity and owner.
- **Assumptions:** `table` of every `ASM` not `superseded` or `withdrawn`: title, if false, validate by and owner.

## Minimum form

The FAQ joins with its first question, so What have people asked? is never empty.
