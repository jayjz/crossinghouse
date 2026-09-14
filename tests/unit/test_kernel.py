import pytest
from pydantic import ValidationError

from crossinghouse.contracts import (
    Authority,
    Budget,
    LifecycleError,
    LifecycleState,
    OperationKind,
    RiskTier,
    TaskContract,
    VerificationStatus,
    transition,
)
from crossinghouse.escalation import EscalationAction, decide
from crossinghouse.execution import ExecutionRequest, MockExecutor, RequestedOperation
from crossinghouse.routing import RouteAction, route
from crossinghouse.verification import DeterministicVerifier


@pytest.fixture
def task() -> TaskContract:
    return TaskContract(
        task_id="task-1",
        objective="Change a bounded fixture",
        authority=Authority(allowed_paths=("src/example",)),
        required_checks=("unit",),
        risk_tier=RiskTier.LOW,
        budget=Budget(retry_limit=2),
    )


def request_for(
    task: TaskContract, path: str = "src/example/file.py"
) -> ExecutionRequest:
    return ExecutionRequest(
        task=task,
        attempt=1,
        operations=(RequestedOperation(kind=OperationKind.MODIFY_FILE, path=path),),
    )


def test_valid_task_contract(task: TaskContract) -> None:
    assert task.authority.allowed_paths == ("src/example",)
    assert task.budget.retry_limit == 2


def test_invalid_authority_scope_is_rejected() -> None:
    with pytest.raises(ValidationError, match="relative path"):
        Authority(allowed_paths=("../outside",))


def test_allowed_mock_execution(task: TaskContract) -> None:
    result = MockExecutor().execute(request_for(task))

    assert result.completed is True
    assert result.files_changed == ("src/example/file.py",)
    assert result.claimed_operations[0].kind is OperationKind.MODIFY_FILE


def test_mock_executor_denies_scope_escape(task: TaskContract) -> None:
    result = MockExecutor().execute(request_for(task, "tests/escape.py"))

    assert result.completed is False
    assert result.error == "path outside authority: tests/escape.py"


def test_execution_success_does_not_imply_verified_success(task: TaskContract) -> None:
    execution = MockExecutor().execute(request_for(task))
    results = DeterministicVerifier({"unit": VerificationStatus.FAIL}).verify(
        task, execution
    )

    assert execution.completed is True
    assert results[0].status is VerificationStatus.FAIL
    with pytest.raises(LifecycleError):
        transition(LifecycleState.EXECUTED, LifecycleState.VERIFIED, results)


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (VerificationStatus.PASS, VerificationStatus.PASS),
        (VerificationStatus.FAIL, VerificationStatus.FAIL),
        (VerificationStatus.INDETERMINATE, VerificationStatus.INDETERMINATE),
    ],
)
def test_deterministic_verifier_outcomes(
    task: TaskContract, status: VerificationStatus, expected: VerificationStatus
) -> None:
    results = DeterministicVerifier({"unit": status}).verify(
        task, MockExecutor().execute(request_for(task))
    )

    assert results[0].status is expected


def test_indeterminate_verification_fails_closed(task: TaskContract) -> None:
    results = DeterministicVerifier({}).verify(
        task, MockExecutor().execute(request_for(task))
    )

    with pytest.raises(LifecycleError, match="passing verification"):
        transition(LifecycleState.VERIFYING, LifecycleState.VERIFIED, results)


def test_valid_lifecycle_transitions_require_independent_pass(
    task: TaskContract,
) -> None:
    result = DeterministicVerifier({"unit": VerificationStatus.PASS}).verify(
        task, MockExecutor().execute(request_for(task))
    )
    state = transition(LifecycleState.PENDING, LifecycleState.PLANNED)
    state = transition(state, LifecycleState.EXECUTING)
    state = transition(state, LifecycleState.EXECUTED)
    state = transition(state, LifecycleState.VERIFYING)

    assert transition(state, LifecycleState.VERIFIED, result) is LifecycleState.VERIFIED


@pytest.mark.parametrize(
    ("current", "target"),
    [
        (LifecycleState.PENDING, LifecycleState.EXECUTED),
        (LifecycleState.EXECUTED, LifecycleState.VERIFIED),
        (LifecycleState.VERIFIED, LifecycleState.EXECUTING),
        (LifecycleState.TERMINATED, LifecycleState.PLANNED),
    ],
)
def test_invalid_lifecycle_transitions_are_rejected(
    current: LifecycleState, target: LifecycleState
) -> None:
    with pytest.raises(LifecycleError, match="illegal transition"):
        transition(current, target)


def test_retry_below_budget(task: TaskContract) -> None:
    decision = decide(task, VerificationStatus.FAIL, current_attempt=2)

    assert decision.action is EscalationAction.RETRY
    assert decision.next_attempt == 3


def test_retry_exhaustion_terminates_low_risk(task: TaskContract) -> None:
    decision = decide(task, VerificationStatus.FAIL, current_attempt=3)

    assert decision.action is EscalationAction.TERMINATE
    assert decision.next_attempt is None


@pytest.mark.parametrize(
    ("tier", "expected"),
    [
        (RiskTier.LOW, RouteAction.EXECUTE),
        (RiskTier.MEDIUM, RouteAction.PLAN_REVIEW),
        (RiskTier.HIGH, RouteAction.DENY_REVIEW),
    ],
)
def test_deterministic_routing(
    task: TaskContract, tier: RiskTier, expected: RouteAction
) -> None:
    decision = route(task.model_copy(update={"risk_tier": tier}))

    assert decision.action is expected


def test_escalation_does_not_expand_immutable_authority(task: TaskContract) -> None:
    original_authority = task.authority
    high_risk = task.model_copy(update={"risk_tier": RiskTier.HIGH})
    decision = decide(high_risk, VerificationStatus.FAIL, current_attempt=1)

    assert decision.action is EscalationAction.ESCALATE
    assert high_risk.authority == original_authority
    assert not hasattr(decision, "authority")


def test_executor_does_not_mutate_contract_or_budget(task: TaskContract) -> None:
    request = request_for(task)
    MockExecutor().execute(request)

    assert request.task == task
    assert request.task.budget.retry_limit == 2
