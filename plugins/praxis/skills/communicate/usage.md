# communicate — usage

Produce a human-facing artifact of the work — a doc, status update, decision record, onboarding note, or review/handoff message — and route it to the right people, pitched to a named audience at the right altitude. communicate owns the judgment (what to say, to whom, how much, in what form, whether to send); it hands the actual posting and publishing to the `communication` and `publish-artifact` ports.

## When to use
- The substance already exists (a decision was made, work shipped, a design settled) and the job is to *land it on people* — shape it and get it to the right readers.
- You want the artifact pitched to a specific reader: a one-line exec summary, a peer-dense design note, a self-contained external release note, or an onboarding walkthrough for a newcomer.
- You want it routed, not just written: returned for review, announced to a channel or person, or published as a durable team-facing document — with the delivery degrading gracefully when no backend is wired.
- You want a decision record that preserves the *why* and the rejected alternatives, not just the conclusion.

## Not for / use instead
- Live-incident status at a severity-keyed cadence (acknowledge → mitigate → resolve) → **operate** (it owns the incident cadence matrix and the resolution declaration; communicate is for the non-incident artifact stream).
- The mechanical act of posting a message or reading a thread → the **communication** port (communicate decides *what* and *whether*; the port carries it out).
- The mechanical act of publishing a document to a backend → the **publish-artifact** port (communicate produces the clean export; the port publishes it faithfully).
- Gathering the substance in the first place — the weighted cross-lane investigation → **gather**; communicate reads knowledge as direct doc-context, it does not run the investigation.
- Writing the code change and its craft → **develop**; reviewing a diff and reporting findings → **review**. communicate carries *findings and decisions to an audience*, it does not produce them.

## Examples
`communicate` — produce the artifact for the current work and return it (the default: no external delivery unless a flag asks for it).
`--audience=exec` — pitch it to a decision-maker: bottom-line-up-front, impact and cost, minimal mechanism.
`--audience=newcomer --as=doc` — a self-contained onboarding document that defines house terms and states the why before the how.
`--as=doc --publish` — render as a durable document and publish it through the artifacts capability, returning the canonical location.
`--notify=@team-channel` — after producing the artifact, announce it (a fit-for-channel summary with a link back) to that communication target.
`--publish --notify=@team-channel` — publish the durable document, then post the link to the channel (two ports: publish the doc, announce it).
`--lang=pt-BR` — produce the artifact in Brazilian Portuguese, preserving the original's intent and tone.
`--draft` — stop after tighten-and-verify and hand the content back unsent for review; delivery flags are held.

## Gotchas
- **communicate needs no configuration of its own.** Producing and returning the artifact is ambient. The communication capability (reached by `--notify`), the artifacts capability (reached by `--publish`), and the knowledge read that grounds the framing are all delegated to their ports, which own `tools.communication` / `tools.artifacts` / `tools.knowledge`. If a backend isn't configured, the port guides you through `init` (or blocks), and communicate degrades on its own side: it returns the finished artifact for you to send or publish by hand, and falls back to what the session already holds when knowledge is unreachable.
- **Clean export is not optional.** Anything communicate hands to a human — returned, posted, or published — carries the content and the decisions and *none* of the machinery: no tool calls, no agent/phase/skill mechanics, no praxis process, no account of how it was produced. The internal-process references are stripped before delivery, every time.
- **`--audience=` and `--as=` name a value, they don't add behavior.** The skill always models an audience and picks a form; these flags override what it would have inferred. Getting the audience wrong silently pitches the whole artifact at the wrong reader — state the tier if you know it.
- **`--draft` wins over delivery.** With `--draft`, the artifact is returned unsent even if `--notify`/`--publish` are also passed — the intent is "let me see it first."
- **`--notify` and `--publish` are different ports.** `--publish` puts a durable document somewhere people can refer back to it; `--notify` posts a message announcing it. Publishing does not notify anyone, and notifying does not create a durable record — pair them to do both.
- **The audience tier is the load-bearing call.** Depth, jargon, framing, and confidentiality all follow from it; a peer-dense note shipped to an external reader leaks internal context, and an exec summary handed to an implementer omits the mechanism they need.
