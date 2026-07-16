# Follow execution, not names

This is understand's founding discipline — the ethos beneath [find-the-source-of-truth](find-the-source-of-truth.md). A name is a promise, a comment is a memory, a doc is an intention, and each can be stale, aspirational, or simply wrong, while the code is what actually runs. Believing the label over the behavior produces a map of the system the author *meant* to write instead of the one that exists — and the bug, the surprise, the thing worth understanding all live exactly where intent and behavior diverge.

## Trust behavior over its labels
When a claim depends on what a symbol does, read the symbol — do not infer its behavior from what it is called. A function named `validate` may reject nothing; a variable typed non-null may be widened by a cast upstream; a comment may describe the code two refactors ago. Names and comments orient you to *where to look*; they are never evidence of *what happens there*.

## Verify the path actually runs
A path that looks reachable in the source may be dead — behind a flag never set, a condition nothing satisfies, an override registered elsewhere. Before resting a claim on a path, confirm the path is real: it is reached with the input in question, and no earlier frame short-circuits it. A behavior behind an unreachable guard is not the system's behavior. This is where certainty is earned: a path you confirmed runs is *observed* or *traced*; a path you only assumed runs is at most *inferred* ([separate-fact-from-inference](separate-fact-from-inference.md)).

Cited from [trace-the-behavior](../phases/03-trace-the-behavior.md) and [corroborate-against-reality](../phases/04-corroborate-against-reality.md).
