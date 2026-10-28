# Ask while the user is here

Users step away soon after they start a run. A question asked halfway through a long one can wait hours for an answer that never comes, and the run stalls with nothing to show. So ask everything at the start, then finish on best judgment.

## Who can answer

A run can't ask when it runs in the background, watches, or is called by another skill, and otherwise asks. `(basis: maintainer, 2026-10-19 — a session can't tell on its own that no one is watching, so only these cases count)`

## How a question is put

- **Each item's default comes first, labelled `(default)`.** It is the cautious side of the item: holding, keeping, running without, or leaving open. An item that chooses between readings of the work, such as two readings of the request or a design choice left open, has no such side: its default is the reading the procedure names as the one the run would take. (basis: maintainer, 2026-10-20 — the named reading rather than stopping, recorded as a default the owner can reverse) A procedure may make a recommended answer that isn't the cautious side its default while someone answers in the conversation, and says so. (basis: maintainer, 2026-10-19)
- **Some answers are never taken by default.** Approving a heavyweight run's cost; delivering anyway before the record is filed; confirming a first write through a learned map; retiring a moved task's documentation; declining or deferring a review comment. An item offering one of these defaults to its cautious side, and a first write through a learned map is refused, as [dispatch-through-a-learned-map](../../learn-adapter/rules/dispatch-through-a-learned-map.md) says. Three items stop a run that can't ask: another session's act marker ([open-the-task](../../work/phases/02-open-the-task.md)); a heavyweight flag a run asks about on its own, with no caller's question to fold it into ([ask-before-a-heavyweight-run](ask-before-a-heavyweight-run.md)); and a review comment a rework would decline or defer ([run-the-act](../../work/phases/03-run-the-act.md)). (basis: maintainer, 2026-10-19)
- **A reply that names no choice** for an item leaves it to its default. A reply that names none for any item, such as a bare "go ahead", leaves every item to its default. (basis: maintainer, 2026-10-19)
- **A default is recorded as one.** Every item that took its default goes into the run's record as taken by default, with the reason: the reply's own words when it gives a reason, "the answer named no choice for it" when someone answered without one, or "no one to answer". It is never recorded as the owner's choice. (basis: maintainer, 2026-10-19 — a default taken silently reads later as a decision someone made)

## At the start

Before any long work, ask every question the run needs answered, in one message: the cost question for a heavyweight flag ([ask-before-a-heavyweight-run](ask-before-a-heavyweight-run.md)), an ambiguity in the ask, a missing input. After that, ask nothing.

## After that

- **Decide and record.** A question that comes up mid-run is settled on best judgment: decide, note the assumption in the report with what would change if it's wrong, and carry on. The cost question is the one worth stopping for; a mid-run clarification isn't.
- **Keep a checklist.** For a run with several parts, list them at the start with the condition that means done, and update the list as each part ends.
- **Don't stop on a progress update.** A turn that reports progress while parts remain hasn't finished: carry on to the completion condition, or stop only where the procedure says to.
- **Background and watch runs never ask.** They decide and record instead.
- **The named exceptions.** A mid-run question is asked only where a procedure names it as an exception to this rule, and only in an interactive run, where someone can answer at once. Otherwise it takes its cautious default.
- **A called skill is mid-run.** A skill another skill invokes asks nothing, even at its own first step: its caller's opening question carries what it needs, the cost question included ([ask-before-a-heavyweight-run](ask-before-a-heavyweight-run.md)). Anything else it decides and records, except where its procedure has a path for when no one can be asked: there it takes that path. One exception asks mid-run whenever the user is present: the confirmation a first write through a learned map needs ([dispatch-through-a-learned-map](../../learn-adapter/rules/dispatch-through-a-learned-map.md)), since nothing else makes that write safe.

(basis: after observed security-review practice, where users step away within about a minute; Anthropic's guidance on long turns ending early on progress updates; maintainer, 2026-09-30)
