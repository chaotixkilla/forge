# praxis

> Engineering processes as skills — understand, spec, plan, build, review, ship, operate.

[![version](https://img.shields.io/github/v/tag/chaotixkilla/forge?filter=praxis-v*&sort=semver&label=version&color=1f6feb)](https://github.com/chaotixkilla/forge/releases?q=praxis)
[![license: MIT](https://img.shields.io/badge/license-MIT-3fb950)](https://github.com/chaotixkilla/forge/blob/main/LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-6E56CF)](https://docs.claude.com/en/docs/claude-code)

**praxis codifies the software-delivery lifecycle as skills.** Each skill runs a real, sourced
procedure — not a prompt — for understanding a system, speccing and planning a change, building and
reviewing it, and shipping and operating it. Skills reach your external systems (version control, CI,
trackers, telemetry, chat, knowledge and artifact stores) through a layer of **ports**, so the process
stays identical whichever backend you use.

## Install

```
/plugin marketplace add chaotixkilla/forge
/plugin install praxis@forge
```

Then configure your project once:

```
/praxis:init
```

`init` detects your remotes and connected backends, proposes a per-capability setup, and writes a
per-project `.claude/praxis.json`. Any skill also offers to configure a backend the first time it
needs one — so you can start immediately and set things up as you go.

## Skills

**Shape the work**

| skill | what it does |
|---|---|
| `understand` | map an unfamiliar system or area before changing it |
| `spec` | pin the *what* — requirements and acceptance, before design |
| `plan` | turn a spec into a buildable design (interfaces, hard flows, rollout) |
| `decompose` | split a settled design into ordered, independently-shippable units |
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
| `init` | detect and configure per-project backends and team roster |

The **tool layer** — `vcs`, `ci`, `telemetry`, `communication`, `project-mgmt`, `publish-artifact`, and
the shared investigation engine `gather` — sits underneath and is delegated to by the skills above; you
rarely invoke it directly.

## Quick start

```
/praxis:init      # configure your project's backends (once)
/praxis:spec      # pin down what to build
/praxis:plan      # turn the spec into a buildable design
/praxis:review    # review a change — ranked and routed
```

## Configuration

praxis prefers backends that store **no credential**:

- **A connected MCP server** (e.g. GitHub or Slack) — rides your existing authorization, stores nothing.
- **An authenticated CLI** on your machine — reuses the ambient session, no stored token.
- **A local filesystem root** — for knowledge and artifacts, no auth.
- **`api` (last resort)** — the only transport needing a token; it goes into Claude Code's secure
  per-user store, never into the committed project config.

## License

[MIT](https://github.com/chaotixkilla/forge/blob/main/LICENSE) © Sérgio Salgado
