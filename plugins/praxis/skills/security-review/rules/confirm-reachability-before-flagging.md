# Confirm reachability before flagging

A security review's credibility dies the first time it reports a "vulnerability" the author cannot reach. They trace the scary sink, find that nothing an attacker controls ever gets there, and quietly discount every later finding. This is the dominant false-positive class in security review — a dangerous-looking sink whose input is not actually adversary-controlled, a custom sanitizer the reviewer didn't notice one frame up, a code path nothing live ever calls. This rule pins the bar a candidate must clear to be a finding at all: reachability is not a severity input, it is the **floor** — an unreachable sink is *dropped*, not graded low.

## What "reachable" requires

A path is *actually reachable* only when all four hold — this is the test practitioners converge on, and it is the same source→sanitizer→sink data-flow the hunt already traced ([follow-the-tainted-data](follow-the-tainted-data.md)):

- **An adversary-controlled source** — you can name who supplies the value and what they control. A value only trusted callers set is not a source.
- **A real entry point reaches it** — an actual route, upload, message, webhook, or job carries the attacker's input to the start of the path. A path with no live entry point is dead code, not an attack.
- **A traced path source → sink** — you followed the value hop by hop, not inferred the connection from names.
- **No neutralizing guard on the path** — you checked the frames between source and sink for the validator, allow-list, parameterizer, or escape that breaks the chain. The most common false positive is a "missing check" that exists one frame up.

*Theoretically reachable* fails one of these: the sink is real but the input isn't attacker-controlled, or a guard already defends it, or no entry point drives it. That is a note at most, not a finding — and if it clears none of them, it is noise, dropped.

## The confidence tiers — how much of the path you traced

Reachability is the yes/no floor; **confidence** grades how firmly you established it, and rides alongside severity ([severity-scale](severity-scale.md)) without collapsing into it (*how reachable and exploitable* versus *how sure you traced it*). It is a graded output, so it carries the same defined-scale obligation severity does — named levels, a per-level test, anchors, and adjacent-level discriminators:

- **confirmed** — every one of the four reads above is done: you can state the attacker, the input, and each hop from entry point to sink. *Anchor:* you traced `id` from the route parameter, through the handler, into the string-concatenated query, and read the intervening frames to confirm no validator neutralizes it.
- **probable** — the source, a real entry point, and the sink are all traced, but one link — typically whether a **neutralizing guard on the path** (a validator, parameterizer, or escape) breaks the chain — rests on a strong inference you did not fully read. *Anchor:* you traced a request field into a string-built query and reached it from a real unauthenticated route, but inferred from the handler's shape that no sanitizer intervenes without reading every frame in between.
- **speculative** — the sink is real and the value looks attacker-shaped, but you **have not finished tracing** whether an adversary-controlled route actually drives input to it: the suspicion stands, the trace does not. *Anchor:* a raw query whose input resembles a request field, and you ran out of trace budget before either establishing or ruling out a route that drives attacker input into it. Reported only when the effort level admits it, always labelled.

**The adjacent-level discriminators** — the tests that stop a candidate sliding between tiers:

- **confirmed vs probable** — is *every* hop read, or does one link rest on inference? Read every hop → confirmed; one link (typically the guard) inferred though the rest is traced → probable.
- **probable vs speculative** — is the path **established as reachable** (a real entry point demonstrably drives attacker input to the sink) or only **plausible**? Established, with one *payload-neutralization* link (a part-4 guard) inferred → probable; attacker-reachability itself not yet established → speculative. Watch the common trap: an inferred **authorization or access-control** check is *not* a part-4 payload guard — it governs whether the *attacker* (rather than a trusted caller) can reach the route at all, which is part-2 reachability. So when attacker-reachability rests on an unread auth check, treat it as unestablished → speculative, not probable. (A guard you traced and found *absent* on a route a real attacker reaches is the finding itself — the missing control of [absence-is-a-finding](absence-is-a-finding.md), graded by [exploit-then-impact](exploit-then-impact.md) — not this speculative case.)
- **speculative vs dropped (the floor)** — this is the seam that decides whether a candidate is a finding at all, and it turns on *what you established, not what you failed to establish*: **speculative is an unfinished trace with a live suspicion** (you did not confirm reachability, but you did not rule it out either) → keep it, labelled; **dropped is a finished trace that came back negative** (you traced and found no adversary-controlled input reaches the sink, or a guard fully neutralizes the path) → it has not cleared the floor and is not a finding. Never drop on an unfinished trace, and never report a confirmed-unreachable sink.

Do not launder a speculation into a certainty: the answer to "am I sure it's reachable?" is another read of the path, not a raised confidence. When a full trace is beyond the run's budget, report at true confidence with the unread link named.

`(basis: the four-part reachability test — attacker-controlled source, real entry point, traced path, no guard — is corroborated practice across SAST-triage and pentest guidance (~7 independent 2024–2026 origins) and matches OWASP/standard taint-analysis theory; the emerging tightening from "statically reachable" toward "attacker can drive the entry point" is why the real-entry-point clause is explicit. The confidence tiers mirror review's confirmed/probable/speculative ladder, keyed here to trace-completeness.)`
