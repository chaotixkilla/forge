# codify — usage

Turn a human or maintainer process into the runnable procedure that lives inside an existing skill — the method, not the file skeleton.

## When to use
- You have a skill skeleton (scaffolded phases/rules slots) and need to pour the actual procedure into it.
- You can describe a process as a *goal* ("triage inbound bugs", "run our retro", "turn briefs into specs") and want it converted into ordered, cold-executable steps.
- The maintainer's process lives in their head, a runbook, a half-written checklist, or a past session — and you want it hardened into steps a fresh agent can run without being in the room.
- You need to re-work an existing procedure: enumerate the forks it left implicit, quantify its vague adjectives, or add the edge/empty/error cases it skipped.
- You're refining rather than drafting — make repeated passes to surface decisions each previous pass created.

## Not for / use instead
- Creating the skill's directory, frontmatter, and empty phase/rule slots — codify fills slots, it does not invent structure → **scaffold-skill** (which can hand its skeleton straight here via `--with-codify`).
- Adding a non-skill component (adapter, explorer, critic, rule, module, hook) to a plugin → **add-component**. Codify may *cite* a rule and, standalone, seed a rule stub, but it does not own component creation.
- Birthing a whole new plugin — its config posture, shell, and skill pool → **new-plugin**. Codify operates on one already-existing skill.
- Checking a finished skill's internal wiring (frontmatter shape, slot placement, flag/config wiring, adapter coverage) → **audit-contract**. Codify writes the procedure; the audit verifies the plumbing after.
- Scanning for concrete tool/vendor names that leaked into the skill layer → **audit-tool-leaks**. Codify *obeys* the no-tool-names rule as it writes; the audit is the independent check.
- Checking the ships-vs-authoring packaging boundary → **audit-packaging**.
- Publishing the plugin — version bump, catalog entry, release notes → **release**.
- Proving the finished skills actually run end-to-end against a real subject → **dogfood**. Codify's own `--verify` dry-runs the *one* procedure it just wrote; dogfood exercises the whole plugin.

## Examples
`--plugin=<plugin> --skill=<skill>` — the two required targets; codify writes the procedure into that skill's `phases/` (and `rules/` for any craft it extracts). Missing either flag stops and asks — writing into the wrong skill is a silent, expensive mistake.

`--plugin=<plugin> --skill=<skill> --first-pass` — return only the goal/process split plus the bare skeleton, then pause for the maintainer to steer. The highest-leverage checkpoint and the cheapest to correct early.

`--plugin=<plugin> --skill=<skill> --from-transcript=<ref>` — seed the process from a prior session/notes instead of interrogating live; the transcript stands in as the primary artifact (mine the durable method, discard the one-time specifics).

`--plugin=<plugin> --skill=<skill> --rounds=3` — make exactly three refine passes over the procedure before returning. Without the flag, codify keeps passing until a pass surfaces no new output-affecting fork; the flag fixes the count instead — for time-boxing, or to steer between passes.

`--plugin=<plugin> --skill=<skill> --verify=strict` — block the handoff while any output-affecting fork stays open or any standard-point stays unclosed. The bar for a procedure meant to run unattended.

`--plugin=<plugin> --skill=<skill> --verify=off` — skip the cold-executor dry-run for a quick draft the maintainer will review by hand.

`--plugin=<plugin> --skill=<skill> --from-transcript=<ref> --first-pass --verify=light` — common combination: seed from a session, return the split + skeleton for steering, and keep the light default that surfaces assumptions and open questions without blocking.

## Gotchas
- `--plugin` and `--skill` are both required and are not guessed from context — codify stops and asks if either is missing.
- Codify fills slots; it does not create structure. The seam is fixed: **scaffold-skill owns structure, codify owns method.** The one exception is a standalone call on a skill with no skeleton — there codify scaffolds `phases/` first, then fills, temporarily doing scaffold-skill's job.
- When the slot count you decomposed differs from what was scaffolded, reconcile with the maintainer — that's a signal, not a license to silently restructure another skill's skeleton.
- Every numbered step in the spine must link its phase file by relative path, and every `rules/` file must be cited inline from the phase that leans on it as a resolvable relative markdown link (`[name](../rules/name.md)` from inside `phases/`) — citation is a rule's only registration, and a bare name in backticks doesn't resolve. An unlinked step or an uncited rule never loads; the executor runs a bare stub with the method missing.
- HARD RULE it will not break: never name a concrete tool, vendor, CLI, or service in a step — a step names the *capability*, the tool lives in an adapter below. Codify's own output must pass the same tool-leak standard it exists to help uphold.
- It resolves what can be resolved and consciously leaves *judgment* room only where pinning would make the procedure brittle — never where it merely ran out of energy to enumerate. Each deliberately-open call records its reason in the procedure text, so an open-by-omission gap is detectable.
- It does not choose implementation details the executor should own, and it does not verify plumbing, package, publish, or dogfood — those are separate skills.
- The default `--verify=light` ships a procedure *with* its assumptions, open questions, and the bars it pinned for the maintainer to ratify; a procedure delivered without that list looks more finished than it is.
