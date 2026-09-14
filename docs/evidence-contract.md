# Evidence contract

## Intended design — not implemented

Each `.runs/<run-id>/` directory is intended to contain append-only, attributable
evidence sufficient to distinguish execution from verification.

- **Run identity:** run ID, timestamps, code revision, environment, and parent run.
- **Task contract:** requested outcome, allowed scope, authority, budget, risk tier,
  retry limit, and required verification.
- **Model calls:** provider/model identifier, request and response references,
  timestamps, token or usage data, and errors. Sensitive values must be redacted.
- **Commands:** exact authorized command, working directory, timestamps, exit status,
  and captured output reference.
- **Modified files:** declared and observed paths plus content-digest references.
- **Verification:** check identity, deterministic inputs, command/output references,
  result, and verifier timestamp.
- **Cost:** attributable provider and execution cost inputs, units, and total.
- **Final lifecycle result:** explicit terminal state, reason, links to supporting
  evidence, and escalation history.

Missing, ambiguous, or unverifiable evidence must not support a success claim.
