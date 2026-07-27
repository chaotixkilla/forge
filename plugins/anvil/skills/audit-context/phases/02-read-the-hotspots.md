The measurement handed you a ranked list of sites where one file cites a lot. This phase decides what each one means, and it is where the audit earns its keep: the number convicts nothing, because a deliberate routing index and a bare roster produce the *same* fan-out. Skip this read and the report becomes a list of ratios a maintainer correctly ignores.

Work the sites the measurement flagged as breaches first, then continue down the ranked list while the ratios stay above roughly half the budget — a site just under a threshold calibrated on one corpus is worth a glance, and the ranking is more trustworthy than the cut-off.

## Apply the discriminator, once per site

For each site, apply the index-versus-roster test in full — the covered-links test, what counts as a firing condition, and the two legitimate shapes that are neither — as defined in [index-vs-roster](../rules/index-vs-roster.md). Read the citing file whole before judging: the conditions are sometimes stated in a paragraph *above* the list rather than on each entry, which is a legitimate index and a common false positive.

Record one of three verdicts per site, and carry the evidence with each:

- **Index — cleared.** Quote the firing condition on a representative entry. No finding. Say so explicitly in the report rather than silently dropping it, or the next run re-reads the same site.
- **Roster — finding.** Quote the entries as they stand, and state what a cold executor would do: open all of them (name the token cost, from the measurement) or pick by filename. The finding's severity comes from the weight behind the site, not from the ratio.
- **Mixed — finding, scoped.** The common real outcome: some entries carry conditions and some are bare. Name which are bare. A partial fix is a real fix here.

## The two mistakes that make this phase worthless

- **Convicting on the number.** A twelve-entry index with a condition per entry is *correct* and cheaper at runtime than a three-entry roster. If you file it because the ratio was high, you have told the maintainer to damage a working file.
- **Clearing on tidiness.** A roster grouped into labelled families reads far better than an ungrouped one and is exactly as undecidable — the label is a property of the file, not of the run. Grouping is not routing. This is the single most likely way to clear a real finding, because the grouped version genuinely looks considered.

## Check whether the contract is what forces the shape

Before writing any roster finding, establish whether the roster is *load-bearing for reachability* — because if it is, the remedy in the report cannot be "add conditions and drop the list," and proposing that would break the plugin.

The mechanism: a rule is registered only by being cited, so a rule whose *only* citation is the roster becomes an orphan the moment the roster is replaced — and an orphaned rule is a finding from [audit-contract](../../audit-contract/SKILL.md), which `release` runs as a hard gate. So for each rule in a roster you are about to flag, count its citations elsewhere in the skill. Where a substantial share are cited *only* here, say so in the finding and state the remedy accordingly: the conditions go **on the existing citations**, which stay in place, rather than the list being replaced by a shorter one. That keeps every rule registered and still makes the site decidable — the same links, now triageable.

This is worth checking rather than assuming, in both directions. A roster whose rules are all cited from several phases can be thinned freely. One whose rules are cited nowhere else cannot, and a report that recommends thinning it has recommended 25 new contract findings.

## What this phase hands forward

A verdict per site with its evidence, and for each roster finding: the entries lacking a condition, the reachable weight behind them, whether the citations are load-bearing for reachability, and the remedy that follows from that. Cleared sites travel too — an audit that reports only failures gives a maintainer no way to tell a clean site from an unexamined one.
