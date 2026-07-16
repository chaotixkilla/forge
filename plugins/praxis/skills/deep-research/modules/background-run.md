# Background run — `--background`

Run the research detached from the session so a long fan-out doesn't block the caller. Referenced from the SKILL.md body because it reshapes the whole run rather than activating inside one phase.

1. **Detach via the harness's own background mechanism.** Running work in the background is an ambient harness capability — deep-research does not reimplement polling or scheduling; it hands the run to the harness detached and lets the session continue. (basis: `--background` mirrors operate's run-in-background posture — the loop/detach primitive is the harness's, configured by the module, not owned by the skill.)
2. **The detached run follows the identical procedure.** Backgrounding changes *where* the run executes, not *what* it does — every phase, the saturation stop, and the verification level apply unchanged.
3. **Report on completion.** When the run finishes it makes its result available to the caller; pair with `--notify` ([notify-on-completion](notify-on-completion.md)) to have the invoker signalled at completion rather than having to poll for it.
