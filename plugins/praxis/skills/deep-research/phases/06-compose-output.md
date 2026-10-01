## Render the answer, confidence-first

Lead with the answer to the original question, then the sub-answers, each carrying its confidence grade ([claim-confidence-scale](../rules/claim-confidence-scale.md)) and, where sources conflicted, the disagreement represented rather than collapsed ([surface-disagreement](../../../craft/evidence/surface-disagreement.md)). State an inference as an inference, never merged into the source's authority ([separate-fact-from-inference](../../../craft/evidence/separate-fact-from-inference.md)). Close with what could not be established — the open sub-questions, the thin-evidence dead ends, the gaps — as plainly as the findings ([name-the-uncertainty](../rules/name-the-uncertainty.md)), and state the verification level the run used ([verification-level](../rules/verification-level.md)) so the reader knows how hard the claims were tested.

The rendered shape, unless the caller asked for another:

```
**Answer.** <the direct answer to the question> — [confidence]

- <sub-question> → <sub-answer> [confidence]
  - <the load-bearing claim>, per <source, date>[; contested by <source> — see below]
- …

**Where sources disagree.** <the dispute, located: what each side holds and on what basis>

**What I could not establish.** <open sub-questions; thin dead ends; gaps> — verified at --verify=<level>
```

A sub-answer may expand from its one line to a short nested list — but only when the structure *is* the finding: a claim whose confidence rests on more than one independent origin, each of which must be shown to justify its grade, or a documented absence whose scope and search must be stated ([claim-confidence-scale](../rules/claim-confidence-scale.md)'s absence case). A sub-answer resting on a single source stays one line.

## Attribution rigor — provenance is always on

Every non-obvious claim carries its source regardless of flags; provenance is tracked from gathering, not bolted on here. `--cited` governs only the *form*: without it, attribution is inline and readable (`per the X spec, 2024`); with it, every non-obvious claim carries a formal, retrievable citation (a numbered reference with its locator), and a claim that cannot be attributed is dropped or explicitly flagged unsourced rather than stated bare. (basis: maintainer's resolution: provenance is always kept, and `--cited` governs only the rendered form)

## Publishing hands off a clean export


The output is the rendered report — answer, attribution, confidence, and gaps — returned to the caller.
