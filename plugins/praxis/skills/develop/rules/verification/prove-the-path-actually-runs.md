# Prove the path actually runs

The judgment this rule governs is what counts as evidence that a change works. In the moment, the cheap signals are seductive — it compiled, the type-checker is happy, the suite is green — and the reflex is to trust them and move on. Left to taste, they diverge: one builder calls a slice proven because the suite passed; another notices the suite never entered the new branch and the "pass" is about code that didn't change. The same slice is *verified* to one and *false-green* to the other.

## The discriminator

Trust **observed execution** over compilation, type-checking, or an assertion that never ran. A slice or test proves nothing about the change until the *changed path is seen to actually execute*.

- **Did the new code path run?** Compilation and a clean type-check prove the code is well-formed, not that it does the right thing — they never enter a branch. A test that exists but asserted on an unchanged path is false green: it passed without touching the lines you wrote. The bar is watching the new branch execute and the assertion evaluate against its result.
- **Can the new test fail?** For a check you just wrote, confirm it can go red before you trust its green — break the code once (or write it against unfixed code) and watch the test fail, then restore. A test never seen red may be asserting nothing, or asserting on the wrong thing; its green is unearned.
- **Reason is not observation.** "It must work because the logic is obviously right" is the trap this rule exists to close. Convince yourself by *seeing it run*, not by re-reading the code — the two disagree exactly where the bugs live.

This is the empirical backbone of [verified-slice](../verified-slice.md): "green" there means *exercised*, and this rule is why compilation and an unrun assertion don't qualify.

(basis: Beck, *Test-Driven Development: By Example* — a test never seen red proves nothing, so drive it red before trusting green; Hunt & Thomas, *The Pragmatic Programmer* — prefer observation over reasoning about what the code does, "don't assume it — prove it.")

## The anchors

- *Good:* you run the loop, watch a log line or debugger confirm the new branch is entered, and see the assertion evaluate against the value the change produced. When you added the test, you first broke the code and watched it go red, so its pass means something.
- *Bad (reject as false-green):* the suite is green and you move on — but the new test set up a case the new branch never handled and asserted on the old path, or the code only compiled and was never run. The green is about code that didn't change; the change itself is unproven.
