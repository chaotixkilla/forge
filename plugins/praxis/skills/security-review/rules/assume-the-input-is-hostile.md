# Assume the input is hostile

An author writes for the input they expect; an attacker sends the input they don't. Most missed vulnerabilities are not subtle — they are the obvious consequence of a value the author never pictured: the id that belongs to someone else, the string that closes the quote and adds a clause, the length that overflows the buffer, the field that is simply absent. Reviewing for the happy-path value re-walks the author's own reasoning and finds what they already handled. This rule is the stance shift: for every input crossing a boundary, ask what the *worst-shaped* value does.

## Construct the hostile value, then ask what it reaches

For each input the surface accepts across a boundary, deliberately construct the adversarial shapes and follow each:

- **Malformed** — the value that violates the format the parser assumes (a broken encoding, an unexpected type, a nested structure deeper than any legitimate caller sends).
- **Boundary** — empty, zero, negative, one, the maximum, one past the maximum; the extremes the validation forgot.
- **Injection-shaped** — the value crafted to escape its data context into an instruction context (the quote, the separator, the control character, the traversal sequence, the template delimiter).
- **Someone else's** — the well-formed value the caller is simply *not entitled to*: another tenant's id, a higher privilege level, a resource outside their scope. This is the value that finds the missing authorization check, not the missing validation.

## The discriminator: the attacker's value, not the author's

The test: **are you reasoning from the value an attacker would send, or the value the code was written to handle?** This rule supplies the hostile *value*; [follow-the-tainted-data](follow-the-tainted-data.md) traces its *path* and [confirm-reachability-before-flagging](confirm-reachability-before-flagging.md) proves the path is reached. The failure it resists is the review that confirms the code works — reading for the input that succeeds instead of constructing the one that breaks. If every hostile shape you construct is caught, that is a real (and reportable-as-clean) result; if one reaches a sink, follow it.

`(basis: adversarial-input first principle underlying fuzzing and abuse-case analysis; the method, not a graded bar.)`
