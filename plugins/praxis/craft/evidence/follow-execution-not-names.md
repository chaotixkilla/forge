# Follow execution, not names

Believing the label over the behavior produces a picture of the system its author *meant* to write instead of the one that exists — and a fault lives exactly where the system does something other than what you believe it does. The fastest-feeling move is to reason from names, comments, types and a mental model of "what this obviously does", and that reasoning walks straight past the place where intent and behavior diverge.

## Trust behavior over its labels

When a claim depends on what a symbol or some state does, read or observe it — the real value, the real path, the real branch — rather than inferring it from what it's called or what it "should" be. A function named `validate` may reject nothing; a variable typed non-null may be widened by a cast upstream; a comment may describe the code two refactors ago; a config you "know" is set may be overridden downstream. Names and comments are the author's *intent*: they orient you to *where to look*, and they are never evidence of *what happens there*.

The test: **does the claim rest on something you read or watched execute, or on what the code is called or said to do?** The second orients the search, and a claim resting on it alone is **unverified**, on the certainty scale [results-and-certainty](results-and-certainty.md) defines; only the first is evidence.

## Verify the path actually runs

A path that looks reachable in the source may be dead — behind a flag never set, a condition nothing satisfies, an override registered elsewhere. Before resting a claim on a path, confirm the path is real: it is reached with the input in question, and no earlier frame short-circuits it. A behavior behind an unreachable guard is not the system's behavior. A path you checked runs can carry a claim as **traced** (read) or **observed** (watched running); one you only assumed runs carries it as **inferred** at most.

`(basis: Agans 2002, rule 3; Zeller, Why Programs Fail)`
