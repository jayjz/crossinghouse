# Routing policy

## Intended initial policy

Routing is deterministic and based on the task contract, not model confidence.

| Tier | Typical task | Initial handling |
| --- | --- | --- |
| LOW | Narrow, reversible change with clear deterministic checks | Inexpensive executor; bounded retry; verify. |
| MEDIUM | Multi-file or moderate ambiguity, but bounded authority and checks | Plan review boundary; inexpensive executor; verify; limited escalation. |
| HIGH | Security-sensitive, broad, destructive, unclear scope, or weak verification | Require explicit human-approved authority or decline; do not silently route onward. |

Retries are bounded by the contract. Escalation triggers include a failed required
check after allowed retries, unavailable deterministic evidence, scope violation,
budget threshold, timeout, ambiguous verification, or a policy-defined risk change.
Escalation creates a new explicit decision and cannot expand authority implicitly.

**Hypothesis:** learned routing may be evaluated later. It is not part of the initial
policy or implementation.
