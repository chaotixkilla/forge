This is where the artifact gets written — but "write it well" is a dozen judgment calls a cold executor would each resolve differently, so this phase routes each to the rule that pins it rather than leaving them to instinct. The frame, the tier, and the form are fixed inputs now; the work here is producing text that lands them on the reader. The order below is the drafting order: skeleton first, then fill, then the craft passes that make it read for *this* reader.

## Lay the skeleton: takeaway first, structured to scan

Open with the takeaway fixed in [frame-the-message](01-frame-the-message.md) — the conclusion or ask in the first sentence or paragraph, so a reader who stops there still knows what to do. The method for putting the point first (and telling it apart from the setup that wants to come first) is [lead-with-the-takeaway](../rules/lead-with-the-takeaway.md). Then lay headings, lists, and bolded anchors so a skimming reader finds their part without reading top to bottom — [structure-for-scanning](../rules/structure-for-scanning.md) carries the layout method. The skeleton exists before the prose because a reader scans structure before they read words.

## Fill to the tier's prescription

Write the body to the prescription the tier carries in [audience-tiers](../rules/audience-tiers.md) — depth, assumed knowledge, and framing are set by the tier assigned in [model-the-audience](02-model-the-audience.md), not chosen afresh here. **When the assigned tier is a split** (a depth-tier + a framing-tier, e.g. "peer-depth / exec-framing" for a high-proximity decision-maker), take depth, jargon, and assumed knowledge from the depth-tier and framing, lead, and what-to-minimize from the framing-tier — do not apply either tier's whole prescription. Two craft rules refine the fill:

- **Vocabulary** — use the terms the reader already uses; define or drop the jargon they don't share rather than displaying it. [match-reader-vocabulary](../rules/match-reader-vocabulary.md) pins when a term is defined-on-first-use, dropped, or used bare, keyed to the tier.
- **Detail altitude** — give exactly the detail the decision or action needs; defer the rest to an appendix or a link. [right-size-the-detail](../rules/right-size-the-detail.md) carries the need-to-know test that sorts every candidate detail into inline / appendix / link, and the stopping test that says when to stop cutting or adding.

## Ground the abstract, and preserve the why

Two content rules apply where the type calls for them:

- Where the artifact makes an abstract claim the reader must grasp or trust, ground it in one concrete example, before/after, or sample — [show-dont-just-tell](../rules/show-dont-just-tell.md) pins when an example is owed versus when it is padding.
- Where the artifact is a **decision record** (or any type that will be re-litigated), record the reasoning and the rejected alternatives, not just the conclusion — the why is what survives and prevents re-arguing a settled call. [preserve-the-why](../rules/preserve-the-why.md) carries what a preserved why must contain.

## Pitch the voice, and scaffold for a learner

Calibrate the register per [calibrate-tone-to-context](../rules/calibrate-tone-to-context.md): match the destination's existing voice read in [model-the-audience](02-model-the-audience.md); absent one, use the house register; where neither fits, that rule routes it to the maintainer. Tone follows the tier — direct for peers, more orienting for newcomers, decision-framed for execs, self-contained for external — never condescending. When the learning-mode overlay is set, layer [meet-the-learner-where-they-are](../rules/meet-the-learner-where-they-are.md) on top: build from what the learner knows toward the gap, explain the reasoning so they can generalize, and prefer a worked example over a description.

## Make the ask land, and keep the export clean

State the ask (or its explicit absence) where the reader will act on it, per [make-the-ask-explicit](../rules/make-the-ask-explicit.md) — usually near the takeaway, not stranded at the end. And draft the artifact as a **clean export from the start**: it is the finished document its audience expects, carrying the content and the decisions and *none* of the machinery that produced it — no tool calls, no agent/phase/skill names, no praxis process, no "here's how I generated this." [clean-export](../rules/clean-export.md) defines exactly what an internal-process reference is and how to tell it from legitimate content; drafting clean is cheaper than scrubbing later, and [tighten-and-verify](05-tighten-and-verify.md) checks it.

## Produce in the target language under `--lang`

The base draft is written in the work's default language. Under `--lang=<code>`, produce it in the target language instead — see [localize-and-translate](../modules/localize-and-translate.md). Translation preserves the intent, the takeaway, and the tier's register; it is not a mechanical word swap, and it happens as the draft is produced (or as a faithful re-expression of it), never as an afterthought that drifts from the original's meaning.

Done-state: a complete draft exists — takeaway-first, scannable, pitched to the tier's depth and vocabulary, grounded where it claims, carrying the why where the type owes it, in the right register and language, with an explicit ask and no internal-process references. It is ready to tighten, not yet delivered.
