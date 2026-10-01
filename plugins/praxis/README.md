# praxis

> Engineering work as skills — each kind of work an act, each act run as steps, every step held to shared craft.

[![version](https://img.shields.io/github/v/tag/chaotixkilla/forge?filter=praxis-v*&sort=semver&label=version&color=1f6feb)](https://github.com/chaotixkilla/forge/releases?q=praxis)
[![license: MIT](https://img.shields.io/badge/license-MIT-3fb950)](https://github.com/chaotixkilla/forge/blob/main/LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-6E56CF)](https://docs.claude.com/en/docs/claude-code)

**praxis codifies software engineering as skills,** so that work done with it can be trusted, is of
high quality, and stays maintainable. Each skill runs a real, sourced procedure — not a prompt — and
the work is organized in three layers:

- **Acts** are the kinds of work someone does: developing a feature, fixing a bug, reviewing a
  teammate's change, shipping, responding to an incident. An act decides which steps run, in what
  order, with what inputs, and delivers the result.
- **Steps** are the procedures an act runs — understand, spec, plan, develop, test, review and the
  rest. A step produces a result and never delivers it: posting, filing and notifying are the act's.
- **Craft** is the standards every step is held to — engineering, evidence and writing — kept once
  and cited by each step that applies it, so plan designs, develop builds, refactor restructures and
  review judges against the same ones.

Skills reach your external systems (version control, CI, trackers, telemetry, chat, knowledge and
artifact stores) through a layer of **ports**, so the process stays identical whichever backend you use.

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

## Start here: `work`

`work` starts or resumes engineering work. It routes the request to an act, opens a **task** for it,
runs the act's steps in order, files each result in the task's documentation, and delivers what the
act delivers. A task survives sessions: `work --task=<key>` picks it up where it stopped.

| act | the request |
|---|---|
| developing | build new behavior or change how existing code behaves |
| fixing a bug | find and remove the cause of a defect that has already shown itself |
| reviewing | judge a change someone else made, before it lands |
| shipping | take finished work into its integration target, and out to an environment |
| responding to an incident | restore a degraded production service, then learn from it |
| maintaining | keep code healthy: restructure it, retire a switch, move a dependency |
| researching | answer a question from outside sources, with no code to change |
| prototyping | answer a feasibility question with something small and throwaway |
| auditing | judge the security posture of a whole system or component |
| learning | understand an unfamiliar part of the system and leave documentation of it |

Each task keeps dated documentation, one content type per page: the task record, the work records its
steps produced (spec, plan, review record, incident record, …), a decision record for each decision
that can't be walked back, and system documentation of the part it touched — explanation, reference,
how-to and concept pages. It's filed on your configured artifacts backend, or locally under
`docs/praxis/` by default.

## Steps

You can run any step on its own; inside an act, the act runs it for you.

**Shape the work**

| skill | what it does |
|---|---|
| `understand` | map an unfamiliar system or area before changing it |
| `spec` | pin the *what* — requirements and acceptance, before design |
| `plan` | turn a spec into a buildable design (interfaces, hard flows, rollout) |
| `decompose` | split a settled design into ordered, independently-shippable units |
| `prototype` | validate feasibility with a throwaway spike |

**Build, verify and judge**

| skill | what it does |
|---|---|
| `develop` | implement to a finished, integrated, self-checked local state |
| `test` | design and run tests to a coverage-adequacy verdict |
| `verify` | drive the running app end-to-end and report what it actually did |
| `review` | review a change for correctness and craft, findings ranked, with questions for the author |
| `security-review` | audit a change or a system for reachable vulnerabilities |
| `debug` | find a known failure's root cause and recommend the fix |

**Maintain**

| skill | what it does |
|---|---|
| `refactor` | restructure existing code with its behavior unchanged |
| `upgrade` | move a dependency to a new version from its migration guide |

**Ship and operate**

| skill | what it does |
|---|---|
| `land` | get a finished change into its integration target, gate green |
| `roll-out` | take a merged change to an environment, reversibly, and judge its health |
| `triage` | decide whether a production signal is a real incident, and how severe |
| `mitigate` | restore a degraded service before its cause is known, and confirm it holds |

**Research and write**

| skill | what it does |
|---|---|
| `deep-research` | multi-source, adversarially-verified research to a cited report |
| `communicate` | write a message, update or document for the people who'll read it |
| `document` | file a task's documentation, one document type per page, and the task log |

`init` sets the project up. Underneath sit the ports — `vcs`, `ci`, `telemetry`, `communication`,
`project-mgmt`, `knowledge`, `artifacts` — and `gather`, the shared investigation engine; the skills
above delegate to them, and you rarely invoke them directly.

## Craft

praxis keeps its standards in a craft library, in three families:

- **engineering** — naming, comments, functions, abstraction, data and types, errors, reuse, change
  hygiene, conventions, design, testing and observability;
- **evidence** — anchoring a claim, telling observation from inference, preserving the evidence,
  changing one thing at a time, fixing the cause rather than the symptom, triangulating sources;
- **writing** — leading with the takeaway, sizing detail to the reader, audience tiers, clean export.

A step cites the standards it applies at the point it applies them, so a standard means the same thing
in every step that uses it.

## Hooks

In a project with praxis settings (`.claude/praxis.json`), praxis enforces what an instruction alone
can't:

- **At session start**, it points engineering work at `work`, applies the project's comment posture,
  and trims closed or idle tasks from Claude's memory index.
- **Before a code change**, it blocks file edits and commits inside the project while no act is
  running, and says how to start one: a trivial change runs the developing act's small-change path.
- **When a step runs outside an act**, it adds a note to offer filing the step's result into a task.
- **At the end of a turn**, three checks block once: a step in a running act skipped without a reason,
  a step's result neither filed nor marked unfiled with a reason, and a praxis skill run without its
  phase files being read.

## Quick start

```
/praxis:init      # configure your project's backends (once)
/praxis:work      # start or resume work — "build PROJ-88", "review PR 230", "the checkout API is down"
/praxis:review    # run one step on its own — here, a review of your own change
```

## Configuration

praxis prefers backends that store **no credential**:

- **A connected MCP server** (e.g. GitHub or Slack) — rides your existing authorization, stores nothing.
- **An authenticated CLI** on your machine — reuses the ambient session, no stored token.
- **A local filesystem root** — for knowledge and artifacts, no auth; the artifacts default.
- **`api` (last resort)** — the only transport needing a token; it goes into Claude Code's secure
  per-user store, never into the committed project config.

## License

[MIT](https://github.com/chaotixkilla/forge/blob/main/LICENSE) © Sérgio Salgado
