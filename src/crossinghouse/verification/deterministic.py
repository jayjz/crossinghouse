"""Fixture-driven verifier used to make kernel behavior deterministic in tests."""

from collections.abc import Mapping

from crossinghouse.contracts.evidence import Evidence
from crossinghouse.contracts.task import TaskContract
from crossinghouse.contracts.verification import VerificationResult, VerificationStatus
from crossinghouse.execution.base import ExecutionResult


class DeterministicVerifier:
    """Return configured check outcomes, without trusting execution claims."""

    def __init__(self, outcomes: Mapping[str, VerificationStatus]) -> None:
        self._outcomes = dict(outcomes)

    def verify(
        self, task: TaskContract, execution: ExecutionResult
    ) -> tuple[VerificationResult, ...]:
        del execution
        return tuple(
            VerificationResult(
                check_id=check,
                status=self._outcomes.get(check, VerificationStatus.INDETERMINATE),
                evidence=(
                    Evidence(
                        kind="deterministic_fixture", detail=f"outcome for {check}"
                    ),
                ),
                reason="configured deterministic outcome",
            )
            for check in task.required_checks
        )
