# ADR 0001: Start with a framework-free kernel

## Status

Accepted

## Context

Crossinghouse needs inspectable routing, authority, lifecycle, evidence, and
verification boundaries before it can evaluate model-routing hypotheses.

## Decision

Start with explicit Python interfaces and typed contracts. Compose dependencies
directly rather than adopting an agent framework or workflow engine.

## Consequences

Initial code has more visible boundary definitions, but lifecycle and verification
semantics remain testable, provider-neutral, and easy to audit. A framework requires
a future demonstrated need and an ADR.
