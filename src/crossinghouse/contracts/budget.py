"""Immutable bounds that an executor cannot change."""

from pydantic import BaseModel, ConfigDict, Field


class Budget(BaseModel):
    """Retry plus optional cost and time limits for one task."""

    model_config = ConfigDict(frozen=True)

    retry_limit: int = Field(ge=0)
    max_cost_usd: float | None = Field(default=None, ge=0)
    timeout_seconds: int | None = Field(default=None, gt=0)
