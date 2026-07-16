# praxis — the SDLC plugin

`praxis` codifies engineering / software-delivery processes — understanding a system, speccing and
planning a change, building and reviewing it, shipping and operating it — as skills and subagents.
Each skill runs a real, sourced procedure (not a prompt), and reaches external systems
(version control, CI, trackers, telemetry, chat, knowledge/artifact stores) through a **tool-layer of
ports** so the process stays the same whichever backend you use.

It is a **published plugin** — catalogued in `../../.claude-plugin/marketplace.json` and installable as
`praxis@forge` (or loaded from its subdir during development via `claude --plugin-dir ./plugins/praxis`).
It is **config-bearing**: its skills use external backends a project chooses, wired once via `init`.

## Configuring backends — MCP-first, no secrets if you can help it

praxis reaches each external capability over a transport you pick per project, and it **prefers the
paths that store no credential**:

- **Already-connected MCP server** (e.g. a GitHub or Slack MCP) → praxis rides your harness
  authorization and stores **nothing**. This is the encouraged path.
- **Authenticated CLI** on your machine → reuses the ambient session; no stored token.
- **Local filesystem** (for knowledge/artifacts) → no auth.
- **`api` (last resort)** → the only transport that needs a token. praxis flags it as the fallback;
  the value goes into the harness's secure per-user `userConfig` (OS keychain), referenced by a
  `<cap>_token` key — **never** written into the committed project config.

Run **`/praxis:init`** after install: it detects your remotes and connected backends, proposes a
per-capability config (steering you toward MCP/CLI), and writes a per-project `.claude/praxis.json`
(providers, transports, team roster) — secrets stay in `userConfig`, not this file. Re-run
`init:<capability>` to (re)configure one slot. Any skill also guides you to `init` the moment it first
needs a backend that isn't set up yet (lazy gating) — so you can install and start without configuring
everything up front.

## Skills

**Shape the work**

| skill | what it does |
|---|---|
| `understand` | map an unfamiliar system / area before changing it |
| `spec` | pin the *what* — requirements and acceptance, before design |
| `plan` | turn a spec into a buildable design (interfaces, hard flows, rollout) |
| `decompose` | split a settled design into ordered, independently-shippable work units |
| `prototype` | validate feasibility with a throwaway spike |

**Build & verify**

| skill | what it does |
|---|---|
| `develop` | implement to a finished, integrated, self-reviewed local state |
| `test` | author and run tests to a coverage/adequacy verdict |
| `review` | review a change for correctness and craft, ranked and routed |
| `security-review` | audit a change for reachable vulnerabilities (severity from CVSS) |
| `debug` | find a known failure's root cause and localize the fix |

**Ship & operate**

| skill | what it does |
|---|---|
| `integrate` | land finished work into a target and roll it out safely |
| `operate` | run incident response — triage, stabilize, diagnose, learn |
| `maintain` | perform a scoped, reversible maintenance change |

**Cross-cutting**

| skill | what it does |
|---|---|
| `communicate` | shape session substance into a human-facing artifact for an audience |
| `deep-research` | multi-source, adversarially-verified research to a cited report |
| `init` | detect and configure per-project backends + team roster |

**Tool layer** (interface skills other skills delegate to — you rarely invoke these directly):
`vcs`, `ci`, `telemetry`, `communication`, `project-mgmt`, `publish-artifact` (each a thin port over its
capability's configured provider), and `gather` (the shared cross-lane investigation engine, which owns
the knowledge capability).

## Agents

- **explorers** (gather facts, read-only): `code`, `repository`, `community-practices`,
  `official-documentation`, `authoritative-literature`, `knowledge-base`
- **critics** (challenge work): `adversary`, `assumption-hunter`, `completeness-auditor`,
  `security-auditor`, `simplicity-hawk`, `trade-off-analyst`, `user-advocate`, `future-self`

## Conventions

Skill bodies use slot structure — `phases/NN-name.md` (ordered procedure), `rules/name.md` (a-la-carte
craft), `modules/name.md` (flag-activated). The skill layer names only **capabilities**; concrete
providers live in each port's `adapters/`. A skill that delegates a capability wholesale declares no
`config_requires` for it — the owning port does (doer-owns-prerequisites). Reference bundled files with
`${CLAUDE_PLUGIN_ROOT}` and project files with `${CLAUDE_PROJECT_DIR}`.
