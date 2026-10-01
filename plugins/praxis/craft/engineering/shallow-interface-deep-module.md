# Shallow interface, deep module

The moment this rule governs is the one where you decide how much a module exposes versus how much it hides — the size and shape of its public face relative to the work behind it. Left to taste, one engineer writes a thin pass-through "for layering" while another folds the same logic into a module with a small face, and the codebase accretes hollow layers that add indirection without subtracting understanding.

## The discriminator

Judge a module by the ratio of **interface cost to hidden complexity.** A module is **deep (good)** when its interface is small relative to the substantial implementation it encapsulates; **shallow (suspect)** when its interface is nearly as complex as just doing the thing directly.

- **Measure what the caller must know against what they're spared.** A deep module lets a caller accomplish something significant through a few well-chosen calls while a large body of logic — ordering, edge cases, state, resource handling — stays hidden.
- **A pass-through wrapper hides nothing.** If the interface has roughly one method per internal operation, or a call just forwards to one other call with the same shape, the layer adds a hop and a name without subtracting any complexity — the caller could invoke the underlying thing as easily. That is a shallow module; reject it — and so is the reflex to chop one job into many small classes, each a shallow layer ("classitis").
- **Watch for the interface that leaks the implementation.** A one-line method that exposes an internal field, or an option-heavy interface that forces the caller to understand the internals to call it correctly, is shallow even if the body is long.

(basis: Ousterhout, *A Philosophy of Software Design*)

This is the depth test [right-altitude-abstraction](right-altitude-abstraction.md) invokes — an indirection at the right altitude is a deep one — and the same test gates extraction: pull code into a function when the resulting interface is simpler than the code it hides, not when it merely relocates it ([when-to-extract-a-function](when-to-extract-a-function.md)).

## The anchors

- *Deep (good):* a store exposing `get(key)` / `put(key, value)` while hiding connection pooling, retries, serialization, and cache invalidation behind them — two easy calls, a mountain of complexity spared.
- *Shallow (reject):* a wrapper whose every method forwards one-to-one to the underlying client with the same arguments and return type, added "to have our own layer" — it hides nothing, so the caller now learns two interfaces to reach one behavior. Either give the layer a genuinely simpler face that hides real complexity, or delete it and call the underlying thing directly.
