# Known noise classes

Some candidates come back on almost every review and are almost never worth the author's time. Without a named list, each run re-derives one, and two reviews of the same diff withhold different things. These classes are withheld unless their exception holds.

| class | withhold when | report anyway when |
|---|---|---|
| **Pre-existing defect** | the change doesn't touch its line, doesn't newly reach it, and doesn't make it worse | the change touches its line, newly reaches it, or makes it worse, which puts it in the blast radius ([read-the-diff-in-its-blast-radius](read-the-diff-in-its-blast-radius.md)) |
| **Tool-catchable** | a linter, type checker or compiler that runs on this code in the project's CI, a pre-commit hook or its build would flag it | no tool that runs there would flag it |
| **Pedantic nitpick** | no craft lens in scope at this rigor covers it ([assess-craft](../phases/04-assess-craft.md)), it breaks no convention the surrounding code holds ([match-the-surrounding-code](../../../craft/engineering/match-the-surrounding-code.md)), and [weight-by-impact-not-count](weight-by-impact-not-count.md)'s keep test drops it | a craft lens in scope covers it, it breaks such a convention, or the keep test keeps it |
| **Unrelated quality issue** | the change neither introduced nor touched it, and the project's own conventions don't demand fixing it in every change | the change introduced or touched it, or the project's conventions demand it of every change |
| **Explicitly silenced** | the code suppresses it with a lint-ignore or similar marker, and what it suppresses is no defect by [separate-correctness-from-taste](separate-correctness-from-taste.md)'s test | what it suppresses is a defect by that test |
| **Intended behavior change** | the change's intent asks for this behavior, and it's no defect by [separate-correctness-from-taste](separate-correctness-from-taste.md)'s test (a caller that still relies on the old behavior makes it one) | the intent didn't ask for it: a scope note ([respect-author-intent](respect-author-intent.md)), and a correctness finding too if it breaks something. Or it's a defect by that test though the intent asked for it: a correctness finding |
| **Looks like a bug, isn't** | tracing shows a guard, invariant or caller contract that makes it safe on every reachable path | on some reachable path nothing makes it safe ([confirm-before-claiming](confirm-before-claiming.md)) |
| **Handled one frame up** | every caller already handles the case | some caller doesn't |

A withheld candidate isn't reported and isn't counted. When you can't tell which side of a row a candidate falls on, report it at its honest confidence. The classes apply at every rigor, max included: rigor moves the confidence floor and the lens set ([calibrate-confidence-to-rigor](calibrate-confidence-to-rigor.md)), not what counts as noise.

(basis: after code-review's published false-positive list, adapted to praxis's blast-radius reading)
