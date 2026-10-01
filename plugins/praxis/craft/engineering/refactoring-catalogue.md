# The refactoring catalogue

A refactoring is a change to code's internal structure that makes it easier to understand and cheaper to modify without changing its observable behavior, and refactoring is reaching a new structure through a *series* of such changes. The series is the point: each move does little, so it's unlikely to go wrong, and the code works after every one, so a mistake shows up in the move that made it instead of at the end of a long rewrite where any of a hundred edits could be the cause. A restructuring made as one large edit and checked at the end isn't refactoring by this definition, however behavior-preserving its intent.

`(basis: Fowler, refactoring.com; Fowler, "RefactoringMalapropism", 2004)`

## One hat at a time

A move either preserves behavior or changes it, never both. Refactoring changes structure with every check staying green; adding behavior adds tests and may change existing ones. Switch between the two deliberately, at a green check — make it work, then make it right — and the same line runs between whole changes ([separate-refactor-from-behavior-change](separate-refactor-from-behavior-change.md)). When a refactoring turns out longer than the work in hand can carry, set it aside and come back to it rather than finishing it inside a behavior change. And don't refactor further than the work in hand needs: tidying past it is its own change.

`(basis: Fowler, "Workflows of Refactoring", 2014, the two hats; Beck, "Canon TDD", 2023)`

## The method: green, one move, green

1. **Start from green.** Refactor only on passing checks — the project's tests, or a characterization of the code's behavior where it has none (below). Set aside work in progress that keeps the checks red first, so the starting point is a known-good state.
2. **Name the move.** Pick one move from the catalogue for the structure you want: "Extract Function on the totals loop", not "clean up the exporter". A named move has a known shape, a known inverse and a condition that keeps it behavior-preserving; an unnamed edit has none of them, and is where behavior quietly changes.
3. **Check its condition, make it, run the checks.** A move whose condition (in the catalogue) fails changes behavior, so it isn't made as a refactoring. After the move, a red check means the move was a mistake: the checks were green before it, and it was meant to change nothing. Don't debug forward into a half-moved structure; not getting trapped in debugging is what the small move buys.
4. **Keep the breakage short.** The code shouldn't stay broken — not building, or red — for more than a few minutes at a time. A move that can't be finished inside that is too big: split it into smaller moves, or reach the structure by parallel change (below).
5. **Commit at the green points worth returning to**, so a later mistake rolls back one move, not the session.

`(basis: Fowler, "Workflows of Refactoring", 2014; Fowler, "RefactoringMalapropism", 2004, for the few-minutes limit, the only number the sources give)`

**When a move turns the checks red — the fork.** The authorities agree a red check is a mistake and that debugging forward is the trap; they don't pin the recovery. Two positions are defensible: **revert to the last green and redo the move in smaller steps** — Beck's test-commit-or-revert makes that automatic, and it keeps every state you can reach a known-good one; or **fix it in place when the mistake is plain in the move just made** — a typo, a call site the move itself named and missed — which is cheaper than redoing a move whose one flaw is evident. The discriminator: can you name the mistake from the move's own diff, without investigating? Yes → fix it and re-run the checks; no → revert and take a smaller step. `(routed to maintainer: the fix-in-place branch, bounded to a mistake named from the move's own diff; no source pins the recovery)`

**An automated move gets checked like a manual one.** A tool that performs the move saves the typing, not the verification: run the checks after it exactly as after a hand-made move, since a tool's result doesn't certify itself. `(basis: refactoring.com, tools "valuable … but not essential"; Fowler on an IDE refactoring that "doesn't do it correctly", 2016)`

## Untested code: characterize it first

Code with no tests is refactored blind. Before the first move, pin its actual behavior: with characterization tests — write a test with a placeholder expectation, run it, put in the value it actually produced, and name the test after what you learned — or, where the change mustn't add tests, with a throwaway harness whose recorded outputs serve the same purpose. Either records what the code does, not what it should do — an apparent bug included, because a system in production has become its own specification. Behavior that looks wrong is noted for its own change, never fixed inside the refactoring.

`(basis: Feathers, "Characterization Testing", 2016)`

## An interface others call: parallel change

A move that changes a signature, a field or a boundary is one move only when every caller changes with it, in the same green step. When some can't — callers beyond the change, or too many for one step — reach the new structure by parallel change: **expand** the interface to support the old form and the new; **migrate** the callers to the new form, incrementally; **contract**, removing the old form once nothing uses it. The code stays releasable in every phase. The cost is carrying both forms through the migration, and a contract phase that never runs leaves the code worse than it started, so the contract step is owed and tracked until it's done. How much migration and notice a contract owes consumers outside the team is [preserve-the-contract](preserve-the-contract.md)'s call.

`(basis: Sato, "Parallel Change", 2014; Fowler, "Workflows of Refactoring", 2014, branch by abstraction)`

## The catalogue

The names are those of Fowler's *Refactoring*, second edition — the vocabulary to name a move in — and paired moves undo each other. For each: the situation that calls for it, and the condition that keeps it behavior-preserving, where it has one.

| move | reach for it when | preserves behavior only if |
|---|---|---|
| Extract Function ↔ Inline Function | a fragment needs a name to be understood, or repeats (a long function, duplicated code, a comment explaining a block) ↔ a function's body says no more than its name (a lazy element, a middle man) | inline: the function isn't overridden or dispatched dynamically |
| Extract Variable ↔ Inline Variable | an expression needs a name ↔ a name says no more than its expression | extract: evaluating the expression once, where it was evaluated before, changes nothing it computes or does |
| Change Function Declaration | a function's name or parameters mislead or no longer fit | every caller changes in the same step; otherwise, parallel change |
| Rename Variable · Rename Field | a name doesn't say what the thing is | every reference moves with it, serialized and configured names included |
| Encapsulate Variable | widely used data is reached directly (global or mutable data) | — |
| Introduce Parameter Object | the same parameters travel together (a long parameter list, data clumps) | — |
| Split Phase | one piece of code does two things in sequence (divergent change) | the second phase uses only what the first hands it |
| Replace Temp with Query | a temporary holds a value a function could compute | the temp is assigned once, and the expression has no side effects |
| Extract Class ↔ Inline Class | a class does two jobs (divergent change, data clumps, a temporary field) ↔ a class no longer earns its place | — |
| Move Function · Move Field | a function or field uses another module more than its own (feature envy, shotgun surgery) | every reference reaches it at its new home |
| Slide Statements | related statements are scattered | a moved statement reads and writes nothing the statements it passes over write |
| Split Loop | one loop does several things | no computation in one loop depends on the other's within an iteration |
| Replace Loop with Pipeline | a loop filters, maps and accumulates by hand | the pipeline keeps the loop's order, its early exits and its side effects |
| Split Variable | one variable holds different things at different times | — |
| Decompose Conditional · Consolidate Conditional Expression | a condition's tests or branches are hard to read | consolidate: the checks being combined have no side effects |
| Replace Nested Conditional with Guard Clauses | special cases bury the normal path | — |
| Replace Conditional with Polymorphism | the same switch on a kind of thing recurs (repeated switches) | every branch of the switch maps to one type |
| Separate Query from Modifier | a function returns a value and also changes state | every caller that relied on the change now calls the modifier |
| Remove Dead Code | code nothing reaches | nothing reaches it from any entry point, reflective and configured ones included |

This is the working core, not the whole catalogue: the second edition's other moves — Combine Functions into Class, Replace Primitive with Object, Hide Delegate ↔ Remove Middle Man, Preserve Whole Object, Remove Flag Argument, Introduce Special Case, the Pull Up and Push Down moves, Replace Function with Command and the rest — follow the same method under their own names.

`(basis: Fowler, *Refactoring*, 2nd ed., 2018 — the move names and their grouping, and chapter 3 for the situations that call for each; the conditions in the last column are derived from what each move changes, not quoted from the book's mechanics)`

## What the catalogue doesn't decide

When a structure is bad enough to refactor is left to judgment on purpose: the authors give no metric — "no set of metrics rivals informed human intuition" — so no length, count or complexity number here triggers a move. The engineering standards for functions, names, abstraction and data describe the shape to move toward, and the work in hand bounds how far to go.

`(basis: Fowler and Beck, *Refactoring*, 2nd ed., chapter 3)`
