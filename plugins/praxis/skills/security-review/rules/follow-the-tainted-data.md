# Follow the tainted data

The fastest way to produce a security review no one trusts is to grep for dangerous function names and flag every hit. Half are unreachable, the input to the other half is never attacker-controlled, and the one real vulnerability — an innocuous-looking call reached by hostile data — isn't on the list because its function name looked safe. A vulnerability is not a keyword; it is a *reachable path* from an untrusted source to a dangerous sink with the taint preserved along the way. This rule is the discipline of reasoning along that path rather than pattern-matching its endpoints.

## Trace source → sink, and ask whether taint survives

For each candidate, name three things and confirm the chain holds:

- **The source** — where adversary-controlled input enters: a request field, a header, a filename, a message payload, a value read back from storage that an attacker earlier wrote. If you cannot name an attacker-controlled source, there is no taint to follow — stop.
- **The sink** — the operation that becomes dangerous when fed hostile input: an interpreter (a query, a command, a template, a deserializer), a file path, a redirect target, a response body, a privileged action.
- **The path between them** — does the taint *survive*? A parameterized query, an escaper, a strict allow-list, a type that structurally can't carry the payload — any of these breaks the chain, and a broken chain is not a finding. Read the path; do not assume the sanitizer is there and do not assume it is absent.

## The discriminator: a path, not an endpoint

The test that separates a finding from a keyword hit: **can you state the value an attacker supplies at the source and trace it, hop by hop, to the sink without a step that neutralizes it?** If yes, it is a tainted path — carry it to [confirm-reachability-before-flagging](confirm-reachability-before-flagging.md) to establish it is actually reached. If you can only point at the sink and assert "this function is dangerous," you have an endpoint, not a path — the two failure modes this resists are flagging a dangerous-looking sink whose input is never hostile, and missing a plain-looking sink that tainted data reaches. Reason from the data, and both disappear.

`(basis: standard taint-tracking analysis — source/sink/sanitizer is the canonical data-flow decomposition SAST and manual review both use; the method, not a graded bar.)`
