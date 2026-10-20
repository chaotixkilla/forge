# Seed the feedback loop

Every plugin anvil builds carries a developer mode. Its maintainer turns it on, and then each run ends by writing down what the plugin cost that run, in the shape [revise](../../revise/SKILL.md) reads with `--from`. The session that hit the friction knows most about it, and without the loop that knowledge leaves with the session. `(basis: maintainer, 2026-10-20)`

## The switch

The switch is the environment variable `<PLUGIN>_DEVELOPER`: the plugin's name uppercased, with every character outside `A-Z0-9` made an underscore, so `p2p-kit` reads `P2P_KIT_DEVELOPER`. A non-empty value turns it on. It is the same for a config-bearing plugin, since a config's path is fixed only once its setup skill is codified, and a hook written at birth can't know it. `(basis: derived — the one switch a birth-time hook can read for certain)`

The switch's name goes in new-plugin's hand-off report and nowhere a user reads: not the README, the usage docs or a config schema.

## What the shell gets

- **A SessionStart hook,** `hooks/developer-mode.py`, bound in `hooks/hooks.json` as [add-component](../../add-component/SKILL.md)'s hook wiring binds one, its command running `hooks/developer-mode.py` under `${CLAUDE_PLUGIN_ROOT}`, as add-component's hook wiring writes a handler's command. It is the one hook every plugin is born with, an exception to leaving `hooks/` empty until earned ([plugin-shell-conventions](plugin-shell-conventions.md)).
  - **Switch on:** it adds one line to the session's context: developer mode is on, so close each run with feedback as the plugin's feedback standard says, giving that standard's absolute path: `${CLAUDE_PLUGIN_ROOT}` resolved, else the hook file's own plugin folder.
  - **Switch off:** it says nothing.
  - **On any error:** it exits 0 and adds nothing. It never blocks.

## The feedback standard

It is born with the shell, at `craft/upkeep/feedback-on-<plugin>.md`, whatever the number of skills. That makes it the one exception to the craft library being earned ([choosing-slots](../../scaffold-skill/rules/choosing-slots.md)), since every skill a user can invoke cites it, the config-setup skill included. The hook names it at that path. It says:

- **When.** When a run that a user invoked ends, after its report, asking nothing. That includes a run the user stops partway, which writes at the stop. A skill run by another skill writes nothing of its own, since its caller's ending covers the run. A preview run, such as a dry run, writes nothing.
- **What counts.** A place where the plugin had what it needed to do the work right the first time, and didn't. These, and nothing else:
  - the user corrected or redirected what it did or proposed;
  - the user stopped the run, or dropped part of it, with a reason;
  - a part broke down, or a check looped past its bound;
  - a hook blocked an action the procedure called for or the user had approved;
  - the user didn't understand a question, or answered outside the choices it offered;
  - the procedure left two readings, and the run had to pick one;
  - following a rule to the letter gave an outcome the user then corrected or undid.

  Each counts only when its cause lay in the plugin: not a change of the user's own mind, not an answer to a choice the plugin offered, and not a hook from outside the plugin. Nothing that went well is recorded. A run with no finding writes no file and adds no line.
- **Each finding.**
  - its defect, in a line;
  - a pointer, by path inside the plugin;
  - its evidence, from what this session saw;
  - a route, the engine likely to own the fix: codify for a procedure's wording, add-component for a new rule or component or a hook's body;
  - a grade: **blocker** when a part broke down or the run reached a wrong result, **friction** when it cost the user a correction, a repeat, a stop or a wait, **nit** otherwise. revise may regrade it on its own ladder. `(basis: derived from what the user paid, the one cost a session can see)`

  Two findings with one cause in this run are one entry.
- **Nothing from the user's work.** Names, keys, paths outside the plugin, code and quoted text are left out, or told by their kind. The test: the file could be handed to the plugin's maintainer from any project.
- **Where.** `${CLAUDE_PLUGIN_DATA}/feedback/<YYYY-MM-DD>-<n>.md`, with `<n>` the next free number that day, headed by the plugin's version and what ran. One line follows the report, `Feedback on <plugin>: <count> findings → <path>`. When the data folder isn't set or can't be written, the findings are shown after the report instead, and that line says nothing was written. Nothing is sent anywhere, and the plugin's own files are never edited.

## Where it is cited

Every skill a user can invoke cites the standard at the point its run ends. That is its last phase, or, for a skill with no phases, a line in its SKILL.md body outside the numbered procedure. The citation reads: in developer mode, close with feedback, followed by the link. [scaffold-skill](../../scaffold-skill/SKILL.md) seeds it.
