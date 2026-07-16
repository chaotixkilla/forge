# deep-mode (`--deep`)

Activated by `--deep`, referenced from the [SKILL.md](../SKILL.md) body (it raises rigor across the whole run, not one phase).

The base run designs at standard rigor — enough exploration and scoring to close the solution space soundly. This module turns the dial to maximum for a design that has to be right the first time. Deletion test: remove it and plan still runs end to end at standard rigor; `--deep` only widens and deepens what the base phases already do.

## The delta

- **Widen the approach search** in [choosing-approach](../phases/02-choosing-approach.md): enumerate more candidate approaches before gating, and run the evidence-gathering wider — delegate to `gather` in its own deep mode (`gather --deep`: wider lane set, more lead-chasing rounds) so prior art and stack-official support are canvassed rather than sampled.
- **Produce the trade-off scoring as a written, legible artifact.** The base run already scores every survivor on all five axes and records each rejected alternative with its losing axis ([choosing-approach](../phases/02-choosing-approach.md) Step 2–3, [record-rejected-alternatives](../rules/record-rejected-alternatives.md)) — that is not the delta. Under `--deep` the delta is that this comparison is **written out in full** — a scored table with every approach, every rung assignment, and every rejection reason, in the design document — so a reviewer can audit the choice rather than re-derive it.
- **Dig into hard-part mechanics** in [working-the-hard-parts](../phases/04-working-the-hard-parts.md): sequence more of the tricky flows explicitly, specify failure mechanics to a finer grain, and rate more flows on the risk scale rather than only the obvious ones.
- **Raise the default critic panel.** Unset, the base run recruits its natural per-phase critics; `--deep` defaults to one full pass of each of the four distinct lenses (trade-off-analyst, future-self, adversary, simplicity-hawk) on the committed design. `--deep` is the *breadth* dial (more exploration, explicit scoring, deeper mechanics); [`--critics=<n>`](adversarial-critics.md) is the *depth-of-scrutiny* dial and **overrides** the count. They compose — `--deep --critics=3` is the heavyweight combination — and neither subsumes the other.
