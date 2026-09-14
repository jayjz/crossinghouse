# Threat model

## Intended threats and controls

| Threat | Control direction |
| --- | --- |
| Scope escape | Enforce contract-scoped paths and commands; deny expansion. |
| Verification manipulation | Independent deterministic checks and immutable evidence references. |
| Secret leakage | Redaction, least-privilege environment exposure, and no secret prompts. |
| Command injection | Structured command interfaces, allowlists, and no shell interpolation by default. |
| Evidence fabrication | Capture execution-derived artifacts; provenance and digests support claims. |
| Cost runaway | Per-run budgets, timeout limits, and bounded retries/escalations. |
| Prompt injection | Treat repository and model text as data, not authority or instructions. |

This is a design baseline; no security-control implementation is claimed in P0.
