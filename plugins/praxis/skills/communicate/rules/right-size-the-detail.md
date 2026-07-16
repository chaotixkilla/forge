# Right-size the detail

Detail altitude is where "tailor it to the reader" most often collapses into instinct: one writer inlines every caveat and buries the point, another cuts so hard the reader can't act, and both believe they judged well. The cost is real either way — a padded artifact wastes every reader's time, a thin one fails the decision it was written for. This rule makes altitude decidable: a test that sorts every candidate detail into a tier, discriminators for the close calls, and a stopping test that says when two writers have converged. It is applied in [draft-the-content](../phases/04-draft-the-content.md) (sizing as you fill) and [tighten-and-verify](../phases/05-tighten-and-verify.md) (the cut).

## The precondition

The need-to-know test is only decidable once two things are fixed: **the target reader** and **the single decision or action the artifact must enable**. [frame-the-message](../phases/01-frame-the-message.md) fixes both; if either is genuinely unknown, altitude cannot be judged and the artifact is not ready to size — route it back, don't guess. `(basis: plain-language "write for your reader and their task" — altitude is relative to a named reader and action, so the pair is the precondition, not an input to average.)`

## Classify the artifact — it sets the default

The right default flips on artifact type, and the two defaults genuinely pull opposite ways — so classify before sizing rather than picking a side:

- **Guidance artifact** (teaches, decides, or persuades: status updates, decision records, onboarding notes, reviews, proposals) → default **minimize-and-defer**: cut aggressively, keep only what supports the reader's decision. `(basis: Carroll's minimalism — a definitive, experimentally-grounded result for instructional content; plain-language regulation.)`
- **Reference artifact** (a contract or lookup: an API reference, a data-contract doc, an exhaustive spec) → default **complete-and-exhaustive**: omitting a detail is a defect, not concision — but still ordered bottom-line-first. `(basis: the reference-documentation tradition — completeness is the contract.)`

`(fork — do not collapse: guidance and reference pull opposite directions and neither is universally right. The routing rule is the classification above: minimize for guidance, complete for reference; a guidance artifact that goes exhaustive buries its point, a reference that minimizes drops a fact some reader needed. Resolve by type, per the artifact type fixed in framing, not by preference.)`

## The need-to-know test — sort every detail into a tier

For each candidate detail, ask what its absence costs the *named* reader pursuing the *named* action:

- **Tier 1 — inline** (need-to-know): removing it changes what the reader can decide or do. Keep in the body, ordered by descending importance.
- **Tier 2 — appendix / collapsed section** (verify-to-trust): not required to act, but a reader may need it to verify, audit, or handle an edge case. Defer *within* the artifact.
- **Tier 3 — link or omit** (nice-to-know / owned-elsewhere): background, tangential, or authoritatively owned by another canonical source → link, never duplicate; serves no reader task at all → omit.

## Discriminators for the close calls

- **inline vs appendix** — "Does the reader need this to complete the named action?" Yes → inline. Only to verify, audit, or handle an edge case → appendix.
- **appendix vs link** — "Is *this* artifact the canonical owner of the detail?" Owner → appendix (co-locate it). Someone else owns it, or it's a reference lookup → link out (duplicating it forks a source that will drift).
- **too thin** — the summary fails when a reader of the opening alone can't name the decision, *or* a Tier-1 item is missing.
- **too padded** — the artifact fails when it contains any Tier-3 item, *or* a sentence whose removal loses no Tier-1 fact (the word-level cut is [respect-the-readers-time](respect-the-readers-time.md); this rule decides *which facts*, that rule decides *how tightly each is written*).

## The stopping test — when two writers converge

Stop cutting or adding when all hold:

1. The bottom line is in the first paragraph. `(basis: BLUF — inverted pyramid; US Army AR 25-50 makes it a MUST in its domain.)`
2. **Stop-anywhere:** at every section break, everything above is self-sufficient for a reader who stops there, and nothing below is Tier-1 for the main point. `(basis: inverted pyramid.)`
3. Every retained inline item passes the need-to-know test for the named reader and action.
4. Every removed or deferred item failed that test and sits at its correct tier (2 or 3).
5. No inline sentence can be deleted without losing a Tier-1 fact. The sentence-level word-cut that establishes this — and owns it as a craft — is [respect-the-readers-time](respect-the-readers-time.md); this test only requires that cut has been run. (This rule decides *which facts* survive; that rule decides *how tightly each surviving one is written* — one owner per altitude, no duplicated bar.)
6. Deferral depth is at most two levels within the artifact (inline + one deferred layer); deeper material is chunked out to a link. `(basis: adopted as a house rule from NN/g's ≤2-level disclosure finding — which is validated on UI, not prose, so it is imported by analogy and pinned as a house cap, not asserted as a measured result for documents.)`

When 1–6 hold, two writers have the same inline set, the same deferral set, and the same ordering — modulo the precondition. The residue that is genuinely context-dependent is exactly the reader-and-action definition; that is the open-by-design boundary, and framing bounds it by *stating* the pair rather than defaulting it.

## No numeric budget is authoritative

There is no authority-backed word count or percentage for "the right length"; if a run wants a cap, it is a house choice stated explicitly, not a bar this rule pins. The only defensible numeric anchors are *readability* hints, not altitude: roughly 15–20 words per sentence, 3–7 lines per paragraph. `(basis: plain-language and Microsoft style readability guidance — these bound sentence/paragraph size, not how much the artifact should contain, which the need-to-know test governs instead.)`
