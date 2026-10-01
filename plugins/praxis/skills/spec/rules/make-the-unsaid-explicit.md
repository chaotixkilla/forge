# Make the unsaid explicit

Most of what a spec gets wrong is never stated at all. The specifier inferred a default (files cap at 10 MB, deleted data is purged after 30 days, an expired session redirects to login) and wrote the requirement as if the inference were shared fact. It isn't: it lives only in their head, invisible to the builder, the reviewer, and the stakeholder who would have said "actually, 10 MB is far too small."

## The three kinds, and the discriminator between them

Every not-given statement is one of three things, and they are handled differently — so the first move is to sort each correctly:

- **A fact** — it was given (in the prompt, the issue, the thread) or confirmed against authority. It stands as a requirement.
- **An assumption** — a *likely answer you chose* to fill a gap the input left open. You can defend it, but you decided it; it might be wrong. It goes on the page as an explicit, labeled assumption the reader can override.
- **An open question** — a fork you *cannot* resolve and won't pretend to: a genuine unknown only a stakeholder can settle. It goes on the page as an open question, routed to whoever owns the answer.

The discriminator between the three: **was this given, did I decide it, or can no one here decide it?** Given → fact. I decided it → assumption (surface it). No one here can decide it → open question (route it).

## The discriminator between an assumption and an open question

**An assumption is a likely answer you've taken and labeled; an open question is a fork you genuinely cannot resolve.** The test: *do you have a defensible default?* If yes, take it and label it an assumption (progress continues, the reader can veto). If no — any answer you'd give would be a coin flip a stakeholder must actually make — it's an open question (stop guessing, route it). Recording a real open question as an assumption hides a decision that needs an owner; recording a resolvable default as an open question stalls the spec on a call you could have made.

## Method

As requirements are interrogated ([interrogating-prompts](../phases/01-interrogating-prompts.md)) and made concrete ([making-it-concrete](../phases/04-making-it-concrete.md)), sweep for the silent defaults — limits, retention, failure behavior, auth model, empty/error states, concurrency, ordering — and write each as its own line, tagged assumption or open question. An assumption states the default taken and, ideally, why. An open question states the fork and who must decide. This surfacing is what [strict-gate](../modules/strict-gate.md) escalates on: under `--strict`, an unconfirmed assumption blocks completion.

The payoff is asymmetric: surfacing an assumption costs one line now; the same assumption discovered wrong after the build costs a rewrite. A spec that reads clean because it hid its assumptions is more dangerous than one visibly studded with them.
