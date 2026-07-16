# Route secrets to userConfig

A token written into `praxis.json` is a token committed to the repository — the one outcome init must never produce. The config file is shared, version-controlled project state; a credential belongs in per-user, keychain-backed storage the repo never sees. This rule pins how a secret is *pointed at* from the config without ever being *stored in* it, so the file stays safe to commit and the consuming skill can still find the credential at call time.

## The file holds a reference, never the value

`(basis: ratified by the maintainer, 2026-07-05. That secret_ref names a userConfig key — value in the plugin's keychain-backed userConfig, never in praxis.json — is the maintainer's ratified secret convention; it matches config-mechanism's "secrets go in the plugin's userConfig" and the adapters that already read "auth from the configured secret_ref.")`

- **`secret_ref` holds the *name of a userConfig key*, not the token.** Convention: the key is namespaced by capability — `vcs_token`, `knowledge_token`, `communication_token`, and so on for each slot that needs one. init writes only that name into the slot's `secret_ref`.
- **The value lives in the harness's userConfig** — the plugin's keychain-backed, per-user config, entered through the harness's secure prompt, never in a project file. (Declaring those `<cap>_token` keys in the plugin's `userConfig` schema is a plugin-manifest concern, downstream of init — see the handoff note below.)
- **The consuming adapter dereferences the name at call time**: it reads `secret_ref`, then reads that userConfig key's value — the harness exposes it as `${user_config.<cap>_token}` (and as the `CLAUDE_PLUGIN_OPTION_<CAP>_TOKEN` environment variable) — and authenticates with it. init's job ends at recording the name and telling the user where to put the value.

## Which slots need a secret at all — the transport discriminator

Not every configured slot needs a credential, and asking for one where none is used is the same interrogation failure [infer-before-asking](infer-before-asking.md) forbids. Decide by the slot's transport:

- **`api`** — always needs a credential; a raw API call authenticates per request. Set `secret_ref`.
- **`mcp`** — decide by *where the connector's auth lives*, which has three cases, not two:
  - **Already authorized at the harness level** (a connected MCP server, harness-held OAuth) — the harness holds the auth, praxis supplies nothing. Leave `secret_ref` **empty**.
  - **Harness-managed auth, not yet authorized** (a connector whose credentials the harness manages via its own OAuth/connect flow, which the user simply hasn't completed yet) — praxis *still* supplies nothing: the credential will live in the harness once the user connects, not in a userConfig key. Leave `secret_ref` **empty** and direct the user to authorize the connector through the harness (its `/mcp` / connector settings), **not** to a token. Writing a `secret_ref` here would point at a userConfig key that must stay empty — a **dead reference** the consuming adapter can never dereference. This is the branch the binary rule missed; it is *not* "not harness-authorized → set a ref."
  - **Static-token MCP** (a self-hosted or custom MCP server that authenticates with an API key praxis must provide, with no harness-managed flow) — this is the only mcp case that needs a stored credential. Set `secret_ref`.

  The discriminator: **does the connector's auth flow through the harness (managed/OAuth — whether or not connected yet), or does it need a static credential praxis hands it?** Only the latter sets `secret_ref`; a not-yet-connected harness-managed connector is an *authorize-it-in-the-harness* instruction, never a token.
- **`cli`** — reuses an already-authenticated command-line tool's ambient session; praxis supplies no token. Leave `secret_ref` empty.
- **`fs`** — a local filesystem path; no authentication. Leave `secret_ref` empty.

`(basis: derived from the transport semantics — api authenticates per-call, cli/fs reuse ambient or no auth, mcp depends on harness authorization; the boundary is a property of the transport, not a house choice.)`

**Prefer the transports that store nothing — `api` is the last resort.** Three of the four transports make praxis hold *no* credential: an already-authorized `mcp` connector (the harness holds the auth), an authenticated `cli` (ambient session), a local `fs` path (no auth). Only `api` forces a stored token. So `api` is the **last-resort** transport — chosen only when no MCP connector and no authenticated CLI is available for the provider — and [resolve-tools](../phases/02-resolve-tools.md) proposes it last, signalling that picking it means entering a token into userConfig. A slot reachable by an already-connected MCP server or an authenticated CLI *should* use that: it is lower-friction for the user and leaves praxis holding no secret at all. Steer the user there first; reach for `api` only when the no-secret paths genuinely aren't available.

## The instruction init hands the user

When a slot needs a credential, init does two concrete things and no more: it writes `secret_ref: "<cap>_token"` into the slot, and it tells the user to set that key's value in the harness userConfig (the plugin's secure per-user config), explicitly *not* in `praxis.json`. It never prompts for the token itself and never echoes one back. Under [dry-run](../modules/dry-run.md), even the "set it in userConfig" side effect is skipped — the run reports that the ref *would* be recorded, and stops. If you find a token being typed into the config, stop: that is the exact failure this rule exists to prevent.

**Handoff note (not init's job):** the seven `<cap>_token` keys (`vcs_token`, `ci_token`, `knowledge_token`, `artifacts_token`, `project_mgmt_token`, `communication_token`, `telemetry_token`) are declared in praxis's plugin `userConfig` schema, each `sensitive` — so the harness prompts securely and stores the value in the OS keychain, never in a project file. init relies on that declaration existing but does not own it: it records the `secret_ref` name into the slot and directs the user to fill the matching userConfig key. If a future capability ever needs a secret whose key isn't among those seven, adding it is a plugin-manifest follow-up, not init's to write.
