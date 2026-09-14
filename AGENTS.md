# AGENTS.md

## Purpose

Crossinghouse is an experimental task-routing and verification runtime.

The primary research question is:

> Can cheaper model execution combined with deterministic verification and
> selective escalation reduce cost per verified successful task without
> reducing reliability?

This repository is research infrastructure, not an autonomous-agent product.

## Repository map

Read the relevant documentation before changing code.

- `README.md` — project purpose and current status
- `ARCHITECTURE.md` — system boundaries and package architecture
- `docs/index.md` — documentation map
- `docs/design/core-beliefs.md` — non-negotiable engineering principles
- `docs/evidence-contract.md` — required run evidence
- `docs/routing-policy.md` — routing and escalation semantics
- `docs/evaluation-methodology.md` — experimental methodology
- `docs/security.md` — security boundaries
- `docs/reliability.md` — failure and recovery expectations
- `docs/adr/` — architectural decisions
- `docs/exec-plans/active/` — current multi-step implementation plans

## Development rules

Prefer:

- explicit contracts over implicit behavior
- deterministic checks over model judgment
- typed boundaries over guessed data shapes
- bounded authority over autonomous expansion
- append-only run evidence over narrative summaries
- small composable modules over framework-heavy abstractions
- dependency injection over hidden global state
- reproducible experiments over demos
- fail-closed behavior when authority or verification is ambiguous

Do not introduce infrastructure merely because it may be useful later.

Avoid adding without an accepted architectural decision:

- agent frameworks
- workflow engines
- vector databases
- Redis
- PostgreSQL
- web UI frameworks
- background workers
- autonomous GitHub writes
- learned routing
- long-term agent memory

## Model authority

Models may propose and execute bounded work.

Models must not be trusted to determine whether their own work succeeded when
a deterministic verification mechanism exists.

Execution success and task verification are separate states.

The executor must not:

- expand its own allowed file scope
- change its own budget
- change required verification
- declare deterministic checks successful without evidence
- silently escalate privileges
- invent unavailable tool results

## Implementation workflow

Before substantial work:

1. Read this file.
2. Read `ARCHITECTURE.md`.
3. Read the relevant documents under `docs/`.
4. Inspect existing tests and implementation.
5. For non-trivial work, create or update an execution plan under
   `docs/exec-plans/active/`.

During implementation:

1. Keep changes inside the requested scope.
2. Add or update tests with behavior changes.
3. Record architectural decisions as ADRs when boundaries or invariants change.
4. Update durable documentation when behavior changes.

## Required verification

Before declaring work complete, run:

uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest