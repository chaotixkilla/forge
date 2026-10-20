# Feedback on praxis

With developer mode on, each close-out records what praxis itself cost this run. The session that hit the friction knows most about it, and without this, what it knows leaves with the session. The output is in the shape praxis's maintainer feeds to its revision. (basis: maintainer, 2026-10-20)

## When

Developer mode is on when `.claude/praxis.json` sets `"developer": true`, which the session's start states. It runs after close-out's report, asking nothing. When an act stops before close-out, at the user's stop or at a question a run that can't ask reports, it runs at the stop instead. A `--dry-run` writes none. It is never offered, explained or suggested to a user who hasn't set it.

## What counts

A finding is a place where praxis had what it needed to do the work right the first time, and didn't. These, and nothing else, drawn from what this session saw:

- the user corrected or redirected what praxis did or proposed;
- the user stopped the act or dropped a step, with a reason;
- a step broke down, or a check looped past its bound;
- a hook blocked an action the procedure called for or the user had approved;
- the user didn't understand a question, or answered outside the choices it offered;
- praxis's procedure left two readings, and the run had to pick one;
- following a rule to the letter gave an outcome the user then corrected or undid.

Each counts only when its cause lay in praxis: not a change of the user's own mind, not an answer to a choice praxis offered, and not a hook from outside praxis. What went well isn't recorded. A run with no finding writes no file and adds no line.

## How each finding is written

One entry per finding:

- **Defect:** what praxis did wrong, in one line.
- **Pointer:** the praxis file and section it lives in, by its path inside the plugin.
- **Evidence:** what happened in this run, in plain terms.
- **Route:** the engine likely to own the fix: codify for a procedure's wording, add-component for a new rule or component or a hook's body.
- **Grade:**
  - **blocker** when a step broke down or the run reached a wrong result;
  - **friction** when it cost the user a correction, a repeat, a stop or a wait;
  - **nit** otherwise.

  The revision may regrade a finding on its own ladder.

Two findings with one cause in this run are one entry, with the evidence of both.

**Nothing from the project.** An entry holds no repository, organization or people's names, no ticket keys, no file paths outside praxis, and no code or quoted text from the project. The user's words are paraphrased into what they asked of praxis. A finding that can't be told without the project's specifics is told by its kind, such as "a stacked change of three requests", or left out. The test: the file could be handed to praxis's maintainer from any project.

## Where it goes

Write it to `${CLAUDE_PLUGIN_DATA}/feedback/<YYYY-MM-DD>-<n>.md`, with `<n>` the next free number that day, headed with praxis's version, the act and the round's kind. One line follows the report: `Feedback on praxis: <count> findings → <path>`. When the data folder isn't set or can't be written, the findings are shown after the report instead, and the line says nothing was written. Nothing is sent anywhere, and praxis's own files are never edited.
