# Honor the repo's commit policy

A repo often enforces policy on the commit *object* itself — hooks that must run, a signature that must be present — and the failure mode is quiet: a commit made in a way that bypasses the hook or omits the signature lands, and a later check (or an auditor) rejects it, or worse, a secret a pre-commit scan would have caught is now in history. Every commit **follows** the repo's enforced commit policy and never cheats it. It is detect-and-follow, not a house default: most repos require neither, some require both, so read which before committing — never impose signing or hooks a repo doesn't use, nor skip ones it does.

## Pre-commit hooks — run them, never bypass them

- **Let the hooks run.** Committing normally fires the repo's commit-time hooks (formatters, staged-file linters, secret-scanners, message linters). Commit normally so they run; **never** take the skip-verification shortcut to force a commit past a hook.
- **A hook failure is a stop, not a warning.** If a hook rejects the commit — a formatter rewrote files, a secret was detected, the message failed a linter — **stop**, surface what the hook reported, and resolve it (re-stage the formatter's changes, remove the secret, fix the message) before committing, rather than forcing the commit through. A secret-scan hit in particular is a hard stop: never commit past it.
- **This composes with the gate, doesn't duplicate it.** Hooks run at *commit* time; a pre-merge gate runs later against the merged result. A hook is not a substitute for the gate or vice-versa — both are honored, and bypassing the hook to "let the gate catch it" is exactly the cheat this standard forbids.

## Commit signing — sign when the repo requires it

- **Detect the signing requirement.** Read whether the repo/team requires signed commits — its configuration (a sign-by-default / required-signature setting) or a history of signed commits. This is not assumed: an unsigned-history repo's commits aren't signed, and a signed-history or required-signature repo's are. The **config signal is authoritative** (it, not history, drives the required-but-unable stop below); a **history signal alone** establishes a requirement only when it is *consistent* (recent commits are signed) — a **mixed** signed/unsigned history with no config signal establishes **no** requirement, so signing is treated as not required there (never guessed from a 50/50 split).
- **Sign when required; stop when required-but-unable.** Where signing is required, sign the commits per the repo's configured signing method. Where signing is required but the commit **can't** be signed (no signing key configured or available), **stop and report** the missing signing setup rather than recording unsigned commits a signature check will later reject — an unsigned commit into a signed-required line is the quiet failure this prevents.

`(basis: derived from detect-and-follow team practice and a red gate's hard stop; practitioner reports of bypassed hooks)`
