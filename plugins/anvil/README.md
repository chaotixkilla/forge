# anvil

> Build Claude Code plugins — scaffold, codify, audit, and release.

[![version](https://img.shields.io/github/v/tag/chaotixkilla/forge?filter=anvil-v*&sort=semver&label=version&color=1f6feb)](https://github.com/chaotixkilla/forge/releases?q=anvil)
[![license: MIT](https://img.shields.io/badge/license-MIT-3fb950)](https://github.com/chaotixkilla/forge/blob/main/LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-6E56CF)](https://docs.claude.com/en/docs/claude-code)

**anvil is a plugin that builds plugins.** Its skills turn a process into a real, runnable skill,
keep the skill layer honest with a set of audits, and ship the result to a marketplace — all from
inside Claude Code. It's self-contained, config-less, and self-hosting: anvil builds, audits, and
releases anvil.

## Install

```
/plugin marketplace add chaotixkilla/forge
/plugin install anvil@forge
```

## Skills

Plugin-level skills take `--plugin=<name>`; the rest act on the marketplace as a whole.

**Create**

| skill | what it does |
|---|---|
| `new-plugin` | birth a new plugin — config posture, shell, and skill-pool design |
| `scaffold-skill` | lay a new skill's slot skeleton (frontmatter + phases/rules) |
| `codify` | turn a process into a skill's runnable procedure (the content engine) |
| `add-component` | add an adapter, explorer, critic, rule, module, or hook |

**Audit**

| skill | what it does |
|---|---|
| `audit-tool-leaks` | scan the skill layer for concrete-tool leaks (the HARD RULE) |
| `audit-contract` | check frontmatter, slot, flag, and config conformance |
| `audit-context` | measure what skills cost to load, and whether the loads that matter happen |
| `audit-packaging` | enforce the ships-vs-authoring boundary across the marketplace |

**Ship & iterate**

| skill | what it does |
|---|---|
| `release` | publish a plugin to the catalog, gated by the three audits |
| `revise` | apply a batch of findings or feedback as the smallest verified change set |
| `dogfood` | run a plugin's own skills on itself to surface friction |

## Quick start

```
# design and scaffold a new plugin
/anvil:new-plugin

# turn a process into a skill, then flesh it out
/anvil:scaffold-skill --plugin=myplugin
/anvil:codify --plugin=myplugin

# keep it honest, then ship
/anvil:audit-contract --plugin=myplugin
/anvil:release --plugin=myplugin
```

## Under the hood

Skills recruit read-only **explorers** to gather facts (`plugin`, `authoritative-sources`,
`plugin-community-practices`) and **critics** to challenge the work before it lands (`leak-hunter`,
`contract-skeptic`, `cold-executor`, `scaffolding-skeptic`, `economy-skeptic`, `boundary-keeper`,
`standards-skeptic`).
The skill layer names only capabilities — concrete tools live in adapters — so a skill reads the same
whatever backend it runs against.

## License

[MIT](https://github.com/chaotixkilla/forge/blob/main/LICENSE) © Sérgio Salgado
