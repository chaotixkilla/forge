# Run code in the task's workspace

Running the project's tooling on the host behind the workspace's back uses whatever language versions the machine happens to have, reaches the shared servers' defaults instead of the task's own data, and collides with another task running beside it; a migration run that way lands on someone else's database.

## Run through the workspace

Whatever the project's tooling runs goes through the [workspace](../../skills/workspace/SKILL.md) capability, which says what runs there and what stays where the session is. `(basis: maintainer, 2026-10-13)`

- **Recipe or bare command.** Use the recipe for the purpose when there is one, formatters counting as lint, with any narrowing — one file, a filter — as its arguments; otherwise a bare command from the service's root folder. Tell the workspace when a run installs or changes dependencies. A scratch file lives in the task's worktree, where the service can see it.
- **Services.** A long-running process is a service: start every app and worker the work passes through via the workspace, and reach them only on the ports it returns, never the project's documented defaults; a request seen going to a default port is an environment fault: the step stops and reports it. Nothing interactive runs there; a scratch script stands in for a console.
- **Which task.** Inside an act, the key is the open task's, from this session's act marker. With no marker for this session, the step is on its own: its key is `adhoc-<the step's name>-<the session id's first 8 characters>`, it works in the current checkout, and it tears that environment down when it finishes, its report first quoting what it needs from the saved output.
- **A baseline** of the code before the change, once the task's worktree holds the change, runs in a detached worktree at the change's base, under `<key>-baseline`, its namespace made and set up from the baseline worktree, then given the same data by replaying the steps that loaded the task's — never by copying the task's namespace, whose schema may hold the change — and torn down once read. Data a reproduction needs goes into the task's own namespace; reading it from the shared server to copy it there is fine, since only changing shared data is ruled out.

## Read what came back

- **A result.** The command ran; its exit status is the result, a failure of the code under test included. A `migrate-` run's duration is kept with the step's result, as the [documentation-kit](../writing/documentation-kit.md)'s migration timing.
- **Not run.** Unavailable, not found, unsupported by the setup, permanent: report the run as not run and why, never as the code's result; never rewrite the command to get past it, and never run it on the host instead — a result from the wrong environment is no result. A retryable fault is retried once, then treated as unavailable. Partial: use what was made, and report the rest.
- **Refused.** Never route around a refusal, by a bare command or otherwise: it guards shared data.
- **A git hook** that fails because the host lacks the project's dependencies is reported as that, never bypassed.
- **Host mode** is the exception to never running on the host: the workspace's results say it runs there. A run goes ahead as the user would run it; a service the workspace can't start is started the way the project documents, unless that start is the dev stack's own definition, which is the user's and is reported instead. A migration or seed — a command whose purpose is to change the schema or the data — is withheld and reported, since it would land on the shared default. Note it once per task.

## Get the task its own instance before a server-wide change

Before applying a change that alters a server for everyone using it, get the task its own instance of that server, or its own full stack, through the workspace, and apply the change there; the workspace's table names the cases. The discriminator: a change confined to the task's own database, prefix or bucket is not server-wide, whatever tool makes it; one that changes the server itself is — a migration that creates a role or another object outside any one database included. When the workspace can't give an instance or stack in its setup, don't apply the change: report that it needs one. `(basis: maintainer, 2026-10-14)`
