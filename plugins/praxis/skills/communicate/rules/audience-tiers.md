# The audience-tier scale

Every artifact communicate produces is pitched at a reader, and the tier is what makes "tailor it to the audience" a decision two writers reach the same way instead of a vibe each fills from instinct. Depth, jargon, framing, what to lead with, and whether internal context may appear all follow from the tier — so an undefined "audience" is not a lighter-touch instruction, it is the most load-bearing judgment in the skill left to chance. This rule pins the tiers, the method for assigning one, and the boundaries between them, so a borderline reader lands on the same tier whoever runs it. It is assigned in [model-the-audience](../phases/02-model-the-audience.md) and consumed by [draft-the-content](../phases/04-draft-the-content.md) (the prescription) and [tighten-and-verify](../phases/05-tighten-and-verify.md) (the fit check).

## The assignment method — two axes

Audience is not one scale; every authority that decomposes it splits it into two independent dimensions, and conflating them is what makes tier assignment feel arbitrary. Place the reader on both, then map to the nearest tier:

- **Axis A — knowledge proximity to *this* subject**: `has-our-context` / `in-domain-but-new` / `outside-the-org`. How much of the specific mental model, vocabulary, and history the reader already holds. **This axis governs depth and jargon.**
- **Axis B — role and stake**: `implements-the-work` / `decides-on-the-work` / `sits-outside`. What the reader does with the artifact. **This axis governs framing and what to lead with.**

The tie-breakers when the axes pull apart: **proximity (A) decides depth and jargon; role (B) decides framing and lead.** A high-proximity decision-maker (a staff engineer approving a design in their own area) gets peer-level depth with exec-level framing — dense mechanism, but led by the decision. `(basis: Google developer-documentation guidance — audience = role + proximity, and "the knowledge gap"; DITA (OASIS) models audience on orthogonal @type (role) and @experiencelevel (proximity) attributes. Using A for depth and B for framing is the house calibration these sources inform but do not dictate.)`

## The four tiers

`(basis: ratified by the maintainer, 2026-07-13. The four tiers and their prescriptions are derived from the sources below; because no authority pins a named tier set for engineering artifacts — the style guides leave tiering to the writer and Diátaxis argues against audience-tiering for product docs — the tier boundaries and prescriptions are the maintainer's ratified house standard. Sources: DITA @experiencelevel novice/general/expert; Pearsall/McMurrey's expert/technician/executive/nonspecialist typology; Google role+proximity; Microsoft "get to the point fast"; the primary/secondary/hidden reception model.)`

- **peer** *(top of scale — most shared context)* — shares your working context and domain expertise; could pick up the task with little ramp.
  - *Assignment test:* "Would they already know our system's vocabulary without a glossary?" → yes.
  - *Prescription:* maximal density; house jargon, acronyms, and internal names used freely; assume the shared mental model; lead with the technically load-bearing detail; omit motivation they already hold; link rather than restate.
  - *Anchor (top):* a design-doc note to a teammate on the same service — "Switched dedupe to the Bloom filter in IngestV2; watch the FP-rate knob, it's shared with the replay path." Full jargon, no definitions, load-bearing detail first.

- **newcomer** — technically capable but new to *this* system, team, or codebase: high skill elsewhere, low proximity here.
  - *Assignment test:* "Do they know the domain generally but not our specifics or history?" → yes. Newcomer is a *proximity* position, not a seniority label — a staff engineer on day one is a newcomer to your service.
  - *Prescription:* define house terms on first use; state the *why* and *where-this-fits* before the *how*; make implicit steps explicit; link to foundational context; no unexplained acronyms. Orient, then instruct.

- **exec / decision-maker** — reads to decide, fund, approve, or prioritize, not to implement; typically low technical proximity and time-boxed.
  - *Assignment test:* "Do they act on the conclusion rather than the mechanism?" → yes.
  - *Prescription:* bottom-line-up-front — lead with the conclusion, recommendation, impact, cost/risk, and the decision requested; minimize mechanism; translate technical detail into impact terms; short and scannable.

- **external** *(bottom of scale — least shared context)* — outside your org or trust boundary; no access to internal context, tools, or history; expertise unknown, so assume none unless established.
  - *Assignment test:* "Would this be read without our internal context — does it leave the building?" → yes.
  - *Prescription:* no internal jargon, codenames, or internal links; define everything; state assumptions explicitly; write self-contained and durable; check confidentiality and tone (this is the record of record); assume the widest, least-context reader.
  - *Anchor (bottom):* a customer-facing release note or a post-mortem shared with a customer — every term defined, no internal service names, impact and remediation stated plainly, self-contained, reviewed for confidentiality.

Each prescription names a jargon posture (used freely / defined on first use / dropped) as part of what the tier means, but the *vocabulary craft* — the treatment of each term and the use-it-again discriminator — is owned by [match-reader-vocabulary](match-reader-vocabulary.md); the postures here are the tier's summary of it, not a second authority. Where the two ever seem to differ, the vocabulary rule owns the term-level call.

## The adjacent-tier discriminators

Assign by walking from most-shared-context to least until a tier fits; the boundary tests stop a reader sliding between two:

- **peer vs newcomer** — does the reader already hold *our* vocabulary and history (peer), or are they skilled but new *here* (newcomer)? The line is proximity to this subject, not seniority. (Axis A)
- **newcomer vs exec** — does the reader act on the *mechanism* (they will implement or maintain it → newcomer, give them the how) or on the *conclusion* (they will decide → exec, give them the impact)? The line is role. (Axis B)
- **exec vs external** — does the reader sit *inside* the org's context (exec — internal framing and names are fine) or *outside* it (external — nothing internal may appear)? The line is the trust boundary. (Axis B)

When two tiers both seem to fit, pitch to the one with *less* shared context — under-assuming context costs a peer a few skippable definitions; over-assuming it strands a newcomer or leaks internals to an outsider. The asymmetry favors the lower tier.

## When the axes split — apply each layer to its own tier

The two axes usually agree, and the reader maps to one tier. But they can genuinely diverge — a reader high on Axis A and pulling a different tier on Axis B — and the archetype is a **high-proximity decision-maker**: a staff engineer approving a design in their own area is `has-our-context` (Axis A → peer depth) *and* `decides-on-the-work` (Axis B → exec framing). Do **not** collapse this to one tier and apply that tier's whole prescription — that is the divergence this section prevents (one writer picks peer and buries the decision in mechanism; another picks exec and strips the mechanism the reader is qualified to want). Instead **split the prescription along the axis each governs**:

- **Depth, jargon, and assumed knowledge come from the Axis-A (proximity) tier** — the high-proximity reader gets full density and bare house jargon.
- **Framing, lead, and what-to-minimize come from the Axis-B (role) tier** — the decision-maker gets bottom-line-up-front, the decision and its impact led, mechanism present but not the opening.

Record a split result as a **pair** — "peer-depth / exec-framing" — not a single label, so [draft-the-content](../phases/04-draft-the-content.md) knows to consume both. The staff-engineer-approving-their-own-design case resolves to exactly this: dense mechanism (peer depth) led by the decision and its consequences (exec framing). When `--audience=<tier>` names a single tier, it sets that single tier and suppresses the split — the caller has asserted one reader; honor it, but still surface a plain mismatch (all mechanism, no decision, under `--audience=exec`) per [model-the-audience](../phases/02-model-the-audience.md).

## The learning-mode overlay — not a fifth tier

A reader in **learning mode** — being onboarded or mentored, acquiring the skill rather than applying it once — needs acquisition-oriented scaffolding (worked examples, motivation, safe-to-fail framing) layered *on top of* whichever tier they occupy, per [meet-the-learner-where-they-are](meet-the-learner-where-they-are.md). Record it as a modifier ("peer, learning mode"), never as a tier: the same person is a peer at work and a learner at study, and making learning a tier would double-count against newcomer. `(basis: Diátaxis — acquisition-vs-application is a situation the reader is in, orthogonal to who they are; ratified 2026-07-13.)`

## Scope

This scale governs **human-to-human artifacts** — status updates, decision records, onboarding notes, review/handoff messages, and the docs a team reads to act. For **reference product-documentation** (API references, exhaustive specs), Diátaxis argues persuasively for organizing by *need* (tutorial / how-to / reference / explanation) rather than by audience tier; where communicate produces that kind of artifact, defer to the need-based organization and treat the tier only as a depth hint. `(basis: Diátaxis explicitly argues against audience-tiering for product documentation; ratified scope decision, 2026-07-13 — the house adopts the tier scale for human-to-human artifacts and defers to Diátaxis for reference docs, rather than overriding it.)`
