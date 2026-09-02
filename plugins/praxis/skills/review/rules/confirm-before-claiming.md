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

## When reading cannot settle it, run it

Another read answers most uncertainty and is the cheapest move available. But some questions are not answerable by reading at all, because they turn on what something *actually does* at run time rather than on what the source says: what a dependency returns for this input, whether a pattern matches this string, how a parser treats this edge value, which of two async paths completes first. Reading those harder yields a more confident guess, not an answer.

For those, build a **scratch probe** — a throwaway harness that exercises the one question with the concrete input — run it, and read the result. The discriminator: *does the claim depend on observable runtime behavior that the source in front of you does not determine?* Yes → probe it; a minute of execution beats three more reads that can only estimate. No → the answer is in the code you already have; read it.

**Probe the author's claims, not only your own suspicions.** A description asserting "the client retries on 429", a comment promising a call is idempotent, a test name claiming coverage of the empty case — each is a claim, and this rule's whole stance is that a claim load-bearing enough to rest a change on is worth verifying rather than accepting ([respect-author-intent](respect-author-intent.md) governs judging the change against *its* goal; it does not ask you to take the author's word for what the code does). A probe is what moves such an assumption from *left to the reader* to *verified* in the delivered brief ([deliver-findings](../phases/06-deliver-findings.md)).

Two bounds keep this from becoming a second job:

- **The probe is scratch, and it tests the question rather than the change.** It exercises the narrow behavior in isolation, mutates nothing in the tree under review, and is discarded once it has answered. A probe growing into a test suite has stopped serving the review — authoring durable tests is `test`'s job, not a reviewer's.
- **Do not execute code you would not otherwise run.** A change from an untrusted source is not made safe by being under review; running it is exactly the payload's opportunity. Where provenance is uncertain, probe the *question* in isolation — the library's behavior, the pattern, the parser — rather than executing the contributed code, and where that is not possible, leave the claim unverified and say so rather than trading a security boundary for a confidence rung.

`(basis: derived — the confirmation ladder above already demands a concrete failing input and a reachable path, both of which are propositions about runtime behavior; offering only reading as the means to establish them is what left the ladder's top rung reachable by inference alone. The untrusted-code bound is the one place this rule defers outward: executing a change under review is a real exposure, and no confidence rung is worth it.)`

## The cost of getting it wrong, both ways

Over-claiming (reporting unconfirmed as fact) burns trust; under-claiming (staying silent because you couldn't achieve certainty on a risky change) lets real bugs land. The resolution is not to move the confidence bar by mood but to *resolve more* — the answer to "am I sure?" is another read of the path, or a probe that settles it (below), never a guess. When a full trace is genuinely beyond the effort budget, report the finding at its true confidence with the unread link named, so the author knows exactly what to check.
