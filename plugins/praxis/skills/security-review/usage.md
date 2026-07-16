# security-review — usage

Audit a change or a subject through a threat lens — scoped to a named adversary — and return substantiated, severity-ranked findings, each traced from adversary-controlled input to the abuse it enables, optionally as a machine-readable findings document or a pass/fail CI gate.

## When to use
- A dedicated threat audit of a change or a component before it ships: authn/authz, injection, secret handling, data exposure across a trust boundary, and supply-chain trust — reasoned from a named adversary, not a generic checklist.
- You want findings you can act on and trust — each with the adversary, the traced path from their input to the sink, the abuse it grants, and a concrete remediation — not a list of theoretical weaknesses.
- You want to bias the audit toward a specific adversary or attack class (`--threat-model`), map it onto a compliance framework and report coverage (`--standard`), or run it as a merge-blocking gate (`--gate`).
- You want the audit to land where the work lives: a human report, a machine-readable findings document for tooling (`--sarif`), or a CI verdict.

## Not for / use instead
- A general correctness/craft read of a diff with a code-review-depth security lens → **review** (review carries a security lens; security-review is the full adversary-scoped threat audit).
- Confirming a suspected exploit actually fires end-to-end against the running system → **verify** (security-review reasons statically about reachability; it does not execute the exploit).
- Building the change or applying the remediations → **develop** (security-review reads a finished subject and recommends fixes; it does not build).
- Root-causing a specific known incident or failure → **debug** (security-review hunts latent, reachable weaknesses; debug chases one that already fired).
- Broad, open-world research into a vulnerability class or a CVE → **deep-research** (security-review audits *this* subject against *its* surface).

## Examples
`security-review` — audit the whole subject (the default surface): map its entry points and trust boundaries, model threats, hunt, and return severity-ranked findings.
`security-review --changed` — narrow the surface to the working-tree diff and its blast radius (the touched code plus what newly reaches it), read ambiently from the local tree.
`security-review --threat-model=STRIDE` — bias the hunt toward a named threat-modeling framework or adversary and weight which threats to prioritize.
`security-review --standard=owasp-top-10` — map findings onto a named framework's control taxonomy and report coverage against it.
`security-review --exhaustive` — enumerate every entry point and every threat class rather than the high-likelihood subset; slower, for a high-assurance pass.
`security-review --severity-min=high` — drop anything below high severity before delivery.
`security-review --sarif=findings.sarif` — emit findings as a machine-readable document at the path, alongside the human report.
`security-review --gate --severity-min=high` — run as a pass/fail check that exits non-zero if any high-or-above finding remains; for CI.

## Gotchas
- **Reachability is the floor, not a nicety.** An unreachable sink is *not a finding* — it is dropped, not down-graded. Every finding names the adversary, what they control, and the traced path from their input to the sink; a weakness with no reachable attacker is at most a note, not a severity-ranked finding.
- **A hardening nit is not a vulnerability.** security-review reports exploitable defects where a reachable adversary gains something concrete; defense-in-depth suggestions with no reachable abuse are kept separate from the ranked findings, not padded into them.
- **Silence is a valid result.** A subject whose trust holds returns "no reachable abuse found under the threat lens," explicitly — not a manufactured list.
- **security-review needs no configuration of its own.** Reading the local subject — and, under `--changed`, the local diff and its base — is ambient, needing no backend, exactly as review reads a local diff. If the subject isn't a version-controlled tree with a derivable base, `--changed` degrades: it audits the whole subject and says it couldn't scope a diff. (A change hosted on a version-control host would delegate to the `vcs` skill, which owns `tools.vcs`; this skill takes no such flag.)
- **`--sarif` writes a file; `--gate` sets an exit status.** Neither posts anywhere or needs a backend — the document is a local write, the verdict is a local exit code.
- **The threat-model framework and attack-class taxonomy are dials, not the audit.** With `--threat-model`/`--standard` unset, the audit runs against its default framework and taxonomy; the flags bias and map, they do not gate whether the hunt happens.
