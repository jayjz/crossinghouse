# Contributing

Read [AGENTS.md](AGENTS.md), [ARCHITECTURE.md](ARCHITECTURE.md), and the relevant
documents under `docs/` before changing behavior. Keep work within its approved
authority and treat model, provider, repository, and subprocess output as untrusted.

For substantial work, create or update an active execution plan. Add tests with
behavior changes, document durable behavior changes, and record architectural
boundary decisions as ADRs.

Before proposing a change, run:

```powershell
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
```
