# Confirm before claiming

A review's credibility is spent the first time it reports a bug that isn't one. The author traces the "defect," finds the code is correct, and quietly discounts every later finding. The failure almost always has the same root: the reviewer judged the change by what the names, comments, and types *say* it does rather than by what the code *actually* does. This rule is the discipline of tracing the real path before asserting a defect — trust behavior over description, every time they can diverge.

## Trust the code, not its labels

A function called `validate` may not reject anything; a comment may describe the code as it was two refactors ago; a type may be widened by a cast three lines up. Names and comments are the author's *intent*; the bug you are hunting is exactly where intent and behavior diverge. So when a finding depends on what a symbol does, read the symbol — do not infer its behavior from what it is called. The rule from the understand craft applies: follow execution, not names.

## What "confirmed" requires before you claim a correctness defect

Before you assert a change is *wrong* (not merely suspicious — the confidence ladder in [calibrate-confidence-to-effort](calibrate-confidence-to-effort.md) covers the graded case), you owe three reads:

- **The failing input exists** — you can state a concrete value or state that triggers the wrong behavior, not a hand-wave at "bad input."
- **The path is reachable** — a caller actually reaches this code with that input; a bug behind a condition nothing satisfies is at most speculative.
- **No guard already handles it** — you checked the lines between the caller and the suspect code for the validation, early-return, or clamp that would make the bug unreachable. The most common false positive is a "missing check" that exists one frame up.

Clear all three and the finding is *confirmed*; clear the first two but not the third's verification and it is *probable*; clear only the pattern and it is *speculative*. The point is not to suppress uncertain findings — effort decides which to report — but to *label* honestly and never dress a speculation as a certainty.

## The cost of getting it wrong, both ways

Over-claiming (reporting unconfirmed as fact) burns trust; under-claiming (staying silent because you couldn't achieve certainty on a risky change) lets real bugs land. The resolution is not to move the confidence bar by mood but to *trace more* — the answer to "am I sure?" is another read of the path, not a guess. When a full trace is genuinely beyond the effort budget, report the finding at its true confidence with the unread link named, so the author knows exactly what to check.
