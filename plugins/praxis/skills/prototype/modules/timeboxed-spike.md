# timeboxed-spike (`--timebox=<duration>`)

Activated by `--timebox=<duration>`, referenced from SKILL.md as a whole-run module (it bounds [build-the-spike](../phases/04-build-the-spike.md) → [evaluate-against-the-question](../phases/05-evaluate-against-the-question.md) and gates the loop-back there).

The base spike runs until it reaches a verdict or the executor judges it done. This module bounds the effort to a fixed budget and makes expiry a defined, non-failure outcome — so a spike can't quietly become open-ended research. **Deletion test:** remove it and prototype runs to natural completion; the flag adds the effort bound, the stop-and-report-best-so-far behavior at expiry, and the budget term in the loop-back gate.

## The delta

- **Bound the effort** to the caller's `<duration>` and track it across build and evaluate.
- **On expiry, stop and report the best answer reached so far** — do not push past the box. "Best so far" is stated honestly on the [verdict-scale](../rules/verdict-scale.md): the current verdict (most often **still-open**), the evidence gathered, and explicitly *what was and wasn't observed* by the time the box closed. An expired spike reported as *answered* on partial evidence is the failure this module exists to prevent.
- **Gate the loop-back** — a still-open verdict may re-spike only if budget remains ([evaluate-against-the-question](../phases/05-evaluate-against-the-question.md)); when the box is spent, still-open is the terminal result and the caller decides whether to proceed under uncertainty or re-invoke on a narrower question.

`(basis: a spike is bounded so its investment is fixed and it has an exit condition — "a spike without a time box is research with no exit condition," and still-open-at-expiry is a valid terminal from which you decide proceed-or-re-spike (Cohn, Mountain Goat). The duration itself is the caller's to set: no authoritative universal cap exists — the published record's ceiling, "a couple of days" (Jeffries), is one team's convention — so prototype pins no default duration and takes the value from the flag.)`
