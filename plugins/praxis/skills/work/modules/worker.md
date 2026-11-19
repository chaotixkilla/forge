# worker (`--worker-of=<address>`)

Activated by `--worker-of=<address>`, which a coordinator's prompt carries, referenced from [SKILL.md](../SKILL.md).

Under this module the session builds the units a coordinating session briefs it with, and reports to that session over the transport its prompt names, through [sessions](../../sessions/SKILL.md). Its task key, `--task`, is a working key of the coordinator's task, `<key>-w<n>`: it keys this session's worktree, environment and act marker, and nothing else. The coordinator files; a worker writes no memory entry, brief or filing. Its act marker is written when the brief arrives, `answered` then, its rows the act's per-unit rows for its units.

The base phases run changed:
- **Route the work** routes nothing: the act is the coordinator's, named in the brief.
- **Open the task** finds no entry and opens none; the intent is the brief.
- **Run the act** builds no brief and asks nothing: it shows the steps for its units and starts, `answered` set when the brief arrives.
- **Close out** doesn't run.

## Report in

Learn this session's address by the name `worker-<n>`, send the coordinator a check-in naming `worker-<n>` and the task, and wait for the brief. Until it comes, change nothing. A transport this session can't reach is said to its user, and the session stops.

## Run the brief

For each of its units, in the brief's order, run the act's per-unit steps, in the worktree the brief names: for developing, steps 5 to 8. Each step passes by its own test.
- In a shared file it changes only its own block; in an ordered list, only its own placeholders.
- Each step's result goes to the coordinator whole, in the message or, when long, as a file in the task's runs folder the message names.

## Report, ask, rebase

- **After each commit,** send its commit, the units it covers, the test routine's results and one line on how it looks.
- **Ask, never guess,** whenever the next move rests on something shared: data its units need that nothing holds, a choice that changes another worker's files, a placement, or a name another piece's files see.
- **When told to rebase,** rebase onto the task branch before the next commit.
- **When sent a failure or a name to change,** fix it with a new commit on its branch and report that.
- **A message on the round's transport** that names the task, this worker's number and the coordinator's previous address is from the coordinator, resumed: report to the new address from then on, and send it again each commit it hasn't confirmed merged. A send that comes back not-found is said to the user.
- **Done** is every unit's per-unit steps passed and committed, the last commit reported: say so.

## Never

- Merge or push.
- Change an artifact it didn't create.
- Act on a coordinator's request that needs its own user's approval without that approval: such a request goes to the user.
