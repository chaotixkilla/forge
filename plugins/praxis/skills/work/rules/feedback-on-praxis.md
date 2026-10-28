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

Each counts only when its cause lay in praxis: not a change of the user's own mind, not an answer to a choice praxis offered, and not a hook from outside praxis.

Before writing, hold each of the user's turns since the act opened against this list, so none is missed because the run had moved on. (basis: maintainer, 2026-10-28 — the user's corrections were the strongest evidence, and runs caught them only when they happened to notice)

A run with no finding still writes its file: the header, then `clean`, so runs without friction are counted beside those with it. (basis: maintainer, 2026-10-28 — with defects alone, nothing shows a change is holding)

## How each finding is written

One entry per finding, numbered from 1 in the order written:

- **Defect:** what praxis did wrong, in one line.
- **Pointer:** the praxis file and section it lives in, by its path inside the plugin.
- **Evidence:** what happened in this run, in plain terms.
- **Cause:** `procedure` when following the pointed-to text as written leads there; `misreading` when that text says otherwise and the run read it wrong. A misreading is graded nit, unless the ladder makes it a blocker. One that a report under this praxis version already records (Seen before, below) is the wording's: then it is `procedure`, graded by the ladder.
- **Cost:** what it cost this run, counted: the user's answers or corrections it took, steps run again, results filed again, turns spent getting past it; `none counted` when there was nothing to count.
- **Route:** the engine likely to own the fix: codify for a procedure's wording, add-component for a new rule or component or a hook's body.
- **Grade:**
  - **blocker** when a step broke down or the run reached a wrong result;
  - **friction** when it cost the user a correction, a repeat, a stop or a wait;
  - **nit** otherwise.

  A `misreading` is capped at nit short of a blocker (Cause, above). The revision may regrade a finding on its own ladder.

Two findings with one cause in this run are one entry, with the evidence of both.

**Seen before.** Before writing, read the Defect and Pointer lines of the reports already in the feedback folder written under this praxis version. A finding with the same pointer that the same change to the pointed-to text would fix is written short: its Defect, `Seen before: <file> #<n>` naming the first report that recorded it (a short entry's own Seen before is followed back to it), and this run's Evidence, Cause, Cost and Grade. A report under another version isn't matched, since a release may have changed what it points at. (basis: maintainer, 2026-10-28 — one defect was written up thirteen times, each run unaware of the others)

**Nothing from the project.** An entry holds no repository, organization or people's names, no ticket keys, no file paths outside praxis, and no code or quoted text from the project. The user's words are paraphrased into what they asked of praxis. A finding that can't be told without the project's specifics is told by its kind, such as "a stacked change of three requests", or left out. The test: the file could be handed to praxis's maintainer from any project.

## Where it goes

Write it to `${CLAUDE_PLUGIN_DATA}/feedback/<YYYY-MM-DD>-<n>.md`, with `<n>` the next free number that day, headed by one line, `praxis <version> · <act> · <round kind> · install <install> · harness <harness version>`: the version from the installed plugin's manifest, the install as the plugin root's path from its marketplace folder down, as `forge/praxis/0.11.1`, or `local` for a root outside the plugin cache, and the harness's version read from its own version command, or `unknown`. (basis: maintainer, 2026-10-28 — a defect in the harness reads like one in praxis without them) A report with findings is followed by one line: `Feedback on praxis: <count> findings → <path>`. When the data folder isn't set or can't be written, the findings are shown after the report instead, and the line says nothing was written. A clean run adds no line either way. Nothing is sent anywhere, and praxis's own files are never edited.
