This phase turns the recruitment plan into raw material. Searching the web and fetching a source is an ambient capability the run uses directly, through the explorer lanes; your job is to run the lanes, capture what they return with its provenance intact, actively look for what would *break* the emerging answer, and know when the picture has stopped moving.

## Recruit the lanes in parallel

Recruit the web-facing lanes directly, in parallel via the available fan-out mechanism — or, without fan-out available, run each lane's search yourself in sequence, following that lane's own method (its explorer agent in [agents/explorers/](../../../agents/explorers/): [community-practices](../../../agents/explorers/community-practices.md), [official-documentation](../../../agents/explorers/official-documentation.md), [authoritative-literature](../../../agents/explorers/authoritative-literature.md)) before moving to the next. The org-internal **knowledge-base** lane is different: it needs a configured backend, so reach it through the [gather](../../gather/SKILL.md) port — whose [knowledge-base](../../../agents/explorers/knowledge-base.md) lane reads via the [knowledge](../../knowledge/SKILL.md) port, the owner of `tools.knowledge` — rather than recruiting the explorer directly here; when no backend is configured, gather drops the lane with a note and the run proceeds on the web lanes.

Capture each finding as a **claim plus its provenance**, verbatim where load-bearing: the exact assertion, the source that made it (title, author/org, date), a retrievable locator (URL + section), and whether the source is stating something first-hand or relaying it ([prefer-primary-sources](../rules/prefer-primary-sources.md)). Keep what a source *states* distinct from any inference you draw ([separate-claim-from-inference](../rules/separate-claim-from-inference.md)). Do not weigh or resolve yet — collection is neutral; weighing is synthesize.

## Chase leads, and hunt the disconfirming

Harvest the leads a source surfaces — a cited paper, a referenced standard, a named counter-result, a term you didn't know to query — and re-query the lane that owns them ([follow-the-leads](../rules/follow-the-leads.md)). As the answer starts to emerge, spend part of every round trying to *falsify* it, not just to add support: search for the dissenting result and the failure report, not another restatement of the consensus ([guard-against-confirmation](../rules/guard-against-confirmation.md)). An answer that has only been confirmed, never attacked, is not yet gathered.

## Stop at saturation, and document the gaps

Keep chasing across rounds until new sources stop changing the picture — the saturation test in [know-when-to-stop](../rules/know-when-to-stop.md), not "until queries run out." A `--budget` or `--timebox` cap can force a stop before saturation; when it does, say so, so the caller knows the picture is bounded, not complete. A lane whose capability is unavailable is dropped with an explicit note (`lane X not consulted: <reason>`); a lane that returns nothing returns a documented absence (`no finding in lane X; searched <where>`) — an absence is a result, never a gap to hide.

The output is the pooled, anchored claim set — each claim carrying its provenance and primary/derivative status, every consulted lane represented by findings or a documented absence — ready to verify.
