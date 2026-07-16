---
name: codify
description: Turn a human or maintainer process into the runnable procedure inside a skill.
allowed-tools: Read, Glob, Grep, Write, Edit
metadata:
  flags:
    --plugin=<name>: target plugin whose skill is being codified
    --skill=<skill>: the skill whose procedure to author or refine
    --from-transcript=<ref>: seed the process from a transcript/notes instead of interrogating live
    --first-pass: return the goal/process split + skeleton, then pause
    --rounds=<n>: how many refine passes over the procedure before returning
    --verify=off|light|strict: cold-executor validation rigor
---
Usage & examples — when to reach for this skill, and concrete flag invocations: see [usage.md](usage.md).

Each numbered step's full procedure lives in the linked phase file — read it, then carry out the step. The phases cite the rules/ craft where it applies.

**Two lanes — author or regenerate.** codify either authors a procedure into a skill that has none, or **regenerates** one that already carries thin phase bodies (an early-scaffolded skill being lifted to the bar). In a regenerate the goal and process are already encoded in the existing files and the phase skeleton exists on disk, so phases 01–03 mostly *read and confirm* what's there rather than derive it fresh; the work concentrates in 04 (resolve / close standards) → 06 (validate), applied over the pre-existing bodies. **Lift, don't rewrite:** preserve every phase, rule, and slot that already conforms (depth ≠ length), raise only what's below the bar, and grow the layers the skill never had (`rules/`, `modules/`). Discarding conformant content to rebuild fresh is this lane's failure mode.

1. Split the goal from the process: the request names a destination; your job is the route to it  — see [phases/01-split-goal-from-process.md](phases/01-split-goal-from-process.md)
2. Source the process knowledge (infer first, ask last): fill the model cheapest-source-first; explore before you interrogate  — see [phases/02-source-knowledge.md](phases/02-source-knowledge.md)
3. Decompose into the skeleton: get the structural shape down before polishing any part  — see [phases/03-decompose-skeleton.md](phases/03-decompose-skeleton.md)
4. Resolve the decisions: this is the actual work: converting intent into rules  — see [phases/04-resolve-decisions.md](phases/04-resolve-decisions.md)
5. Classify fidelity per step: rule, judgment, or checkpoint — and phrase each at that fidelity as you write it  — see [phases/05-classify-fidelity.md](phases/05-classify-fidelity.md)
6. Validate: prove it convergent, not merely runnable — two cold executors must land on the same judgments  — see [phases/06-validate.md](phases/06-validate.md)
