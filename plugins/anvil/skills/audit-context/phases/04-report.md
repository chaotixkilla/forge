Return the audit as findings a maintainer can act on without re-running it. The organising principle for this report is one distinction the other audits do not have to make: **what was measured** versus **what was judged**. A ratio is reproducible and uncontestable; a roster verdict is a reading, and a reader who cannot tell which is which either over-trusts the judgments or dismisses the measurements along with them.

## Lead with the layer table

Open with the measurement, not the findings. The layer table is the most useful thing this audit produces even when there are no findings at all, because it is the only place a maintainer sees where the plugin's weight actually sits:

- **Always resident**, in tokens and as a share of the corpus, with the largest contributors named. This is the number to watch over time — it is paid on every request and grows one description at a time.
- **Per skill**: spine / usage / phases / rules / modules and the no-flag ceiling, ranked by ceiling. Report the disclosure ratio as the virtue it is: a thin spine governing a large body is the architecture working, not a risk.
- **Fan-out hotspots**, with each site's verdict from the read alongside its ratio — including the cleared ones.

## Then the findings, in two clearly separated groups

**Measured breaches.** A budget was exceeded; the figure is reproducible by re-running the script. State the measurement, the budget, and that the budget is [proposed, not ratified](../rules/context-budget.md). A breach that the read *cleared* is not a finding — report it in the table as cleared, with the firing condition that cleared it.

**Read judgments.** Roster verdicts and register defects. Each carries the quoted text, not a summary of it, because the maintainer's first move will be to disagree, and they cannot do that with a paraphrase. Rank these by consequence, in this order:

1. **A load-bearing citation phrased as an aside.** Highest, because it fails silently: the run completes, the output looks fine, and a pinned standard was never applied. Nothing else here loses correctness.
2. **A roster whose rules are cited only there.** High, because the obvious remedy breaks the contract — flag it *with* that constraint attached, or the fix creates orphan findings at the release gate.
3. **An ordinary roster.** The executor over-reads or guesses; name the token cost from the measurement.
4. **An unmarked optional citation.** Lowest — a small, real routing cost.

## Say what the remedy is, and what it must not be

Every roster finding carries its remedy explicitly, because the intuitive fix is usually wrong: **add the firing conditions to the citations that already exist**; do not propose deleting rules to make the list shorter. Cutting a craft library to fix a routing problem trades a real standard for a token saving, and where those citations are the rules' only registration it also manufactures contract findings. Where a rule genuinely has no firing condition — it applies always, or never — note it and route it to the economy lens rather than resolving it here.

## Record the contested sites as contested

Where the register check and the fan-out read disagreed about one citation, report it as a **contested site**, with both readings and the direction this run resolved it (mandatory, per the asymmetry in [check-registers](03-check-registers.md)). This is not indecision to be tidied away — it is the one place this audit hands a genuine judgment back to the maintainer, and burying it means the next run makes the same call silently.

## Close with an honest verdict

State plainly which of the five checks ran (`--checks` may have narrowed them), what was measured, and what was read. Then one of:

- **Within budget, registers conformant** — the measurements and the counts that support it.
- **Findings** — the counts by group, and the single highest-consequence item.
- **Partial** — a check could not run: the measurement script failed, or a skill's figures were unreliable because its spine's citations do not resolve. Name what was not established rather than reporting on what was, and route a resolution defect to `audit-contract`, whose join it is.

Under `--report=artifact`, publish the layer table and findings through the artifacts capability and return the reference; inline is the default. Never report a budget breach as a settled defect — the budgets are proposed, and this audit's credibility rests on not overclaiming them.
