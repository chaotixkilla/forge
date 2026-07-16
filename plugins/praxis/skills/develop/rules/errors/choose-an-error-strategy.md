# Choose an error strategy

The moment this rule governs is the first time a function in a layer needs to signal that it couldn't do its job — throw, return a failure value, or hand back a code. Whatever you reach for becomes, by gravity, what the next function in that layer reaches for too, so the choice is really a choice for the whole layer. Left to reflex it goes wrong two ways: a layer that mixes mechanisms — some paths throw, some return `null`, some return an error tuple — forces every caller to defend against all three; and a mechanism picked for its convenience at the throw site lets a failure be silently dropped at the catch site. Two builders left to taste pick different mechanisms in the same layer. This rule pins the discriminator so two builders converge on one strategy per layer.

## The discriminator

The property the choice turns on is **how the failure must travel to the code that can act on it**, and the non-negotiables are fixed regardless of mechanism: *one* mechanism per layer, and *never* a path where an error can be silently discarded.

- **Does the caller need to be forced to confront the failure at the call site?** If a dropped error is a correctness disaster (money, auth, data integrity), prefer a mechanism the type system makes un-ignorable — the failure is in the signature, not the ether.
- **Is the failure the exception or the norm?** A rare, unrecoverable-here failure that should unwind many frames to a distant handler wants unwinding semantics; an expected, per-call outcome the immediate caller must branch on wants an explicit return.
- **Match what the layer already does.** A layer with an established mechanism is not a fork — extend the existing one ([match-surrounding-conventions](../change-hygiene/match-surrounding-conventions.md)). The fork below is only live when you're setting the strategy for new ground.

Whichever you pick, the boundary that owns the failure is decided separately ([handle-errors-at-the-boundary](handle-errors-at-the-boundary.md)), and the cheapest error is the one you designed away ([define-errors-out-of-existence](define-errors-out-of-existence.md)).

## The fork: how to signal failure

*Which signalling mechanism* is a genuine, camp-divided fork — encode the trade, don't pick a house winner:

- **Exceptions / unwinding.** Fail loud, unwind to a handler that has the context. Cost: control flow goes invisible — a reader can't see from the signature what throws — and it's one lazy `catch`-all away from swallowing everything.
- **Result / either types.** The failure is in the return type, so the compiler forces the caller to handle it. Cost: verbose, and viral — it colours every signature up the call chain until someone unwraps it.
- **Error codes / sentinels.** Simple, no machinery, C-style. Cost: silently ignorable — a caller that forgets to check the code sails on with bad state, exactly the failure the non-negotiable forbids.

**Routing rule (non-gating): surrounding convention → house rule → maintainer.** Match the layer's existing mechanism; absent one, the house rule; absent that, the maintainer decides. The shared invariant across all three poles: one mechanism per layer, and no path that drops an error on the floor.

(basis: McConnell, *Code Complete* 2nd ed. ch. 8 — error-handling technique is a deliberate per-context selection, not a default; the exceptions-vs-result-types debate is a live split between the OO/exception camp and the functional/either-type camp, with no settled cross-language winner — hence a fork, not a ruling.)

## The anchors

- *Good:* a data-access layer that signals every failure as a typed result the callers must unwrap, uniformly — a reader knows, from any signature, exactly how failure arrives and that it cannot be missed.
- *Bad:* a layer where one function throws, its neighbour returns `null` on failure, and a third returns `-1`, so every caller writes three different defensive shapes and one of them forgets the `-1` and runs on garbage.
