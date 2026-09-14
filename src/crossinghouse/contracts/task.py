"""Task contract fixing authority, verification, and risk before execution."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator

from crossinghouse.contracts.authority import Authority
from crossinghouse.contracts.budget import Budget


class RiskTier(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskContract(BaseModel):
    """Immutable task boundary that the executor is not allowed to alter."""

    model_config = ConfigDict(frozen=True)

    task_id: str = Field(min_length=1)
    objective: str = Field(min_length=1)
    authority: Authority
    required_checks: tuple[str, ...] = Field(min_length=1)
    risk_tier: RiskTier
    budget: Budget

    @field_validator("required_checks")
    @classmethod
    def validate_checks(cls, checks: tuple[str, ...]) -> tuple[str, ...]:
        if any(not check.strip() for check in checks):
            raise ValueError("required checks must be non-empty")
        if len(set(checks)) != len(checks):
            raise ValueError("required checks must be unique")
        return checks
