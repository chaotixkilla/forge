# Ask while the user is here

Users step away soon after they start a run. A question asked halfway through a long one can wait hours for an answer that never comes, and the run stalls with nothing to show. So ask everything at the start, then finish on best judgment.

## Who can answer

A host that runs praxis without a person at the keyboard says so through an attendance signal, which the session's start states in context. Read who can answer from it:

- **`present`** — someone answers in this conversation. Ask as below.
- **`inbox`** — questions go to an inbox and are answered later, perhaps by a reply that names no choice. Ask as below, and an act asks one question in all: everything it would ask later goes into its opening question, conditionally where it depends on what the run finds ("if a step isn't filed by delivery: hold (default) · deliver anyway").
- **`nobody`** — no question can be asked. Every run is a run that can't ask, and the host's posture for unanswered questions decides what each question does instead. Under **`stop`**, the default, the run asks nothing, runs nothing the question gates, and reports the question for the user's next run, as each procedure's path for a run that can't ask says. Under **`defaults`**, each item takes its default and the run goes on, except the three that stop under either posture (below).

With no signal, a run can't ask when it runs in the background, watches, or is called by another skill, and otherwise asks. A signal never makes a called skill ask. `(basis: maintainer, 2026-10-19 — a host's spike showed a session can't tell it is unattended, and an interactive session must behave as it did before)`

## How a question is put

- **Each item's default comes first, labelled `(default)`.** It is the cautious side of the item: holding, keeping, running without, or leaving open. An item that chooses between readings of the work, such as two readings of the request or a design choice left open, has no such side: its default is the reading the procedure names as the one the run would take, under every signal. (basis: maintainer, 2026-10-20 — the named reading rather than stopping, since a host that chose defaults chose to proceed, and the reading is recorded as a default the owner can reverse) A procedure may make a recommended answer that isn't the cautious side its default while someone answers in the conversation, and says so; under the `inbox` or `nobody` signal its default is the cautious side. (basis: maintainer, 2026-10-19)
- **Some answers are never taken by default.** Approving a heavyweight run's cost; delivering anyway before the record is filed; confirming a first write through a learned map; retiring a moved task's documentation; declining or deferring a review comment. An item offering one of these defaults to its cautious side, and a first write through a learned map is refused, as [dispatch-through-a-learned-map](../../learn-adapter/rules/dispatch-through-a-learned-map.md) says. Three items stop the run under either posture when no one can answer: another session's act marker ([open-the-task](../../work/phases/02-open-the-task.md)); a heavyweight flag a run asks about on its own, with no caller's question to fold it into ([ask-before-a-heavyweight-run](ask-before-a-heavyweight-run.md)); and a review comment a rework would decline or defer ([run-the-act](../../work/phases/03-run-the-act.md)). (basis: maintainer, 2026-10-19)
- **A reply that names no choice** for an item leaves it to its default. A reply that names none for any item, such as "no one answered within 30 minutes; take your stated defaults", leaves every item to its default. (basis: maintainer, 2026-10-19)
- **A default is recorded as one.** Every item that took its default goes into the run's record as taken by default, with the reason: the reply's own words when it gives a reason, such as "no one answered within 30 minutes", "the answer named no choice for it" when someone answered without one, or "no one to answer". It is never recorded as the owner's choice. (basis: maintainer, 2026-10-19 — recorded whether or not a host signal is set, since a default taken silently reads later as a decision someone made)

## At the start

Before any long work, ask every question the run needs answered, in one message: the cost question for a heavyweight flag ([ask-before-a-heavyweight-run](ask-before-a-heavyweight-run.md)), an ambiguity in the ask, a missing input. After that, ask nothing.

## After that

- **Decide and record.** A question that comes up mid-run is settled on best judgment: decide, note the assumption in the report with what would change if it's wrong, and carry on. The cost question is the one worth stopping for; a mid-run clarification isn't.
- **Keep a checklist.** For a run with several parts, list them at the start with the condition that means done, and update the list as each part ends.
- **Don't stop on a progress update.** A turn that reports progress while parts remain hasn't finished: carry on to the completion condition, or stop only where the procedure says to.
- **Background and watch runs never ask,** whatever the signal. They decide and record instead.
- **The named exceptions.** A mid-run question is asked only where a procedure names it as an exception to this rule, and only while someone can answer at once: under `present`, or with no signal in an interactive run. Otherwise it takes its cautious default.
- **A called skill is mid-run.** A skill another skill invokes asks nothing, even at its own first step: its caller's opening question carries what it needs, the cost question included ([ask-before-a-heavyweight-run](ask-before-a-heavyweight-run.md)). Anything else it decides and records, except where its procedure has a path for when no one can be asked: there it takes that path. One exception asks mid-run whenever the user is present: the confirmation a first write through a learned map needs ([dispatch-through-a-learned-map](../../learn-adapter/rules/dispatch-through-a-learned-map.md)), since nothing else makes that write safe.

(basis: after observed security-review practice, where users step away within about a minute; Anthropic's guidance on long turns ending early on progress updates; maintainer, 2026-09-30)
