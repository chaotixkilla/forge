# communicate — usage

Produce a human-facing artifact of the work — a doc, status update, decision record, onboarding note, or review/handoff message — and route it to the right people, pitched to a named audience at the right altitude. communicate owns the judgment (what to say, to whom, how much, in what form, through which channel, whether to send at all); it returns the artifact, and the act that ran it delivers it through the `communication` and `artifacts` ports.

## When to use
- The substance already exists (a decision was made, work shipped, a design settled) and the job is to *land it on people* — shape it and get it to the right readers.
- You want the artifact pitched to a specific reader: a one-line exec summary, a peer-dense design note, a self-contained external release note, or an onboarding walkthrough for a newcomer.
- You want it routed, not just written: returned for review, announced to a channel or person, or published as a durable team-facing document — with the delivery degrading gracefully when no backend is wired.
- You want a decision record that preserves the *why* and the rejected alternatives, not just the conclusion.

## Not for / use instead
- Live-incident status at a severity-keyed cadence (acknowledge → mitigate → resolve) → the incident act in **work**, which owns the cadence and the resolution declaration. communicate writes the incident's retrospective once the service is stable.
- The mechanical act of posting a message or reading a thread → the **communication** port (communicate decides *what* and *whether*; the port carries it out).
- The mechanical act of publishing a document to a backend → the **artifacts** port (communicate produces the clean export; the port publishes it faithfully).
- Gathering the substance in the first place — the weighted cross-lane investigation → **gather**; communicate reads knowledge as direct doc-context, it does not run the investigation.
- Writing the code change and its craft → **develop**; reviewing a diff and reporting findings → **review**. communicate carries *findings and decisions to an audience*, it does not produce them.

## Examples
`communicate` — produce the artifact for the current work and return it (the default: no external delivery unless a flag asks for it).
`--audience=exec` — pitch it to a decision-maker: bottom-line-up-front, impact and cost, minimal mechanism.
`--audience=newcomer --as=doc` — a self-contained onboarding document that defines house terms and states the why before the how.
`--lang=pt-BR` — produce the artifact in Brazilian Portuguese, preserving the original's intent and tone.

## Gotchas
- **communicate needs no configuration of its own.** Producing and returning the artifact is ambient. Sending it — posting, publishing, filing — is the delivering act's in **work**; communicate hands back the artifact with where it's meant to go.
- **Clean export is not optional.** Anything communicate hands to a human — returned, posted, or published — carries the content and the decisions and *none* of the machinery: no tool calls, no agent/phase/skill mechanics, no praxis process, no account of how it was produced. The internal-process references are stripped before delivery, every time.
- **`--audience=` and `--as=` name a value, they don't add behavior.** The skill always models an audience and picks a form; these flags override what it would have inferred. Getting the audience wrong silently pitches the whole artifact at the wrong reader — state the tier if you know it.
- **The audience tier is the load-bearing call.** Depth, jargon, framing, and confidentiality all follow from it; a peer-dense note shipped to an external reader leaks internal context, and an exec summary handed to an implementer omits the mechanism they need.
