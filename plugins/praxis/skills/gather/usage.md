# gather — usage

## When to use
Reach for `gather` from *inside another skill* that needs evidence gathered and weighed across more than one source lane before it does its own work — understand's locate/trace step, plan's map-to-system, spec's constraint-gathering, debug's hypothesis-sourcing, review's context pass, deep-research's gather-evidence. It owns the fan-out-and-weigh; the caller owns what to do with the weighted picture.

## Not for — use instead
- **Mapping a system for a human** → `understand` (user-facing; it *consumes* gather, then builds the map).
- **An open-world, cited research report** → `deep-research` (user-facing; it consumes gather, then adds adversarial claim-verification and report composition).
- **Publishing a finished document** → `publish-artifact`.
- **A single-lane read where you already know the one source** → recruit that one explorer directly; gather is for multi-lane synthesis, and one lane doesn't need weighing.

## Examples
- `gather --explorers=code,repository "how does the retry path behave and why is it that way"` — two project-internal lanes, findings tiered and anchored to file:line / commit.
- `gather --deep --explorers=official-documentation,authoritative-literature,community-practices "the API contract for X plus the pitfalls people hit"` — full web fan-out with lead-chasing across the authoritative and anecdotal tiers.
- `gather --inputs-only --explorers=code,knowledge-base "what our own code and docs say about Z"` — no open web; project-internal ground truth only.
- `gather --budget=20 --explorers=community-practices "known workarounds for Y"` — bounded number of recruit/fetch operations.

## Gotchas
- **Delegated, not user-facing.** It returns raw weighted findings (by tier, with conflicts and gaps), not a formatted deliverable — the calling skill shapes the output.
- **It surfaces, it doesn't decide.** Conflicts and the transfer-to-this-project question are handed back flagged; gather never resolves them — the caller, which has the project context gather lacks, makes the transfer call.
- **The knowledge backend is the caller's.** gather recruits `knowledge-base` with the backend the caller passes in; it never resolves the backend itself. Needs `tools.knowledge` configured, or it degrades to the remaining lanes.
- **Consumers shed the prerequisite.** A skill that delegates its whole gather step to `gather` drops its own `tools.knowledge` from `config_requires` — the doer owns the prerequisite (as `spec` sheds `tools.artifacts` to `publish-artifact`).
