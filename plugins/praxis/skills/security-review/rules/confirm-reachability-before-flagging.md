# Confirm reachability before flagging

A security review's credibility dies the first time it reports a "vulnerability" the author cannot reach. They trace the scary sink, find that nothing an attacker controls ever gets there, and quietly discount every later finding. This is the dominant false-positive class in security review — a dangerous-looking sink whose input is not actually adversary-controlled, a custom sanitizer the reviewer didn't notice one frame up, a code path nothing live ever calls. Reachability is not a severity input; it is the **floor** a candidate must clear to be a finding at all — an unreachable sink is *dropped*, not graded low.

## What "reachable" requires

A path is *actually reachable* only when all four hold — the same source→sanitizer→sink data-flow the hunt already traced ([follow-the-tainted-data](follow-the-tainted-data.md)):

- **An adversary-controlled source** — you can name who supplies the value and what they control. A value only trusted callers set is not a source.
- **A real entry point reaches it** — an actual route, upload, message, webhook, or job carries the attacker's input to the start of the path. A path with no live entry point is dead code, not an attack.
- **A traced path source → sink** — you followed the value hop by hop, not inferred the connection from names.
- **No neutralizing guard on the path** — you checked the frames between source and sink for the validator, allow-list, parameterizer, or escape that breaks the chain. The most common false positive is a "missing check" that exists one frame up.

*Theoretically reachable* fails one of these: the sink is real but the input isn't attacker-controlled, or a guard already defends it, or no entry point drives it. That is not a finding. It is reported only as a hardening note when it has something to improve — a missing second layer of defense ([separate-finding-from-noise](separate-finding-from-noise.md)) — and otherwise dropped; if it clears none of the reads, it is noise, dropped.

## Certainty — how much of the path you traced

Reachability is the yes/no floor; **certainty** grades how firmly you established it, on the certainty scale in [results-and-certainty](../../../craft/evidence/results-and-certainty.md), and rides alongside severity ([severity-scale](severity-scale.md)) without collapsing into it (*how reachable and exploitable* versus *how sure you traced it*). security-review reasons statically and never runs the exploit, so **traced** is the ceiling: no finding here is graded observed. What places a finding:

- **traced** — every one of the four reads above is done: you can state the attacker, the input, and each hop from entry point to sink. *Anchor:* you traced `id` from the route parameter, through the handler, into the string-concatenated query, and read the intervening frames to establish that no validator neutralizes it.
- **inferred** — the path from entry point to sink was followed, and at least one link of it rests on inference rather than a read: a **neutralizing guard on the path** (a validator, parameterizer, or escape) whose frames you didn't all read, an authorization check you didn't open, or a hop you reasoned rather than followed, such as a call through dynamic dispatch whose target you inferred. *Anchor:* you traced a request field into a string-built query and reached it from a real unauthenticated route, but inferred from the handler's shape that no sanitizer intervenes without reading every frame in between.
- **unverified** — reachability rests on a pattern with **no traced path**: the sink is real and the value looks attacker-shaped, but you traced no route that drives adversary-controlled input to it. The suspicion stands, the trace does not. Reading the sink is not a first-hand reading of the reachability the finding claims, so it is the value's resemblance alone that backs it. *Anchor:* a raw query whose input resembles a request field, and you ran out of trace budget before either establishing or ruling out a route that drives attacker input into it. Always reported, always labelled ([assessing-severity](../phases/04-assessing-severity.md)).

**The placement tests** — what stops a candidate sliding between levels in this domain:

- **traced vs inferred** — is *every* hop read, or does any link rest on inference? Read every hop → traced; any link, a guard or a hop, inferred though the rest is traced → inferred.
- **inferred vs unverified** — does reachability rest on a **path you followed** with some link inferred, or on a **pattern** with no path followed? A path followed from a real entry point to the sink, any link of it inferred → inferred; the value's shape, a sink pattern or a name alone, with no path followed → unverified. (A guard you traced and found *absent* on a route a real attacker reaches is the finding itself — the missing control of [absence-is-a-finding](absence-is-a-finding.md), graded by [exploit-then-impact](exploit-then-impact.md) — not this unverified case.)
- **kept vs dropped (the floor)** — this is the seam that decides whether a candidate is a finding at all, and it turns on *what you established, not what you failed to establish*: **an unfinished trace with a live suspicion is kept** (you did not establish reachability, but you did not rule it out either), labelled inferred or unverified by the test above; **dropped is a finished trace that came back negative** (you traced and found no adversary-controlled input reaches the sink, or a guard fully neutralizes the path) → it has not cleared the floor and is not a finding (a hardening note at most, by the carve-out above). Never drop on an unfinished trace, and never report a sink traced as unreachable.

Do not launder a speculation into a certainty: the answer to "am I sure it's reachable?" is another read of the path, not a raised level. When a full trace is beyond the run's budget, report at true certainty with the unread link named.

`(basis: SAST-triage and pentest guidance, 2024–2026; OWASP taint analysis; the placement tests after review's certainty placement; the levels, and the inferred-vs-unverified line as its any-first-hand-read test, per the cited standard)`
