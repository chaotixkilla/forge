# debug — usage

Root-cause a specific failure that has already bitten — reproduce it, prove the mechanism, and either hand off a precise diagnosis or fix it at the cause with a guarding regression test.

## When to use
- A concrete defect has surfaced — a crash, a wrong result, a regression, a flaky test, a production error — and you need its *true* root cause, not a plausible guess or a symptom patch.
- You want the mechanism proven: the failure appears and disappears when the claimed cause is toggled, with every link from cause to symptom traced — so the fix is derived, not hoped.
- You want to start from where the evidence already lives: a production error's traces and frequency (`--from-telemetry`), a log stream (`--from-logs`), or a postmortem's symptoms and timeline (`--from-incident`).
- You want the fix recommended at the cause — its altitude, whether it's bounded or needs design work, and the test that would guard it — before anyone changes the code.

## Not for / use instead
- Hunting *latent* defects in a finished change → **review** (debug chases a failure that already bit; review reads a change for what might bite).
- Authoring or running tests to confirm *intended* behavior → **test**; driving the running app to observe a change works end-to-end → **verify** (debug root-causes a known failure; test and verify confirm behavior).
- Building a feature or implementing to a finished standard → **develop**.
- Running on-call incident response → the incident act in **work**, which triages, mitigates and then runs debug as its diagnosis step. Restoring service before the cause is known is **mitigate**'s.
- A scoped refactor, dependency upgrade, or tech-debt paydown → **refactor** or **upgrade**, or the maintaining act in **work**.

## Examples
`/debug` — root-cause a failure you can already trigger locally.
`--from-telemetry=<telemetry-ref>` — start from a production error's real stack traces, onset, and frequency (the reference resolves through the configured telemetry provider).
`--from-logs=./var/log/app.log` — root-cause from these log lines (a local file read).
`--from-logs=<store-ref>` — root-cause from a hosted log stream, read via the telemetry capability.
`--from-incident=INC-204` — seed from the postmortem's symptoms, timeline, and affected scope.
`--sandbox` — run reproduction and experiments in an isolated throwaway environment, never the working tree.
`--from-incident=INC-204` — diagnose from an incident record, with any mitigation already applied recorded as provisional context.

## Gotchas
- **No reproduction, no fix.** debug never acts on a fix it cannot first make fail on demand; if the bug cannot be reproduced, *reproduction is the job*, not the fix.
- **Cause, not symptom, always.** debug resolves only at a confirmed mechanism; a patch at the symptom layer leaves the cause live. Under a declared incident, restoring service first is **mitigate**'s, and debug records a mitigation already in place as provisional context.
- **debug doesn't change the code.** It returns a confirmed diagnosis with the fix it recommends; the fixing-a-bug act in **work** applies the fix, guards it and verifies it.
- **debug diagnoses; it does not confirm broad health.** The guarding test proves *this* bug is gone; end-to-end confirmation that the whole app still works is verify / **test**'s job.
- **debug needs no configuration of its own.** It delegates telemetry reads to the `telemetry` port, incident reads to `project-mgmt` / `communication`, and recruits explorers directly. If telemetry isn't configured, `--from-telemetry` degrades — the port guides via `init:telemetry` (or blocks) and debug falls back to other evidence lanes.
- **`--from-logs` is dual.** A local path is a plain file read (no backend); a store reference is a hosted log stream read through the telemetry capability.
