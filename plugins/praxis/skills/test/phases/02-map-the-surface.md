Cases designed without knowing where the change lives, how it is reached, and how the codebase already tests similar surfaces are cases that don't fit and don't run. This phase maps the touched surface and learns the suite's conventions before a single case is designed — so the next phase designs cases that are both complete and native to this codebase.

## Locate the touched surface (explore · code)

Recruit the **code explorer** to locate: the code paths the change introduces or alters, the seams it crosses (external dependencies, I/O), its callers and callees (the reverse-dependents that inherit the change's behavior), and where the existing tests for this area live. Without fan-out, do these reads inline — locate the touched symbols, their call sites, and the existing tests yourself before proceeding; the reads are not optional, only the delegation is — see [code](../../../agents/explorers/code.md). Under `--changed`, scope this to the changed files plus their reverse-dependents.

## Learn how this codebase already tests

Read the surrounding suite to learn its conventions ([match-the-suites-conventions](../rules/match-the-suites-conventions.md)): the runner it uses, the directory layout and naming, the fixture and double style, and how it exercises similar surfaces. **Discover the project's own test command** — how the suite is invoked *here* — and carry it forward as "the project's configured runner" for later phases; never assume or hardcode a framework. The goal is that the cases designed next read as natives of this suite, not imports.

## How much mapping is enough — deliberately open

**Deliberately open-by-design:** how far to trace is per-change, and pinning a hop count would be false precision — a leaf function needs its handful of callers, a changed shared contract needs all of them. The stopping test that bounds it: **mapped enough when you can name every behavior the change alters and point to where each is currently exercised (or confirm it is not).** Stop when reading one more file would not change which cases you would design.

## Degraded case

If there is no runnable suite and no way to author one — no language runtime, no test surface (a docs-only or config-only change) — that is a **stated stop** reported through [report-the-verdict](06-report-the-verdict.md), not a silent pass.

## Output

The mapped surface — touched paths, seams, and reverse-dependents; the existing test locations and conventions; and the project's runner — handed to [design-the-cases](03-design-the-cases.md).
