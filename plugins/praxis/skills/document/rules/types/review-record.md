# Review record

The reviewer's own copy of a delivered review, kept whole; the change carries the comments.

**Reader and question.** Reviewer: "what did this review find, and what still stands?"

**Page.** `own page`

## Membership

A review's final result: its brief, its findings and its questions for the author, each with where it was posted, or "not posted" and why. When the review was formed before the author's explanation was read and then revisited with it, that's the revisited result, with the mark the review gives each item the explanation touched ([prior-pass](../../../review/modules/prior-pass.md)). A finding the explanation withdrew is `withdrawn`, with the why. The working results the review built on — a map of the area, gathered evidence, test runs, the findings formed before the author's explanation was read — belong to the scratchpad. (basis: maintainer, 2026-09-30)

Each round's review is a record of its own, about the change and commit the round reviewed ([pages-belong-to-their-task](../pages-belong-to-their-task.md)). (basis: maintainer, 2026-10-02) That change and commit is its subject, held in `reviewed at` on its findings and questions, so a task has one per round. Its items belong to the round that found them and aren't carried to the next round's record. A finding the next round doesn't find again is withdrawn, as "fixed in <commit>", only when that round's review says so, and shows on the record of the round named in its `withdrawn in`. The decisions the brief lists stay in the brief's prose, but for those that earn a [decision record](decision-record.md), which take their own.

## Items

**Finding `FND`.**
- Fields: `severity` enum `critical`, `high`, `medium`, `low`, `info` ([severity-scale](../../../review/rules/severity-scale.md)); `certainty` enum `observed`, `traced`, `inferred`, `unverified` ([results-and-certainty](../../../../craft/evidence/results-and-certainty.md)); `pile` enum `correctness`, `craft`; `location` text, the file and line; `scenario` text, the failing scenario or concrete cost; `fix` text, the smallest suggested fix; `posted` text, where, or "not posted" and why; `mark` text, the prior-pass mark, when the explanation touched it; `reviewed at` text, the round and commit that found it; `withdrawn in` text, the round that withdrew it, when one did.
- Links: it `breaks` the requirement or acceptance criterion it shows doesn't hold, when it shows one.
- Granularity: one defect. Several symptoms of one cause are one finding with several locations.
- Change regime: `baseline`.
- Agreement: `none`.
- Live fields: `thread` — vcs: whether the finding's comment thread on the change is resolved.

**Question for the author `ASK`.**
- Fields: `location` text; `raised by` text, what raised it; `posted` text, as for a finding; `answer` text, where the author's explanation answers it, when it does; `reviewed at` text, the round and commit that raised it. An answered question stays `recorded`, with its `answer` filled.
- Granularity: one question, in the form [questions-for-the-author](../../../review/rules/questions-for-the-author.md) pins.
- Change regime: `baseline`.
- Agreement: `none`.

A scope finding carries no severity, so it is a line of prose, not an item.

## Sections

1. **Where does the review stand?** Always. The stance posted (request changes, approve or comment-only), or the stance proposed while not posted, and the verdict line: the count of standing findings by severity, highest first, or "no findings".
2. **What did the reviewer expect the change to do?** Always. The brief, in prose, as formed before the author's explanation was read, or "brief turned off".
3. **Does it do what it set out to?** Always. The fitness results, one row per acceptance the brief names, each on [results-and-certainty](../../../../craft/evidence/results-and-certainty.md)'s scale.
4. **What's wrong?** Always. The finding table, then the withdrawn-finding table.
5. **What's out of scope?** When the review found bundled, unrelated changes. Prose, one line each.
6. **What does the reviewer need to know?** When there are questions. The question table.

## Checks

- *Computed:*
  - every `FND` whose `reviewed at` is the page subject has a `location` and a `scenario` (basis: anchor-every-claim, review's fixed finding record);
  - every `FND` and `ASK` whose `reviewed at` is the page subject has `posted` filled;
  - every `FND` whose state is `withdrawn` has `withdrawn in` filled;
  - the verdict line's counts equal the standing `FND` whose `reviewed at` is the page subject, by severity.
- *Judgment:*
  - a finding graded on taste, not on consequence;
  - a high or critical finding at `unverified`, stated as fact;
  - a suggested fix larger than the finding needs;
  - a question that is really a finding, or a finding that is really a question.

## Views

- **Finding table** (section 4): `table` of `FND` whose `reviewed at` is `page subject`, grouped by `pile`, sorted by `severity` then `certainty`, each descending: severity, certainty, location, what it `breaks` (empty marker `none`), `thread` (empty marker `none`).
- **Withdrawn-finding table** (section 4): `table` of `FND` whose state is `withdrawn` and whose `withdrawn in` is `page subject`: severity, location, its state with its reason.
- **Question table** (section 6): `table` of `ASK` whose `reviewed at` is `page subject`: location, raised by, posted, answer (empty marker `not answered`).

## Minimum form

The stance "proposed, not posted", the brief "not formed", the fitness section naming the acceptances not judged, and "no findings".
