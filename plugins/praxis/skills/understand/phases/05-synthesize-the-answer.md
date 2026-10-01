## Validate the map's hidden premises
Before assembling, hunt the premises the emerging map rests on: recruit the [assumption-hunter](../../../agents/critics/assumption-hunter.md) critic — its lens is "what is this map taking for granted that a reachable reality could falsify?" — and fold its surviving findings in as claims, each graded on the certainty scale: hand the critic [certainty-scale](../rules/certainty-scale.md) with the recruit so it grades on that rule's own rungs and anchors, and where it hands a premise back in plain terms understand assigns the rung its evidence earns. Without fan-out, apply the lens yourself: for each load-bearing claim, name the premise it needs to be true and try to construct the reachable case where it is false, before letting the claim stand. A premise that survives becomes a claim; a falsifiable one becomes a flagged uncertainty or drops the claim's certainty rung.

## Assemble the map — the pinned shape
Render the map in a fixed shape, so two runs are comparable:

- **The answer** — the framed question answered directly, in a sentence or two, leading with the highest-certainty claims.
- **The claims**, each as a fixed record: `certainty · what is true · anchor (file:line / commit / observed output)`. Group them **by sub-question** — the parts the framed question decomposes into — as the default *and the tiebreak*. Use a different grouping only when the question is *unambiguously* one shape and names no sub-questions: **by execution-path stages** for a question about a single named flow ("what happens, step by step, when …"), or **by component** for a question purely about how named parts relate ("how do A and B interact"). When more than one could fit — the common "how does X decide/do Y," which reads as flow *and* structure *and* a set of sub-questions — **sub-question wins**, so the axis read always resolves. *Which* sub-questions the parts are is deliberately open — they emerge from the framed question and what the dig surfaced, so enumerating them up front would be false precision; two maps of the same dig converge on the grouping axis, the record format, and the grades, and may still differ by a bucket boundary. `(basis: derived from the fixed-grouping convention review and gather follow)` The grouping is chosen independently of the `--diagram` kind, which [render-diagram](../modules/render-diagram.md) selects on its own axis. Every claim carries its certainty rung ([certainty-scale](../rules/certainty-scale.md)) and its anchor ([anchor-every-claim](../../../craft/evidence/anchor-every-claim.md)); an ungraded or unanchored claim does not go in the map.
- **Divergences** — the record-vs-code conflicts surfaced in [corroborate-against-reality](04-corroborate-against-reality.md), each as "source X says A, code does B — bug / stale doc / open," never silently reconciled ([find-the-source-of-truth](../rules/find-the-source-of-truth.md)).
- **External contracts** — the libraries, frameworks, services and published standards the mapped code relies on where the question touches them, each with the version the project pins or "not pinned". Stated as **none** when the mapped code relies on none: a caller deciding whether to look outside the code reads this line.
- **What stays unknown** — the sub-questions not decided and the paths noted-but-not-traced, stated explicitly. A gap named is honest scope; a gap omitted reads as "covered," a different and false claim.

`(basis: derived from review's pinned finding shape)`

## Before it goes out, read it as its reader

Put the finished map through [deliver-at-the-readers-register](../../../craft/writing/deliver-at-the-readers-register.md) before delivering it, applying its honesty floor item by item from the rule, not from memory. Classify this deliverable on that rule's fork before any cut: its shape invites the guidance default, and the honesty floor is what a wrong classification reaches first.

## Confirm the question is answered, then stop
Confirm the stopping test holds ([stop-when-answered](../rules/stop-when-answered.md)): every claim the question requires is at or above its target rung and no open divergence would change the answer. If a load-bearing claim is still below its target rung, that is a signal to trace more, not to ship the gap unflagged — or, when the rung is genuinely unreachable (e.g. *observed* under `--read-only`), state the cap. When the test holds, return the map.

## Output shape and boundaries
- `--diagram` adds a diagram of the traced structure or flow to the map — see [render-diagram](../modules/render-diagram.md).
- **Durable-artifact output is out of scope** (deliberately open by design: a publish path here would duplicate the communicate/artifacts capability and pull a config prerequisite into a read-only skill that has none). understand returns the map inline (or as a `--diagram`); a caller who wants it as a team document pipes it to that capability.

The output of this phase: the certainty-graded, anchored map answering the framed question — divergences surfaced, gaps named.
