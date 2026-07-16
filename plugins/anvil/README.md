# anvil — the authoring kit

`anvil` is forge's **authoring kit**: a plugin whose skills build, audit, and release the
other plugins in this marketplace (you forge plugins on the anvil).

It is a **published plugin** — catalogued in `../../.claude-plugin/marketplace.json` alongside the marketplace's other
plugins and installable as `anvil@forge` (or loaded straight from its subdir during development via
`claude --plugin-dir ./plugins/anvil`). It is **self-contained** (its own explorers, critics, and
`codify` — depends on no other plugin) and **config-less** (operates on the repo via primitives,
with git ambient). It is **self-hosting** — anvil's skills build, audit, and release anvil itself.

## Skills (9)

| skill | level | what it does |
|---|---|---|
| `scaffold-skill` | plugin | lay a new skill's slot skeleton (frontmatter + phases/rules) |
| `codify` | plugin | turn a process into a skill's runnable procedure (the content engine) |
| `add-component` | plugin | add an adapter / explorer / critic / rule / module / hook to a plugin |
| `audit-tool-leaks` | plugin | scan the skill layer for concrete-tool leaks (the HARD RULE) |
| `audit-contract` | plugin | check frontmatter / slot / flag / config conformance |
| `new-plugin` | marketplace | birth a new plugin (config posture, shell, pool design) |
| `audit-packaging` | marketplace | ships-vs-authoring boundary across the marketplace |
| `release` | marketplace | publish a plugin to the catalog (gated by the three audits) |
| `dogfood` | reflexive | run a plugin's own skills on itself (`--self` = self-hosting proof) |

## Agents

- **explorers** (gather, read-only): `plugin`, `authoritative-sources`, `community-practices`
- **critics** (challenge): `leak-hunter`, `contract-skeptic`, `cold-executor`, `scaffolding-skeptic`, `boundary-keeper`

## Conventions

Plugin-level skills take `--plugin=<name>`; marketplace-level skills act on the catalog. Skill bodies
use slot structure: `phases/NN-name.md` (ordered procedure), `rules/name.md` (a-la-carte craft),
`modules/name.md` (flag-activated). Frontmatter is `name` + `description` + flags/config_requires under
`metadata`. The skill layer names only **capabilities** — concrete tools live in adapters.
