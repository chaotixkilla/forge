# spec — usage

Turn a fuzzy request into hard, testable, sequenced requirements — the contract a build is held to.

## When to use
- The ask is real but vague ("add sharing", "make it faster") and you need to pin down what "done" means before anyone designs or builds.
- You want requirements that are pass/fail checkable, not prose that sounds agreeable but can't be verified.
- A tracker issue or a decision thread needs to become a structured spec: functional, non-functional, data, and interface requirements.
- You need scope carved into independently shippable slices with priorities, so time pressure cuts the right things.

## Not for / use instead
- Understanding an unfamiliar system or codebase before you can even frame the ask → understand
- Turning a settled spec into a buildable design with concrete interfaces and a rollout → plan
- Breaking an already-agreed body of work into tasks/tickets for execution → decompose
- Validating a rough idea by building a throwaway to learn → prototype
- Writing the tests that check a requirement → test (spec defines the acceptance criteria; test implements them)

## Examples
`--from-issue=<ref>` — seed the spec from a tracker issue (title, description, acceptance criteria) instead of a blank page; you still interrogate and harden it.
`--from-discussion=<ref>` — seed from a discussion thread, lifting the decisions and constraints already argued out so you don't re-litigate them.
`--strict` — hold a high bar: every requirement must be pass/fail checkable, every vague adjective quantified; rejects "should be fast" until it's a number.
`--first-pass` — return the structural skeleton after the first phase and pause for steering, so you correct scope before investing in detail.
`--publish` — send the finished spec to the configured artifacts backend via the publish capability.
`--from-issue=<ref> --strict` — harden an inherited issue into a rigorous, checkable spec.
`--from-discussion=<ref> --first-pass` — turn a thread into a skeleton, confirm the shape, then flesh out.

## Gotchas
- **Delegates its evidence-gathering to the `gather` skill (phases 1 and 3),** which pulls glossary, standing conventions, and behavioral invariants — perf budgets, a11y/security baselines, tenancy rules — that the spec must respect. spec declares no knowledge configuration of its own: the `knowledge` port owns the `tools.knowledge` prerequisite and, if it is unset, guides you through init:knowledge or `gather` degrades to spec'ing without that grounding (weaker, more assumption-laden).
- `--publish` hands the finished spec to the `publish-artifact` skill, which owns the artifacts prerequisite; if it isn't configured, `publish-artifact` guides you through init:artifacts (or blocks), and spec degrades by returning the spec locally. What it publishes is a clean, team-facing document — the requirements and decisions, never the interrogation machinery.
- `--from-issue` / `--from-discussion` reach an external source (a tracker, a discussion thread) through a capability owned by its port skill. Those ports are proposed but not yet built; until they exist, these flags degrade to interrogating whatever request content you can provide inline rather than fetching it.
- The value is in the interrogation and quantification, not the document — feed it a fuzzy ask and let it attack, don't hand it a finished spec to reformat.
- Deliberately stops at requirements. It does not choose an approach, design interfaces, or map onto existing code — that's plan. It states what's out of scope but does not build.
- `--first-pass` returns a skeleton, not a partial spec you should ship; it exists to catch scope drift early.
