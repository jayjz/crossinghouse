"""Explicit lifecycle transition policy for task runs."""

from collections.abc import Collection
from enum import StrEnum

from crossinghouse.contracts.verification import VerificationResult, VerificationStatus


class LifecycleState(StrEnum):
    PENDING = "pending"
    PLANNED = "planned"
    EXECUTING = "executing"
    EXECUTED = "executed"
    VERIFYING = "verifying"
    VERIFIED = "verified"
    FAILED = "failed"
    ESCALATED = "escalated"
    TERMINATED = "terminated"


class LifecycleError(ValueError):
    """Raised when a transition would misrepresent run state."""


_ALLOWED_TRANSITIONS: dict[LifecycleState, frozenset[LifecycleState]] = {
    LifecycleState.PENDING: frozenset(
        {
            LifecycleState.PLANNED,
            LifecycleState.FAILED,
            LifecycleState.ESCALATED,
            LifecycleState.TERMINATED,
        }
    ),
    LifecycleState.PLANNED: frozenset(
        {LifecycleState.EXECUTING, LifecycleState.ESCALATED, LifecycleState.TERMINATED}
    ),
    LifecycleState.EXECUTING: frozenset(
        {
            LifecycleState.EXECUTED,
            LifecycleState.FAILED,
            LifecycleState.ESCALATED,
            LifecycleState.TERMINATED,
        }
    ),
    LifecycleState.EXECUTED: frozenset(
        {
            LifecycleState.VERIFYING,
            LifecycleState.FAILED,
            LifecycleState.ESCALATED,
            LifecycleState.TERMINATED,
        }
    ),
    LifecycleState.VERIFYING: frozenset(
        {
            LifecycleState.VERIFIED,
            LifecycleState.FAILED,
            LifecycleState.ESCALATED,
            LifecycleState.TERMINATED,
        }
    ),
    LifecycleState.FAILED: frozenset(
        {LifecycleState.PLANNED, LifecycleState.ESCALATED, LifecycleState.TERMINATED}
    ),
    LifecycleState.ESCALATED: frozenset({LifecycleState.TERMINATED}),
    LifecycleState.VERIFIED: frozenset(),
    LifecycleState.TERMINATED: frozenset(),
}


def transition(
    current: LifecycleState,
    target: LifecycleState,
    verification_results: Collection[VerificationResult] = (),
) -> LifecycleState:
    """Validate and return a lifecycle transition without storing mutable state."""
    if target not in _ALLOWED_TRANSITIONS[current]:
        raise LifecycleError(f"illegal transition: {current.value} -> {target.value}")
    if target is LifecycleState.VERIFIED and (
        not verification_results
        or any(
            result.status is not VerificationStatus.PASS
            for result in verification_results
        )
    ):
        raise LifecycleError(
            "verified requires at least one passing verification result"
        )
    return target
