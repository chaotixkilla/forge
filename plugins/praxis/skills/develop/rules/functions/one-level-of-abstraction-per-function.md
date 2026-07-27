# One level of abstraction per function

Inside a function, the temptation is to reach down for a detail right where you need it — inline a bit-twiddle, a string-format fiddle, a manual index loop — in the middle of a run of high-level calls. The judgment this rule governs is whether a statement belongs *in* this function or behind a call from it. Left to taste, one builder writes a function that reads as clean orchestration and another writes the same function with a low-level detail wedged between two domain steps, and the second reader has to context-switch mid-line.

## The discriminator

Within a single function, **every statement should read at the same conceptual level** — all orchestration, or all detail, not a mix. The test is a *level mismatch*: scan the body and ask whether each line sits at roughly the same altitude as its neighbors.

- A run of high-level, intent-named calls with **one low-level fiddle sitting among them** is the tell — the fiddle is at the wrong altitude and wants extracting behind a named call that restores the run to one level ([when-to-extract-a-function](when-to-extract-a-function.md)).
- Read the function top to bottom: it should narrate as *what happens*, a sequence of same-altitude steps, with the *how* of each step one level down behind its name. When you hit a line that's suddenly about bytes or indices while its neighbors are about orders and users, you've found the altitude break.
- This is not "make everything tiny" — a low-level function full of low-level detail is perfectly level. The fault is *mixing*: high-level narrative interrupted by a raw mechanism, or a detail routine that suddenly makes a policy decision.

(basis: the Single Level of Abstraction Principle (SLAP); Fowler & Beck's composed-method style — a function should read as a sequence of steps all at the same level of detail, each step a call whose name states its intent and whose body lives one level below.)

## The anchors

- *Good:* `placeOrder` reads `validate(cart); reserveStock(cart); charge(customer, total); notify(customer)` — four steps, one altitude, each *how* hidden behind its name; the function narrates the policy and nothing else.
- *Bad:* the same `placeOrder` where, between `reserveStock` and `charge`, sits a raw loop summing line items and rounding half-even with a magic factor — a byte-level detail crashing a policy-level narrative. Lift it to `computeTotal(cart)` and the function reads at one level again.
