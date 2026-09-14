# Evaluation methodology

## Initial experiment conditions

Compare equivalent task sets and fixed acceptance criteria:

| Condition | Pipeline |
| --- | --- |
| A | Inexpensive executor only |
| B | Strong model only |
| C | Strong planner → inexpensive executor → verifier |
| D | Planner → executor → verifier → conditional escalation |

The primary metric is **cost per verified successful task**. Record verified success
rate, total cost, latency, retries, escalations, and failure categories as supporting
measures. Run repeated trials under comparable environments and preserve all failed
runs and their evidence. Do not change acceptance criteria after observing results.

These are intended experimental conditions, not implemented benchmarks.
