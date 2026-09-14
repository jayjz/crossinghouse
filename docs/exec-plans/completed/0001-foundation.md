# 0001 - P1 typed kernel foundation

## Status

Completed on 2026-09-14. P1 remains provider-neutral and does not authorize
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

Completed successfully:

- `uv sync --locked`
- `uv run ruff check .`
- `uv run ruff format --check .`
- `uv run mypy src`
- `uv run pytest` - 22 passed
- `git diff --check`

Tests distinguish execution completion from deterministic verification success.

## Non-goals

No model providers, agent framework, web service, background worker, learned
routing, persistent database, or autonomous repository writes.
