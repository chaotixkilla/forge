## Run the probe and record what was observed

Execute the spike and capture the raw observation — the number, the output, the error, the behavior — as *evidence*, separately from any interpretation of it. Trust what ran over what the code looks like it should do ([observation-over-inference](../../../craft/evidence/observation-over-inference.md)): a feasibility claim holds only once something actually ran and showed it. Record enough of the observation that the verdict below is reconstructable by someone who wasn't there — the input, the conditions, and the result — because this evidence, not the code, is what survives into [capture-and-discard](06-capture-and-discard.md).

## Assign the verdict against the framed question

Read the observation against the success test framed in [frame-the-question](01-frame-the-question.md) — the *pre-committed* one, not a bar chosen after seeing the result — and assign exactly one verdict on the [verdict-scale](../rules/verdict-scale.md) — **answered**, **refuted**, or **still-open** — by its assignment test.

Then state how far the verdict generalizes: name the shortcuts the spike took that would not survive production scale, data, or constraints ([keep-the-real-thing-in-view](../rules/keep-the-real-thing-in-view.md)), so the caller reads the verdict as what it is — a signal about the framed unknown under the spike's conditions — and not as more.

## Under `--max-agents` — compare the raced approaches

When approaches were raced, this is where they are compared and one is selected, verdict-first, on the declared basis — see [parallel-fan-out](../modules/parallel-fan-out.md). A single-probe run skips this.

## The loop-back gate — spike again, or stop

A still-open verdict poses one decision: probe again, or stop and report it. Resolve it mechanically:

- **Loop back** to [pick-the-cheapest-probe](03-pick-the-cheapest-probe.md) — re-entering with a *narrowed* question — only when **all** hold: the verdict is **still-open**; budget remains (`--timebox` not expired and, under `--max-agents`, approaches not exhausted — see [timeboxed-spike](../modules/timeboxed-spike.md)); **and** you can name the *specific* reason it's still-open and a different or narrower probe that would resolve it (e.g. "the serialization stub hid the real cost — next probe runs real serialization on 10 records"). Each loop-back must *narrow the unknown* — isolate more, stub less, or fix the confound — never merely re-run the same probe hoping for a different number.
- **Stop** — proceed to [capture-and-discard](06-capture-and-discard.md) — when the verdict is **answered** or **refuted** (the question is resolved either way), **or** budget is exhausted, **or** the still-open reason names no narrower probe that would resolve it. A still-open verdict that can't be narrowed within budget is a complete, honest result: re-invoking prototype on a re-framed question is the outer loop, not an in-run spin.

`(basis: maintainer, 2026-07-09; after Ries's build-measure-learn, Frey et al. 2009 and Cohn)`

The output of this phase: the verdict, the observed evidence it rests on, the generalization caveats, and (under `--max-agents`) the selected approach — the material [capture-and-discard](06-capture-and-discard.md) turns into the durable findings.
