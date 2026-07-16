# Timeboxing — `--timebox=<duration>`

Work to a wall-clock limit and return the best answer reached by then, rather than running to saturation. Activated from [plan-the-search](../phases/02-plan-the-search.md).

1. **Front-load the highest-value evidence.** Order the work so the load-bearing sub-questions are gathered and their key claims verified *first* — if the clock cuts the run short, it cuts the peripheral, not the core.
2. **Degrade gracefully at expiry.** When time runs out, stop and compose from what you have: the answer at the confidence the gathered evidence earns, with the unfinished sub-questions named as open ([name-the-uncertainty](../rules/name-the-uncertainty.md)). Never drop the run — a best-effort answer that states its own incompleteness is the deliverable.
3. **Report as time-bound.** Say the answer is timeboxed and which sub-questions were still open at expiry, so the caller reads it as bounded, not saturated — the same honesty [budget-discipline](budget-discipline.md) owes. Verification degrades to fit the remaining time the same way the budget cap degrades it ([verification-level](../rules/verification-level.md)).
