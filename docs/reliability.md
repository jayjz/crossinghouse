# Reliability

## Intended reliability posture

Failure classes include invalid contracts, routing denial, authorization or scope
violations, executor errors, timeouts, provider failures, malformed output,
verification failures, evidence write failures, and budget exhaustion.

The system should fail closed when authority, evidence, or verification is missing
or ambiguous. Retries must be contract-bounded and timeouts explicit. Failed and
timed-out runs remain evidence rather than being rewritten as success. Future tests
must inject failures across boundaries to validate recovery and terminal states.
