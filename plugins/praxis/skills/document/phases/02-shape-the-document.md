A result arrives in the shape its step produced; this phase decides its document type and shapes it to that type, adding nothing the result doesn't carry.

## Which type

Match the result to a type by its membership test: the [task record](../rules/types/task-record.md) for the task's state — what it is, what's been done (a skipped step's outcome and reason included), what's next — or one of these:

- **work records** — the [spec](../rules/types/spec.md), the [plan](../rules/types/plan.md), the [traceability](../rules/types/traceability.md) table, the [scratchpad](../rules/types/scratchpad.md), the [review record](../rules/types/review-record.md), [ship notes](../rules/types/ship-notes.md), an [incident record](../rules/types/incident-record.md), a [research report](../rules/types/research-report.md), [spike findings](../rules/types/spike-findings.md), an [audit report](../rules/types/audit-report.md);
- **decision records** — a [decision record](../rules/types/decision-record.md);
- **system documentation** of the part the task touched — an [explanation](../rules/types/explanation.md), a [reference](../rules/types/reference.md), a [how-to](../rules/types/how-to.md), a [concept](../rules/types/concept.md).

When the act file names the type a result files as, that decides. One result can yield several documents: a review record, and a decision record for each of its decisions that passes that type's test. A result that matches no type isn't filed: tell the caller, naming the result. (basis: maintainer, 2026-09-30, the three kinds of documentation)

A document already filed is updated, not filed again, and a decision keeps the number it was first filed under.

## Shape it

Shape each document to its type, under [one-type-per-page](../rules/one-type-per-page.md). Every page opens with a line naming its type, the part of the system it covers, its task and its date: `Review record · the invoice export module · review-pr-230 · 2026-10-02`. Three things hold for every type:

- **Laid out for a reader who scans.** After that line, a page leads with its conclusion — a review's verdict, a research answer, an incident's impact, the decision ([lead-with-the-takeaway](../../../craft/writing/lead-with-the-takeaway.md)) — and its headings, lists and tables let a reader find their part without reading in order ([structure-for-scanning](../../../craft/writing/structure-for-scanning.md)). A relation the result carries — a flow, a set of states, what depends on what — is drawn as a diagram where [when-a-visual-is-owed](../../../craft/writing/when-a-visual-is-owed.md) says one is owed, to [diagram-legibility](../../../craft/writing/diagram-legibility.md). Laying a result out moves and formats what it carries; it adds no claim.
- **Every claim keeps its source.** Carry each claim's source through from the result: code at a commit and `file:line`, a document, a test run, a conversation. A claim the result gives no source for is marked `(unsourced)` where it stands, never given one. (basis: maintainer, 2026-09-30)
- **Plain terms, no machinery.** A page is written in the terms its readers already use ([match-reader-vocabulary](../../../craft/writing/match-reader-vocabulary.md)). It says what was done and found, never how praxis ran it: no skill, step, phase, lane or explorer names, and no tool calls ([clean-export](../../../craft/writing/clean-export.md)). Work that was skipped is still recorded, as what wasn't checked and why — "the retry library's behavior wasn't checked against its documentation: the reviewer judged it unnecessary" — never as a skipped step.

The output is the shaped documents, for [publish-and-link](03-publish-and-link.md).
