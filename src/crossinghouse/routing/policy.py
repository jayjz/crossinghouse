"""The documented LOW/MEDIUM/HIGH deterministic baseline."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from crossinghouse.contracts.task import RiskTier, TaskContract


class RouteAction(StrEnum):
    EXECUTE = "execute"
    PLAN_REVIEW = "plan_review"
    DENY_REVIEW = "deny_review"


class RoutingDecision(BaseModel):
    model_config = ConfigDict(frozen=True)

    action: RouteAction
    reason: str
    task_id: str


def route(task: TaskContract) -> RoutingDecision:
    if task.risk_tier is RiskTier.LOW:
        return RoutingDecision(
            action=RouteAction.EXECUTE,
            reason="low-risk bounded execution",
            task_id=task.task_id,
        )
    if task.risk_tier is RiskTier.MEDIUM:
        return RoutingDecision(
            action=RouteAction.PLAN_REVIEW,
            reason="medium risk requires plan review",
            task_id=task.task_id,
        )
    return RoutingDecision(
        action=RouteAction.DENY_REVIEW,
        reason="high risk requires explicit authorized review",
        task_id=task.task_id,
    )
