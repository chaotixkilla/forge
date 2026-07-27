# Name for the reader

A name is read far more often than it is written, and almost always somewhere other than where it was defined. The judgment this rule governs is which name to pick in the moment of writing — and it goes wrong quietly: a name that made sense to the author at the definition reads as a riddle at the call site, and the next person pays with a jump-to-definition on every encounter. Two builders naming the same thing from private taste produce a codebase that reads in two dialects.

## The discriminator

Judge a name by the question: **can a reader at the call site predict what this is or does, without jumping to its definition?** Not "is it short," not "does it match a style guide" — does it carry its meaning to where it's used.

- A name **reveals intent and role at the call site** — a reader following the calling code can predict the value's meaning, the function's effect, and (for a function) whether it has side effects, from the name alone. That is the bar.
- Calibrate the *length and specificity to the scope*: a loop index living three lines is fine as `i`; a value that crosses functions or lives on a type earns a name that survives the distance. Scope sets the budget — a wide-scope name that's terse is as wrong as a one-line-scope name that's ceremonial.
- The name is calibrated to the **local convention** — the casing, the domain vocabulary, the get/fetch/load distinctions the surrounding code already draws ([match-surrounding-conventions](../change-hygiene/match-surrounding-conventions.md)). A perfectly descriptive name in a foreign style is still a bad citizen.

(basis: McConnell, *Code Complete* 2nd ed. ch. 11 — name length/specificity scaled to scope, names that state intent; Ousterhout, *A Philosophy of Software Design* — names should be precise and consistent, a name you must read the code to understand is a red flag. The call-site-predictability framing is the shared thread.)

## The anchors

- *Good:* `remainingRetries` at a call site tells you it's a count and what it counts; `chargeCard(order)` tells you it acts and on what. A reader predicts correctly without leaving the line.
- *Bad:* `data`, `tmp`, `flag`, `doIt()`, `process(x)` at the call site tell you nothing — every use forces a trip to the definition; or `getUser()` that silently writes to a cache (the name lies about the effect — [avoid-misleading-names](avoid-misleading-names.md)).

The specific craft of variable names ([naming-variables](naming-variables.md)) and function names ([naming-functions](naming-functions.md)) refines this; a name that misleads about type, mutation, or cost is worse than a vague one ([avoid-misleading-names](avoid-misleading-names.md)), and one concept should keep [one-name-per-concept](one-name-per-concept.md) across the change. This rule is the umbrella test they all serve.
