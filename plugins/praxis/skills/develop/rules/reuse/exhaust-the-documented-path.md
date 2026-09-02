# Exhaust the documented path

A library or SDK almost does what you need, and the last ten percent doesn't fit. The pull is to bridge the gap yourself, right there, because you are already in the code and the bridge looks small. The judgment this rule governs is how much reading is owed *before* that first line of workaround. Left to instinct it fails at both ends — one builder starts bridging immediately and ships a shim around a path the vendor never supported, which breaks on the next upgrade with no warning; another treats every gap as a wall and abandons a component that documents the exact thing they needed three pages further on. Both spent the afternoon, and only one of them has a defect that will outlive them.

## The discriminator

The test is **whether the vendor documents a supported path for this case** — and you do not get to answer it from memory or from the shape of the API.

- **Make the documentation pass first, and make it real.** One honest pass over three surfaces: the vendor's own documentation for the component and the operation you need, its worked examples, and its published changelog or issue tracker for the case. Three surfaces, one pass each — that is the bar. It is reconnaissance, not a research project, bounded the same way the search that precedes writing new code is ([reuse-before-writing](reuse-before-writing.md)). The pass is owed *before* the workaround, not after it fails to work.
- **A documented path found ends the question.** Take it, and discard what you had started building. The half-built shim is a sunk cost; keeping it because it is already written is precisely how an unsupported mechanism ships.
- **Silence is evidence, not an invitation.** When the pass turns up nothing, the likeliest explanation is that the component does not support the case — not that you are the first person to want it. A gap the documentation never mentions is a fact you just learned about where the fix belongs, and the answer is usually "not here."

(basis: ratified by the maintainer, 2026-09-01 — the reasoning is theirs: if the official documentation does not mention the thing you are trying to overcome, the component most likely does not support the use case, and the solution belongs at another layer rather than in a workaround here. Pinned as a rule because the failure it prevents is invisible at the time — a workaround written against an unsupported path looks like progress on the day and fails on an upgrade nobody connects to it.)

## When the case really is unsupported

Building around it is one option, and rarely the cheapest. The usual alternatives are a change of approach so the component is used as intended, moving the concern to a different layer, or using a different component. That comparison is not yours to settle quietly: adopting a substitute for behavior a dependency was meant to provide is materially different from what was asked and expensive to unwind, which makes it a decision the build **surfaces rather than takes** ([orient-in-the-code](../../phases/01-orient-in-the-code.md)).

**Reaching into internals is already past the line, not a workaround to weigh.** An undocumented endpoint, a private attribute, a monkey-patched method: these *are* the definition of unsupported. They carry no compatibility promise, and the upgrade that breaks them will do it silently, in code that no longer resembles the code that made the choice.

## What this does not forbid

A workaround against a **known, identified** upstream defect is ordinary engineering: you read the documentation, the behavior contradicts it, and there is a specific defect to point at. Name it — the issue, the affected versions, the condition that triggers it — and the workaround becomes a documented bridge with a removal condition rather than a guess ([comment-the-why-not-the-what](../comments/comment-the-why-not-the-what.md) covers what that comment owes). What the rule forbids is narrower and more common: the workaround adopted because the documentation was never read, or was read, found silent, and the silence ignored.

## The anchors

- *Good:* an SDK's list call seems to cap at 100 results, so before writing the offset-and-stitch loop you make the pass — and its own docs show a cursor helper on the same client that pages properly. The loop you had started goes in the bin, and the code uses the component as designed.
- *Bad:* the same cap, no pass, and a retry-and-stitch layer grows around it over an afternoon. An upgrade later changes how the cap interacts with ordering, and the stitching silently drops records — a data-loss bug whose origin is a documentation page nobody opened.
