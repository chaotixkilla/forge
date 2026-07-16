# Match the surrounding code

A maintenance change that follows its own style instead of the code's leaves a seam — a patch of different naming, error handling, or structure that tells the next reader "someone from outside was here." The change should read as though the person who wrote the module wrote it. So conform to the conventions already in this file and module — naming, error handling, control structure, test style, import order — over your own defaults and over the wider ecosystem's "best practice." The local pattern wins, because consistency within a codebase is worth more than global correctness of style.

## Which local pattern governs

The convention to match is the *nearest consistent* one: the file first, then the module, then the package. When the file is internally consistent, match it. When the file is itself inconsistent — two error-handling styles already present — match the one that dominates the module around it, and don't add a third. Read enough of the surrounding code to know what the pattern *is* before you assume it; a convention you guessed at is one you'll violate.

## Where "the local pattern wins" stops

Matching the surroundings is a style-and-structure rule, not a correctness one. It stops at three edges:

- **A local pattern that is a bug** is not a convention to preserve — matching a broken error-swallow because the file does it elsewhere propagates a defect. That's a [cause to fix](fix-the-cause-not-the-symptom.md) or a follow-up to surface, not a style to mirror.
- **A local pattern you're deliberately improving** is a [campsite-cleaner](leave-the-campsite-cleaner.md) call — allowed within that rule's line, but then improve it *consistently* within the touched scope, not halfway.
- **A security or contract requirement** overrides local style — you don't match a convention of interpolating input into queries because the file does it; [distrust-untyped-input-and-secrets](distrust-untyped-input-and-secrets.md) and [preserve-the-contract](preserve-the-contract.md) outrank it.

Outside those edges, the local pattern wins even when your own taste disagrees — taste is not a reason to introduce a seam.
