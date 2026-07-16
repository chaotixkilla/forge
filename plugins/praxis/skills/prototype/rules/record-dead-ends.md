# Record dead ends

Note the approaches that didn't work and why — the rejected paths are often the most valuable thing a prototype produces. A spike's positive result ("X works") saves you one build; its negative results ("Y looked promising but failed because Z", "the obvious approach W hits this wall") save everyone who comes after from re-walking ground you already covered. Because the code is thrown away, these dead-ends would otherwise vanish entirely — the one durable trace that the approach was tried and why it lost.

Capture each dead-end with its *cause*, not just its existence: "approach Y — refuted because it can't hold ordering under concurrent writes," not "Y didn't work." A rejected path without its reason is an invitation to try it again. Under `--max-agents`, the runner-up approaches are dead-ends in exactly this sense ([parallel-fan-out](../modules/parallel-fan-out.md)) — the priced reason each lost is part of the record.

Cited from [capture-and-discard](../phases/06-capture-and-discard.md).
