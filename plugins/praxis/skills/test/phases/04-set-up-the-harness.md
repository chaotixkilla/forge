The designed cases run correctly only in a harness that makes them deterministic and isolated. The load-bearing decision here is what is *real* versus *stubbed* at each seam — get it wrong in either direction and every case downstream lies about whether the change works.

## Decide real vs stubbed at each boundary

Apply [mock-at-the-boundary](../rules/mock-at-the-boundary.md): keep the unit under test and its in-process collaborators **real**; substitute a double only at a true external / unmanaged seam (a third-party API, message bus, clock, filesystem, or other nondeterministic external dependency); use a real or containerized instance for a *managed* dependency such as your own datastore; wrap an un-owned library in an owned adapter and cover the adapter with one real integration test. The classicist default, and the internal / managed / unmanaged / owned discriminators that decide each seam, live in the rule; *which* specific seams are external for this change is the per-context call the rule deliberately leaves open.

## Pin the sources of nondeterminism

Apply [control-nondeterminism](../rules/control-nondeterminism.md): pin time, randomness, ordering, and concurrency at setup so a case's result depends only on the behavior under test. A case that can pass or fail on the *unchanged* code is a defect in the harness, fixed here — not something to retry past in [run-and-observe](05-run-and-observe.md).

## Establish fixtures and the execution environment

Seed the fixtures the cases need, following the suite's fixture style ([match-the-suites-conventions](../rules/match-the-suites-conventions.md)), and establish the environment the project's runner expects.

## Under `--sandbox`

Provision a disposable, network/filesystem-isolated **local** environment with seeded fixtures, so the run is reproducible and cannot touch real state — see [isolated-sandbox](../modules/isolated-sandbox.md). Without the flag, the harness runs in the ambient environment.

## Output

A harness in which every designed case runs deterministically and in isolation, with the real/stubbed boundary decided per seam — handed to [run-and-observe](05-run-and-observe.md).
</content>
