# Minimize state scope

Declaring a variable, the reflex is to hoist it — put it at the top of the function, or out at the module level, "so it's available." The judgment this rule governs is *how wide* a variable's scope should be and *how early* it should be declared. Left to taste, one builder declares everything up front and mutates it as the function runs, while another declares each value at its first use in the narrowest block that needs it — and the first version breeds the bug where one branch forgets to set the variable and a stale value leaks downstream. This rule pins the discriminator so two builders converge on the call.

## The discriminator

A variable's scope should be **the smallest region that actually needs it**, and its declaration should sit at the point of first use — not hoisted above the code that uses it.

- **Narrow the scope to the live span.** If two adjacent lines are the only ones that touch a variable, it does not belong at function top or, worse, module level; declare it right where it comes alive and let it die at the end of the block. A wide-scope variable that only lives briefly is a *leak* — it invites reads and writes from code that has no business touching it, and it widens the surface any reader must hold in their head.
- **Shrink the "live time."** The distance between a variable's first and last use is its live time; keep it short. A value computed at the top and used only at the bottom forces the reader to carry it across everything between. Move the declaration down to meet its use.
- **Prefer immutable, and prefer local over shared.** A value that never changes can't be corrupted by a forgotten branch; reach for a constant before a reassigned variable ([immutable-by-default](../data-and-types/immutable-by-default.md)). State shared across a function — set in one branch, read in another — is where the "forgot to set it on this path" bug lives; a value confined to the branch that needs it cannot have that bug.

(basis: McConnell, *Code Complete* — minimize variable scope and shorten the "live time" between a variable's references; the narrowest-scope, declare-at-first-use principle reduces the span of code in which a variable can be misused.)

## The anchors

- *Good:* a loop's accumulator declared inside the loop's enclosing block, used across its few lines, and out of scope the moment the result is returned — nothing outside can read or corrupt it.
- *Bad:* a `result` variable declared at function top, left `null`, assigned inside one arm of a conditional and read after — so the path that skips the arm sails past with a stale or null value, a bug that a block-scoped, assigned-once binding makes impossible to write.
