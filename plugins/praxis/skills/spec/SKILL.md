---
name: spec
description: Turn a fuzzy request into hard, testable, sequenced requirements — attack assumptions, quantify every vague adjective, structure the requirements, and carve scope into prioritized, independently shippable slices, each requirement pass/fail checkable; optionally seeded from a tracker issue or a discussion thread, hardened under a strict gate, and published as a clean team-facing spec.
metadata:
  flags:
    --from-issue=<ref>: seed the spec from a tracker issue (title, description, acceptance criteria), then interrogate and harden it — activates the ingest-from-issue module
    --from-discussion=<ref>: seed from a discussion thread's decisions, constraints, and open points — activates the ingest-from-discussion module
    --strict: escalate the always-on testability check from warn to hard block — no requirement ships non-verifiable, no ambiguity unresolved, no assumption unconfirmed — activates the strict-gate module
    --first-pass: return the structural skeleton after structuring and pause for steering, gaps marked open — activates the first-pass-draft module
    --publish: hand the finished spec to the artifacts capability as a clean team-facing document — activates the publish-spec module
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies. spec owns no backend of its own: it delegates evidence-gathering to the `gather` skill and every flag-borne capability (issue/discussion ingest, publish) to a port skill, so it declares no `config_requires`.

`--strict` raises the testability bar across the whole run from warn to block: see [modules/strict-gate.md](modules/strict-gate.md). `--first-pass` stops after structuring and returns a steer-me skeleton: see [modules/first-pass-draft.md](modules/first-pass-draft.md).

1. Interrogate the prompt: attack the request with questions before writing anything; surface what was assumed, not just what was said  — see [phases/01-interrogating-prompts.md](phases/01-interrogating-prompts.md)
2. Pin down the ambiguity: convert fuzzy intent into hard constraints; this is where most value is  — see [phases/02-pin-down-ambiguity.md](phases/02-pin-down-ambiguity.md)
3. Structure the requirements: organize what you extracted into the house taxonomy, grounded against standing conventions  — see [phases/03-requirement-structuring.md](phases/03-requirement-structuring.md)
4. Make it concrete and testable: every requirement pass/fail checkable, with examples, counter-examples, and explicit out-of-scope  — see [phases/04-making-it-concrete.md](phases/04-making-it-concrete.md)
5. Sequence and size: carve scope into prioritized, independently shippable slices with dependencies and risks  — see [phases/05-sequencing-and-sizing.md](phases/05-sequencing-and-sizing.md)
