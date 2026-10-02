# Placing a claim on the certainty scale

Every claim in understand's map carries a certainty level from [results-and-certainty](../../../craft/evidence/results-and-certainty.md): observed, traced, inferred or unverified. That standard defines the levels and how to place a claim on them; this rule adds understand's one placement test of its own. Certainty is orthogonal to [find-the-source-of-truth](find-the-source-of-truth.md): that rule picks which source to believe when sources disagree, and certainty says how well the belief is established once chosen.

## When the system is declarative

`(basis: derived from the standard's declarative case)`
A config, a schema, an IaC manifest or a skill behaves as its interpreter consumes it: the loader that reads the config, the validator that applies the schema, the harness that loads the skill. A claim about how it is consumed is **traced** only when you read the artifact's operative text end to end *and* the consuming rule that applies is one you rely on without reasoning it, in one of two ways:
- you read the artifact-specific consuming logic; or
- the rule is **platform-general**, governing every artifact of this kind and relied on the way an executable trace relies on a language's evaluation rules. The harness's "load only referenced slots" rule is one: it is not a claim about this one skill.

It is **inferred** when you read the artifact but reasoned about how it is consumed, or took an **artifact-specific** consuming behavior from a document you have not seen borne out. The test between the two: does the consuming rule govern every artifact of the kind (traced), or only this system (read or observed it, or it stays inferred)?

Cited from [trace-the-behavior](../phases/03-trace-the-behavior.md), [synthesize-the-answer](../phases/05-synthesize-the-answer.md), where it is also handed to the assumption-hunter critic, and [find-the-source-of-truth](find-the-source-of-truth.md).
