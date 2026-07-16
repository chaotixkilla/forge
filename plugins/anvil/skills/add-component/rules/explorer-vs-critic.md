Agents come in two roles, and keeping them distinct is what makes a plugin's reasoning trustworthy. An explorer establishes *what is true*; a critic establishes *what might be wrong*. Blur them — let an explorer start judging, or a critic start inventing facts — and you lose the property that makes each useful: an explorer you can't trust to be neutral is just another opinion, and a critic that gathers its own evidence can no longer be checked against an independent reading. The two roles are separate components, separate folders, separate output contracts. This rule is how to tell which you're writing and how to keep it pure.

## An explorer gathers

An explorer is read-only and neutral. Its job is to find information and return findings anchored to their source — file, line, location — so a caller can verify every claim. It does not judge, recommend, rank by preference, or edit anything. Its output answers one question: *"what is true, and where did I find it?"*

For example, an explorer that reads a target plugin's structure returns *"skill X declares flag `--foo`; no module backs it; here are the file:line anchors"* — a fact with provenance, no verdict on whether that's good or bad. The anchoring is non-negotiable: an unanchored finding is an assertion the caller can't check, which defeats the point of a neutral gatherer.

## A critic challenges

A critic is adversarial and opinionated by design. It assumes the work in front of it is flawed and tries to prove it, surfacing risk, gaps, and unstated assumptions through a specific lens it owns. It does *not* gather fresh facts — it pressure-tests what it's given. Its output is a verdict plus the reasoning that justifies it.

For example, a critic with a cold-executor lens assumes a fresh agent with zero context and walks a procedure step by step, flagging every point that would force a guess — a judgment about the procedure's runnability, not a new survey of the codebase. Each critic owns one angle of attack (the abstraction boundary, the contract, the packaging boundary, runnability); state that lens up front so its scope is unambiguous.

## Keep the roles distinct

The clean test: if a component needs to read the world *and* render judgment on it, it's two components, not one — split the gathering into an explorer and the judging into a critic, so the verdict can be checked against an independent reading of the facts. Each role has a drift test. **Explorer drifting critic-ward:** strip every finding down to its claim; if any contains a should/prefer/better/instead, judgment has leaked in — move that sentence to a critic. **Critic drifting explorer-ward:** if any of its checks requires reading material beyond the work handed to it, that's fieldwork — route it through an explorer and challenge the returned facts instead. This separation is also why they live in different folders (`agents/explorers/` vs `agents/critics/`) and why they're recruited at different moments: a skill recruits an explorer where it *gathers* and a critic where it *challenges*. A single agent that does both collapses that distinction and hides which of its claims are observed and which are argued — exactly the ambiguity this split exists to prevent.
