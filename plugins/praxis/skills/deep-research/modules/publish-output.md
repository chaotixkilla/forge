# Publish output — `--publish`

Publish the finished report as a durable, team-facing document under the **`research`** type-key instead of returning it inline. deep-research delegates the mechanism wholesale to the `publish-artifact` port through the artifacts capability, so it declares no `tools.artifacts` of its own — the port owns that prerequisite and guides setup or blocks if it is unconfigured (doer-owns-prerequisites). It names the type-key, not the destination; the port resolves the key to the configured target. Activated from [compose-output](../phases/06-compose-output.md).

## The clean-export bar

What `--publish` exports is a **team-facing document for a human audience** — the findings, sources, and confidence rendered for a reader who will act on them — not a record of how the research ran. Before handing the report to the port, strip every internal-process reference:

- **Strip:** tool calls and capability names; agent, phase, skill, or module mechanics ("the adversary critic," "the verify-claims phase," "fan-out"); praxis process and this skill's own vocabulary; and confidence expressed as internal machinery rather than reader-facing plain language.
- **Keep:** the answer and sub-answers, the sources and their attribution, the disagreements represented ([surface-disagreement](../rules/surface-disagreement.md)), the confidence of each finding stated in plain terms ([claim-confidence-scale](../rules/claim-confidence-scale.md)), and what could not be established ([name-the-uncertainty](../rules/name-the-uncertainty.md)).

The test: a reader outside the team, with no knowledge of praxis, reads the document as a research report — never as a transcript of an agent's run. (basis: the settled §2 artifacts rule — an artifact is a clean export of the substance for a human audience, carrying the content and the decisions, never the machinery; the producing skill strips internal-process references before publishing.)
