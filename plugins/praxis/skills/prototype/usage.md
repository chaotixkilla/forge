# prototype — usage

Reduce uncertainty by building the smallest throwaway thing that answers one open question — spike a risky assumption or race candidate approaches empirically, read the result against the question, extract the learnings, and discard the code.

## When to use
- You're about to commit to a design or approach that rests on a risky assumption you haven't actually tested — build the smallest throwaway thing that proves or kills it before you build for real.
- A plan or spec surfaced a known unknown ("needs a spike") — feasibility, throughput, a library's real behavior, an integration's actual contract — and you want an empirical answer, not a guess.
- Two or more candidate approaches look plausible and you want to race them and pick on evidence rather than argument (`--max-agents`).
- You want the *learnings* to persist but the *code* thrown away — a de-risked verdict plus the rejected paths and gotchas, not a half-built feature.

## Not for / use instead
- Building the real, durable change → **develop** (prototype builds to learn and discard; develop builds to keep).
- Designing the approach or slicing scope on paper → **plan**; hardening requirements → **spec** (prototype answers one empirical unknown a plan/spec surfaced — it does not produce the design or the requirements, it de-risks them).
- Understanding how existing code already behaves → **understand** (understand reads what's there and changes nothing; prototype builds something new to answer a question about what isn't there yet).
- Root-causing a specific failure that already happened → **debug** (debug chases a known bug; prototype de-risks an open question before you commit).
- Open-world research synthesized from sources rather than from a built experiment → **deep-research** / **gather** (prototype's evidence is a run, not a literature synthesis).

## Examples
`--sandbox` — run the spike in an isolated throwaway environment so it can't touch real state and is trivial to discard.
`--max-agents=3` — race three candidate approaches to the same question in parallel, then compare and select on the declared basis.
`--prior-art=REF` — seed from a named reference: reproduce it to a working baseline, then diverge toward the framed question.
`--timebox=2h` — bound the spike to two hours; on expiry, stop and report the best answer reached so far.
`--publish` — hand the extracted learnings to the artifacts capability as a clean, team-facing findings document.
`--max-agents=3 --timebox=1h --sandbox` — race three approaches, each in isolation, under a shared one-hour budget.

## Gotchas
- **The code is meant to be thrown away.** prototype optimizes for learning speed, not durability; hardening a spike in place is the anti-pattern `favor-disposability` names. If you want to keep and grow the code, that's a tracer-bullet/evolutionary build — a different posture (see the fork in `favor-disposability`).
- **A verdict must be grounded in a run, not in reasoning.** "This should work" is not *answered*; *answered* means the framed unknown itself was exercised by something that actually ran (`ground-claims-in-a-run`).
- **`still-open` is a real, honest result.** A spike that ran but stubbed the very thing under test has not answered its question — reporting it as answered is exactly the failure mode the verdict scale guards against.
- **prototype is config-less and a leaf.** By default it returns a findings blob to the caller; it invokes no downstream skill. `--publish` is the only path that writes anywhere, and it delegates wholesale to `publish-artifact` (which owns the artifacts prerequisite; if unconfigured, prototype degrades by returning the findings locally).
- **It answers ONE framed question.** With several unknowns, frame and spike them separately (or re-invoke); a spike that tries to answer everything muddies the signal (`isolate-what-you-test`).
- **Isolation and timeboxes don't make the result more trustworthy** — only exercising the real risk does. `keep-the-real-thing-in-view`: track which shortcuts wouldn't survive production scale or data, so the result isn't read as more than it is.
