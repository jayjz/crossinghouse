# Security boundaries

## Intended security posture

Treat model output, repository contents, provider responses, and subprocess output
as potentially untrusted input. Parse and validate data at typed boundaries; never
grant authority because untrusted text requests it.

Execution must enforce the task contract's file scope, command authority, budgets,
and verification requirements. Redact secrets from logs and artifacts, avoid passing
secrets through prompts or command lines, and preserve evidence with integrity-aware
metadata. Security-sensitive or ambiguous work must fail closed or require explicit
authorized review.
