# One reason to fail

Shape each case so that when it goes red, the failure points at a single cause. Narrow the arrange-act-assert: set up exactly the state the behavior needs, perform one logical action, and assert the one thing that action must produce. A case that bundles unrelated assertions — checks three independent behaviors in one test — turns a single red into a guessing game about which of the three broke, and it stops at the first failed assertion, hiding the other two.

The discriminator is *cause*, not *assertion count*: a case may assert several facts about one outcome (a returned object's shape across several fields is one behavior) — that is one reason to fail. It may not verify several outcomes that could break independently — those are separate cases. This is what makes a red result diagnostic before you even read the message ([make-failures-diagnostic](make-failures-diagnostic.md)), and it is what lets [design-the-cases](../phases/03-design-the-cases.md) prune redundant cases cleanly: two cases that fail for the same reason are one, but two assertions in one case that fail for different reasons are a case that should be split.
</content>
