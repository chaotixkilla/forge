---
name: prototype
description: Reduce uncertainty about a risky assumption or unproven approach by building the smallest throwaway thing that answers one framed question empirically — scout prior art, run the cheapest probe (or race candidate approaches), read the observed result against the question as answered/refuted/still-open, then extract the learnings and discard the code. The de-risking spike to run before committing a design; distinct from understand (reads existing code, builds nothing) and plan/spec (produce durable design, not throwaway experiments).
metadata:
  flags:
    --sandbox: run the spike in an isolated throwaway environment (a scratch workspace, or version-controlled isolation delegated to the vcs capability) so it can't touch real state and is trivial to discard wholesale — activates the sandbox-isolation module
    --max-agents=<n>: race up to n candidate approaches to the same question in parallel, then compare them on a common basis and select — activates the parallel-fan-out module
    --prior-art=REF: seed the spike from a named reference (repo, paper, example) — reproduce it to a working baseline, then diverge toward the framed question — activates the anchor-to-prior-art module
    --timebox=<duration>: bound the spike to a fixed effort budget; when it expires, stop and report the best answer reached so far rather than chasing completeness — activates the timeboxed-spike module
    --publish: hand the extracted learnings to the artifacts capability as a clean, team-facing findings document — activates the publish-learnings module
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

prototype owns no backend of its own: it is config-less. It resolves `--sandbox` locally (a scratch throwaway environment), and delegates every flag-borne capability wholesale to a port skill — `--publish` to `publish-artifact`, and version-controlled isolation to `vcs` — each of which owns its own prerequisite. So it declares no `config_requires`. It is a leaf: by default it returns the findings to its caller and invokes no downstream skill.

`--max-agents=<n>` reshapes the middle of the run — pick, build, and compare N candidate approaches instead of one: see [modules/parallel-fan-out.md](modules/parallel-fan-out.md). `--timebox=<duration>` bounds the whole spike effort and gates whether evaluate loops back: see [modules/timeboxed-spike.md](modules/timeboxed-spike.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies.

1. Frame the question: state the specific unknown, the decision it unblocks, and the observation that would change course — the spike's success test  — see [phases/01-frame-the-question.md](phases/01-frame-the-question.md)
2. Scout prior art: recruit the code, official-documentation, and community-practices explorers for existing solutions, reference implementations, and known dead-ends before building anything  — see [phases/02-scout-prior-art.md](phases/02-scout-prior-art.md)
3. Pick the cheapest probe: choose the smallest experiment that answers the framed question — stub everything not under test, bias to throwaway  — see [phases/03-pick-the-cheapest-probe.md](phases/03-pick-the-cheapest-probe.md)
4. Build the spike: build fast and disposably toward a clear pass/fail signal — hardcode, skip polish, optimize for learning speed not durability  — see [phases/04-build-the-spike.md](phases/04-build-the-spike.md)
5. Evaluate against the question: run the probe and read the observed result against the framed question — answered, refuted, or still-open — grounded in what actually ran  — see [phases/05-evaluate-against-the-question.md](phases/05-evaluate-against-the-question.md)
6. Capture and discard: extract the durable learnings (verdict, evidence, rejected paths, caveats), hand them off, and throw away the throwaway code  — see [phases/06-capture-and-discard.md](phases/06-capture-and-discard.md)
