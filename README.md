# Crossinghouse

Crossinghouse is experimental research infrastructure for task routing and
verification. It investigates whether inexpensive model execution, deterministic
verification, and selective escalation can reduce the cost per verified
successful task without reducing reliability.

## Status

**Implemented:** repository foundation and development tooling only. There are
no model-provider integrations, orchestration runtime, or run artifact writer.

**Intended design:** task planning, bounded task contracts, deterministic routing,
execution, evidence capture, verification, and conditional escalation are separate
components. See [ARCHITECTURE.md](ARCHITECTURE.md) and [the documentation map](docs/index.md).

## Development

Python 3.12 and [uv](https://docs.astral.sh/uv/) are required.

```powershell
uv sync
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
```

See [CONTRIBUTING.md](CONTRIBUTING.md) before changing the project.
