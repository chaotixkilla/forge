# Notify on completion — `--notify`

On completion of a detached run, signal the invoker that the research has finished. Activated from [compose-output](../phases/06-compose-output.md) (the completion point).

1. **The signal is an ambient completion ping to the invoker.** `--notify` tells the *person who launched the run* that it is done — it is the harness's own background-completion notification, carrying no backend, no adapter, and no port delegation. deep-research stays config-less. (basis: ratified by the maintainer, 2026-07-13 — `--notify` here signals the invoker that a detached run completed, an ambient-harness completion signal, distinct from a team-facing announcement over the communication capability the way `communicate`'s `--notify` delegates to the communication port. The target is the invoker, not an audience; team-facing delivery is `--publish`'s job.)
2. **It presumes a detached run.** A foreground run is already watched, so a completion signal is redundant; `--notify` is meaningful paired with `--background` ([background-run](background-run.md)). On its own it is a no-op, stated as such rather than silently ignored.
