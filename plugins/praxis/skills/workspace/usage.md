# workspace — usage

A tool-layer interface skill: the single place praxis decides where a task's work happens. It fronts the `workspace` capability, so an act or step names what it needs (a worktree for the task, a command run in the task's environment, a service started for it) and this skill resolves it to the configured container runtime, or to the host.

## When to use
- An act gives a task its worktree, or tears it down at close-out.
- A step runs the project's code: tests, linters, scratch scripts, dependency installs, migrations, a service.
- A task needs its own database, bucket or key prefix on a shared server, or its own instance of a service.

## Not for / use instead
- git operations on the code host (push, review requests) → **vcs**.
- The hosted pipeline → **ci**.
- Deciding what to run, or whether a result is good → the calling step.

## Gotchas
- **It degrades, never blocks.** With no `tools.workspace`, work runs in place on the host; a task loses isolation, not its ability to run. Every result says where it ran.
- **Host mode isolates nothing.** On the host the project's code reaches whatever its own environment points at; praxis refuses only the recipes it knows reach a shared database.
- **Containers are the default, not a fallback.** With a container setup configured and the runtime down, an operation is *unavailable*, never silently run on the host's language versions.
- **A task's environment is its own.** It runs beside the user's dev stack, reaches its shared servers through its own namespaces, and gets its own instance where a change is server-wide; the dev stack itself is never started, stopped or changed.
- **Stop keeps, teardown removes.** Stopping an idle task's environment keeps its data; teardown at close-out removes everything made for the task.

## Example

    workspace — make a task's worktree: task PROJ-88, branch feat/proj-88-export, base main
    workspace — run a command: task PROJ-88, recipe test-api
    workspace — give a task its namespace: task PROJ-88, service db
    workspace — tear a task's environment down: task PROJ-88
