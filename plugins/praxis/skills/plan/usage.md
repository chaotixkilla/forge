# plan — usage

Convert a spec into a buildable design — anchored to the real system, with concrete interfaces and a safe rollout.

## When to use
- You have a spec (or settled requirements) and need the *how*: the design that turns intent into something a developer can build without re-deciding mid-build.
- The change touches existing code and you need to know its blast radius, the constraints the current architecture imposes, and where each piece of logic should live.
- Multiple viable approaches exist and you want the solution space closed deliberately — one approach committed, the rejected alternatives recorded with reasons.
- The tricky flows (migrations, partial failures, idempotency, multi-step sequences) need pre-solving on paper before anyone writes code.
- You need a rollout that reaches production safely: migration/backfill, backwards compatibility during transition, testing strategy, observability hooks.

## Not for / use instead
- Requirements are still fuzzy or unagreed — pin down the *what* first → `spec`
- You need to understand an unfamiliar system before you can design against it → `understand`
- Splitting a settled design into ordered, independently shippable work units → `decompose`
- Actually building it → `develop`
- Validating an approach is even feasible by building a throwaway → `prototype`

## Examples
`--from-spec=<path>` — treat a written spec as the authoritative input; the design is held accountable to it, and phase 6 confirms every requirement is addressed.
`--deep` — maximum-rigor mode; fan out explorer and critic sub-agents before committing to an approach. Reach for it on high-blast-radius or hard-to-reverse designs.
`--prior-art=<ref>` — model the design on an existing implementation/pattern (or deliberately diverge from it); grounds the approach in something proven instead of inventing from scratch.
`--critics=<n>` — set how many perspective-diverse critics stress-test the design (e.g. `--critics=3`). Pairs naturally with `--deep`.
`--phase=<name|n>` — run or resume a single phase in isolation (e.g. `--phase=3` to redo just the interface contracts, or `--phase=rollout`). Use when an earlier phase's output changed and you want to rework one slice without re-running the whole spine.
`--publish` — hand the finished plan to the artifacts backend via `publish-artifact` as a clean, team-facing design document: the design and its decisions, with every phase/agent/skill/process reference stripped.
`--from-spec=<path> --deep --critics=3` — the heavyweight combination for a design that has to be right the first time: authoritative spec in, wide exploration, multiple critics.

## Gotchas
- plan declares **no config of its own**. Its evidence-gathering (blast radius in phase 1, prior art in phase 2, hard-flow literature in phase 4) is delegated to the `gather` skill, whose knowledge lane reads through the `knowledge` port (the owner of `tools.knowledge`), and which degrades to its remaining lanes if the knowledge backend is unconfigured — so the documented architecture/invariants won't feed the design, but code/repository/web lanes still do.
- `--publish` delegates wholesale to `publish-artifact`, which owns `tools.artifacts` and guides you through `init:artifacts` if it's unconfigured; without a backend the plan is still produced and returned locally, just not sent anywhere.
- This is design, not requirements-gathering and not building. It assumes the *what* is settled — if the spec is thin, plan will surface the gaps but won't invent the missing intent for you.
- The rejected-alternatives record (phase 2) is deliberate, not busywork — it's the part of the design that ages well and answers "why not X?" six months later.
- Phase 6 is a closure gate: it confirms the design is sliceable into independently buildable units, that every decision the spec left open (surfaced in phase 1) is now closed, and it flags what still needs a spike/prototype before committing. A plan that leaves opens is not done.
- `--phase` runs one slice in isolation — it trusts the upstream phases' outputs rather than regenerating them, so those outputs must be present in context (or at a referenced path) and current before resuming mid-spine; if a required upstream output is missing it halts and asks rather than regenerating or guessing. Names resolve against a fixed set (`1=mapping … 6=validate`).
