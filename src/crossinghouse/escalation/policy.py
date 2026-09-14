"""Deterministic retry and escalation policy without authority expansion."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from crossinghouse.contracts.task import RiskTier, TaskContract
from crossinghouse.contracts.verification import VerificationStatus


class EscalationAction(StrEnum):
    RETRY = "retry"
    ESCALATE = "escalate"
    TERMINATE = "terminate"


class EscalationDecision(BaseModel):
    model_config = ConfigDict(frozen=True)

    action: EscalationAction
    reason: str
    next_attempt: int | None = None


def decide(
    task: TaskContract,
    verification: VerificationStatus,
    current_attempt: int,
    *,
    scope_violation: bool = False,
) -> EscalationDecision:
    """Make a bounded decision; the returned decision contains no new authority."""
    if current_attempt < 1:
        raise ValueError("current attempt must be at least one")
    if verification is VerificationStatus.PASS:
        return EscalationDecision(
            action=EscalationAction.TERMINATE,
            reason="verification passed",
        )
    if scope_violation or task.risk_tier is RiskTier.HIGH:
        return EscalationDecision(
            action=EscalationAction.ESCALATE,
            reason="review required for scope or high risk",
        )
    if current_attempt <= task.budget.retry_limit:
        return EscalationDecision(
            action=EscalationAction.RETRY,
            reason="retry budget remains",
            next_attempt=current_attempt + 1,
        )
    if task.risk_tier is RiskTier.MEDIUM:
        return EscalationDecision(
            action=EscalationAction.ESCALATE,
            reason="retry budget exhausted for medium risk",
        )
    return EscalationDecision(
        action=EscalationAction.TERMINATE,
        reason="retry budget exhausted",
    )
