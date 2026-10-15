Pin down what is being mapped, onto what, and where the map lives, before reading any tool.

## The port

`--port` names it: one of vcs, ci, knowledge, artifacts, project-mgmt, communication or telemetry. Refuse the workspace port, and any name that isn't a port. The workspace port's guarantees keep a task off shared infrastructure, and only running things could show them kept. `(basis: derived — mapping is read-only)`

Read the port's SKILL.md for three things:

- its operations, from step 2;
- its outcomes, from step 4 and the taxonomy it links;
- its **Guarantees** section.

Those are what the map answers to.

## The provider, its transport and its entry

The provider is `--provider` if given, else the one the port's slot names (`tools.<port>.provider`). For knowledge and artifacts, transport and credentials live on each source or audience space. `--entry` names the source or space to read them from; without it, use the first entry whose provider this is. The map is keyed by the provider, never by the entry's name, so every entry with that provider shares one map.

Read the transport, `secret_ref` and `adapter` from the entry, else from the slot:

- `mcp` — a connector in this session whose name is the provider's, ignoring case, hyphens and underscores;
- `cli` — a command-line tool on the path by the provider's name, or the one the slot's `command` names;
- `api` — an HTTP interface, reached with the `secret_ref`.

If nothing fits, the result is `unavailable`, naming what is missing. If several connectors fit, it is also `unavailable`, naming them, so the user can set the one they mean.

## Where the map lives

The map's path is `${CLAUDE_PLUGIN_DATA}/adapters/<port>/<provider>.md`, with the provider's name lowercased and every character outside `a-z0-9-` made a hyphen.

- When the data folder doesn't resolve, the result is `unavailable`. Nothing is written anywhere else.
- The map is per user and never versioned.
- One file holds one section per transport, since the same provider over another transport offers other calls.

`(basis: maintainer, 2026-10-13)`

## When the base run stops here

These apply to learning only. `--show` and `--forget` use the resolution above and skip them.

- **A dedicated adapter exists** for the provider and the slot or entry doesn't set `"adapter": "learned"`. Say so and stop: the adapter governs.
- **A section for this transport already exists.** This is a relearn: see [relearn](../modules/relearn.md).

The output is the port's operations, outcomes and guarantees, the provider, transport and entry, and the map's path, for [read-the-surface](02-read-the-surface.md).
