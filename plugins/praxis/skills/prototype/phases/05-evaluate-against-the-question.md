This is the phase the whole spike was built to reach: the probe has run, and now you read what it *did* against the question you framed. The discipline here is to report the observation, not your hopes for it — a spike earns its keep only if the verdict is trustworthy, and the fastest way to waste one is to read a promising-looking run as proof of something it never exercised. Run the probe, observe, assign the verdict, and decide whether one pass was enough.

## Run the probe and record what was observed

Execute the spike and capture the raw observation — the number, the output, the error, the behavior — as *evidence*, separately from any interpretation of it. Trust what ran over what the code looks like it should do ([ground-claims-in-a-run](../rules/ground-claims-in-a-run.md)): a feasibility claim holds only once something actually ran and showed it. Record enough of the observation that the verdict below is reconstructable by someone who wasn't there — the input, the conditions, and the result — because this evidence, not the code, is what survives into [capture-and-discard](06-capture-and-discard.md).

## Assign the verdict against the framed question

Read the observation against the success test framed in [frame-the-question](01-frame-the-question.md) — the *pre-committed* one, not a bar chosen after seeing the result — and assign exactly one verdict on the [verdict-scale](../rules/verdict-scale.md) — **answered**, **refuted**, or **still-open** — by its assignment test. Two checks carry the weight: a run is *answered* only if it exercised the framed unknown itself under conditions faithful to the question and the observation reproduced (a promising signal from a run that stubbed the real risk is *still-open*, not answered); and *refuted* needs the run to positively *show the assumption failing*, not merely fail to show it working (a spike that ran out of road is *still-open*, not refuted). Don't round a still-open run up to answered because the number looked good, and don't collapse it down to refuted because you didn't see success — both ship a decision on evidence never gathered.

Then state how far the verdict generalizes: name the shortcuts the spike took that would not survive production scale, data, or constraints ([keep-the-real-thing-in-view](../rules/keep-the-real-thing-in-view.md)), so the caller reads the verdict as what it is — a signal about the framed unknown under the spike's conditions — and not as more.

## Under `--max-agents` — compare the raced approaches

When approaches were raced, this is where they are compared and one is selected, verdict-first, on the declared basis — see [parallel-fan-out](../modules/parallel-fan-out.md). A single-probe run skips this.

## The loop-back gate — spike again, or stop

A still-open verdict poses one decision: probe again, or stop and report it. Resolve it mechanically:

- **Loop back** to [pick-the-cheapest-probe](03-pick-the-cheapest-probe.md) — re-entering with a *narrowed* question — only when **all** hold: the verdict is **still-open**; budget remains (`--timebox` not expired and, under `--max-agents`, approaches not exhausted — see [timeboxed-spike](../modules/timeboxed-spike.md)); **and** you can name the *specific* reason it's still-open and a different or narrower probe that would resolve it (e.g. "the serialization stub hid the real cost — next probe runs real serialization on 10 records"). Each loop-back must *narrow the unknown* — isolate more, stub less, or fix the confound — never merely re-run the same probe hoping for a different number.
- **Stop** — proceed to [capture-and-discard](06-capture-and-discard.md) — when the verdict is **answered** or **refuted** (the question is resolved either way), **or** budget is exhausted, **or** the still-open reason names no narrower probe that would resolve it. A still-open verdict that can't be narrowed within budget is a complete, honest result: re-invoking prototype on a re-framed question is the outer loop, not an in-run spin.

`(basis: ratified by the maintainer, 2026-07-09 — bounded loop-back. Iterative spiking is permitted but must converge: gated on a still-open verdict, remaining budget, and a named narrowing so each pass reduces the unknown. This encodes the single-pass-vs-loop fork — the disposable-spike tradition leans single-pass; iterative/evolutionary spiking (Ries's build-measure-learn; Frey et al. 2009 on iterated convergence) leans loop — resolved as loop-within-a-bound, with re-invocation as the unbounded outer loop. The bound is what makes iteration safe: "a spike without a time box is research with no exit condition" and still-open-at-expiry is a valid terminal from which you decide proceed-or-re-spike, not a reason to keep running — Cohn, Mountain Goat.)`

The output of this phase: the verdict, the observed evidence it rests on, the generalization caveats, and (under `--max-agents`) the selected approach — the material [capture-and-discard](06-capture-and-discard.md) turns into the durable findings.
