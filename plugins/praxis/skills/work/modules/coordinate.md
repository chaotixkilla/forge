# coordinate (`--coordinate`)

Activated by `--coordinate`, or by a yes to [offer-to-coordinate](../rules/offer-to-coordinate.md), referenced from there.

Under this module this session builds none of the round's units: worker sessions build them, each running [worker](worker.md). It is the round's only filer. Messages go through [sessions](../../sessions/SKILL.md). A piece that can't go on is reported to the user; work isn't moved between workers mid-round. (basis: maintainer, 2026-11-19, rebalancing left out of scope)

Every worker runs on this machine, in a worktree of this repository, so its branch merges here. A resumed coordinator never builds a unit, and sends each worker the task, its worker number and the previous address with its own.

## Split the ownership

Number the pieces 1 to N in the round's unit order; piece n is `worker-<n>`, its working task key `<key>-w<n>`. Before any prompt goes out, commit on the task branch, for each file more than one piece changes:
- **An ordered list or table,** where the order changes what the project does: one placeholder line per unit that adds entries, in the file's comment syntax, `reserved <key> <unit id>`, where the list's own order puts that unit's entries, else at its end in unit order. A worker replaces only its own units' placeholders; any other change is asked for.
- **A file each piece only appends to:** for each worker, an empty block between the lines `begin <key> worker-<n>` and `end <key> worker-<n>`, in the file's comment syntax, at the place the file takes additions, in worker order. A worker writes only inside its own. A file with no comment syntax, or no such place, is an ordered list.

Then run every worker's test routine (below) on the task branch: this is the first passing run each merge is measured against, and a test failing here is noted as failing before the round and never sends a merge back.

Write the split, each worker's units, files and blocks, into the round's brief.

## Hand out the prompts

Learn this session's address through sessions, by the name `coordinator`. Give the user one prompt per worker, each ready to paste into a new session in this repository on this machine:

> You're worker-&lt;n&gt; on praxis task &lt;key&gt;, coordinated by &lt;address&gt; over &lt;transport&gt;. Run praxis work with `--task=<key>-w<n> --worker-of=<address>`, and use that transport. Report in and wait for a brief.

A worker that says it can't reach the transport is given its prompt again over the transport that needs nothing installed. Tell the user the round now uses about N+1 sessions' usage.

## Brief each worker as it checks in

A check-in names its `worker-<n>`. Cut its branch `<task branch>-w<n>` at the task branch's local head, make its worktree on that branch through [workspace](../../workspace/SKILL.md) by its working task key, and send its brief:
- its worktree, branch and working task key;
- its units by id, with the parts of the round's brief they need;
- its blocks and placeholders;
- the test routine: the test commands the plan or the project's CI names for its units' areas, else the commands its first commit report names its test step ran;
- the project's commit rule.

## While they work

- **Answer** a worker's question from the round's brief. One the brief doesn't settle goes to the user, as run-the-act allows. Each answer is a finding of the round, filed with the next filing.
- **File** each result a worker reports as the round's, through document, as it arrives, under its step and unit, labelled with the worker, and record the step's outcome on this session's marker. A unit is `done` once its last commit is merged and its checks pass.
- **Merge** each reported commit: merge the worker's branch at that commit into the task branch, a merge commit naming the worker and unit, then check, in this order:
  - **Names.** In each code file the merge changes, its top-level names, the functions, classes, variables and constants, against the names the task branch defines where the language resolves them together: the file, or the files sharing one namespace. A name defined twice, the second not said by the brief or its unit to replace the first, returns the task branch to before the merge and goes back to the worker whose commit merged later, to rename. Worker names never carry a worker's mark into the product's code. (basis: maintainer, 2026-11-19, prefixes refused in delivered code)
  - **Tests.** Every worker's test routine, by its commands, not as a step. A test that passed on the task branch's last passing run and fails now returns the task branch to before the merge and sends the worker the failure. A filed result this contradicts is corrected in the next filing.
  - A conflict inside a block or placeholder is that block's owner's to fix; send it back. Any other conflict is resolved here and filed as a finding.
- **Once a merge's checks pass,** tell every worker to rebase onto the task branch before its next commit.

## Close out once

When every worker has said its units are done and its last commit is merged:
- remove every block's begin and end lines, and any placeholder left, in one commit;
- run the act's steps that follow its per-unit ones, and [close-out](../phases/04-close-out.md) once, delivering the round as one review request from the task branch, its units listed in unit order (basis: maintainer, 2026-11-19, one request, since units built in parallel merge interleaved);
- file who built which unit and each merge with its commit, in the round's task history;
- tell each worker the round is closed and its session can end; then, through workspace, with the task branch as the integration line, tear each worker's environment down and remove its worktree; delete its merged `-w<n>` branch; remove its act marker and runs folder; and clear the round's messages through sessions.
