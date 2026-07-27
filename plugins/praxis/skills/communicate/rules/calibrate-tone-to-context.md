# Calibrate tone to context

Register — how formal, how warm, how direct — is the layer that decides whether an artifact reads as native to its destination or as an import from somewhere else. It is genuinely house- and context-specific: there is no universal "right voice," and a model default here is the average of all writing, which reads as no one's. So this rule does not *pick* a register; it pins the order in which a register is derived, and the per-tier tone that layers on top. It is applied in [draft-the-content](../phases/04-draft-the-content.md) and checked in [tighten-and-verify](../phases/05-tighten-and-verify.md).

## The register fork — derive it, in order

Resolve the register by walking this order and stopping at the first that answers; this is a fork, not a single default, because the right source of voice depends on what the destination already has:

1. **Match the destination's existing artifacts.** A decision record matches the team's other decision records; a repo doc matches the repo's docs; a channel post matches how that channel reads. The surrounding convention is the strongest signal — an artifact that reads like its neighbors is trusted, one that reads foreign is second-guessed. [model-the-audience](../phases/02-model-the-audience.md) reads the destination's voice for exactly this.
2. **Absent a local convention, use the house register.** When the destination is new, or has no artifact of this type to match, fall back to the house default (below).
3. **Where neither fits** — a genuinely novel destination whose expected register the house default plainly mis-serves — surface it to the maintainer rather than guessing. This is rare, and it is routed, not defaulted.

`(basis: the routing order — surrounding convention → house rule → maintainer — is the house's standard fork-resolution rule for a contested, context-dependent call; encoding the fork rather than picking one register is required because authorities on "good voice" genuinely conflict and the right answer is destination-relative.)`

## The house register default

When no local convention exists to match, the house register is: **terse, precise, and high-density; method over fact; imperative and active; no throat-clearing, no hedging, no hype.** Concretely — lead with the point, state it plainly, cut the qualifier that adds no information, prefer the concrete verb to the abstract noun, and never inflate ("leverage a robust solution" → "use X"). This is the register of this repo's own documents (the skill files, the READMEs), adopted as the default so a house-authored artifact reads as one of them.

`(basis: ratified by the maintainer, 2026-07-13. The house default register is the voice derivable from this repo's existing docs; because "the register when no local convention exists" is a house standard no external authority can set, it is the maintainer's ratified call, not a model default. It applies only at step 2 of the fork — a destination with its own voice still wins.)`

## Tone follows the tier — and never condescends

Register is the house voice; *tone* adjusts within it to the reader and the stakes, keyed to the tier in [audience-tiers](audience-tiers.md):

- **peer** — direct and colleague-to-colleague; assume competence; no over-explaining.
- **newcomer** — orienting and patient; more scaffolding, but never talking down — explain the unfamiliar, not the obvious.
- **exec** — decision-framed and confident; state the recommendation and own it; no burying it in qualifiers.
- **external** — measured and self-contained; more formal, careful with claims and confidentiality.

The one invariant across all tiers: **never condescending.** More scaffolding for a newcomer or a learner is meeting them where they are, not treating them as less capable — the tell of condescension is explaining what the reader plainly already knows, or a tone that performs the writer's expertise rather than serving the reader's understanding. When correcting or delivering hard news, stay direct and factual; softening into vagueness to be "nice" fails the reader who needs to know what is actually wrong.
