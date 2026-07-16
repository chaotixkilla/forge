# Ground claims in a run

Trust observed behavior over reasoning about the prototype. A claim about feasibility holds only once something actually ran and showed it — "this should work," "the library clearly supports this," "the types line up so it'll be fine" are hypotheses, not results, and a spike exists precisely to replace the hypothesis with an observation. The moment you find yourself concluding from how the code *looks* rather than from what a run *did*, you've stopped spiking and started guessing, and a guess dressed as a verdict is worse than no spike at all.

This is the evidence bar underneath the [verdict-scale](verdict-scale.md): a verdict of *answered* or *refuted* must point to a specific thing that ran and what it produced; a conclusion resting on reasoning rather than a run is *still-open*, however confident the reasoning. The discipline: before recording any verdict, name the run that grounds it — the input, the execution, the observed output. If you can't, you haven't run the probe yet.

`(basis: the observed-over-reasoned principle — Ries's *validated learning* (Lean Startup): a claim is validated only by observed evidence from a real experiment, not by argument; and the empirical premise of the XP spike solution — you build the spike to *find out*, because you cannot reason your way to the answer.)`

Cited from [evaluate-against-the-question](../phases/05-evaluate-against-the-question.md).
