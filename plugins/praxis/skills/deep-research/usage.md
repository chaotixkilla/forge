# deep-research — usage

Turn a genuinely open question into a verified, cited report: fan out across web-facing source lanes, fetch and adversarially verify the load-bearing claims, and synthesize an answer that separates what's established from what's contested — with the confidence and the gaps stated plainly.

## When to use
- The answer isn't in context or the repository, and settling it needs the open web — official docs, standards and papers, and community practice, weighed against each other rather than trusted one at a time.
- You want claims you can trust: each traced to a source, the load-bearing ones corroborated across independent origins and chased to their primary source, disconfirming evidence actively sought.
- You want the disagreement represented honestly — where sources conflict, the answer locates the dispute instead of collapsing to one side — and the uncertainty named as plainly as the findings.
- You want to dial the rigor and spend: a fast light pass, a deep multi-round sweep, a bounded budget, or a wall-clock timebox — and optionally a publishable team-facing report at the end.

## Not for / use instead
- Investigating **this** codebase — how it behaves, why it's this way → **understand** (deep-research reads the open world; it does not trace local code).
- A project-grounded evidence-gathering step inside another skill (recruit the explorer fleet, synthesize one weighted picture, hand it back) → **gather** (the delegated investigation core; deep-research is the user-facing open-world harness, not a reusable sub-step).
- Landing substance that already exists on an audience — a doc, status update, or handoff message → **communicate** (deep-research produces the substance; communicate pitches and routes it).
- Root-causing a specific known failure → **debug**; reading a finished change for defects → **review**.

## Examples
`deep-research "<question>"` — a default single-pass run: fan out, verify the load-bearing claims at the default rigor, and return a cited answer with confidence and gaps.
`--deep` — escalate: wider fan-out, more rounds of lead-chasing, and the authoritative-literature lane engaged on every sub-question (not only where it fits by default); for a hard or high-stakes question.
`--verify=strict` — adversarially check every material claim, not just the load-bearing few; `--verify=off` skips verification and returns a clearly-flagged unverified sweep.
`--budget=40` — bound the run to ~40 searches/fetches, allocated across sub-questions by importance and spent down first on the ones that matter.
`--timebox=15m` — prioritize the highest-value evidence early and degrade gracefully to a best-effort answer when the clock runs out.
`--cited` — render a formal citation for every non-obvious claim (provenance is tracked regardless; this governs the output form).
`--artifact` — publish the finished report as a team-facing document through the artifacts capability instead of returning it inline.
`--background --notify` — run a long fan-out detached so it doesn't block the session, and signal you when it completes.

## Gotchas
- **A thin-evidence dead end is not saturation.** deep-research stops when new sources stop *changing the answer*, not when the answer is merely repeated by weak echoes of one origin; it names which of the two it hit, and a dead end returns a low-confidence answer, not a confident one.
- **Confidence is not fluency.** A source is weighed by its basis — method, expertise, independence, currency — not by how confidently or fluently it asserts; a polished blog post does not outweigh a primary standard.
- **The report is a clean export.** `--artifact` publishes a team-facing document — the findings, sources, and confidence for a human reader — carrying no internal tool calls, agent/phase mechanics, or praxis process; the machinery stays out of the deliverable.
- **`--verify=off` returns an unverified sweep.** It is a fast scan of what the sources say, every claim flagged unverified — useful for orientation, not for a decision that rests on the answer being right.
- **`--notify` presumes a detached run.** It signals the invoker on completion; with a foreground run you are already watching, so pair it with `--background`.
- **deep-research needs no configuration of its own.** Web search and source-fetch are ambient; the org-internal knowledge lane is reached through the `gather` port (which owns the knowledge prerequisite), so it is present only when a knowledge backend is configured and degrades cleanly when it isn't; publishing (`--artifact`) is delegated to the `publish-artifact` port. Each doer owns its prerequisite, so deep-research declares none.
