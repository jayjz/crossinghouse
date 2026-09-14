# Architecture

## Objective

Crossinghouse tests whether bounded inexpensive execution plus deterministic
verification and selective escalation can lower cost per verified successful task.
It is research infrastructure, not an autonomous-agent framework.

## Intended design

The intended lifecycle is:

`planner → task contract → router → executor → evidence → deterministic verifier → retry or escalation`

The planner proposes work; the task contract fixes scope, budget, authority, and
required checks. The router selects a risk tier. The executor performs only
authorized work. Evidence records what occurred. A verifier independently evaluates
the required checks. Retry or escalation follows explicit policy; execution success
does not establish verification success.

## Package boundaries

- `planning`: task decomposition and proposed plans.
- `contracts`: typed task, authority, budget, and lifecycle boundaries.
- `routing`: deterministic risk classification and routing decisions.
- `execution`: bounded execution interfaces and implementations.
- `telemetry`: append-only run evidence interfaces.
- `verification`: deterministic verification interfaces and results.
- `escalation`: retry and escalation policy decisions.

Provider SDK types belong only in provider adapters at system edges. Core contracts
must use provider-neutral types and receive dependencies explicitly.

## P1 kernel

**Implemented:** `contracts`, `routing`, `execution`, `verification`, and
`escalation` provide a small in-memory, provider-neutral kernel. The mock executor
simulates only contract-authorized file operations; deterministic verification is
independent from its completion claim. The kernel deliberately has no run-artifact
writer or provider adapter.

## Run artifacts

**Intended, not implemented:** each run will have `.runs/<run-id>/` artifacts for
its contract, calls, commands, file changes, verification, cost, and final lifecycle
result. Artifacts are evidence, not a model-authored success summary.

## V0 non-goals

V0 excludes real model providers, agent frameworks, workflow engines, Redis,
PostgreSQL, vector databases, web APIs or UI, background workers, learned routing,
long-term memory, and autonomous GitHub writes.
