"""Verification protocol independent from executor self-reporting."""

from typing import Protocol

from crossinghouse.contracts.task import TaskContract
from crossinghouse.contracts.verification import VerificationResult
from crossinghouse.execution.base import ExecutionResult


class Verifier(Protocol):
    def verify(
        self, task: TaskContract, execution: ExecutionResult
    ) -> tuple[VerificationResult, ...]:
        """Evaluate required checks using verifier-owned deterministic fixtures."""
