The synthesis is the answer; this phase renders it so a reader can act on it and re-check it. What separates a research report from an essay is that every load-bearing claim is attributable and every confidence is stated — the reader can see not just what the answer is, but how strongly it is held and where it is thin.

## Render the answer, confidence-first

Lead with the answer to the original question, then the sub-answers, each carrying its confidence grade ([claim-confidence-scale](../rules/claim-confidence-scale.md)) and, where sources conflicted, the disagreement represented rather than collapsed ([surface-disagreement](../rules/surface-disagreement.md)). State an inference as an inference, never merged into the source's authority ([separate-claim-from-inference](../rules/separate-claim-from-inference.md)). Close with what could not be established — the open sub-questions, the thin-evidence dead ends, the gaps — as plainly as the findings ([name-the-uncertainty](../rules/name-the-uncertainty.md)), and state the verification level the run used ([verification-level](../rules/verification-level.md)) so the reader knows how hard the claims were tested.

The rendered shape, unless the caller asked for another:

```
**Answer.** <the direct answer to the question> — [confidence]

- <sub-question> → <sub-answer> [confidence]
  - <the load-bearing claim>, per <source, date>[; contested by <source> — see below]
- …

**Where sources disagree.** <the dispute, located: what each side holds and on what basis>

**What I could not establish.** <open sub-questions; thin dead ends; gaps> — verified at --verify=<level>
```

A sub-answer may expand from its one line to a short nested list — but only when the structure *is* the finding: a claim whose confidence rests on more than one independent origin, each of which must be shown to justify its grade, or a documented absence whose scope and search must be stated ([claim-confidence-scale](../rules/claim-confidence-scale.md)'s absence case). A sub-answer resting on a single source stays one line. This keeps two runs nesting the same way — by what the confidence rests on, not by preference.

## Attribution rigor — provenance is always on

Every non-obvious claim carries its source regardless of flags; provenance is tracked from gathering, not bolted on here. `--cited` governs only the *form*: without it, attribution is inline and readable (`per the X spec, 2024`); with it, every non-obvious claim carries a formal, retrievable citation (a numbered reference with its locator), and a claim that cannot be attributed is dropped or explicitly flagged unsourced rather than stated bare. (basis: provenance-always-on with `--cited` governing rendered form resolves the seed's open question #4 — turning citation "off" must never let claims float unsourced internally; only the output's formality changes.)

## Publishing hands off a clean export

`--publish` publishes the report as a team-facing document through the artifacts capability ([publish-output](../modules/publish-output.md)). Before handing it to the port, strip every internal-process reference — tool calls, agent/phase/skill mechanics, praxis process — so the deliverable carries the findings, sources, and confidence for a human reader and none of the machinery ([publish-output](../modules/publish-output.md) owns the clean-export bar). `--notify` signals the invoker when a detached run completes ([notify-on-completion](../modules/notify-on-completion.md)).

The output is the rendered report — answer, attribution, confidence, and gaps — inline by default, or published as a clean team-facing document under `--publish`.
