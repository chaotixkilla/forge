# forge

A [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin marketplace.

| plugin | what it is |
|---|---|
| **anvil** | An authoring kit for building Claude Code plugins — skills that scaffold, codify, audit, and release other plugins. Self-contained and config-less. |
| **praxis** | Codifies engineering/SDLC processes — spec, plan, review, and more — as skills and subagents. Configured per project on first run. |

## Install

Add the marketplace, then install the plugins you want:

```
/plugin marketplace add chaotixkilla/forge
/plugin install anvil@forge
/plugin install praxis@forge
```

praxis is configured per project — on first use its `init` skill guides you through a
`.claude/praxis.json` for your repo's tools (version control, CI, trackers, and so on).

## Develop / load locally

Clone the repo and load a plugin's directory directly, without installing:

```
git clone https://github.com/chaotixkilla/forge.git
claude --plugin-dir ./forge/plugins/anvil
claude --plugin-dir ./forge/plugins/praxis
```

Validate a plugin's manifest and structure:

```
claude plugin validate ./forge/plugins/anvil
claude plugin validate ./forge/plugins/praxis
```

## Layout

```
forge/
├── .claude-plugin/
│   └── marketplace.json      # the catalog — lists anvil and praxis
└── plugins/
    ├── anvil/                # the authoring kit
    │   └── .claude-plugin/plugin.json
    └── praxis/               # the SDLC plugin
        └── .claude-plugin/plugin.json
```

Each plugin is self-contained under `plugins/<name>/`; installing one copies only that directory.

## License

[MIT](LICENSE) © Sergio Salgado
