# 0001 — P1 typed kernel foundation

## Status

Planned. P0 creates repository and tooling only; this plan does not authorize
provider integrations.

## Scope

1. Define typed, provider-neutral task, authority, budget, evidence, verification,
   routing, and lifecycle contracts.
2. Define explicit lifecycle states and permitted transitions.
3. Implement a dependency-injected mock executor constrained by a task contract.
4. Define a deterministic verifier abstraction and a test implementation.
5. Add unit tests for contracts, transitions, scope denial, verifier outcomes, and
   retry/escalation decisions.

## Verification

Run the repository's required Ruff, formatting, mypy, and pytest commands. Tests
must distinguish execution completion from deterministic verification success.

## Non-goals

No model providers, agent framework, web service, background worker, learned
routing, persistent database, or autonomous repository writes.
