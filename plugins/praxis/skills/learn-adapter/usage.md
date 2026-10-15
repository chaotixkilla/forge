# learn-adapter — usage

## When to use

- A port reports that it has no adapter for your provider, and you have that tool connected: a connector in this session, or its command-line tool on the path.
- You want to see what praxis learned about a tool (`--show`), map it again after the tool changed (`--relearn`), or drop the map (`--forget`).

Ports call this skill on their own at first contact, so you rarely need to run it to start.

## When not to use

- The provider has an adapter in praxis: the port uses it. Set the slot's `adapter` to `learned` only to force the learned route.
- The workspace port: its guarantees protect shared infrastructure and can't be shown kept without running things, so it never takes a learned map.

## Examples

- `learn-adapter --port=project-mgmt` — maps the tracker the project-management slot names, from the connector you have connected, and writes your map.
- `learn-adapter --port=vcs --show` — lists each version-control operation, the call it maps to, and each guarantee's verdict.
- `learn-adapter --port=knowledge --provider=wiki --dry-run` — shows the map it would write for that source, writing nothing.
- `learn-adapter --port=vcs --forget` — deletes the map; the next version-control call learns again.

## Gotchas

- **The first write through each operation asks.** A learned operation that changes something shows exactly what it will send and asks you once; after it succeeds it doesn't ask again. A run with no one to answer refuses it.
- **`unsupported` is a safeguard.** An operation answers it when the tool can't be shown to keep one of the port's guarantees, such as never force-pushing. Wait for a dedicated adapter, or use the operation by hand.
- **Maps are per user.** They live in your plugin data folder, not the repository, and go away when the plugin is uninstalled; they're relearned at the next call.
